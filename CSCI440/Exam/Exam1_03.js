var gl;

var theta = 0.0;
var thetaLoc;

var pause = true;
var direction = true;
var speed = 0.05;

var colors = [];
var flip = false;


window.onload = function init() {
    var canvas = document.getElementById("gl-canvas");

    gl = canvas.getContext('webgl2');
    if (!gl) alert("WebGL 2.0 isn't available");

    //  Configure WebGL
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0.8, 0.8, 0.8, 1.0);
    gl.enable(gl.DEPTH_TEST);


    //  Load shaders and initialize attribute buffers
    var program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);

    var vertices = [
        //x , y , z
        //triangle 1
        vec3(-1.0, 0.25, 0.0),
        vec3(0.0, 1.0, 0.0),
        vec3(1.0, 0.25, 0.0),

        //triangle 2
        vec3(-1.0, -0.25, 0.0),
        vec3(1.0, -0.25, 0.0),
        vec3(0.0, -1.0, 0.0),

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

    colors = [baseColors[0], baseColors[1], baseColors[2], baseColors[5], baseColors[4], baseColors[3]];


    //Set color buffer (Next 6 lines are required for color)
    var cBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW);

    var colorLoc = gl.getAttribLocation(program, "aColor");
    gl.vertexAttribPointer(colorLoc, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(colorLoc);

    // Create a buffer object, initialize it, and associate it with the
    //  associated attribute variable in our vertex shader
    var vBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(vertices), gl.STATIC_DRAW);

    var positionLoc = gl.getAttribLocation(program, "aPosition");
    gl.vertexAttribPointer(positionLoc, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(positionLoc);

    thetaLoc = gl.getUniformLocation(program, "uTheta");

    // Initialize event handlers
    document.getElementById("Color").onclick = function () {
        //change colors
        flip = !flip;
        if (flip) {
            //Flip colors
            colors = [baseColors[3], baseColors[4], baseColors[5], baseColors[2], baseColors[1], baseColors[0]];
        }
        if (!flip) {
            //top triangle R, G, B Bottom triangle Cy, Ye, Mg
            colors = [baseColors[0], baseColors[1], baseColors[2], baseColors[5], baseColors[4], baseColors[3]];
        }
        //Update the color buffer
        gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW);
    };

    document.getElementById("Controls").onclick = function (event) {
        switch (event.target.index) {
            case 0:
                //pause
                pause = !pause;
                break;
            case 1:
                //direction
                direction = !direction;
                break;
            case 2:
                //speed up
                speed = speed * 2.0;
                break;
            case 3:
                //slow down
                speed = speed / 2.0;
                break;
        }
    };

    render();
};

function render() {
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    if (!pause) {
        if (direction) {
            theta += speed;
        }
        if (!direction) {
            theta -= speed;
        }
    }
    gl.uniform1f(thetaLoc, theta);

    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 3);
    gl.drawArrays(gl.TRIANGLE_STRIP, 3, 3);

    requestAnimationFrame(render);

}
