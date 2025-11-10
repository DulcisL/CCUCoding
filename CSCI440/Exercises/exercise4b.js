/*
Change colors/ camera view, change to mettalic or matte etc, be able to alter physical appearance
Buttons: Walk (Start with move legs back and forth between 2 stops,later move head , arms (Upper/ Lower seperately))
         Reset
         possible buttons later:
         Nod
         Run
         Wave         
         Turn
*/
"use strict";

//Button Variables
var initialPos = true;
var walk = false;
var run = false;
var wave = false;
var nod = false;
var shakeHead = false;
var lookAround = false;
var turnAround = false;

//Movement variables
var legFWD = true;
var armFWD = true;
var lookLft = true;
var lookUp = true;
var legStop = 0;
var armStop = 0;
var headStop = 0;
var speed = 0;

//Color variables
var vertexColors = [
    vec4( 0.0, 0.0, 0.0, 1.0 ),  // black
    vec4( 1.0, 0.0, 0.0, 1.0 ),  // red
    vec4( 1.0, 1.0, 0.0, 1.0 ),  // yellow
    vec4( 0.0, 1.0, 0.0, 1.0 ),  // green
    vec4( 0.0, 0.0, 1.0, 1.0 ),  // blue
    vec4( 1.0, 0.0, 1.0, 1.0 ),  // magenta
    vec4( 1.0, 1.0, 1.0, 1.0 ),  // white
    vec4( 0.0, 1.0, 1.0, 1.0 )   // cyan
];

var lightPosition = vec4(1.0, -10.0, 10.0, 0.0);
var lightAmbient = vec4(0.2, 0.2, 0.2, 1.0);
var lightDiffuse = vec4(1.0, 1.0, 1.0, 1.0);
var lightSpecular = vec4(1.0, 1.0, 1.0, 1.0);

var materialAmbient = vec4(1.0, 0.0, 1.0, 1.0);
var materialDiffuse = vec4(1.0, 0.8, 0.0, 1.0);
var materialSpecular = vec4(1.0, 0.8, 0.0, 1.0);
var materialShininess = 50.0;

//Everything else

var canvas;
var gl;
var program;

var projectionMatrix;
var modelViewMatrix;

var instanceMatrix;

var modelViewMatrixLoc;

var vertices = [

    vec4( -0.5, -0.5,  0.5, 1.0 ),
    vec4( -0.5,  0.5,  0.5, 1.0 ),
    vec4( 0.5,  0.5,  0.5, 1.0 ),
    vec4( 0.5, -0.5,  0.5, 1.0 ),
    vec4( -0.5, -0.5, -0.5, 1.0 ),
    vec4( -0.5,  0.5, -0.5, 1.0 ),
    vec4( 0.5,  0.5, -0.5, 1.0 ),
    vec4( 0.5, -0.5, -0.5, 1.0 )
];


var torsoId = 0;
var headId  = 1;
var head1Id = 1;
var head2Id = 10;
var leftUpperArmId = 2;
var leftLowerArmId = 3;
var rightUpperArmId = 4;
var rightLowerArmId = 5;
var leftUpperLegId = 6;
var leftLowerLegId = 7;
var rightUpperLegId = 8;
var rightLowerLegId = 9;


var torsoHeight = 5.0;
var torsoWidth = 2.0;
var upperArmHeight = 3.0;
var lowerArmHeight = 2.0;
var upperArmWidth  = 0.75;
var lowerArmWidth  = 0.5;
var upperLegWidth  = 0.75;
var lowerLegWidth  = 0.5;
var lowerLegHeight = 2.0;
var upperLegHeight = 3.0;
var headHeight = 1.5;
var headWidth = 1.0;

var numNodes = 10;
var numAngles = 11;
var angle = 0;
//Order: Torso, Head y, Upper LA, Lower LA, Upper RA, Lower LA, Upper LL, Lower LL, Upper RL, Lower LL, Head x
var theta = [45, 0, 180, 45, 180, 45, 180, 0, 180, 0, 0];

var numVertices = 24;

var stack = [];

var figure = [];

var normalsArray = [];

for( var i=0; i<numNodes; i++) figure[i] = createNode(null, null, null, null);

var vBuffer;
var modelViewLoc;

var pointsArray = [];


//-------------------------------------------

function scale4(a, b, c) {
   var result = mat4();
   result[0] = a;
   result[5] = b;
   result[10] = c;
   return result;
}

//--------------------------------------------


function createNode(transform, render, sibling, child){
    var node = {
    transform: transform,
    render: render,
    sibling: sibling,
    child: child,
    }
    return node;
}


function initNodes(Id) {

    var m = mat4();

    switch(Id) {

        case torsoId:

            m = rotate(theta[torsoId], vec3(0, 1, 0) );
            figure[torsoId] = createNode( m, torso, null, headId );
            break;

        case headId:
        case head1Id:
        case head2Id:


            m = translate(0.0, torsoHeight+0.5*headHeight, 0.0);
            m = mult(m, rotate(theta[head1Id], vec3(1, 0, 0)));
            m = mult(m, rotate(theta[head2Id], vec3(0, 1, 0)));
            m = mult(m, translate(0.0, -0.5*headHeight, 0.0));
            figure[headId] = createNode( m, head, leftUpperArmId, null);
            break;


        case leftUpperArmId:

            m = translate(-(torsoWidth/2 + .25), 0.9*torsoHeight, 0.0);
            m = mult(m, rotate(theta[leftUpperArmId], vec3(1, 0, 0)));
            figure[leftUpperArmId] = createNode( m, leftUpperArm, rightUpperArmId, leftLowerArmId );
            break;

        case rightUpperArmId:

            m = translate(torsoWidth/2 + .25, 0.9*torsoHeight, 0.0);
            m = mult(m, rotate(theta[rightUpperArmId], vec3(1, 0, 0)));
            figure[rightUpperArmId] = createNode( m, rightUpperArm, leftUpperLegId, rightLowerArmId );
            break;

        case leftUpperLegId:

            m = translate(-(torsoWidth/2), 0.1*upperLegHeight, 0.0);
            m = mult(m , rotate(theta[leftUpperLegId], vec3(1, 0, 0)));
            figure[leftUpperLegId] = createNode( m, leftUpperLeg, rightUpperLegId, leftLowerLegId );
            break;

        case rightUpperLegId:

            m = translate(torsoWidth/2, 0.1*upperLegHeight, 0.0);
            m = mult(m, rotate(theta[rightUpperLegId], vec3(1, 0, 0)));
            figure[rightUpperLegId] = createNode( m, rightUpperLeg, null, rightLowerLegId );
            break;

        case leftLowerArmId:

            m = translate(0.0, upperArmHeight, 0.0);
            m = mult(m, rotate(theta[leftLowerArmId], vec3(1, 0, 0)));
            figure[leftLowerArmId] = createNode( m, leftLowerArm, null, null );
            break;

        case rightLowerArmId:

            m = translate(0.0, upperArmHeight, 0.0);
            m = mult(m, rotate(theta[rightLowerArmId], vec3(1, 0, 0)));
            figure[rightLowerArmId] = createNode( m, rightLowerArm, null, null );
            break;

        case leftLowerLegId:

            m = translate(0.0, upperLegHeight, 0.0);
            m = mult(m, rotate(theta[leftLowerLegId],vec3(1, 0, 0)));
            figure[leftLowerLegId] = createNode( m, leftLowerLeg, null, null );
            break;

        case rightLowerLegId:

            m = translate(0.0, upperLegHeight, 0.0);
            m = mult(m, rotate(theta[rightLowerLegId], vec3(1, 0, 0)));
            figure[rightLowerLegId] = createNode( m, rightLowerLeg, null, null );
            break;

    }

}

function traverse(Id) {

   if(Id == null) return;
   stack.push(modelViewMatrix);
   modelViewMatrix = mult(modelViewMatrix, figure[Id].transform);
   figure[Id].render();
   if(figure[Id].child != null) traverse(figure[Id].child);
    modelViewMatrix = stack.pop();
   if(figure[Id].sibling != null) traverse(figure[Id].sibling);
}

function torso() {

    instanceMatrix = mult(modelViewMatrix, translate(0.0, 0.5*torsoHeight, 0.0) );
    instanceMatrix = mult(instanceMatrix, scale( torsoWidth, torsoHeight, torsoWidth));
    gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(instanceMatrix) );
    for(var i =0; i<6; i++) gl.drawArrays(gl.TRIANGLE_FAN, 4*i, 4);
}

function head() {

    instanceMatrix = mult(modelViewMatrix, translate(0.0, 0.5 * headHeight, 0.0 ));
	instanceMatrix = mult(instanceMatrix, scale(headWidth, headHeight, headWidth) );
    gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(instanceMatrix) );
    for(var i =0; i<6; i++) gl.drawArrays(gl.TRIANGLE_FAN, 4*i, 4);
}

function leftUpperArm() {

    instanceMatrix = mult(modelViewMatrix, translate(0.0, 0.5 * upperArmHeight, 0.0) );
	instanceMatrix = mult(instanceMatrix, scale(upperArmWidth, upperArmHeight, upperArmWidth) );
    gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(instanceMatrix) );
    for(var i =0; i<6; i++) gl.drawArrays(gl.TRIANGLE_FAN, 4*i, 4);
}

function leftLowerArm() {

    instanceMatrix = mult(modelViewMatrix, translate(0.0, 0.5 * lowerArmHeight, 0.0) );
	instanceMatrix = mult(instanceMatrix, scale(lowerArmWidth, lowerArmHeight, lowerArmWidth) );
    gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(instanceMatrix) );
    for(var i =0; i<6; i++) gl.drawArrays(gl.TRIANGLE_FAN, 4*i, 4);
}

function rightUpperArm() {

    instanceMatrix = mult(modelViewMatrix, translate(0.0, 0.5 * upperArmHeight, 0.0) );
	instanceMatrix = mult(instanceMatrix, scale(upperArmWidth, upperArmHeight, upperArmWidth) );
  gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(instanceMatrix) );
    for(var i =0; i<6; i++) gl.drawArrays(gl.TRIANGLE_FAN, 4*i, 4);
}

function rightLowerArm() {

    instanceMatrix = mult(modelViewMatrix, translate(0.0, 0.5 * lowerArmHeight, 0.0) );
	instanceMatrix = mult(instanceMatrix, scale(lowerArmWidth, lowerArmHeight, lowerArmWidth) );
    gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(instanceMatrix) );
    for(var i =0; i<6; i++) gl.drawArrays(gl.TRIANGLE_FAN, 4*i, 4);
}

function  leftUpperLeg() {

    instanceMatrix = mult(modelViewMatrix, translate(0.0, 0.5 * upperLegHeight, 0.0) );
	instanceMatrix = mult(instanceMatrix, scale(upperLegWidth, upperLegHeight, upperLegWidth) );
    gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(instanceMatrix) );
    for(var i =0; i<6; i++) gl.drawArrays(gl.TRIANGLE_FAN, 4*i, 4);
}

function leftLowerLeg() {

    instanceMatrix = mult(modelViewMatrix, translate( 0.0, 0.5 * lowerLegHeight, 0.0) );
	instanceMatrix = mult(instanceMatrix, scale(lowerLegWidth, lowerLegHeight, lowerLegWidth) );
    gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(instanceMatrix) );
    for(var i =0; i<6; i++) gl.drawArrays(gl.TRIANGLE_FAN, 4*i, 4);
}

function rightUpperLeg() {

    instanceMatrix = mult(modelViewMatrix, translate(0.0, 0.5 * upperLegHeight, 0.0) );
	instanceMatrix = mult(instanceMatrix, scale(upperLegWidth, upperLegHeight, upperLegWidth) );
    gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(instanceMatrix) );
    for(var i =0; i<6; i++) gl.drawArrays(gl.TRIANGLE_FAN, 4*i, 4);
}

function rightLowerLeg() {

    instanceMatrix = mult(modelViewMatrix, translate(0.0, 0.5 * lowerLegHeight, 0.0) );
	instanceMatrix = mult(instanceMatrix, scale(lowerLegWidth, lowerLegHeight, lowerLegWidth) )
    gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(instanceMatrix) );
    for(var i =0; i<6; i++) gl.drawArrays(gl.TRIANGLE_FAN, 4*i, 4);
}

function quad(a, b, c, d) {

    var t1 = subtract(vertices[b], vertices[a]);
    var t2 = subtract(vertices[c], vertices[b]);
    var normal = cross(t1, t2);
    normal = vec3(normal);

     pointsArray.push(vertices[a]);
     normalsArray.push(normal);
     pointsArray.push(vertices[b]);
     normalsArray.push(normal);
     pointsArray.push(vertices[c]);
     normalsArray.push(normal);
     pointsArray.push(vertices[d]);
     normalsArray.push(normal);
}


function cube()
{
    quad( 1, 0, 3, 2 );
    quad( 2, 3, 7, 6 );
    quad( 3, 0, 4, 7 );
    quad( 6, 5, 1, 2 );
    quad( 4, 5, 6, 7 );
    quad( 5, 4, 0, 1 );
}
//-------------------------------------------

function lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess) {

    var ambientProduct = mult(lightAmbient, materialAmbient);
    var diffuseProduct = mult(lightDiffuse, materialDiffuse);
    var specularProduct = mult(lightSpecular, materialSpecular);

    gl.uniform4fv(gl.getUniformLocation(program, "uAmbientProduct"),
        ambientProduct);
    gl.uniform4fv(gl.getUniformLocation(program, "uDiffuseProduct"),
        diffuseProduct);
    gl.uniform4fv(gl.getUniformLocation(program, "uSpecularProduct"),
        specularProduct);
    gl.uniform4fv(gl.getUniformLocation(program, "uLightPosition"),
        lightPosition);

    gl.uniform1f(gl.getUniformLocation(program,
        "uShininess"), materialShininess);

    gl.uniformMatrix4fv(gl.getUniformLocation(program, "uProjectionMatrix"),
        false, flatten(projectionMatrix));

   }

window.onload = function init() {

    canvas = document.getElementById( "gl-canvas" );

    gl = canvas.getContext('webgl2');
    if (!gl) { alert( "WebGL 2.0 isn't available" ); }

    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( 1.0, 1.0, 1.0, 1.0 );
    gl.enable( gl.DEPTH_TEST );

    //
    //  Load shaders and initialize attribute buffers
    //
    program = initShaders( gl, "vertex-shader", "fragment-shader");

    gl.useProgram( program);

    instanceMatrix = mat4();

    projectionMatrix = ortho(-10.0,10.0,-10.0, 10.0,-10.0,10.0);
    modelViewMatrix = mat4();


    gl.uniformMatrix4fv(gl.getUniformLocation( program, "modelViewMatrix"), false, flatten(modelViewMatrix)  );
    gl.uniformMatrix4fv( gl.getUniformLocation( program, "projectionMatrix"), false, flatten(projectionMatrix)  );

    modelViewMatrixLoc = gl.getUniformLocation(program, "modelViewMatrix")

    cube();

    var nBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, nBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(normalsArray), gl.STATIC_DRAW);

    var normalLoc = gl.getAttribLocation(program, "aNormal");
    gl.vertexAttribPointer(normalLoc, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(normalLoc);

    vBuffer = gl.createBuffer();

    gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
    gl.bufferData(gl.ARRAY_BUFFER, flatten(pointsArray), gl.STATIC_DRAW);

    var positionLoc = gl.getAttribLocation( program, "aPosition" );
    gl.vertexAttribPointer( positionLoc, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( positionLoc );

    lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);


    document.getElementById("Button0").onclick = function() {
        //Reset
        initialPos = true;
        walk = false;
        run = false;
        wave = false;
        nod = false;
        shakeHead = false;
        lookAround = false;
        turnAround = false;
        
    };
    document.getElementById("Button1").onclick = function() {
        //Walk
        walk = !walk;
        initialPos = false;
        run = false;
        
    };
    document.getElementById("Button2").onclick = function() {
        //Run
        run = !run;
        initialPos = false;
        walk = false;
    };
    document.getElementById("Button3").onclick = function() {
        //Wave
        wave = !wave;
        initialPos = false;

    };
   document.getElementById("Button4").onclick = function() {
        //Nod
        nod = !nod;
        initialPos = false;
    };
    document.getElementById("Button5").onclick = function() {
        //Shake Head
        shakeHead = !shakeHead
        initialPos = false;
    };
    document.getElementById("Button6").onclick = function() {
        //Look around
        lookAround = !lookAround;
        initialPos = false;

    };
   document.getElementById("Button7").onclick = function() {
        //Turn
        turnAround = !turnAround;
        initialPos = false;

    };

    for(i=0; i<numNodes; i++) initNodes(i);

    render();
}


var render = function() {
        /*ToDo
        Add camera view change (look at function?)
        Add color
        */
       if (initialPos){
            //Order: Torso, Head X, Upper LA, Lower LA, Upper RA, Lower LA, Upper LL, Lower LL, Upper RL, Lower LL, Head Y
            theta = [45, 0, 180, 45, 180, 45, 180, 0, 180, 0, 0];
        }
        if (!initialPos){

            //Need to fix other buttons besides reset and walks

            if (walk || run){
                if (walk){
                speed = 1;
                legStop = 45;
                armStop = 45;
                run = false;
                }
                if (run){
                    speed = 3;
                    legStop = 55;
                    armStop = 55;
                    walk = false;
                }
                //create stops for limbs to set direction
                //legs and arms move inversely so only need to check on of each limb
                if (legFWD){
                    //Change direction if greater than stop value
                    if (theta[leftUpperLegId] >= (180 + legStop)){
                        legFWD = !legFWD;
                    }
                    //otherwise move leg
                    theta[leftUpperLegId] += speed; 
                    theta[rightUpperLegId] -= speed;
                    }
                if (!legFWD){
                    //Change direction if less than stop value
                    if (theta[leftUpperLegId] <= (180 - legStop)){
                        legFWD = !legFWD;
                    }
                    //otherwise move leg
                    theta[leftUpperLegId] -= speed;
                    theta[rightUpperLegId] += speed;
                }

                if (armFWD){
                    if (theta[leftUpperArmId] >= (180 + armStop)){
                        armFWD = !armFWD;
                    }
                    theta[leftUpperArmId] += speed;
                    theta[rightUpperArmId] -= speed;
                    
                }
                if (!armFWD){
                    if (theta[leftUpperArmId] <= (180 - armStop)){
                        armFWD = !armFWD;
                    }
                    theta[leftUpperArmId] -= speed;
                    theta[rightUpperArmId] += speed;
                    

                }
            }

            if(turnAround){
                theta[torsoId] += 1;
            }

            if (lookAround){
                headStop = 45;
                nod = true;
                shakeHead = true;
            }

            if (nod){
                if (lookUp){
                    //Y
                    if(theta[head2Id] >= headStop){
                        lookUp = !lookUp;
                    }
                    theta[head2Id] += 1;
                }
                if (!lookUp){
                    if(theta[head2Id] <= headStop){
                        lookUp = !lookUp;
                    }
                    theta[head2Id] -= 1;
                }
                if (!lookAround){
                    shakeHead = false;
                }
            }

            if (shakeHead){
                //X
                 if (lookLft){
                    if(theta[head1Id] >=  (theta[torsoId] + headStop)){
                        lookLft = !lookLft;
                    }
                    theta[head1Id] += 1;
                }
                if (!lookLft){
                    if(theta[head1Id] <= (theta[torsoId] - headStop)){
                        lookLft = !lookLft;
                    }
                    theta[head1Id] -= 1;
                }
                if (!lookAround){
                    nod = false;
                }
            }

        }
        

        //send new theta values
        for(i=0; i<numNodes; i++) initNodes(i);
        
        gl.clear( gl.COLOR_BUFFER_BIT );
        traverse(torsoId);
        requestAnimationFrame(render);
}
