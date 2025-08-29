/*Create an interpolated square with Red in the bottom left
green in the top left, blue in the top right, and white in the
bottom right
*/
"use strict";

var canvas;
var gl;

var positions = [];
var colors = [];

window.onload = function init() {
    canvas = document.getElementById("gl-canvas");

    gl = canvas.getContext('webgl2');
    if (!gl) { alert("WebGL 2.0 isn't available"); }

    // Four Vertices

    var vertices = [
        vec3(-0.5, -0.5, 0.0), // Bottom left
        vec3(-0.5, 0.5, 0.0),  // Top left
        vec3(0.5, 0.5, 0.0),   // Top right
        vec3(0.5, -0.5, 0.0)   // Bottom right
    ];

    square(vertices[0], vertices[1], vertices[2], vertices[3]);

    //  Configure WebGL

    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0.0, 0.0, 0.0, 1.0);

    //  Load shaders and initialize attribute buffers

    var program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);

    // Create a buffer object, initialize it, and associate it with the
    //  associated attribute variable in our vertex shader

    var cBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW);

    var colorLoc = gl.getAttribLocation(program, "aColor");
    gl.vertexAttribPointer(colorLoc, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(colorLoc);

    var vBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(positions), gl.STATIC_DRAW);

    var positionLoc = gl.getAttribLocation(program, "aPosition");
    gl.vertexAttribPointer(positionLoc, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(positionLoc);

    render();
};
function square(a, b, c, d) {

    // add colors and vertices for one triangle

    var baseColors = [
        vec3(1.0, 0.0, 0.0), //Red
        vec3(0.0, 1.0, 0.0), //Green
        vec3(0.0, 0.0, 1.0), //Blue
        vec3(0.0, 0.0, 0.0), //Black
        vec3(1.0, 1.0, 1.0) //White

    ];

    colors.push(baseColors[0]);
    positions.push(a);
    colors.push(baseColors[1]);
    positions.push(b);
    colors.push(baseColors[2]);
    positions.push(c);
    colors.push(baseColors[4]);
    positions.push(d);
}

function render() {
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.drawArrays(gl.TRIANGLE_FAN, 0, positions.length);
}
