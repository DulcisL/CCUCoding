/*
Change square colors to blue and background to grey, make 2 squares, one square stays in the same spot
one square is translated directly to the right, squares are rotating in opposite directions, both squares
are scaled down
*/

"use strict";

//const { mod } = require("three/tsl");

var canvas;
var gl;

var positionsArray = [];
var colorLoc;
var modelViewMatrix, modelViewMatrix2, modelViewMatrixLoc;
var theta = 0.00;

var blue;

window.onload = function init() {
    canvas = document.getElementById("gl-canvas");
    gl = canvas.getContext('webgl2');
    if (!gl) alert("WebGL 2.0 isn't available");

    gl.viewport(0, 0, canvas.width, canvas.height);
    //Set background to grey
    gl.clearColor(0.9, 0.9, 0.9, 1.0);
    gl.enable(gl.DEPTH_TEST);

    //change color to blue
    //red = vec4(1.0, 0.0, 0.0, 1.0);
    blue = vec4(0.0, 0.0, 1.0, 1.0);

    // square
    // DO NOT MODIFY THESE POSITIONS
    positionsArray.push(vec4(0.2, 0.2, 0, 1));
    positionsArray.push(vec4(0.6, 0.2, 0, 1));
    positionsArray.push(vec4(0.6, 0.6, 0, 1));
    positionsArray.push(vec4(0.2, 0.6, 0, 1));

    //  Load shaders and initialize attribute buffers
    var program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);

    var vBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(positionsArray), gl.STATIC_DRAW);

    var positionLoc = gl.getAttribLocation(program, "aPosition");
    gl.vertexAttribPointer(positionLoc, 4, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(positionLoc);

    colorLoc = gl.getUniformLocation(program, "uColor");

    modelViewMatrixLoc = gl.getUniformLocation(program, "uModelViewMatrix");

    render();
}

var render = function () {

    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    modelViewMatrix = mat4();
    //set up a copy for second square
    modelViewMatrix2 = modelViewMatrix;

    //translate to original place
    modelViewMatrix = mult(modelViewMatrix, translate(0.4, 0.4, 0.0));

    //rotation counter clockwise
    theta -= 0.5;
    modelViewMatrix = mult(modelViewMatrix, rotate(theta, 0, 0, 1));

    //scale down by factor of 2 on x and y
    modelViewMatrix = mult(modelViewMatrix, scale(0.5, 0.5, 1.0));

    //translate to origin
    modelViewMatrix = mult(modelViewMatrix, translate(-0.4, -0.4, 0.0));

    //translate to new location (change x values to the a negative)
    modelViewMatrix2 = mult(modelViewMatrix2, translate(-0.4, 0.4, 0.0));


    //rotation clockwise
    modelViewMatrix2 = mult(modelViewMatrix2, rotate(-theta, 0, 0, 1));

    //scale down by factor of 2 on x and y
    modelViewMatrix2 = mult(modelViewMatrix2, scale(0.5, 0.5, 1.0));

    //translate to origin
    modelViewMatrix2 = mult(modelViewMatrix2, translate(-0.4, -0.4, 0.0));


    // send color and matrix for square then render
    gl.uniform4fv(colorLoc, flatten(blue));
    //render square 1
    gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(modelViewMatrix));
    gl.drawArrays(gl.TRIANGLE_FAN, 0, 4);
    //render square 2
    gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(modelViewMatrix2));
    gl.drawArrays(gl.TRIANGLE_FAN, 0, 4);

    requestAnimationFrame(render);
}

