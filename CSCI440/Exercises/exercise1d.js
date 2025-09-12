var gl;

var theta = 0.0;
var thetaLoc;

var positions;
var numVertices = 4;
var colors = [];

var direction = true;
var pause = false;
var speed = 0.01;

window.onload = function init() {
    var canvas = document.getElementById("gl-canvas");

    gl = canvas.getContext('webgl2');
    if (!gl) alert("WebGL 2.0 isn't available");

    // Four vertices
    var vertices = [
        vec2(0, 1),
        vec2(-1, 0),
        vec2(1, 0),
        vec2(0, -1)
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

    colors = [baseColors[0], baseColors[1], baseColors[2], baseColors[6]];

    //  Configure WebGL

    gl.viewport(0, 0, canvas.width, canvas.height);
    //set background color
    gl.clearColor(0.0, 0.0, 0.0, 0.10);
    //enable hidden-surface removal
    gl.enable(gl.DEPTH_TEST);

    //  Load shaders and initialize attribute buffers

    var program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);

    // Load the data into the GPU
    // Associate out shader variables with our data buffer

    var vBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
    //use vertices array to fill buffer for color
    gl.bufferData(gl.ARRAY_BUFFER, flatten(vertices), gl.STATIC_DRAW);

    var positionLoc = gl.getAttribLocation(program, "aPosition");
    gl.vertexAttribPointer(positionLoc, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(positionLoc);

    thetaLoc = gl.getUniformLocation(program, "uTheta");

    // Initialize event handlers
    document.getElementById("Pause").onclick = function () {
        pause = !pause
    };

    document.getElementById("Controls").onclick = function (event) {
        switch (event.target.index) {
            case 0:
                direction = !direction;
                break;
            case 1:
                speed *= 2;
                break;
            case 2:
                speed /= 2;
                break;
        }
    };

    render();
};

function render() {
    gl.clear(gl.COLOR_BUFFER_BIT);
    /* This is not necessary only need the below if statement
    if (pause){
        //do nothing (stop the changing of theta)
    }
    */
    if (!pause) {
        if (direction) {
            theta += speed;
        }

        if (!direction) {
            theta -= speed;
        }
    }

    gl.uniform1f(thetaLoc, theta);

    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);

    requestAnimationFrame(render);
}
