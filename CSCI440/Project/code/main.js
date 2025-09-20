/* This is the main js file for the project. This project is to have a piece of paper go through
    a series of transformations to turn into a origami bird / plane. After the transformations the shape will
    then be animated to look like it is flying through a series of scenes.
*/
var canvas;
var gl;
var colors = [];
const COLOR_PALLET = [
    vec3(1.0, 0.0, 0.0), //Red
    vec3(0.0, 1.0, 0.0), //Green
    vec3(0.0, 0.0, 1.0), //Blue
    vec3(1.0, 0.0, 1.0), //Magenta
    vec3(1.0, 1.0, 0.0), //Yellow
    vec3(0.0, 1.0, 1.0), //Cyan
    vec3(0.6, 0.3, 0.0), //Brown
    vec3(0.0, 0.0, 0.0), //Black
    vec3(1.0, 1.0, 1.0) //White
];
colors = [COLOR_PALLET[8], COLOR_PALLET[8], COLOR_PALLET[8], COLOR_PALLET[8], COLOR_PALLET[6], COLOR_PALLET[6], COLOR_PALLET[6], COLOR_PALLET[6]];

window.onload = function init() {
    canvas = document.getElementById("gl-canvas");

    gl = gl = canvas.getContext('webgl2');
    if (!gl) { alert("WebGL 2.0 isn't available"); }

    //Vertices

    var vertices = [
        //paper square
        vec3(-0.25, -0.25, 0.0), //back left
        vec3(-0.25, 0.25, 0.0),  //back right
        vec3(0.25, 0.25, 0.0),  //front right
        vec3(0.25, -0.25, 0.0), //front left

        //Desktop square
        vec3(-0.65, -0.5, 0.5), //back left
        vec3(-0.75, 0.5, 0.5),   //back right
        vec3(0.55, 0.5, 0.5),    //front right
        vec3(0.75, -0.5, 0.5),   //front left

        //desk legs
        vec3(-0.6, -0.5, 0.5), //back left
        vec3(-0.55, -0.5, -0.5), //back right
        vec3(-0.45, -0.5, -0.5), //front right
        vec3(-0.4, -0.5, 0.5), //front left
    ];


    //  Configure WebGL



    //  Load shaders and initialize attribute buffers

    var program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);

    // Load the data into the GPU
    //Set color buffer (Next 6 lines are required for color)
    var cBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW);

    var colorLoc = gl.getAttribLocation(program, "aColor");
    gl.vertexAttribPointer(colorLoc, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(colorLoc);

    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0.0, 0.0, 1.0, 1.0);
    gl.enable(gl.DEPTH_TEST);

    var bufferId = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, bufferId);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(vertices), gl.STATIC_DRAW);

    // Associate out shader variable with our data buffer

    var aPosition = gl.getAttribLocation(program, "aPosition");
    gl.vertexAttribPointer(aPosition, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(aPosition);

    render();
};

function render() {
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    //draw desk
    gl.drawArrays(gl.TRIANGLE_FAN, 4, 4);

    //draw paper
    gl.drawArrays(gl.TRIANGLE_FAN, 0, 4);
}
