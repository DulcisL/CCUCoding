/* Main file for project
    This file is to focus on the user story of a map that shows the status of the parking lots across campus
        - "As a student I want to be able to see a visual reference of the current capacity of the parking 
        lot to easily judge the parking across campus. An example would be a map with green, yellow, or red
        overlayed over the parking lots on campus."
         Image courtesy of https://x.com/CCUHousing/status/1039140856673054725
*/
// Minimal WebGL: draw image + overlay rectangles with opacity

const imgUrl = "/img/campus.jpg";       // your served image
const boxes = [
    // x, y, width, height, rgba
    { x: 439, y: 458, w: 175, h: 180, color: [1, 0, 0, 0.4] }, // red (KK)
    { x: 570, y: 305, w: 100, h: 90, color: [0, 1, 0, 0.4] }, // green (GG)
    { x: 174, y: 512, w: 125, h: 80, color: [1, 1, 0, 0.4] },  // yellow (stadium)
];

const vsTex = `
attribute vec2 a_position;   // in pixels
attribute vec2 a_texcoord;
uniform vec2 u_resolution;   // canvas size in pixels
varying vec2 v_texcoord;
void main() {
  // convert from pixels to clipspace
  vec2 zeroToOne = a_position / u_resolution;
  vec2 zeroToTwo = zeroToOne * 2.0;
  vec2 clip = zeroToTwo - 1.0;
  gl_Position = vec4(clip * vec2(1.0, -1.0), 0.0, 1.0);
  v_texcoord = a_texcoord;
}
`;

const fsTex = `
precision mediump float;
uniform sampler2D u_image;
varying vec2 v_texcoord;
void main() {
  gl_FragColor = texture2D(u_image, v_texcoord);
}
`;

const vsRect = `
attribute vec2 a_position;   // in pixels
uniform vec2 u_resolution;
void main() {
  vec2 zeroToOne = a_position / u_resolution;
  vec2 zeroToTwo = zeroToOne * 2.0;
  vec2 clip = zeroToTwo - 1.0;
  gl_Position = vec4(clip * vec2(1.0, -1.0), 0.0, 1.0);
}
`;

const fsRect = `
precision mediump float;
uniform vec4 u_color;  // rgba
void main() {
  gl_FragColor = u_color;
}
`;

function createShader(gl, type, src) {
    const sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
        throw new Error(gl.getShaderInfoLog(sh));
    }
    return sh;
}

function createProgram(gl, vsSrc, fsSrc) {
    const vs = createShader(gl, gl.VERTEX_SHADER, vsSrc);
    const fs = createShader(gl, gl.FRAGMENT_SHADER, fsSrc);
    const prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
        throw new Error(gl.getProgramInfoLog(prog));
    }
    return prog;
}

function loadTexture(gl, image) {
    const tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, tex);
    // set parameters for non-power-of-two images
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    // upload pixels
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
    return tex;
}

(async function main() {
    const canvas = document.getElementById("glcanvas");
    const gl = canvas.getContext("webgl");
    if (!gl) {
        alert("WebGL not available");
        return;
    }

    // Load image
    const img = await new Promise((resolve, reject) => {
        const i = new Image();
        i.crossOrigin = "anonymous";
        i.onload = () => resolve(i);
        i.onerror = reject;
        i.src = imgUrl;
    });

    // Size canvas to image
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    gl.viewport(0, 0, canvas.width, canvas.height);

    // Programs
    const progTex = createProgram(gl, vsTex, fsTex);
    const progRect = createProgram(gl, vsRect, fsRect);

    // ----- Draw image as a textured quad -----
    // Position buffer (2 triangles covering the image in pixel space)
    const posBufImg = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, posBufImg);
    // 0,0 to imgW,imgH rectangle
    const x0 = 0, y0 = 0, x1 = canvas.width, y1 = canvas.height;
    const imgPositions = new Float32Array([
        x0, y0, x1, y0, x0, y1,
        x0, y1, x1, y0, x1, y1,
    ]);
    gl.bufferData(gl.ARRAY_BUFFER, imgPositions, gl.STATIC_DRAW);

    // Texcoord buffer
    const texBuf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, texBuf);
    const texcoords = new Float32Array([
        0, 0, 1, 0, 0, 1,
        0, 1, 1, 0, 1, 1,
    ]);
    gl.bufferData(gl.ARRAY_BUFFER, texcoords, gl.STATIC_DRAW);

    // Texture
    const texture = loadTexture(gl, img);

    // Clear & draw image
    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT);

    gl.useProgram(progTex);

    // Attributes
    const aPosTex = gl.getAttribLocation(progTex, "a_position");
    const aTc = gl.getAttribLocation(progTex, "a_texcoord");
    const uResTex = gl.getUniformLocation(progTex, "u_resolution");

    gl.uniform2f(uResTex, canvas.width, canvas.height);

    // position
    gl.bindBuffer(gl.ARRAY_BUFFER, posBufImg);
    gl.enableVertexAttribArray(aPosTex);
    gl.vertexAttribPointer(aPosTex, 2, gl.FLOAT, false, 0, 0);

    // texcoord
    gl.bindBuffer(gl.ARRAY_BUFFER, texBuf);
    gl.enableVertexAttribArray(aTc);
    gl.vertexAttribPointer(aTc, 2, gl.FLOAT, false, 0, 0);

    // texture unit 0
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, texture);
    const uImage = gl.getUniformLocation(progTex, "u_image");
    gl.uniform1i(uImage, 0);

    gl.drawArrays(gl.TRIANGLES, 0, 6);

    // ----- Draw rectangles on top with blending -----
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

    gl.useProgram(progRect);

    const aPosRect = gl.getAttribLocation(progRect, "a_position");
    const uResRect = gl.getUniformLocation(progRect, "u_resolution");
    const uColor = gl.getUniformLocation(progRect, "u_color");
    gl.uniform2f(uResRect, canvas.width, canvas.height);

    // One buffer we’ll re-fill per rectangle
    const posBufRect = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, posBufRect);
    gl.enableVertexAttribArray(aPosRect);
    gl.vertexAttribPointer(aPosRect, 2, gl.FLOAT, false, 0, 0);

    boxes.forEach(({ x, y, w, h, color }) => {
        const x0 = x, y0 = y;
        const x1 = x + w, y1 = y + h;
        const rect = new Float32Array([
            x0, y0, x1, y0, x0, y1,
            x0, y1, x1, y0, x1, y1,
        ]);
        gl.bufferData(gl.ARRAY_BUFFER, rect, gl.DYNAMIC_DRAW);
        gl.uniform4fv(uColor, color);
        gl.drawArrays(gl.TRIANGLES, 0, 6);
    });
})();
