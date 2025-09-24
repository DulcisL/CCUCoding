/* Using menus change the rotation menu to include a toggle 
    rotation (change direction) and a pause Rotation
    add another menu that scales x-, x+, y-, y+ ,z-, z+ 
    (factor through application of a uniform variable)
    
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

var thetaLoc;
var scaleLoc;

var factor = 1.0;
var speed = 2.0;

window.onload = function init() {
    canvas = document.getElementById("gl-canvas");

    gl = canvas.getContext('webgl2');
    if (!gl) alert("WebGL 2.0 isn't available");

    colorCube();

    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(1.0, 1.0, 1.0, 1.0);

    gl.enable(gl.DEPTH_TEST);

    //
    //  Load shaders and initialize attribute buffers
    //
    var program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);

    var cBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW);

    var colorLoc = gl.getAttribLocation(program, "aColor");
    gl.vertexAttribPointer(colorLoc, 4, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(colorLoc);

    var vBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(positions), gl.STATIC_DRAW);


    var positionLoc = gl.getAttribLocation(program, "aPosition");
    gl.vertexAttribPointer(positionLoc, 4, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(positionLoc);

    thetaLoc = gl.getUniformLocation(program, "uTheta");
    scaleLoc = gl.getUniformLocation(program, "uScale");

    //event listeners for buttons

    document.getElementById("Rotations").onclick = function (event) {
        switch (event.target.index) {
            case 0:
                //rotate X
                axis = xAxis;
                break;
            case 1:
                //rotate y
                axis = yAxis;
                break;
            case 2:
                //rotate z
                axis = zAxis;
                break;
            case 3:
                //change direction
                speed = -speed
                break;
            case 4:
                //pause
                if (speed != 0)
                    speed = 0;
                else {
                    speed = 2.0;
                }
                break;
        }
    };
    document.getElementById("Scales").onclick = function (event) {
        factor = .2
        switch (event.target.index) {
            case 0:
                //scale x +
                //set axis
                scaleAxis = xAxis;
                //set factor to scale by
                scale[scaleAxis] += factor;
                break;
            case 1:
                //scale x -
                scaleAxis = xAxis;
                scale[scaleAxis] -= factor;
                break;
            case 2:
                //scale y +
                scaleAxis = yAxis;
                scale[scaleAxis] += factor;
                break;
            case 3:
                //scale y -
                scaleAxis = yAxis;
                scale[scaleAxis] -= factor;
                break;
            case 4:
                //scale z +
                scaleAxis = zAxis;
                scale[scaleAxis] += factor;
                break;
            case 5:
                //scale z -
                scaleAxis = zAxis;
                scale[scaleAxis] -= factor;
                break;
        }
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

    // We need to parition the quad into two triangles in order for
    // WebGL to be able to render it.  In this case, we create two
    // triangles from the quad indices

    //vertex color assigned by the index of the vertex

    var indices = [a, b, c, a, c, d];

    for (var i = 0; i < indices.length; ++i) {
        positions.push(vertices[indices[i]]);
        //colors.push( vertexColors[indices[i]] );

        // for solid colored faces use
        colors.push(vertexColors[a]);
    }
}

function render() {
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    theta[axis] += speed;

    gl.uniform3fv(thetaLoc, theta);
    gl.uniform3fv(scaleLoc, scale);

    gl.drawArrays(gl.TRIANGLES, 0, numPositions);
    requestAnimationFrame(render);
}
