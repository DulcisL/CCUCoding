/* 
buttons - Rotate x, rotate y, rotate z, toggle rotation (change direction), pause
sliders - add sliders for each light / material ambient, diffuse and specular in RGB (0 - 1.0)
background grey
cube color orange by default
*/
"use strict";

var shadedCube = function () {

   var canvas;
   var gl;

   var numPositions = 36;

   var positionsArray = [];
   var normalsArray = [];

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

   var lightPosition = vec4(1.0, 1.0, 1.0, 0.0);
   var lightAmbient = vec4(0.2, 0.2, 0.2, 1.0);
   var lightDiffuse = vec4(1.0, 1.0, 1.0, 1.0);
   var lightSpecular = vec4(1.0, 1.0, 1.0, 1.0);

   var materialAmbient = vec4(1.0, 0.0, 1.0, 1.0);
   var materialDiffuse = vec4(1.0, 0.8, 0.0, 1.0);
   var materialSpecular = vec4(1.0, 0.8, 0.0, 1.0);
   var materialShininess = 100.0;

   var ctm;
   var ambientColor, diffuseColor, specularColor;
   var modelViewMatrix, projectionMatrix;
   var viewerPos;
   var program;

   var xAxis = 0;
   var yAxis = 1;
   var zAxis = 2;
   var axis = 0;
   var theta = vec3(0, 0, 0);

   var thetaLoc;

   var flag = true;
   var direction = false;

   function quad(a, b, c, d) {

      var t1 = subtract(vertices[b], vertices[a]);
      var t2 = subtract(vertices[c], vertices[b]);
      var normal = cross(t1, t2);
      normal = vec3(normal);


      positionsArray.push(vertices[a]);
      normalsArray.push(normal);
      positionsArray.push(vertices[b]);
      normalsArray.push(normal);
      positionsArray.push(vertices[c]);
      normalsArray.push(normal);
      positionsArray.push(vertices[a]);
      normalsArray.push(normal);
      positionsArray.push(vertices[c]);
      normalsArray.push(normal);
      positionsArray.push(vertices[d]);
      normalsArray.push(normal);
   }


   function colorCube() {
      quad(1, 0, 3, 2);
      quad(2, 3, 7, 6);
      quad(3, 0, 4, 7);
      quad(6, 5, 1, 2);
      quad(4, 5, 6, 7);
      quad(5, 4, 0, 1);
   }

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
      canvas = document.getElementById("gl-canvas");

      gl = canvas.getContext('webgl2');
      if (!gl) alert("WebGL 2.0 isn't available");


      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.clearColor(1.0, 1.0, 1.0, 0.30);

      gl.enable(gl.DEPTH_TEST);

      //
      //  Load shaders and initialize attribute buffers
      //
      program = initShaders(gl, "vertex-shader", "fragment-shader");
      gl.useProgram(program);

      colorCube();

      var nBuffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, nBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, flatten(normalsArray), gl.STATIC_DRAW);

      var normalLoc = gl.getAttribLocation(program, "aNormal");
      gl.vertexAttribPointer(normalLoc, 3, gl.FLOAT, false, 0, 0);
      gl.enableVertexAttribArray(normalLoc);

      var vBuffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, flatten(positionsArray), gl.STATIC_DRAW);

      var positionLoc = gl.getAttribLocation(program, "aPosition");
      gl.vertexAttribPointer(positionLoc, 4, gl.FLOAT, false, 0, 0);
      gl.enableVertexAttribArray(positionLoc);

      thetaLoc = gl.getUniformLocation(program, "theta");

      viewerPos = vec3(0.0, 0.0, -20.0);

      projectionMatrix = ortho(-1, 1, -1, 1, -100, 100);

      lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);


      //Buttons
      document.getElementById("button1").onclick = function () { axis = xAxis; };
      document.getElementById("button2").onclick = function () { axis = yAxis; };
      document.getElementById("button3").onclick = function () { axis = zAxis; };
      document.getElementById("button4").onclick = function () { direction = !direction; };
      document.getElementById("button5").onclick = function () { flag = !flag; };

      //Sliders
      //Material
      //Ambient (RGB)
      document.getElementById("slider1").oninput = function () {
         //Set new value
         materialAmbient[0] = this.value;
         //Resend color calculations
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };
      document.getElementById("slider2").oninput = function () {
         materialAmbient[1] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };
      document.getElementById("slider3").oninput = function () {
         materialAmbient[2] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };
      //Diffusion
      document.getElementById("slider4").oninput = function () {
         materialDiffuse[0] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };
      document.getElementById("slider5").oninput = function () {
         materialDiffuse[1] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };
      document.getElementById("slider6").oninput = function () {
         materialDiffuse[2] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };
      //Specular
      document.getElementById("slider7").oninput = function () {
         materialSpecular[0] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };
      document.getElementById("slider8").oninput = function () {
         materialSpecular[1] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };
      document.getElementById("slider9").oninput = function () {
         materialSpecular[2] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };

      //Light
      //Ambient
      document.getElementById("slider10").oninput = function () {
         lightAmbient[0] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };
      document.getElementById("slider11").oninput = function () {
         lightAmbient[1] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };
      document.getElementById("slider12").oninput = function () {
         lightAmbient[2] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };
      //Diffusion
      document.getElementById("slider13").oninput = function () {
         lightDiffuse[0] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };
      document.getElementById("slider14").oninput = function () {
         lightDiffuse[1] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };
      document.getElementById("slider15").oninput = function () {
         lightDiffuse[2] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };
      //Specular
      document.getElementById("slider16").oninput = function () {
         lightSpecular[0] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };
      document.getElementById("slider17").oninput = function () {
         lightSpecular[1] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };
      document.getElementById("slider18").oninput = function () {
         lightSpecular[2] = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };

      //Shininess
      document.getElementById("slider19").oninput = function () {
         materialShininess = this.value;
         lightColor(lightAmbient, lightDiffuse, lightSpecular, materialAmbient, materialDiffuse, materialSpecular, materialShininess);
      };

      render();
   }

   var render = function () {

      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

      if (!direction) {
         if (flag) theta[axis] += 2.0;
      }
      if (direction) {
         if (flag) theta[axis] -= 2.0;
      }


      modelViewMatrix = mat4();
      modelViewMatrix = mult(modelViewMatrix, rotate(theta[xAxis], vec3(1, 0, 0)));
      modelViewMatrix = mult(modelViewMatrix, rotate(theta[yAxis], vec3(0, 1, 0)));
      modelViewMatrix = mult(modelViewMatrix, rotate(theta[zAxis], vec3(0, 0, 1)));

      gl.uniformMatrix4fv(gl.getUniformLocation(program,
         "uModelViewMatrix"), false, flatten(modelViewMatrix));

      gl.drawArrays(gl.TRIANGLES, 0, numPositions);


      requestAnimationFrame(render);
   }

}

shadedCube();
