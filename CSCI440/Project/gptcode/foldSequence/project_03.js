"use strict";

/* ===== WebGL state ===== */
let gl, program;

/* ===== Uniform locations ===== */
let uModelLoc, uViewLoc, uProjLoc;
let uFoldCountLoc, uFoldAngleLoc, uFoldPointLoc, uFoldAxisLoc, uFoldNormalLoc, uFoldSideLoc, uFoldUseOrigSideLoc;

/* ===== Geometry ===== */
let vaoHalf = null;   // right half only (x ∈ [0, +W/2])
let halfCount = 0;

/* ===== Camera (orbit controls) ===== */
const ORBIT = { radius: 3.0, minR: 0.6, maxR: 8.0, theta: 0.0, phi: 0.30, minPhi: -1.2, maxPhi: 1.2 };
const ORBIT_SENS = { rotate: 1.2, zoom: 0.25 };
let isDragging = false; let lastX = 0, lastY = 0;

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
  return window.vec3(r * cp * st, r * sp, r * cp * ct);
}

/* ==================== Build only the RIGHT HALF of paper ==================== */
function createRightHalfGrid(cols = 24, rows = 24) {
  // Paper size in object space
  const W = 0.5, H = 0.35;
  const xC = 0.0, xR = +W * 0.5; // center to right edge
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

  halfCount = positions.length / 3;

  vaoHalf = gl.createVertexArray();
  gl.bindVertexArray(vaoHalf);

  // Positions
  const posBuf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, posBuf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positions), gl.STATIC_DRAW);
  const aPosition = gl.getAttribLocation(program, "aPosition");
  gl.enableVertexAttribArray(aPosition);
  gl.vertexAttribPointer(aPosition, 3, gl.FLOAT, false, 0, 0);

  // Colors
  const colBuf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, colBuf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(colors), gl.STATIC_DRAW);
  const aColor = gl.getAttribLocation(program, "aColor");
  gl.enableVertexAttribArray(aColor);
  gl.vertexAttribPointer(aColor, 3, gl.FLOAT, false, 0, 0);

  gl.bindVertexArray(null);

  return { W, H };
}

/* ============ One-sided airplane folds (RIGHT half only) ============ */
/* Sequence: top-right diagonal → fuse (centerline) → right wing */
const folds = [];
const foldDur = [];

function buildRightFolds(W, H) {
  folds.length = 0; foldDur.length = 0;

  // 1) Top-right corner -> centerline diagonal: from (0, H/2) to (+W/2, 0)
  {
    const a = v2(0,  H/2), b = v2(+W/2, 0);
    const axisDir = norm2([b[0]-a[0], b[1]-a[1]]);
    const n = norm2(perp2(axisDir));  // 2D normal for side test
    const side = +1;                  // choose +normal side to fold (outer corner region)
    folds.push({
      p: v3(a[0], a[1], 0),
      axis: v3(axisDir[0], axisDir[1], 0),
      normal: v2(n[0], n[1]),
      side: side,
      target: Math.PI * 0.98,
      useOrig: false
    });
    foldDur.push(900);
  }

  // 2) Fuse along x = 0: fold the existing +X half over the centerline.
  //    Use ORIGINAL coords for the side test so the earlier diagonal
  //    doesn't confuse which vertices should move.
  {
    const n = v2(1, 0);  // +X normal; x>0 is the half we have
    folds.push({
      p: v3(0, 0, 0),    // hinge on centerline
      axis: v3(0, 1, 0), // hinge runs up/down (Y)
      normal: n,
      side: +1,          // select original x > 0
      target: Math.PI/2,   // 60°
      useOrig: true      // <<< important (test against ORIGINAL coords)
    });
    foldDur.push(1200);
  }



  // 3) Right wing: crease at x = +W*0.15, fold DOWN
  {
    const wingX = W * 0.25;
    folds.push({
      p: v3(+wingX, 0, 0),
      axis: v3(0, 1, 0),
      normal: v2(1, 0),
      side: +1,          // work on right half only
      target: -0.95,     // negative → down
      useOrig: true
    });
    foldDur.push(800);
  }
}

/* ================ Animate folds sequentially: 0 → target =============== */
function foldProgress(nowMs) {
  const tAbs = nowMs - startTime;
  const ang = new Float32Array(folds.length);
  let t = tAbs;
  for (let i = 0; i < folds.length; i++) {
    const d = foldDur[i] || 1000;
    if (t <= 0) { ang[i] = 0; break; }
    const seg = Math.min(1, t / d);
    ang[i] = easeInOut(seg) * folds[i].target;
    t -= d;
    if (seg < 1) break;
  }
  return ang;
}

/* ============================= Resize / View ============================ */
function resizeCanvas() {
  const canvas = gl.canvas;
  const dpr = window.devicePixelRatio || 1;
  const w = Math.floor(canvas.clientWidth * dpr);
  const h = Math.floor(canvas.clientHeight * dpr);
  if (canvas.width !== w || canvas.height !== h) {
    canvas.width = w;
    canvas.height = h;
    gl.viewport(0, 0, w, h);

    if (program) {
      const aspect = w / h;
      const P = window.perspective(45.0, aspect, 0.01, 20.0);
      gl.useProgram(program);
      gl.uniformMatrix4fv(uProjLoc, false, window.flatten(P));
    }
  }
}

/* ====================== Orbit control handlers ========================= */
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

/* ================================= Init ================================ */
function init() {
  const canvas = document.getElementById("gl-canvas");
  canvas.style.width = "100vw"; canvas.style.height = "100vh";

  gl = canvas.getContext("webgl2", { antialias: true });
  if (!gl) { alert("WebGL 2.0 not available"); return; }

  resizeCanvas();
  window.addEventListener("resize", resizeCanvas);
  attachOrbitControls(canvas);

  gl.clearColor(0.15, 0.15, 0.18, 1.0);
  gl.enable(gl.DEPTH_TEST);
  // (We don't enable CULL_FACE so mirrored winding still shows. If you enable it,
  //  remember to flip FRONT_FACE between passes.)

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

  // Projection / Model (model changes per pass)
  const aspect = gl.canvas.width / gl.canvas.height;
  const P = window.perspective(45.0, aspect, 0.01, 20.0);
  gl.uniformMatrix4fv(uProjLoc, false, window.flatten(P));

  // Geometry (RIGHT half only)
  const { W, H } = createRightHalfGrid(36, 24);
  buildRightFolds(W, H);

  startTime = performance.now();
  requestAnimationFrame(render);
}

/* ================================ Render ================================ */
function uploadFoldUniforms(angles) {
  const count = folds.length;
  const points   = new Float32Array(count * 3);
  const axes     = new Float32Array(count * 3);
  const normals  = new Float32Array(count * 2);
  const sides    = new Int32Array(count);
  const useOrigI = new Int32Array(count);

  for (let i = 0; i < count; i++) {
    const f = folds[i];
    points.set(f.p,        i * 3);
    axes.set(  f.axis,     i * 3);
    normals.set(f.normal,  i * 2);
    sides[i]    = f.side | 0;
    useOrigI[i] = f.useOrig ? 1 : 0;
  }

  gl.uniform1i(uFoldCountLoc, count);
  gl.uniform1fv(uFoldAngleLoc, angles);
  gl.uniform3fv(uFoldPointLoc, points);
  gl.uniform3fv(uFoldAxisLoc,  axes);
  gl.uniform2fv(uFoldNormalLoc, normals);
  gl.uniform1iv(uFoldSideLoc,  sides);
  gl.uniform1iv(uFoldUseOrigSideLoc, useOrigI);
}

function render(now) {
  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

  // Camera
  const eye = orbitToEye();
  const V = window.lookAt(eye, window.vec3(0,0,0), window.vec3(0,1,0));
  gl.uniformMatrix4fv(uViewLoc, false, window.flatten(V));

  // Fold progress for this frame
  const angles = foldProgress(now);

  // Upload fold arrays once (same for both passes)
  uploadFoldUniforms(angles);

  gl.bindVertexArray(vaoHalf);

  // PASS 1: draw RIGHT half with identity model
  gl.uniformMatrix4fv(uModelLoc, false, window.flatten(window.mat4()));
  gl.drawArrays(gl.TRIANGLES, 0, halfCount);

  // PASS 2: draw LEFT half by mirroring X in the model matrix
  // Build a simple scale(-1,1,1) matrix (MVnew.js doesn’t expose scalem reliably)
  const S = [
    [-1,0,0,0],
    [ 0,1,0,0],
    [ 0,0,1,0],
    [ 0,0,0,1]
  ];
  gl.uniformMatrix4fv(uModelLoc, false, window.flatten(S));
  gl.drawArrays(gl.TRIANGLES, 0, halfCount);

  gl.bindVertexArray(null);
  requestAnimationFrame(render);
}

/* ============================== Boot strap ============================= */
window.addEventListener("DOMContentLoaded", init);
