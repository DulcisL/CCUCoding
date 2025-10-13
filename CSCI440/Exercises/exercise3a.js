/*
Modify the camera so the position is set by rectangular coordinates (x,y,z). 
Initalize the camer at [1.0,1.0,4.0]. The increments/ decrements shoudl be 0.25. 
Add a button to switch between orthographic and perspective projections

suggested values
perspective: fovy = 60.0, near = 0.3
orthographic: near = -6.0 
*/
"use strict";

function orthoExample() {

    var canvas;
    var gl;

    var numVertices = 36;

    var positionsArray = [];
    var colorsArray = [];

    var vertices = [
        vec4(-0.5, -0.5, 0.5, 1.0),
        vec4(-0.5, 0.5, 0.5, 1.0),
        vec4(0.5, 0.5, 0.5, 1.0),
        vec4(0.5, -0.5, 0.5, 1.0),
        vec4(-0.5, -0.5, -0.5, 1.0),
        vec4(-0.5, 0.5, -0.5, 1.0),
        vec4(0.5, 0.5, -0.5, 1.0),
        vec4(0.5, -0.5, -0.5, 1.0),
    ];

    var vertexColors = [
        vec4(0.0, 0.0, 0.0, 1.0),  // black
        vec4(1.0, 0.0, 0.0, 1.0),  // red
        vec4(1.0, 1.0, 0.0, 1.0),  // yellow
        vec4(0.0, 1.0, 0.0, 1.0),  // green
        vec4(0.0, 0.0, 1.0, 1.0),  // blue
        vec4(1.0, 0.0, 1.0, 1.0),  // magenta
        vec4(0.0, 1.0, 1.0, 1.0),  // cyan
        vec4(1.0, 1.0, 1.0, 1.0),  // white
    ];

    var near;
    var far;

    var left = -1.0;
    var right = 1.0;
    var top = 1.0;
    var bottom = -1.0;

    var modelViewMatrixLoc, projectionMatrixLoc;
    var modelViewMatrix, projectionMatrix;
    //set to initial eye position
    var eye = vec3(1.0, 1.0, 4.0);
    var switchPersp = false;

    const at = vec3(0.0, 0.0, 0.0);
    const up = vec3(0.0, 1.0, 0.0);

    // quad uses first index to set color for face

    function quad(a, b, c, d) {
        positionsArray.push(vertices[a]);
        colorsArray.push(vertexColors[a]);
        positionsArray.push(vertices[b]);
        colorsArray.push(vertexColors[a]);
        positionsArray.push(vertices[c]);
        colorsArray.push(vertexColors[a]);
        positionsArray.push(vertices[a]);
        colorsArray.push(vertexColors[a]);
        positionsArray.push(vertices[c]);
        colorsArray.push(vertexColors[a]);
        positionsArray.push(vertices[d]);
        colorsArray.push(vertexColors[a]);
    }

    // Each face determines two triangles

    function colorCube() {
        quad(1, 0, 3, 2);
        quad(2, 3, 7, 6);
        quad(3, 0, 4, 7);
        quad(6, 5, 1, 2);
        quad(4, 5, 6, 7);
        quad(5, 4, 0, 1);
    }


    window.onload = function init() {
        canvas = document.getElementById("gl-canvas");

        gl = canvas.getContext('webgl2');
        if (!gl) alert("WebGL 2.0 isn't available");

        gl.viewport(0, 0, canvas.width, canvas.height);

        gl.clearColor(1.0, 1.0, 1.0, 1.0);

        gl.enable(gl.DEPTH_TEST);

        //
        //  Load shaders and initialize attribute buffers
        //
        var program = initShaders(gl, "vertex-shader", "fragment-shader");
        gl.useProgram(program);

        colorCube();

        var cBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, flatten(colorsArray), gl.STATIC_DRAW);

        var colorLoc = gl.getAttribLocation(program, "aColor");
        gl.vertexAttribPointer(colorLoc, 4, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(colorLoc);

        var vBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, flatten(positionsArray), gl.STATIC_DRAW);

        var positionLoc = gl.getAttribLocation(program, "aPosition");
        gl.vertexAttribPointer(positionLoc, 4, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(positionLoc);

        modelViewMatrixLoc = gl.getUniformLocation(program, "uModelViewMatrix");
        projectionMatrixLoc = gl.getUniformLocation(program, "uProjectionMatrix");

        // buttons to change viewing parameters

        document.getElementById("Button1").onclick = function () { eye[0] += 0.25; };
        document.getElementById("Button2").onclick = function () { eye[0] -= 0.25; };
        document.getElementById("Button3").onclick = function () { eye[1] += 0.25; };
        document.getElementById("Button4").onclick = function () { eye[1] -= 0.25; };
        document.getElementById("Button5").onclick = function () { eye[2] += 0.25; };
        document.getElementById("Button6").onclick = function () { eye[2] -= 0.25; };
        document.getElementById("Button7").onclick = function () { switchPersp = !switchPersp; };

        render();
    }


    var render = function () {
        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

        //eye = vec3(radius * Math.sin(phi), radius * Math.sin(theta), radius * Math.cos(phi));

        modelViewMatrix = lookAt(eye, at, up);
        //Use orthographic
        if (switchPersp) {
            near = -6.0
            far = 6.0;
            projectionMatrix = ortho(left, right, bottom, top, near, far);
        }

        //use perspective
        if (!switchPersp) {
            var fovy = 60.0;
            near = 0.3;
            far = 6.0;
            projectionMatrix = perspective(fovy, 1, near, far);
        }


        gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(modelViewMatrix));
        gl.uniformMatrix4fv(projectionMatrixLoc, false, flatten(projectionMatrix));

        gl.drawArrays(gl.TRIANGLES, 0, numVertices);
        requestAnimationFrame(render);
    }
}
orthoExample();
