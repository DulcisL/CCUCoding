/*Save the Exam2_XX files with XX replaced by your student number. Modify the code to make the buttons work as demonstrated for the Exercises. The Scene button works as demonstrated in class.

Apply the transformations in the vertex shader by sending the angles, scaling, and translation factors as uniform variables.

Do not use the rotate, scale, or translate functions included in MV.js or MVnew.js.
Do not name any variables “rotate”, “scale”, or “translate”.
Do not modify the “vertices” variable.
Do not add any vertices or buffers.
Upload your files in the space below.

for scene make 3 copies at smaller scales, smallest is top left biggest bottome right
    send factors as uniform variables
*/
"use strict";

var canvas;
var gl;

var numPositions = 36;

var positions = [];
var colors = [];

var xAxis = 0;
var yAxis = 1;
var zAxis = 2;

var axis = 0;
var scaleAxis;
var theta = [0, 0, 0];
var scale = [1.0, 1.0, 1.0];
var translateFac = [0, 0, 0];

var thetaLoc;
var scaleLoc;
var translateLoc;

var factor = 0.5;
var pause = false;
var direction = true;
var solid = true;
var scene = false;

var vertices = [
    vec4(-0.5, -0.5, 0.5, 1.0),
    vec4(-0.5, 0.5, 0.5, 1.0),
    vec4(0.5, 0.5, 0.5, 1.0),
    vec4(0.5, -0.5, 0.5, 1.0),
    vec4(-0.5, -0.5, -0.5, 1.0),
    vec4(-0.5, 0.5, -0.5, 1.0),
    vec4(0.5, 0.5, -0.5, 1.0),
    vec4(0.5, -0.5, -0.5, 1.0)
];
var vertexColors = [
    vec4(0.0, 0.0, 0.0, 1.0),  // black
    vec4(1.0, 0.0, 0.0, 1.0),  // red
    vec4(1.0, 1.0, 0.0, 1.0),  // yellow
    vec4(0.0, 1.0, 0.0, 1.0),  // green
    vec4(0.0, 0.0, 1.0, 1.0),  // blue
    vec4(1.0, 0.0, 1.0, 1.0),  // magenta
    vec4(0.0, 1.0, 1.0, 1.0),  // cyan
    vec4(1.0, 1.0, 1.0, 1.0)   // white
];

window.onload = function init() {
    canvas = document.getElementById("gl-canvas");

    gl = canvas.getContext('webgl2');
    if (!gl) alert("WebGL 2.0 isn't available");

    colorCube();

    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0.7, 0.7, 0.7, 1.0);

    gl.enable(gl.DEPTH_TEST);

    //  Load shaders and initialize attribute buffers
    var program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);

    var vBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(positions), gl.STATIC_DRAW);

    var positionLoc = gl.getAttribLocation(program, "aPosition");
    gl.vertexAttribPointer(positionLoc, 4, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(positionLoc);

    var cBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW);

    var colorLoc = gl.getAttribLocation(program, "aColor");
    gl.vertexAttribPointer(colorLoc, 4, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(colorLoc);

    thetaLoc = gl.getUniformLocation(program, "uTheta");
    scaleLoc = gl.getUniformLocation(program, "uScale");
    //translateLoc = gl.getUniformLocation(program, "uTranslate");



    //event listeners for buttons
    document.getElementById("xButton").onclick = function () {
        axis = xAxis;
    };
    document.getElementById("yButton").onclick = function () {
        axis = yAxis;
    };
    document.getElementById("zButton").onclick = function () {
        axis = zAxis;
    };
    document.getElementById("pauseButton").onclick = function () {
        pause = !pause
        if (pause == true) {
            theta = theta;
        }
    };
    document.getElementById("sceneButton").onclick = function () {
        scene = !scene
    };
    document.getElementById("directionButton").onclick = function () {
        direction = !direction;
    };
    document.getElementById("colorButton").onclick = function () {
        solid = !solid;
        //Reset color array
        colors = [];
        //call for new colors
        colorCube();
        //Update colors
        gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW);
    };
    render();
}

function colorCube() {
    quad(1, 0, 3, 2);
    quad(2, 3, 7, 6);
    quad(3, 0, 4, 7);
    quad(6, 5, 1, 2);
    quad(4, 5, 6, 7);
    quad(5, 4, 0, 1);
}

function quad(a, b, c, d) {
    // We need to parition the quad into two triangles in order for
    // WebGL to be able to render it.  In this case, we create two
    // triangles from the quad indices

    var indices = [a, b, c, a, c, d];
    if (solid) {
        for (var i = 0; i < indices.length; ++i) {
            positions.push(vertices[indices[i]]);
            // for solid colored faces use (only pushes 6 colors)
            colors.push(vertexColors[a]);
        }
    }
    if (!solid) {
        for (var i = 0; i < indices.length; ++i) {
            // for interpolated vertex colors use (pushes a color per vertex)
            positions.push(vertices[indices[i]]);
            colors.push(vertexColors[indices[i]]);
        }
    }
}

function render() {
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    if (direction == true && !pause) {
        theta[axis] += 2.0;
    }
    if (direction == false && !pause) {
        theta[axis] -= 2.0;
    }
    if (scene) {
        //Make 3 copies
        /*
        for (var i = 0; i < 3; ++i) {
            if (i == 0) {
                translateFac = [.4, -.4, 0]
            }
            if (i == 1) {
                translateFac = [0, 0, 0]
            }
            if (i == 2) {
                translateFac = [-.4, .4, 0]
            }

            scaleFac = scaleFac * 1 / (i + 1);

            gl.uniform3fv(thetaLoc, theta);
            gl.uniform3fv(scaleLoc, scaleFac);
            gl.uniform3fv(translateLoc, translateFac);

            gl.drawArrays(gl.TRIANGLES, 0, numPositions);
            */



    }
    if (!scene) {
        gl.uniform3fv(thetaLoc, theta);
        gl.uniform3fv(scaleLoc, scale);

        //gl.uniform3fv(translateLoc, translateFac);

        gl.drawArrays(gl.TRIANGLES, 0, numPositions);
    }



    requestAnimationFrame(render);
}
