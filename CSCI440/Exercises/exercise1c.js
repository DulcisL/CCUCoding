/*
Create an hourglass line shape that is spinning similar to the spinning square. 
It must be interpolated in color. Know how to speed it up or slow it down
    and change directions.
*/
"use strict";

var canvas;
var gl;

var theta = 0.0;
var thetaLoc;

var colors = [];
var vertices = [];

window.onload = function init() {
    canvas = document.getElementById("gl-canvas");

    gl = canvas.getContext('webgl2');
    if (!gl) alert("WebGL 2.0 isn't available");


    //
    //  Configure WebGL
    //
    gl.viewport(0, 0, canvas.width, canvas.height);
    //set background color
    gl.clearColor(1.0, 1.0, 1.0, 1.0);

    //  Load shaders and initialize attribute buffers
    var program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);

    vertices = [
        vec2(0, 1),
        vec2(-1, 0),
        vec2(1, 0),
        vec2(0, -1),
        vec2(0, 1)
    ];
    var baseColors = [
        vec3(1.0, 0.0, 0.0), //Red
        vec3(0.0, 1.0, 0.0), //Green
        vec3(0.0, 0.0, 1.0), //Blue
        vec3(1.0, 0.0, 1.0), //Magenta
        vec3(1.0, 1.0, 0.0), //Yellow
        vec3(0.0, 1.0, 1.0), //Cyan
        vec3(0.0, 0.0, 0.0), //Black
        vec3(1.0, 1.0, 1.0) //White
    ];

    colors = [baseColors[3], baseColors[5], baseColors[6], baseColors[4], baseColors[3]];

    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0.8, 0.8, 0.8, 1.0);

    gl.enable(gl.DEPTH_TEST);

    // Load the data into the GPU

    //Set color buffer (Next 6 lines are required for color)
    var cBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW);

    var colorLoc = gl.getAttribLocation(program, "aColor");
    gl.vertexAttribPointer(colorLoc, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(colorLoc);

    var bufferId = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, bufferId);
    //Only need vertices to fill buffer instead of like gasket 4
    gl.bufferData(gl.ARRAY_BUFFER, flatten(vertices), gl.STATIC_DRAW);

    // Associate out shader variables with our data bufferData

    var positionLoc = gl.getAttribLocation(program, "aPosition");
    gl.vertexAttribPointer(positionLoc, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(positionLoc);


    thetaLoc = gl.getUniformLocation(program, "uTheta");


    render();
};

function render() {

    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    //Changes speed and direction 
    theta -= 0.01;
    gl.uniform1f(thetaLoc, theta);

    //Change how drawn
    gl.drawArrays(gl.LINE_STRIP, 0, vertices.length);

    requestAnimationFrame(render);
}
