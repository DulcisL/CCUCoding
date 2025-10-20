/*
Exercise 3b
- Change shape to a rectangle
- Use interpolated colors: TL - Green, TR - Red BL - Blue BR - Yellow
- Add buttons for:
    - camera move x,y,z like 3a 
    - add light up and light down buttons
*/
"use strict";

var shadow = function () {

    var canvas;
    var gl;

    var positionsArray = [];
    var near = -4;
    var far = 4;

    var theta = 0.0;

    var left = -2.0;
    var right = 2.0;
    var top = 2.0;
    var bottom = -2.0;

    var modelViewMatrix, projectionMatrix;
    var modelViewMatrixLoc, projectionMatrixLoc;

    var colorLoc;

    var eye, at, up;
    var light;

    var m;

    window.onload = function init() {

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

        canvas = document.getElementById("gl-canvas");

        gl = canvas.getContext('webgl2');
        if (!gl) alert("WebGL 2.0 isn't available");


        gl.viewport(0, 0, canvas.width, canvas.height);

        gl.clearColor(1.0, 1.0, 1.0, 1.0);

        gl.enable(gl.DEPTH_TEST);

        light = vec3(0.0, 2.0, 0.0);

        // matrix for shadow projection

        m = mat4();
        m[3][3] = 0;
        m[3][1] = -1 / light[1];

        //console.log("m");
        //printm(m);

        at = vec3(0.0, 0.0, 0.0);
        up = vec3(0.0, 1.0, 0.0);
        eye = vec3(1.0, 1.0, 1.0);

        // rectangle

        positionsArray.push(vec4(-0.8, 0.5, -0.4, 1.0));
        positionsArray.push(vec4(-0.8, 0.5, 0.4, 1.0));
        positionsArray.push(vec4(0.5, 0.5, 0.4, 1.0));
        positionsArray.push(vec4(0.5, 0.5, -0.4, 1.0));
        var colors = [vertexColors[3], vertexColors[1], vertexColors[4], vertexColors[2]];

        //
        //  Load shaders and initialize attribute buffers
        //
        var program = initShaders(gl, "vertex-shader", "fragment-shader");
        gl.useProgram(program);

        //Get variables from html
        colorLoc = gl.getAttribLocation(program, "aColor");
        gl.enableVertexAttribArray(colorLoc);

        var vBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, flatten(positionsArray), gl.STATIC_DRAW);

        var positionLoc = gl.getAttribLocation(program, "aPosition");
        gl.vertexAttribPointer(positionLoc, 4, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(positionLoc);

        modelViewMatrixLoc = gl.getUniformLocation(program, "uModelViewMatrix");
        projectionMatrixLoc = gl.getUniformLocation(program, "uProjectionMatrix");

        projectionMatrix = ortho(left, right, bottom, top, near, far);
        gl.uniformMatrix4fv(projectionMatrixLoc, false, flatten(projectionMatrix));

        document.getElementById("Button1").onclick = function () { eye[0] += 0.25; };
        document.getElementById("Button2").onclick = function () { eye[0] -= 0.25; };
        document.getElementById("Button3").onclick = function () { eye[1] += 0.25; };
        document.getElementById("Button4").onclick = function () { eye[1] -= 0.25; };
        document.getElementById("Button5").onclick = function () { eye[2] += 0.25; };
        document.getElementById("Button6").onclick = function () { eye[2] -= 0.25; };
        document.getElementById("Button7").onclick = function () { light[1] += 0.25 };
        document.getElementById("Button8").onclick = function () { light[1] -= 0.25 };

        render();

    }

    var render = function () {

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

        theta += 0.1;
        if (theta > 2 * Math.PI) theta -= 2 * Math.PI;

        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

        // model-view matrix for square

        modelViewMatrix = lookAt(eye, at, up);

        //set color
        var colors = [vertexColors[3], vertexColors[1], vertexColors[4], vertexColors[2]];
        //set buffer
        var cBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
        //send color and matrix to render
        gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW);
        gl.vertexAttribPointer(colorLoc, 4, gl.FLOAT, false, 0, 0);
        gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(modelViewMatrix));
        gl.drawArrays(gl.TRIANGLE_FAN, 0, 4);

        // rotate light source

        light[0] = Math.sin(theta);
        light[2] = Math.cos(theta);


        modelViewMatrix = mult(modelViewMatrix, translate(light[0], light[1], light[2]));

        modelViewMatrix = mult(modelViewMatrix, m);

        modelViewMatrix = mult(modelViewMatrix, translate(-light[0], -light[1],
            -light[2]));

        //Set color
        colors = [vertexColors[0], vertexColors[0], vertexColors[0], vertexColors[0]];
        //reset color buffer
        cBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
        //send color and matrix for shadow
        gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW);
        gl.vertexAttribPointer(colorLoc, 4, gl.FLOAT, false, 0, 0);

        gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(modelViewMatrix));
        gl.drawArrays(gl.TRIANGLE_FAN, 0, 4);

        requestAnimationFrame(render);
    }

}


shadow();
