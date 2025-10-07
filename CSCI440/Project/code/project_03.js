/* This is the main js file for the project. This project is to have a piece of paper go through
    a series of transformations to turn into a origami plane. After the transformations the shape will
    then be animated to look like it is flying through a scene.
*/

"use strict";

var canvas;
var gl;

// buffers
var positionsPaper = [];
var colorsPaper = [];
var positionsDesk = [];
var colorsDesk = [];

const COLOR_PALLET = [
  vec3(1.0, 0.0, 0.0), //Red
  vec3(0.0, 1.0, 0.0), //Green
  vec3(0.0, 0.0, 1.0), //Blue
  vec3(1.0, 0.0, 1.0), //Magenta
  vec3(1.0, 1.0, 0.0), //Yellow
  vec3(0.0, 1.0, 1.0), //Cyan
  vec3(0.6, 0.3, 0.0), //Brown
  vec3(0.0, 0.0, 0.0), //Black
  vec3(1.0, 1.0, 1.0), //White
];

const paperVertices = [
  //x, y, z, w (y is axis vertically)
  //paper square
  //top
  vec4(-0.25, 0.111, -0.25, 1.0), //front left
  vec4(-0.25, 0.111, 0.25, 1.0), //back left
  vec4(0.25, 0.111, 0.25, 1.0), //back right
  vec4(0.25, 0.111, -0.25, 1.0), //front right
  //bottom
  vec4(-0.25, 0.101, -0.25, 1.0), //front left
  vec4(-0.25, 0.101, 0.25, 1.0), //back left
  vec4(0.25, 0.101, 0.25, 1.0), //back right
  vec4(0.25, 0.101, -0.25, 1.0), //front right
];

const deskVertices = [
  //Desktop rectangle
  //top
  vec4(-0.65, 0.1, -0.5, 1.0), //front left
  vec4(-0.65, 0.1, 0.5, 1.0), //back left
  vec4(0.65, 0.1, 0.5, 1.0), //back right
  vec4(0.65, 0.1, -0.5, 1.0), //front right
  //bottom
  vec4(-0.65, 0.0, -0.5, 1.0), //front left
  vec4(-0.65, 0.0, 0.5, 1.0), //back left
  vec4(0.65, 0.0, 0.5, 1.0), //back right
  vec4(0.65, 0.0, -0.5, 1.0), //front right
];

const legUnit = [
  //Front-left leg
  //top
  vec4(-0.5, 0.0, -0.5, 1.0),
  vec4(0.5, 0.0, -0.5, 1.0),
  vec4(0.5, 0.0, 0.5, 1.0),
  vec4(-0.5, 0.0, 0.5, 1.0),

  //bottom
  vec4(-0.5, -1.0, -0.5, 1.0),
  vec4(0.5, -1.0, -0.5, 1.0),
  vec4(0.5, -1.0, 0.5, 1.0),
  vec4(-0.5, -1.0, 0.5, 1.0),
];

window.onload = function init() {
  canvas = document.getElementById("gl-canvas");
  gl = canvas.getContext("webgl2");
  if (!gl) {
    alert("WebGL 2.0 isn't available");
    return;
  }

  // Build geometry
  buildPaper();
  buildDeskAndLegs();

  // Shaders
  var program = initShaders(gl, "vertex-shader", "fragment-shader");
  gl.useProgram(program);

  // Attributes
  var aPosition = gl.getAttribLocation(program, "aPosition");
  var aColor = gl.getAttribLocation(program, "aColor");

  // Uniforms
  var uModel = gl.getUniformLocation(program, "uModel");
  var uView = gl.getUniformLocation(program, "uView");
  var uProj = gl.getUniformLocation(program, "uProj");

  // State
  gl.viewport(0, 0, canvas.width, canvas.height);
  gl.clearColor(0.0, 0.0, 1.0, 1.0);
  gl.enable(gl.DEPTH_TEST);

  // Make VAOs
  function makeVAO(posArray, colArray) {
    const vao = gl.createVertexArray();
    gl.bindVertexArray(vao);

    // positions (vec4)
    const pbuf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, pbuf);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(posArray), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(aPosition);
    gl.vertexAttribPointer(aPosition, 4, gl.FLOAT, false, 0, 0);

    // colors (vec3)
    const cbuf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, cbuf);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(colArray), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(aColor);
    gl.vertexAttribPointer(aColor, 3, gl.FLOAT, false, 0, 0);

    gl.bindVertexArray(null);
    return { vao, count: posArray.length };
  }

  const VAOdesk = makeVAO(positionsDesk, colorsDesk);
  const VAOpaper = makeVAO(positionsPaper, colorsPaper);

  // Camera matrices using MV.js
  function computeMatrices() {
    const eye = vec3(0.0, 0.6, 1.8);
    const at = vec3(0.0, 0.25, 0.0);
    const up = vec3(0.0, 1.0, 0.0);

    // MV.js gives us lookAt() and perspective()
    const view = lookAt(eye, at, up);
    const proj = perspective(45.0, canvas.width / canvas.height, 0.01, 10.0);
    const model = mat4(); // identity

    gl.uniformMatrix4fv(uModel, false, flatten(model));
    gl.uniformMatrix4fv(uView, false, flatten(view));
    gl.uniformMatrix4fv(uProj, false, flatten(proj));
  }

  function render() {
    computeMatrices();

    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // draw desk first (brown), then paper (white)
    gl.bindVertexArray(VAOdesk.vao);
    gl.drawArrays(gl.TRIANGLES, 0, VAOdesk.count);

    gl.bindVertexArray(VAOpaper.vao);
    gl.drawArrays(gl.TRIANGLES, 0, VAOpaper.count);

    gl.bindVertexArray(null);

    requestAnimationFrame(render);
  }
  render();
};
//helper functions were made by chatgpt to help with rendering and creating the desk and paper
// helper: (v0,v1,v2,v3) -> two triangles
function pushQuad(posArr, colArr, v0, v1, v2, v3, color) {
  posArr.push(v0, v1, v2, v0, v2, v3);
  for (let i = 0; i < 6; i++) colArr.push(color);
}

// Apply a mat4 to an array of vec4 points (MVNew's mult(M, v) returns vec4)
function transformVerts8(verts8, M) {
  const out = [];
  for (let v of verts8) out.push(mult(M, v));
  return out;
}

// Push a box from an 8-vertex array: [a,b,c,d, e,f,g,h]
function pushBoxFrom8(posArr, colArr, v, color) {
  const [a, b, c, d, e, f, g, h] = v;
  // top, bottom
  pushQuad(posArr, colArr, a, b, c, d, color);
  pushQuad(posArr, colArr, e, f, g, h, color);
  // sides
  pushQuad(posArr, colArr, a, d, h, e, color); // front
  pushQuad(posArr, colArr, b, a, e, f, color); // left
  pushQuad(posArr, colArr, c, b, f, g, color); // back
  pushQuad(posArr, colArr, d, c, g, h, color); // right
}

function buildPaper() {
  const white = COLOR_PALLET[8];
  const [p0, p1, p2, p3, p4, p5, p6, p7] = paperVertices;

  pushQuad(positionsPaper, colorsPaper, p0, p1, p2, p3, white);
  pushQuad(positionsPaper, colorsPaper, p4, p5, p6, p7, white);
  pushQuad(positionsPaper, colorsPaper, p0, p3, p7, p4, white);
  pushQuad(positionsPaper, colorsPaper, p1, p0, p4, p5, white);
  pushQuad(positionsPaper, colorsPaper, p2, p1, p5, p6, white);
  pushQuad(positionsPaper, colorsPaper, p3, p2, p6, p7, white);
}

function buildDeskAndLegs() {
  const brown = COLOR_PALLET[6];
  const [d0, d1, d2, d3, d4, d5, d6, d7] = deskVertices;

  // desk top
  pushQuad(positionsDesk, colorsDesk, d0, d1, d2, d3, brown);
  pushQuad(positionsDesk, colorsDesk, d4, d5, d6, d7, brown);
  pushQuad(positionsDesk, colorsDesk, d0, d3, d7, d4, brown);
  pushQuad(positionsDesk, colorsDesk, d1, d0, d4, d5, brown);
  pushQuad(positionsDesk, colorsDesk, d2, d1, d5, d6, brown);
  pushQuad(positionsDesk, colorsDesk, d3, d2, d6, d7, brown);

  // reuse the leg geometry at different positions
  const S_leg = scale(0.05, 0.5, 0.05);

  // Corner centers under the desktop (x,z match your earlier placement)
  // NOTE: y MUST be 0.0 so the leg top touches the desk bottom (y=0.00)
  const legCenters = [
    vec3(-0.575, 0.0, -0.425), // front-left
    vec3(0.575, 0.0, -0.425), // front-right
    vec3(-0.575, 0.0, 0.425), // back-left
    vec3(0.575, 0.0, 0.425), // back-right
  ];

  legCenters.forEach((c) => {
    const T_leg = translate(c[0], c[1], c[2]); // MVNew
    const M_leg = mult(T_leg, S_leg); // T * S (no rotation here)
    const leg = transformVerts8(legUnit, M_leg);
    pushBoxFrom8(positionsDesk, colorsDesk, leg, COLOR_PALLET[6]); // brown
  });
}
