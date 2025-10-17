/* This is the main js file for Project 03. This file sets up the room and starting placement of the paper
for the scene. 
*/

"use strict";

var canvas;
var gl;

// buffers
var positionsPaper = [];
var colorsPaper = [];
var positionsDesk = [];
var colorsDesk = [];

// NEW: room buffers
var positionsRoom = [];
var colorsRoom = [];

const COLOR_PALLET = [
  vec3(1.0, 0.0, 0.0), // 0 Red
  vec3(0.0, 1.0, 0.0), // 1 Green
  vec3(0.0, 0.0, 1.0), // 2 Blue
  vec3(1.0, 0.0, 1.0), // 3 Magenta
  vec3(1.0, 1.0, 0.0), // 4 Yellow
  vec3(0.0, 1.0, 1.0), // 5 Cyan
  vec3(0.6, 0.3, 0.0), // 6 Brown
  vec3(0.1, 0.1, 0.1), // 7 Dark gray
  vec3(1.0, 1.0, 1.0), // 8 White
  vec3(0.85, 0.85, 0.85), // 9 Light gray 
  vec3(0.2, 0.2, 0.2), // 10 Charcoal 
  vec3(0.75, 0.6, 0.4), // 11 Wood light
  vec3(0.35, 0.2, 0.1), // 12 Wood dark
  vec3(0.9, 0.9, 0.95), // 13 Off-white 
  vec3(0.5, 0.2, 0.7), // 14 Purple 
  vec3(0.2, 0.6, 0.8), // 15 Teal 
  vec3(0.8, 0.4, 0.2), // 16 Orange 
];

const paperVertices = [
  //x, y, z, w (y is vertical)
  // paper (thin box)
  // top
  vec4(-0.25, 0.111, -2.55, 1.0),
  vec4(-0.25, 0.111, -2.25, 1.0),
  vec4(0.25, 0.111, -2.25, 1.0),
  vec4(0.25, 0.111, -2.55, 1.0),
  // bottom
  vec4(-0.25, 0.101, -2.55, 1.0),
  vec4(-0.25, 0.101, -2.25, 1.0),
  vec4(0.25, 0.101, -2.25, 1.0),
  vec4(0.25, 0.101, -2.55, 1.0),
];
//doesn't sit flat with wall needs work may do closer to the chatgpt objects
const deskVertices = [
  // Desktop rectangle
  // top
  vec4(-0.65, 0.1, -2.99, 1.0),
  vec4(-0.65, 0.1, -1.99, 1.0),
  vec4(0.65, 0.1, -1.99, 1.0),
  vec4(0.65, 0.1, -2.99, 1.0),
  // bottom
  vec4(-0.65, 0.0, -2.99, 1.0),
  vec4(-0.65, 0.0, -1.99, 1.0),
  vec4(0.65, 0.0, -1.99, 1.0),
  vec4(0.65, 0.0, -2.99, 1.0),
];

// Unit box with top at y=0 and bottom at y=-1 (like your leg)
const legUnit = [
  // top ring (y = 0)
  vec4(-0.5, 0.0, -0.5, 1.0),
  vec4(0.5, 0.0, -0.5, 1.0),
  vec4(0.5, 0.0, 0.5, 1.0),
  vec4(-0.5, 0.0, 0.5, 1.0),
  // bottom ring (y = -1)
  vec4(-0.5, -1.0, -0.5, 1.0),
  vec4(0.5, -1.0, -0.5, 1.0),
  vec4(0.5, -1.0, 0.5, 1.0),
  vec4(-0.5, -1.0, 0.5, 1.0),
];

// Symmetric unit cube centered at origin (easier for general boxes)
const cubeCentered = [
  vec4(-0.5, 0.5, -0.5, 1.0),
  vec4(0.5, 0.5, -0.5, 1.0),
  vec4(0.5, 0.5, 0.5, 1.0),
  vec4(-0.5, 0.5, 0.5, 1.0),

  vec4(-0.5, -0.5, -0.5, 1.0),
  vec4(0.5, -0.5, -0.5, 1.0),
  vec4(0.5, -0.5, 0.5, 1.0),
  vec4(-0.5, -0.5, 0.5, 1.0),
];

window.onload = function init() {
  canvas = document.getElementById("gl-canvas");
  gl = canvas.getContext("webgl2");
  if (!gl) {
    alert("WebGL 2.0 isn't available");
    return;
  }

  // Build geometry
  buildPaper();
  buildDeskAndLegs();
  buildRoom(); // NEW

  // Shaders
  var program = initShaders(gl, "vertex-shader", "fragment-shader");
  gl.useProgram(program);

  // Attributes
  var aPosition = gl.getAttribLocation(program, "aPosition");
  var aColor = gl.getAttribLocation(program, "aColor");

  // Uniforms
  var uModel = gl.getUniformLocation(program, "uModel");
  var uView = gl.getUniformLocation(program, "uView");
  var uProj = gl.getUniformLocation(program, "uProj");

  // State
  gl.viewport(0, 0, canvas.width, canvas.height);
  gl.clearColor(0.6, 0.75, 0.95, 1.0); // soft sky-ish bg; walls will cover most
  //gl.enable(gl.DEPTH_TEST);
  //renders better without depth test
  gl.disable(gl.CULL_FACE);


  // Make VAOs
  function makeVAO(posArray, colArray) {
    const vao = gl.createVertexArray();
    gl.bindVertexArray(vao);

    // positions (vec4)
    const pbuf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, pbuf);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(posArray), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(aPosition);
    gl.vertexAttribPointer(aPosition, 4, gl.FLOAT, false, 0, 0);

    // colors (vec3)
    const cbuf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, cbuf);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(colArray), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(aColor);
    gl.vertexAttribPointer(aColor, 3, gl.FLOAT, false, 0, 0);

    gl.bindVertexArray(null);
    return { vao, count: posArray.length };
  }

  const VAOroom = makeVAO(positionsRoom, colorsRoom);
  const VAOdesk = makeVAO(positionsDesk, colorsDesk);
  const VAOpaper = makeVAO(positionsPaper, colorsPaper);

  // Camera matrices using MV.js
  function computeMatrices() {
    // Pull back and up a bit to see more of the room
    const eye = vec3(1.0, 1.0, 1.6);
    const at = vec3(0.0, 0.25, 0.0);
    const up = vec3(0.0, 2.6, 0.0);

    const view = lookAt(eye, at, up);
    const proj = perspective(45.0, canvas.width / canvas.height, 0.01, 30.0);
    const model = mat4(); // identity

    gl.uniformMatrix4fv(uModel, false, flatten(model));
    gl.uniformMatrix4fv(uView, false, flatten(view));
    gl.uniformMatrix4fv(uProj, false, flatten(proj));
  }

  function render() {
    computeMatrices();
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // draw order: room -> desk -> paper
    gl.bindVertexArray(VAOroom.vao);
    gl.drawArrays(gl.TRIANGLES, 0, VAOroom.count);

    gl.bindVertexArray(VAOdesk.vao);
    gl.drawArrays(gl.TRIANGLES, 0, VAOdesk.count);

    gl.bindVertexArray(VAOpaper.vao);
    gl.drawArrays(gl.TRIANGLES, 0, VAOpaper.count);

    gl.bindVertexArray(null);
    requestAnimationFrame(render);
  }
  render();
};

// helper: (v0,v1,v2,v3) -> two triangles
function pushQuad(posArr, colArr, v0, v1, v2, v3, color) {
  posArr.push(v0, v1, v2, v0, v2, v3);
  for (let i = 0; i < 6; i++) colArr.push(color);
}

// Apply a mat4 to an array of vec4 points
function transformVerts8(verts8, M) {
  const out = [];
  for (let v of verts8) out.push(mult(M, v));
  return out;
}

// Push a box from an 8-vertex array: [a,b,c,d, e,f,g,h]
function pushBoxFrom8(posArr, colArr, v, color) {
  const [a, b, c, d, e, f, g, h] = v;
  // top, bottom
  pushQuad(posArr, colArr, a, b, c, d, color);
  pushQuad(posArr, colArr, e, f, g, h, color);
  // sides
  pushQuad(posArr, colArr, a, d, h, e, color); // front
  pushQuad(posArr, colArr, b, a, e, f, color); // left
  pushQuad(posArr, colArr, c, b, f, g, color); // back
  pushQuad(posArr, colArr, d, c, g, h, color); // right
}

// Convenience: make a general box centered at 'center' with size (sx,sy,sz)
function pushBoxCentered(posArr, colArr, center, sx, sy, sz, color) {
  const S = scale(sx, sy, sz);
  const T = translate(center[0], center[1], center[2]);
  const M = mult(T, S);
  const vv = transformVerts8(cubeCentered, M);
  pushBoxFrom8(posArr, colArr, vv, color);
}

// Thin panel (like wall panel) from cubeCentered with tiny thickness
function pushPanel(posArr, colArr, center, sx, sy, facing, color) {
  // facing: "x" or "z" to decide thin dimension
  if (facing === "x") pushBoxCentered(posArr, colArr, center, 0.01, sy, sx, color);
  else pushBoxCentered(posArr, colArr, center, sx, sy, 0.01, color);
}

// ---------- Original build functions ----------

function buildPaper() {
  const white = COLOR_PALLET[8];
  const [p0, p1, p2, p3, p4, p5, p6, p7] = paperVertices;

  pushQuad(positionsPaper, colorsPaper, p0, p1, p2, p3, white);
  pushQuad(positionsPaper, colorsPaper, p4, p5, p6, p7, white);
  pushQuad(positionsPaper, colorsPaper, p0, p3, p7, p4, white);
  pushQuad(positionsPaper, colorsPaper, p1, p0, p4, p5, white);
  pushQuad(positionsPaper, colorsPaper, p2, p1, p5, p6, white);
  pushQuad(positionsPaper, colorsPaper, p3, p2, p6, p7, white);
}

function buildDeskAndLegs() {
  const brown = COLOR_PALLET[6];
  const [d0, d1, d2, d3, d4, d5, d6, d7] = deskVertices;

  // desk top
  pushQuad(positionsDesk, colorsDesk, d0, d1, d2, d3, brown);
  pushQuad(positionsDesk, colorsDesk, d4, d5, d6, d7, brown);
  pushQuad(positionsDesk, colorsDesk, d0, d3, d7, d4, brown);
  pushQuad(positionsDesk, colorsDesk, d1, d0, d4, d5, brown);
  pushQuad(positionsDesk, colorsDesk, d2, d1, d5, d6, brown);
  pushQuad(positionsDesk, colorsDesk, d3, d2, d6, d7, brown);

  // legs
  const S_leg = scale(0.05, 0.5, 0.05);
  const legCenters = [
    vec3(-0.575, 0.0, -2.99), // front-left
    vec3(0.575, 0.0, -2.99), // front-right
    vec3(-0.575, 0.0, -1.99), // back-left
    vec3(0.575, 0.0, -1.99), // back-right
  ];

  legCenters.forEach((c) => {
    const T_leg = translate(c[0], c[1], c[2]);
    const M_leg = mult(T_leg, S_leg); // T * S
    const leg = transformVerts8(legUnit, M_leg);
    pushBoxFrom8(positionsDesk, colorsDesk, leg, COLOR_PALLET[6]); // brown
  });
}

// ---------- NEW: build the whole room ----------

function buildRoom() {
  const floorY = -0.001;   // just below y=0 plane
  const roomHalfX = 3.0;   // room extents
  const roomHalfZ = 3.0;
  const wallH = 1.8;

  // Floor (wood)
  pushBoxCentered(positionsRoom, colorsRoom, vec3(0.0, floorY, 0.0), roomHalfX * 2.0, 0.002, roomHalfZ * 2.0, COLOR_PALLET[11]);

  // Baseboards (thin strips around edges) needs work doesn't render in the room
  const baseH = 0.05, baseT = 0.02;
  // Along +Z wall
  pushBoxCentered(positionsRoom, colorsRoom, vec3(0.0, baseH / 2.0, roomHalfZ - 0.01), roomHalfX * 2.0, baseH, baseT, COLOR_PALLET[9]);
  // Along -Z wall
  pushBoxCentered(positionsRoom, colorsRoom, vec3(0.0, baseH / 2.0, -roomHalfZ + 0.01), roomHalfX * 2.0, baseH, baseT, COLOR_PALLET[9]);
  // Along +X wall
  pushBoxCentered(positionsRoom, colorsRoom, vec3(roomHalfX - 0.01, baseH / 2.0, 0.0), baseT, baseH, roomHalfZ * 2.0, COLOR_PALLET[9]);
  // Along -X wall
  pushBoxCentered(positionsRoom, colorsRoom, vec3(-roomHalfX + 0.01, baseH / 2.0, 0.0), baseT, baseH, roomHalfZ * 2.0, COLOR_PALLET[9]);

  // Walls (painted)
  // Back wall (+Z)
  pushPanel(positionsRoom, colorsRoom, vec3(0.0, wallH / 2.0, roomHalfZ), roomHalfX * 2.0, wallH, "z", COLOR_PALLET[9]);
  // Front wall (-Z)
  pushPanel(positionsRoom, colorsRoom, vec3(0.0, wallH / 2.0, -roomHalfZ), roomHalfX * 2.0, wallH, "z", COLOR_PALLET[9]);
  // Right wall (+X)
  pushPanel(positionsRoom, colorsRoom, vec3(roomHalfX, wallH / 2.0, 0.0), roomHalfZ * 2.0, wallH, "x", COLOR_PALLET[9]);
  // Left wall (-X)
  pushPanel(positionsRoom, colorsRoom, vec3(-roomHalfX, wallH / 2.0, 0.0), roomHalfZ * 2.0, wallH, "x", COLOR_PALLET[9]);

  // Simple ceiling trim (thin frame) // needs work doesn't render in the room
  const trimY = wallH - 0.02;
  pushBoxCentered(positionsRoom, colorsRoom, vec3(0.0, trimY, roomHalfZ - 0.02), roomHalfX * 2.0, 0.015, 0.03, COLOR_PALLET[13]);
  pushBoxCentered(positionsRoom, colorsRoom, vec3(0.0, trimY, -roomHalfZ + 0.02), roomHalfX * 2.0, 0.015, 0.03, COLOR_PALLET[13]);
  pushBoxCentered(positionsRoom, colorsRoom, vec3(roomHalfX - 0.02, trimY, 0.0), 0.03, 0.015, roomHalfZ * 2.0, COLOR_PALLET[13]);
  pushBoxCentered(positionsRoom, colorsRoom, vec3(-roomHalfX + 0.02, trimY, 0.0), 0.03, 0.015, roomHalfZ * 2.0, COLOR_PALLET[13]);

  // Window on back wall (+Z)
  // Frame
  const winW = 1.2, winH = 0.7, winY = 1.1, winZ = roomHalfZ - 0.005;
  pushBoxCentered(positionsRoom, colorsRoom, vec3(0.0, winY, winZ), winW + 0.05, winH + 0.05, 0.03, COLOR_PALLET[13]);
  // Glass panel (slightly pushed inward)
  pushPanel(positionsRoom, colorsRoom, vec3(0.0, winY, winZ - 0.015), winW, winH, "z", COLOR_PALLET[5]); // cyan-ish
  // "Outside" (blue panel further back to imply sky)
  pushPanel(positionsRoom, colorsRoom, vec3(0.0, winY, winZ - 0.06), winW * 1.2, winH * 1.2, "z", COLOR_PALLET[2]);

  // Door on right wall (+X)
  const doorW = 0.8, doorH = 1.6, doorX = roomHalfX, doorY = doorH / 2.0, doorZ = -1.2;
  // Door slab (slightly inset)
  pushPanel(positionsRoom, colorsRoom, vec3(doorX - 0.004, doorY, doorZ), doorH, doorW, "x", COLOR_PALLET[13]);
  // Door panel
  pushPanel(positionsRoom, colorsRoom, vec3(doorX - 0.02, doorY, doorZ), doorH * 0.98, doorW * 0.98, "x", COLOR_PALLET[8]);
  // Knob
  pushBoxCentered(positionsRoom, colorsRoom, vec3(doorX - 0.04, 0.95, doorZ + doorW * 0.3), 0.03, 0.03, 0.03, COLOR_PALLET[6]);

  // Rug near desk
  pushBoxCentered(positionsRoom, colorsRoom, vec3(-0.0, 0.001, -2.25), 2.0, 0.002, 0.8, COLOR_PALLET[2]);

  // Trash can (simple tall box) near desk leg
  pushBoxCentered(positionsRoom, colorsRoom, vec3(-0.8, 0.18, -2.35), 0.18, 0.36, 0.18, COLOR_PALLET[7]);
  // “Open” lip
  pushBoxCentered(positionsRoom, colorsRoom, vec3(-0.8, 0.37, -2.35), 0.20, 0.02, 0.20, COLOR_PALLET[10]);

  // Standing lamp (base, pole, shade)
  pushBoxCentered(positionsRoom, colorsRoom, vec3(1.1, 0.02, -2.7), 0.22, 0.02, 0.22, COLOR_PALLET[10]); // base
  pushBoxCentered(positionsRoom, colorsRoom, vec3(1.1, 0.7, -2.7), 0.04, 1.36, 0.04, COLOR_PALLET[10]); // pole
  pushBoxCentered(positionsRoom, colorsRoom, vec3(1.1, 1.35, -2.7), 0.35, 0.18, 0.35, COLOR_PALLET[13]); // shade

  // Chair near desk (seat at y ~ 0.07, desk top is y=0.1)
  // Seat
  pushBoxCentered(positionsRoom, colorsRoom, vec3(-0.25, 0.08, -2.25), 0.35, 0.05, 0.35, COLOR_PALLET[6]);
  // Backrest
  pushBoxCentered(positionsRoom, colorsRoom, vec3(-0.25, 0.28, -2.20), 0.35, 0.4, 0.06, COLOR_PALLET[6]);
  // Legs (reuse thin boxes)
  const cl = [
    vec3(-0.38, 0.04, -2.25),
    vec3(-0.12, 0.04, -2.25),
    vec3(-0.38, 0.04, -2.20),
    vec3(-0.12, 0.04, -2.20),
  ];
  cl.forEach(c => pushBoxCentered(positionsRoom, colorsRoom, c, 0.04, 0.08, 0.04, COLOR_PALLET[7]));

  // Bookshelf against left wall (-X)
  const shelfX = -roomHalfX + 0.12;
  //pushBoxCentered(positionsRoom, colorsRoom, vec3(-3.0, 0.7, -0.9), 0.24, 1.2, 0.5, COLOR_PALLET[12]); //main frame
  // Shelves
  [0.2, 0.5, 0.8, 1.1].forEach(h =>
    pushBoxCentered(positionsRoom, colorsRoom, vec3(shelfX, h, -0.9), 0.22, 0.03, 0.48, COLOR_PALLET[11])
  );
  // Books (simple colored boxes)
  const bookYs = [0.22, 0.52, 0.82, 1.12];
  bookYs.forEach((h, i) => {
    for (let k = 0; k < 4; k++) {
      const z = -0.9 - 0.18 + k * 0.12;
      const col = [COLOR_PALLET[14], COLOR_PALLET[15], COLOR_PALLET[16]][(i + k) % 3];
      pushBoxCentered(positionsRoom, colorsRoom, vec3(shelfX, h + 0.08, z), 0.06, 0.16, 0.08, col);
    }
  });
}
