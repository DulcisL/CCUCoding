/*
================================================================================
Combined WebGL2 Scene + Paper-Airplane Fold Animation (One HTML, One JS)
--------------------------------------------------------------------------------
- This file merges the original room/desk scene with the paper folding animation.
- Single shader program handles both static geometry and foldable paper.
- Folding is applied only to the paper by setting uFoldCount > 0 during its draw.
- Non-paper geometry (room, desk, chair, props) is drawn with uFoldCount = 0.

Controls:
- Left mouse drag: orbit camera
- Mouse wheel: zoom
- Double-click: reset camera

File layout (search for tags):
  [SETUP] WebGL state and uniforms
  [GEOM]  Helpers for meshes (boxes, panels)
  [ROOM]  Build room, desk, CHAIR (chair now matches desk height)
  [PAPER] Build right-half mesh and define fold sequence
  [ANIM]  Fold timeline & easing
  [VIEW]  Resize, camera, orbit controls
  [RENDER]Draw everything; apply folds to paper only
  [BOOT]  Entry point

Desk & Chair Heights:
- Desk top: y in [0.75, 0.85]
- Chair seat center: y = 0.48 (seat thickness 0.05 => top ~ 0.505)
- Chair back center: y = 0.68 (back height 0.40 => bottom aligned to seat)

Adjust the constants in [ROOM] and [PAPER] sections to tweak the scene or folding.
================================================================================
*/

/* Combined scene + folding paper animation
   - Room/desk/paper scene derived from earlier scene setup
   - Folding paper airplane derived from half + mirror fold pipeline
   - Single shader program; we disable folds (uFoldCount=0) when drawing non-paper geometry
*/

"use strict";

/* ===== WebGL state ===== */
let gl, program;

/* ===== Uniform locations ===== */
let uModelLoc, uViewLoc, uProjLoc;
let uFoldCountLoc, uFoldAngleLoc, uFoldPointLoc, uFoldAxisLoc, uFoldNormalLoc, uFoldSideLoc, uFoldUseOrigSideLoc;

/* ===== Geometry VAOs ===== */
let VAOroom = null, roomCount = 0;
let VAOdesk = null, deskCount = 0;
let VAOpaperHalf = null, paperHalfCount = 0;

/* ===== Camera (orbit controls) ===== */
const TARGET = window.vec3(0.0, 0.86, -2.40); // paper center on the desk
const ORBIT = { radius: 1.6, minR: 0.5, maxR: 8.0, theta: -0.8, phi: 0.8, minPhi: -1.2, maxPhi: 1.2 };
const ORBIT_SENS = { rotate: 1.2, zoom: 0.25 };
let isDragging = false; let lastX = 0, lastY = 0;
const FLOOR_Y = 0.0;
const CEILING_Y = 2.4;

/* ===== Timeline ===== */
let startTime = 0;

/* ============================== Utilities ============================== */
function lerp(a, b, t) { return a + (b - a) * t; }
function v2(x, y) { return [x, y]; }
function v3(x, y, z) { return [x, y, z]; }
function norm2(v) { const m = Math.hypot(v[0], v[1]) || 1; return [v[0]/m, v[1]/m]; }
function perp2(v) { return [-v[1], v[0]]; } // 90° CCW
function easeInOut(t){ return (t < 0.5) ? (2 * t * t) : (1 - Math.pow(-2 * t + 2, 2) / 2); }
function clamp(x, a, b){ return Math.max(a, Math.min(b, x)); }

function orbitToEye() {
  const r = ORBIT.radius, th = ORBIT.theta, ph = ORBIT.phi;
  const cp = Math.cos(ph), sp = Math.sin(ph);
  const ct = Math.cos(th), st = Math.sin(th);
  const offset = window.vec3(r * cp * st, r * sp, r * cp * ct);
  return window.add(TARGET, offset);
}


/* [GEOM] Mesh helper functions
   - pushQuad / pushBox*: build triangles with per-vertex colors
   - transformVerts8: transforms a unit cube's 8 corners by matrix M
   - pushPanel: thin "panel" aligned to X or Z (used for walls/trim)
*/
/* ======================= Helpers for building meshes ======================= */

const COLOR_PALLET = [
  window.vec3(1.0, 0.0, 0.0), // 0 Red
  window.vec3(0.0, 1.0, 0.0), // 1 Green
  window.vec3(0.0, 0.0, 1.0), // 2 Blue
  window.vec3(1.0, 0.0, 1.0), // 3 Magenta
  window.vec3(1.0, 1.0, 0.0), // 4 Yellow
  window.vec3(0.0, 1.0, 1.0), // 5 Cyan
  window.vec3(0.6, 0.3, 0.0), // 6 Brown
  window.vec3(0.1, 0.1, 0.1), // 7 Dark gray
  window.vec3(1.0, 1.0, 1.0), // 8 White
  window.vec3(0.85, 0.85, 0.85), // 9 Light gray 
  window.vec3(0.2, 0.2, 0.2), // 10 Charcoal 
  window.vec3(0.75, 0.6, 0.4), // 11 Wood light
  window.vec3(0.35, 0.2, 0.1), // 12 Wood dark
  window.vec3(0.9, 0.9, 0.95), // 13 Off-white 
  window.vec3(0.5, 0.2, 0.7), // 14 Purple 
  window.vec3(0.2, 0.6, 0.8), // 15 Teal 
  window.vec3(0.8, 0.4, 0.2), // 16 Orange 
  window.vec3(1.0, 0.55, 0.45), // 17 Coral
  window.vec3(0.0, 0.75, 0.95), // 18 sky
];

// base primitives from the scene
const cubeCentered = [
  window.vec4(-0.5,  0.5, -0.5, 1.0),
  window.vec4( 0.5,  0.5, -0.5, 1.0),
  window.vec4( 0.5,  0.5,  0.5, 1.0),
  window.vec4(-0.5,  0.5,  0.5, 1.0),
  window.vec4(-0.5, -0.5, -0.5, 1.0),
  window.vec4( 0.5, -0.5, -0.5, 1.0),
  window.vec4( 0.5, -0.5,  0.5, 1.0),
  window.vec4(-0.5, -0.5,  0.5, 1.0),
];

function pushQuad(posArr, colArr, v0, v1, v2, v3, color) {
  posArr.push(v0, v1, v2,  v0, v2, v3);
  for (let i = 0; i < 6; i++) colArr.push(color);
}
function transformVerts8(verts8, M) { const out = []; for (let v of verts8) out.push(window.mult(M, v)); return out; }
function pushBoxFrom8(posArr, colArr, v, color) {
  const [a,b,c,d,e,f,g,h] = v;
  pushQuad(posArr, colArr, a,b,c,d, color);
  pushQuad(posArr, colArr, e,f,g,h, color);
  pushQuad(posArr, colArr, a,d,h,e, color);
  pushQuad(posArr, colArr, b,a,e,f, color);
  pushQuad(posArr, colArr, c,b,f,g, color);
  pushQuad(posArr, colArr, d,c,g,h, color);
}
function pushBoxCentered(posArr, colArr, center, sx, sy, sz, color) {
  const S = window.scale(sx, sy, sz);
  const T = window.translate(center[0], center[1], center[2]);
  const M = window.mult(T, S);
  const vv = transformVerts8(cubeCentered, M);
  pushBoxFrom8(posArr, colArr, vv, color);
}
function pushPanel(posArr, colArr, center, sx, sy, facing, color) {
  if (facing === "x") pushBoxCentered(posArr, colArr, center, 0.01, sy, sx, color);
  else pushBoxCentered(posArr, colArr, center, sx, sy, 0.01, color);
}

/* ========================= Build ROOM + DESK ========================= */

/* [ROOM] Build the room shell, trim, window, door, and props.
   Also builds the DESK (raised to realistic height) and a CHAIR whose
   seat/back align with the new desk height.
   Returns VAOs for room and desk geometry.
*/
function buildRoomAndDesk() {
  const positionsRoom = [], colorsRoom = [];
  const positionsDesk = [], colorsDesk = [];

  // -------- Floor slab and baseboards --------
  const floorY = -0.001, roomHalfX = 3.0, roomHalfZ = 3.0, wallH = 1.8;
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(0.0, floorY, 0.0), roomHalfX*2.0, 0.002, roomHalfZ*2.0, COLOR_PALLET[15]);
  const baseH = 0.05, baseT = 0.02;
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(0.0, baseH/2.0,  roomHalfZ-0.01), roomHalfX*2.0, baseH, baseT, COLOR_PALLET[9]);
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(0.0, baseH/2.0, -roomHalfZ+0.01), roomHalfX*2.0, baseH, baseT, COLOR_PALLET[9]);
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3( roomHalfX-0.01, baseH/2.0, 0.0), baseT, baseH, roomHalfZ*2.0, COLOR_PALLET[9]);
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(-roomHalfX+0.01, baseH/2.0, 0.0), baseT, baseH, roomHalfZ*2.0, COLOR_PALLET[9]);

  // -------- Wall panels --------
  pushPanel(positionsRoom, colorsRoom, window.vec3(0.0, wallH/2.0,  roomHalfZ), roomHalfX*2.0, wallH, "z", COLOR_PALLET[9]);
  pushPanel(positionsRoom, colorsRoom, window.vec3(0.0, wallH/2.0, -roomHalfZ), roomHalfX*2.0, wallH, "z", COLOR_PALLET[9]);
  pushPanel(positionsRoom, colorsRoom, window.vec3( roomHalfX, wallH/2.0, 0.0), roomHalfZ*2.0, wallH, "x", COLOR_PALLET[9]);
  pushPanel(positionsRoom, colorsRoom, window.vec3(-roomHalfX, wallH/2.0, 0.0), roomHalfZ*2.0, wallH, "x", COLOR_PALLET[9]);

  // -------- Crown molding --------
  const trimY = wallH - 0.02;
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(0.0, trimY,  roomHalfZ - 0.02), roomHalfX*2.0, 0.015, 0.03, COLOR_PALLET[13]);
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(0.0, trimY, -roomHalfZ + 0.02), roomHalfX*2.0, 0.015, 0.03, COLOR_PALLET[13]);
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3( roomHalfX - 0.02, trimY, 0.0), 0.03, 0.015, roomHalfZ*2.0, COLOR_PALLET[13]);
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(-roomHalfX + 0.02, trimY, 0.0), 0.03, 0.015, roomHalfZ*2.0, COLOR_PALLET[13]);

  // -------- Window frame, glass, and exterior accent --------
  const winW = 1.2, winH = 0.7, winY = 1.1, winZ = roomHalfZ - 0.005;
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(0.0, winY, winZ), winW+0.05, winH+0.05, 0.03, COLOR_PALLET[11]);
  pushPanel(positionsRoom, colorsRoom, window.vec3(0.0, winY, winZ - 0.015), winW, winH, "z", COLOR_PALLET[5]);
  pushPanel(positionsRoom, colorsRoom, window.vec3(0.0, winY, winZ - 0.06), winW*1.2, winH*1.2, "z", COLOR_PALLET[18]);

  // -------- Door slab, trim, and knob --------
  const doorW = 0.8, doorH = 1.6, doorX = roomHalfX, doorY = doorH/2.0, doorZ = -1.2;
  pushPanel(positionsRoom, colorsRoom, window.vec3(doorX - 0.004, doorY, doorZ), doorH, doorW, "x", COLOR_PALLET[13]);
  pushPanel(positionsRoom, colorsRoom, window.vec3(doorX - 0.02,  doorY, doorZ), doorH*0.98, doorW*0.98, "x", COLOR_PALLET[8]);
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(doorX - 0.04, 0.95, doorZ + doorW*0.3), 0.03, 0.03, 0.03, COLOR_PALLET[6]);

  // -------- Rug, planter, lamp, and couch props --------
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(-0.0, 0.001, -2.25), 3.0, 0.002, 1.5, COLOR_PALLET[17]);
  //Planter
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(-1.0, 0.15, -2.75), 0.4, 0.3, 0.4, COLOR_PALLET[10]);
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(-1.0, 0.2, -2.75), 0.32, 0.23, 0.32, COLOR_PALLET[11]);
  //light
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3( 1.1, 0.02, -2.7), 0.22, 0.02, 0.22, COLOR_PALLET[10]);
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3( 1.1, 0.7,  -2.7), 0.04, 1.36, 0.04, COLOR_PALLET[10]);
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3( 1.1, 1.35, -2.7), 0.35, 0.18, 0.35, COLOR_PALLET[13]);
  //Couch
  const couchCenter = window.vec3(0, 0.15, 2.7);
  pushBoxCentered(positionsRoom, colorsRoom, couchCenter, 1.2, 0.3, 0.5, COLOR_PALLET[11]); // seat
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(couchCenter[0], couchCenter[1] + 0.25, couchCenter[2] + 0.15), 1.2, 0.4, 0.25, COLOR_PALLET[11]); // back
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(couchCenter[0] - 0.525, couchCenter[1] + 0.05, couchCenter[2]), 0.12, 0.4, 0.45, COLOR_PALLET[10]); // left arm
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(couchCenter[0] + 0.525, couchCenter[1] + 0.05, couchCenter[2]), 0.12, 0.4, 0.45, COLOR_PALLET[10]); // right arm
  // -------- Chair: seat, back, and legs --------
  // Chair seat (raised to match desk height): center y=0.48, size ~ 0.35x0.05x0.35
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(0.0, 0.48, -2.0), 0.35, 0.05, 0.35, COLOR_PALLET[6]);
  // Chair back (bottom aligns with seat top): center y=0.68, height 0.40
  pushBoxCentered(positionsRoom, colorsRoom, window.vec3(0.0, 0.5, -1.85), 0.25, 0.5, 0.06, COLOR_PALLET[6]);
  // Chair legs: extend from floor (y=0) up to seat bottom (~0.455).
// Height ~= 0.455, center y ~= 0.2275 (rounded to 0.228)
[window.vec3(-0.12, 0.228, -1.85), window.vec3(0.12, 0.228, -1.85),
 window.vec3(-0.12, 0.228, -2.15), window.vec3(0.12, 0.228, -2.15)].forEach(c =>
  pushBoxCentered(positionsRoom, colorsRoom, c, 0.04, 0.456, 0.04, COLOR_PALLET[7])
);
  // -------- Floating shelves and books --------
  const shelfX = -roomHalfX + 0.12;
  [0.2,0.5,0.8,1.1].forEach(h =>
    pushBoxCentered(positionsRoom, colorsRoom, window.vec3(shelfX, h, -0.9), 0.22, 0.03, 0.48, COLOR_PALLET[6])
  );
  const bookYs = [0.22,0.52,0.82,1.12];
  bookYs.forEach((h,i)=>{
    for(let k=0;k<4;k++){
      const z = -0.9 - 0.18 + k*0.12;
      const col = [COLOR_PALLET[14], COLOR_PALLET[15], COLOR_PALLET[17]][(i+k)%3];
      pushBoxCentered(positionsRoom, colorsRoom, window.vec3(shelfX, h+0.08, z), 0.06, 0.16, 0.08, col);
    }
  });

  // -------- Desk top slab --------
  // Desk (top + legs)
  // Desk top (raised): top y=0.85, bottom y=0.75
  const deskTop = [
    window.vec4(-0.65, 0.85, -2.99, 1.0), window.vec4(-0.65, 0.85, -1.99, 1.0),
    window.vec4( 0.65, 0.85, -1.99, 1.0), window.vec4( 0.65, 0.85, -2.99, 1.0),
    window.vec4(-0.65, 0.75, -2.99, 1.0), window.vec4(-0.65, 0.75, -1.99, 1.0),
    window.vec4( 0.65, 0.75, -1.99, 1.0), window.vec4( 0.65, 0.75, -2.99, 1.0),
  ];
  const brown = COLOR_PALLET[6];
  pushQuad(positionsDesk, colorsDesk, deskTop[0],deskTop[1],deskTop[2],deskTop[3], brown);
  pushQuad(positionsDesk, colorsDesk, deskTop[4],deskTop[5],deskTop[6],deskTop[7], brown);
  pushQuad(positionsDesk, colorsDesk, deskTop[0],deskTop[3],deskTop[7],deskTop[4], brown);
  pushQuad(positionsDesk, colorsDesk, deskTop[1],deskTop[0],deskTop[4],deskTop[5], brown);
  pushQuad(positionsDesk, colorsDesk, deskTop[2],deskTop[1],deskTop[5],deskTop[6], brown);
  pushQuad(positionsDesk, colorsDesk, deskTop[3],deskTop[2],deskTop[6],deskTop[7], brown);

  // Desk legs: centers at underside of desk (y=0.75) with vertical scale 0.75 so feet touch floor
  const legCenters = [
    window.vec3(-0.6, 0.75, -2.90), window.vec3(0.6, 0.75, -2.90),
    window.vec3(-0.6, 0.75, -2.1), window.vec3(0.6, 0.75, -2.1),
  ];
  legCenters.forEach((c)=>{
    // Leg thickness and height (height=0.75 so bottom ~ 0.0 if center at 0.75)
    const S = window.scale(0.05, 0.75, 0.05);
    const T = window.translate(c[0], c[1], c[2]);
    const M = window.mult(T, S);
    const unit = [
      window.vec4(-0.5, 0.0, -0.5, 1.0), window.vec4( 0.5, 0.0, -0.5, 1.0),
      window.vec4( 0.5, 0.0,  0.5, 1.0), window.vec4(-0.5, 0.0,  0.5, 1.0),
      window.vec4(-0.5, -1.0,-0.5, 1.0), window.vec4( 0.5, -1.0,-0.5, 1.0),
      window.vec4( 0.5, -1.0, 0.5, 1.0), window.vec4(-0.5, -1.0, 0.5, 1.0),
    ];
    pushBoxFrom8(positionsDesk, colorsDesk, transformVerts8(unit, M), brown);
  });

  // Make VAOs
  function makeVAO(posArray, colArray) {
    const vao = gl.createVertexArray();
    gl.bindVertexArray(vao);

    const pbuf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, pbuf);
    gl.bufferData(gl.ARRAY_BUFFER, window.flatten(posArray), gl.STATIC_DRAW);
    const aPosition = gl.getAttribLocation(program, "aPosition");
    gl.enableVertexAttribArray(aPosition);
    gl.vertexAttribPointer(aPosition, 4, gl.FLOAT, false, 0, 0);

    const cbuf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, cbuf);
    gl.bufferData(gl.ARRAY_BUFFER, window.flatten(colArray), gl.STATIC_DRAW);
    const aColor = gl.getAttribLocation(program, "aColor");
    gl.enableVertexAttribArray(aColor);
    gl.vertexAttribPointer(aColor, 3, gl.FLOAT, false, 0, 0);

    gl.bindVertexArray(null);
    return { vao, count: posArray.length };
  }

  const roomVAO = makeVAO(positionsRoom, colorsRoom);
  const deskVAO = makeVAO(positionsDesk, colorsDesk);
  return { roomVAO, deskVAO };
}

/* ==================== Build only the RIGHT HALF of paper ==================== */

/* [PAPER] Build only the RIGHT HALF of the paper as a tessellated rectangle.
   We'll draw it twice: once as-is (right half), and once mirrored across X
   to form the left half. The folding shader conditions which side rotates.
*/
function createRightHalfGrid(cols = 36, rows = 24) {
  const W = 0.35, H = 0.5;
  const xC = 0.0, xR = +W * 0.5;
  const yB = -H * 0.5, yT = +H * 0.5;

  const xs = new Float32Array(cols + 1);
  const ys = new Float32Array(rows + 1);
  for (let i = 0; i <= cols; i++) xs[i] = lerp(xC, xR, i / cols);
  for (let j = 0; j <= rows; j++) ys[j] = lerp(yB, yT, j / rows);

  const positions = [], colors = [];
  const pushTri = (ax, ay, bx, by, cx, cy) => {
    positions.push(ax, ay, 0,  bx, by, 0,  cx, cy, 0);
    for (let k = 0; k < 3; k++) colors.push(0.96, 0.96, 0.96);
  };

  for (let j = 0; j < rows; j++) {
    for (let i = 0; i < cols; i++) {
      const xA = xs[i],   yA = ys[j];
      const xB = xs[i+1], yB = ys[j];
      const xC2 = xs[i+1], yC2 = ys[j+1];
      const xD = xs[i],   yD = ys[j+1];
      pushTri(xA,yA, xB,yB, xC2,yC2);
      pushTri(xA,yA, xC2,yC2, xD,yD);
    }
  }

  paperHalfCount = positions.length / 3;

  const vao = gl.createVertexArray();
  gl.bindVertexArray(vao);

  // Positions: provide full vec4 (x,y,z,1) so it matches aPosition
  const pos4 = new Float32Array(paperHalfCount * 4);
  for (let i=0,j=0;i<paperHalfCount;i++,j+=3){
    const k = i*4; pos4[k]=positions[j]; pos4[k+1]=positions[j+1]; pos4[k+2]=positions[j+2]; pos4[k+3]=1.0;
  }
  const posBuf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, posBuf);
  gl.bufferData(gl.ARRAY_BUFFER, pos4, gl.STATIC_DRAW);
  const aPosition = gl.getAttribLocation(program, "aPosition");
  gl.enableVertexAttribArray(aPosition);
  gl.vertexAttribPointer(aPosition, 4, gl.FLOAT, false, 0, 0);

  const colBuf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, colBuf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(colors), gl.STATIC_DRAW);
  const aColor = gl.getAttribLocation(program, "aColor");
  gl.enableVertexAttribArray(aColor);
  gl.vertexAttribPointer(aColor, 3, gl.FLOAT, false, 0, 0);

  gl.bindVertexArray(null);

  return { W, H, vao };
}

/* ============ One-sided airplane folds (RIGHT half only) ============ */
const folds = [];
const foldDur = [];
let totalFoldTimeMs = 0;


const FLIGHT_PATH = {
  delay: 600,              // pause after final fold before launch (ms)
  duration: 4000,          // full travel time once airborne (ms)
  maxHeight: 0.90,         // lift above desk (target height)
  forwardDistance: 3.0,    // no glide section
  lateralArc: 0.0,
  bankAngle: 0.0,
  pitchDown: 0
};
const CRUISE_PATH = {
  duration: 4800,
  turnRadius: 1.0,
  dropHeight: 0.05,
  bankAngle: 22,
  pitchDown: -6,
  yawTurn: 140,
  turnDirection: 1
};
const CRUISE_PATH2 = {
  duration: 4200,
  turnRadius: 0.7,
  dropHeight: 0.2,
  bankAngle: 28,
  pitchDown: -4,
  yawTurn: 80,
  turnDirection: 1
};

const LANDING_PATH = {
  duration: 3200,
  forward: -3.0,
  lateral: 0.6,
  dropHeight: 0.05,
  bankAngle: 28,
  pitchDown: -10,
  yawTurn: 80,
};


/* [PAPER] Define the fold sequence (times and crease lines) for a one-sided
   airplane construction. The left side is mirrored in the render pass.
   Folds (in order):
     1) Top-right corner towards centerline (diagonal crease) ~ 180° close
     2) Fuse along the centerline x=0 (bring right over left) ~ 90°
     3) Wing crease at x = W*0.25 (fold wing down) ~ -0.95 rad
*/
function buildRightFolds(W, H) {
  folds.length = 0; foldDur.length = 0;

  // 1) Top-right corner -> centerline diagonal
  {
    const a = v2(0,  H/2), b = v2(+W/2, 0);
    const axisDir = norm2([b[0]-a[0], b[1]-a[1]]);
    const n = norm2(perp2(axisDir));
    // Fold 1: diagonal corner toward centerline (~90°)
    folds.push({ p: v3(a[0], a[1], 0), axis: v3(axisDir[0], axisDir[1], 0), normal: v2(n[0], n[1]), side: +1, target: Math.PI, useOrig: true });
    foldDur.push(1400);
  }
  // 2) Fuse along x = 0 (centerline)
  {
    // Fold 2: fuse along centerline x=0 (~90°)
    folds.push({ p: v3(0,0,0), axis: v3(0,1,0), normal: v2(1,0), side: +1, target: Math.PI/2, useOrig: true });
    foldDur.push(1400);
  }
  // 3) Right wing crease at x = +W*0.25, fold down
  {
    const wingX = W*0.25;
    // Fold 3: wing crease down (~60°)
    folds.push({ p: v3(+wingX,0,0), axis: v3(0,1,0), normal: v2(1,0), side: +1, target: -Math.PI/3, useOrig: true });
    foldDur.push(1200);
  }

  totalFoldTimeMs = foldDur.reduce((sum, dur) => sum + dur, 0);
}

/* ==================== Animate folds sequentially ==================== */

/* [ANIM] Time -> fold angles mapping.
   - Each fold has a duration; we ease between 0 and its target angle.
   - Earlier folds "finish" before later ones begin to move.
*/
function foldProgress(nowMs) {
  const tAbs = nowMs - startTime;
  const n = folds.length;
  const ang = new Float32Array(n);
  let t = tAbs;
  for (let i = 0; i < n; i++) {
    const d = foldDur[i] || 1000;
    if (t <= 0) { ang[i] = 0; break; }
    const seg = Math.min(1, t / d);
    ang[i] = (0.001) + easeInOut(seg) * folds[i].target;
    t -= d;
    if (seg < 1) {
      for (let j=i+1;j<n;j++) ang[j]=0;
      break;
    }
  }
  return ang;
}

/* =========================== Paper flight path =========================== */

function launchPhaseState(progress) {
  const p = clamp(progress, 0, 1);
  const height = easeInOut(p) * FLIGHT_PATH.maxHeight;
  const forward = lerp(0, FLIGHT_PATH.forwardDistance, p);
  return { pos: [0, height, forward], pitch: FLIGHT_PATH.pitchDown * p, bank: FLIGHT_PATH.bankAngle * p, yaw: 0 };
}

function cruisePhaseState(config, timeMs) {
  const v = clamp(timeMs / Math.max(1, config.duration), 0, 1);
  const angle = v * Math.PI; // half circle
  const radius = config.turnRadius;
  const dir = config.turnDirection || 1;
  const forward = radius * Math.sin(angle);
  const lateral = dir * radius * (1 - Math.cos(angle));
  const drop = easeInOut(Math.max(0, (v - 0.2) / 0.8));
  const height = -drop * config.dropHeight;
  const pitch = config.pitchDown * v;
  const bank = Math.sin(angle) * config.bankAngle * dir;
  const yaw = config.yawTurn * v * dir;
  return { pos: [lateral, height, forward], pitch, bank, yaw };
}

function composeTransform(state) {
  let M = window.mat4();
  M = window.mult(window.translate(state.pos[0], state.pos[1], state.pos[2]), M);
  M = window.mult(window.rotate(state.yaw || 0, window.vec3(0,1,0)), M);
  M = window.mult(window.rotate(state.pitch || 0, window.vec3(1,0,0)), M);
  M = window.mult(window.rotate(state.bank || 0, window.vec3(0,0,1)), M);
  return M;
}

function combineStates(base, delta) {
  const yawRad = (base.yaw || 0) * Math.PI / 180;
  const cosY = Math.cos(yawRad), sinY = Math.sin(yawRad);
  const dx = delta.pos[0], dz = delta.pos[2];
  const rotX = dx * cosY - dz * sinY;
  const rotZ = dx * sinY + dz * cosY;
  return {
    pos: [
      base.pos[0] + rotX,
      base.pos[1] + delta.pos[1],
      base.pos[2] + rotZ,
    ],
    pitch: base.pitch + delta.pitch,
    bank: base.bank + delta.bank,
    yaw: (base.yaw || 0) + (delta.yaw || 0),
  };
}

function landingPhaseState(timeMs, baseHeight = 0) {
  const v = clamp(timeMs / Math.max(1, LANDING_PATH.duration), 0, 1);
  const drop = easeInOut(v);
  const forward = easeInOut(v) * LANDING_PATH.forward;
  const lateral = easeInOut(v) * LANDING_PATH.lateral;
  const height = -(baseHeight + LANDING_PATH.dropHeight) * drop;
  const pitch = LANDING_PATH.pitchDown * v;
  const bank = LANDING_PATH.bankAngle * Math.sin(v * Math.PI);
  const yaw = LANDING_PATH.yawTurn * v;
  return { pos: [lateral, height, forward], pitch, bank, yaw };
}

function paperFlightMatrix(nowMs) {
  if (!startTime) return window.mat4();
  const elapsed = nowMs - startTime;
  const launchStart = totalFoldTimeMs + FLIGHT_PATH.delay;
  if (elapsed <= launchStart) return window.mat4();

  const flightTime = elapsed - launchStart;
  const launchDur = FLIGHT_PATH.duration;
  const launchProgress = clamp(flightTime / launchDur, 0, 1);
  const launchState = launchPhaseState(launchProgress);

  if (flightTime <= launchDur) return composeTransform(launchState);

  let phaseTime = flightTime - launchDur;
  const cruiseLocal1 = cruisePhaseState(CRUISE_PATH, phaseTime);
  const cruiseState1 = combineStates({ pos: launchState.pos.slice(), pitch: launchState.pitch, bank: launchState.bank, yaw: launchState.yaw }, cruiseLocal1);
  if (phaseTime <= CRUISE_PATH.duration) return composeTransform(cruiseState1);

  phaseTime -= CRUISE_PATH.duration;
  const cruiseLocal2 = cruisePhaseState(CRUISE_PATH2, phaseTime);
  const cruiseState2 = combineStates(cruiseState1, cruiseLocal2);
  if (phaseTime <= CRUISE_PATH2.duration) return composeTransform(cruiseState2);

  // Landing
  const landingTime = phaseTime - CRUISE_PATH2.duration;
  const landingLocal = landingPhaseState(landingTime, cruiseState2.pos[1]);
  const landingState = combineStates(cruiseState2, landingLocal);
  return composeTransform(landingState);
}

/* ============================= Resize / View ============================ */

/* [VIEW] Maintain correct viewport and perspective on resize. */
function resizeCanvas() {
  const canvas = gl.canvas;
  const dpr = window.devicePixelRatio || 1;
  const w = Math.floor(canvas.clientWidth * dpr);
  const h = Math.floor(canvas.clientHeight * dpr);
  if (canvas.width !== w || canvas.height !== h) {
    canvas.width = w; canvas.height = h;
    gl.viewport(0, 0, w, h);
    if (program) {
      const aspect = w / h;
      const P = window.perspective(45.0, aspect, 0.01, 30.0);
      gl.useProgram(program);
      gl.uniformMatrix4fv(uProjLoc, false, window.flatten(P));
    }
  }
}

/* ====================== Orbit control handlers ========================= */

/* [VIEW] Simple orbit controls:
   - Drag to rotate (theta, phi)
   - Wheel to zoom (radius)
   - Double-click to reset camera pose
*/
function attachOrbitControls(canvas) {
  canvas.addEventListener("mousedown", (e) => {
    if (e.button !== 0) return;
    isDragging = true; lastX = e.clientX; lastY = e.clientY; e.preventDefault();
  });
  window.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    const dx = e.clientX - lastX, dy = e.clientY - lastY;
    lastX = e.clientX; lastY = e.clientY;
    const w = gl.canvas.clientWidth, h = gl.canvas.clientHeight;
    const dim = Math.max(1, Math.min(w, h));
    ORBIT.theta += (dx / dim) * Math.PI * ORBIT_SENS.rotate;
    ORBIT.phi   += (dy / dim) * Math.PI * ORBIT_SENS.rotate * -1;
    ORBIT.phi    = clamp(ORBIT.phi, ORBIT.minPhi, ORBIT.maxPhi);
  });
  window.addEventListener("mouseup", () => { isDragging = false; });
  canvas.addEventListener("wheel", (e) => {
    const delta = Math.sign(e.deltaY);
    const factor = Math.exp(delta * ORBIT_SENS.zoom);
    ORBIT.radius = clamp(ORBIT.radius * factor, ORBIT.minR, ORBIT.maxR);
    e.preventDefault();
  }, { passive: false });
  canvas.addEventListener("dblclick", () => { ORBIT.radius = 3.0; ORBIT.theta = 0.0; ORBIT.phi = 0.30; });
}

/* ================================ Init ================================ */

/* [BOOT] Initialize GL, compile shaders, build geometry, seed animation. */
function init() {
  const canvas = document.getElementById("gl-canvas");
  canvas.style.width = "100vw"; canvas.style.height = "100vh";

  gl = canvas.getContext("webgl2", { antialias: true });
  if (!gl) { alert("WebGL 2.0 not available"); return; }

  resizeCanvas();
  window.addEventListener("resize", resizeCanvas);
  attachOrbitControls(canvas);

  gl.clearColor(0.6, 0.75, 0.95, 1.0); // soft background
  gl.enable(gl.DEPTH_TEST);
  gl.disable(gl.CULL_FACE);

  program = initShaders(gl, "vertex-shader", "fragment-shader");
  gl.useProgram(program);

  // Matrix uniforms
  uModelLoc = gl.getUniformLocation(program, "uModel");
  uViewLoc  = gl.getUniformLocation(program, "uView");
  uProjLoc  = gl.getUniformLocation(program, "uProj");

  // Multi-fold uniforms
  uFoldCountLoc       = gl.getUniformLocation(program, "uFoldCount");
  uFoldAngleLoc       = gl.getUniformLocation(program, "uFoldAngle");
  uFoldPointLoc       = gl.getUniformLocation(program, "uFoldPoint");
  uFoldAxisLoc        = gl.getUniformLocation(program, "uFoldAxis");
  uFoldNormalLoc      = gl.getUniformLocation(program, "uFoldNormal");
  uFoldSideLoc        = gl.getUniformLocation(program, "uFoldSide");
  uFoldUseOrigSideLoc = gl.getUniformLocation(program, "uFoldUseOrigSide");

  // Projection / initial View
  const aspect = gl.canvas.width / gl.canvas.height;
  const P = window.perspective(45.0, aspect, 0.01, 30.0);
  gl.uniformMatrix4fv(uProjLoc, false, window.flatten(P));

  // Build scene VAOs
  const { roomVAO, deskVAO } = buildRoomAndDesk();
  VAOroom = roomVAO.vao; roomCount = roomVAO.count;
  VAOdesk = deskVAO.vao; deskCount = deskVAO.count;

  // Build paper (right half)
  const { W, H, vao } = createRightHalfGrid(36, 24);
  VAOpaperHalf = vao;
  buildRightFolds(W, H);

  startTime = performance.now();
  requestAnimationFrame(render);
}

/* ============================ Fold uniforms ============================ */

/* [ANIM] Upload fold parameters for the current frame to the shader. */
function uploadFoldUniforms(angles) {
  const MAX_FOLDS = 8; // must match shader

  const count = Math.min(folds.length, MAX_FOLDS);
  const points   = new Float32Array(MAX_FOLDS * 3);
  const axes     = new Float32Array(MAX_FOLDS * 3);
  const normals  = new Float32Array(MAX_FOLDS * 2);
  const sides    = new Int32Array(MAX_FOLDS);
  const useOrigI = new Int32Array(MAX_FOLDS);

  for (let i = 0; i < count; i++) {
    const f = folds[i];
    points.set(f.p,        i * 3);
    axes.set(  f.axis,     i * 3);
    normals.set(f.normal,  i * 2);
    sides[i]    = f.side | 0;
    useOrigI[i] = f.useOrig ? 1 : 0;
  }

  const angFull = new Float32Array(MAX_FOLDS);
  for (let i=0;i<count;i++) angFull[i] = angles[i] || 0;
  gl.uniform1i(uFoldCountLoc, count);
  gl.uniform1fv(uFoldAngleLoc, angFull);
  gl.uniform3fv(uFoldPointLoc, points);
  gl.uniform3fv(uFoldAxisLoc,  axes);
  gl.uniform2fv(uFoldNormalLoc, normals);
  gl.uniform1iv(uFoldSideLoc,  sides);
  gl.uniform1iv(uFoldUseOrigSideLoc, useOrigI);
}

/* ================================ Render ================================ */

/* [RENDER] Draw order:
   1) Room (no folds)
   2) Desk (no folds)
   3) Paper right-half (folds on)
   4) Paper left-half (mirrored, folds on)
*/
function render(now) {
  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

  // Camera
  const eye = vec3(-3, 6.0, -6)//orbitToEye();
  // Camera looks at desk height so scene is framed around the action
  // Camera closer, above-left, looking down to paper center
  const V = window.lookAt(eye, TARGET, window.vec3(0,1,0));
  gl.uniformMatrix4fv(uViewLoc, false, window.flatten(V));

  // ---------- Draw room (no folds) ----------
  gl.uniform1i(uFoldCountLoc, 0); // disable folding
  gl.bindVertexArray(VAOroom);
  gl.uniformMatrix4fv(uModelLoc, false, window.flatten(window.mat4()));
  gl.drawArrays(gl.TRIANGLES, 0, roomCount);

  // ---------- Draw desk (no folds) ----------
  gl.bindVertexArray(VAOdesk);
  gl.uniformMatrix4fv(uModelLoc, false, window.flatten(window.mat4()));
  gl.drawArrays(gl.TRIANGLES, 0, deskCount);

  // ---------- Draw paper (folding, two passes: right half, then mirrored left) ----------
  // Safety: recompute and upload fold uniforms immediately before drawing the paper
  const angles = foldProgress(now);
  uploadFoldUniforms(angles);
  gl.bindVertexArray(VAOpaperHalf);

  // place paper onto desk: y ~ 0.111, z center ~ -2.40
  // Paper placement on desk surface (slightly above top to avoid z-fight)
  const Tdesk = window.translate(0.0, 0.86, -2.40);
  // Rotate paper from XY plane to lie flat on desk (XZ plane)
  const Rx = window.rotate(-90, window.vec3(1,0,0));
  const basePaper = window.mult(Tdesk, Rx);
  let Mpaper = window.mult(paperFlightMatrix(now), basePaper);
  const worldOrigin = window.mult(Mpaper, window.vec4(0,0,0,1));
  if (worldOrigin[1] < FLOOR_Y) {
    const lift = window.translate(0, FLOOR_Y - worldOrigin[1], 0);
    Mpaper = window.mult(lift, Mpaper);
  } else if (worldOrigin[1] > CEILING_Y) {
    const drop = window.translate(0, CEILING_Y - worldOrigin[1], 0);
    Mpaper = window.mult(drop, Mpaper);
  }

  // PASS 1: right half
  gl.uniformMatrix4fv(uModelLoc, false, window.flatten(Mpaper));
  gl.drawArrays(gl.TRIANGLES, 0, paperHalfCount);

  // PASS 2: mirrored left half (mirror across X in object space, then translate)
  const Sx = window.scale(-1, 1, 1);
  const Mleft = window.mult(Mpaper, Sx);
  gl.uniformMatrix4fv(uModelLoc, false, window.flatten(Mleft));
  gl.drawArrays(gl.TRIANGLES, 0, paperHalfCount);

  gl.bindVertexArray(null);
  requestAnimationFrame(render);
}

/* ============================== Boot strap ============================= */
window.addEventListener("DOMContentLoaded", init);
