// server.js
require('dotenv').config();
const express = require('express');
const morgan = require('morgan');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

// NEW: Postgres client
const { Pool } = require('pg');

const app = express();
const PORT = Number(process.env.PORT) || 3000;
const HOST = process.env.HOST || '0.0.0.0'; // important for Docker/WSL

app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

// --- PHP frontend redirect (non-breaking) ---
const FRONTEND_PHP_ORIGIN = process.env.FRONTEND_PHP_ORIGIN; // e.g., "http://127.0.0.1:8081"
if (FRONTEND_PHP_ORIGIN) {
  // Redirect root and any HTML navigations to the PHP server
  app.get('/', (req, res) => res.redirect(FRONTEND_PHP_ORIGIN));
  app.get(['/index.php','/index.html'], (req, res) => res.redirect(FRONTEND_PHP_ORIGIN));
  app.use((req, res, next) => {
    const acceptsHTML = (req.headers.accept || '').includes('text/html');
    const isApi = req.path.startsWith('/api');
    if (acceptsHTML && !isApi) return res.redirect(FRONTEND_PHP_ORIGIN + req.originalUrl);
    next();
  });
  // Optional: quiet favicon.ico when using PHP frontend
  app.get('/favicon.ico', (req, res) => res.status(204).end());
}
// --- end PHP frontend block ---

// Resolve paths once and log them
const webDir = path.join(__dirname, '..', 'apps', 'web');
const dataDir = path.join(__dirname, '..', 'data');
const apiSrcDir = path.join(__dirname, '..', 'apps', 'api', 'src');

console.log('[startup] __dirname:', __dirname);
console.log('[startup] webDir:', webDir);
console.log('[startup] dataDir:', dataDir);
console.log('[startup] apiSrcDir:', apiSrcDir);

// Validate index.html exists — fail early if not
const indexPath = path.join(webDir, 'index.html');
if (!fs.existsSync(indexPath)) {
  console.error(`[startup] Missing index.html at: ${indexPath}`);
}

// Health
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', time: new Date().toISOString(), uptime: process.uptime() });
});

/* ===========================
   NEW: Postgres connection
   =========================== */
const pool = new Pool({
  // Prefer environment variables:
  // PGHOST, PGUSER, PGPASSWORD, PGDATABASE, PGPORT
  // Or a single DATABASE_URL=postgres://user:pass@host:port/dbname
  connectionString: process.env.DATABASE_URL || undefined,
  ssl: process.env.PGSSL === 'true' ? { rejectUnauthorized: false } : false,
});

/* ===========================================================
   NEW: API endpoints consumed by parkingStatus.js / Leaflet
   - Assumes your DB defines:
       get_parking_lots() -> json/jsonb (array of objects)
       get_parking_lots_at(timestamptz) -> json/jsonb  (optional)
   - Each object should include:
       { id, name, capacity, fill, event, geom: GeoJSON }
   =========================================================== */

// Return the current lots as JSON array (already JSON from Postgres)
app.get('/api/lots', async (req, res) => {
  try {
    const { rows } = await pool.query('SELECT get_parking_lots() AS data;');
    // rows[0].data should be json/jsonb → send as-is
    const payload = rows?.[0]?.data;
    if (!payload) return res.json([]); // be kind to the client
    res.json(payload);
  } catch (err) {
    console.error('[api/lots] DB error:', err);
    res.status(500).json({ error: 'DB failure' });
  }
});

// Optional time-sliced endpoint: /api/lots_at?at=2025-10-31T12:00:00Z
app.get('/api/lots_at', async (req, res) => {
  try {
    const at = req.query.at;
    if (!at) return res.status(400).json({ error: 'Missing ?at=ISO8601 timestamp' });
    const { rows } = await pool.query('SELECT get_parking_lots_at($1) AS data;', [at]);
    const payload = rows?.[0]?.data;
    if (!payload) return res.json([]);
    res.json(payload);
  } catch (err) {
    console.error('[api/lots_at] DB error:', err);
    res.status(500).json({ error: 'DB failure' });
  }
});

// Static
app.use(express.static(webDir));
app.use('/data', express.static(dataDir));

// Only expose this if you truly need client-accessible files from api/src
app.use('/src', express.static(apiSrcDir));

// SPA fallback (exclude /api, /data)
app.get(/^\/(?!api|data).*/, (req, res, next) => {
  res.sendFile(indexPath, (err) => {
    if (err) next(err);
  });
});

// Error visibility
app.use((err, req, res, next) => {
  console.error('[error]', err);
  res.status(500).json({ error: 'Internal Server Error' });
});

const server = app.listen(PORT, HOST, () => {
  console.log(`[startup] Server listening on http://${HOST}:${PORT}`);
});

// Catch unhandled errors so you see them
process.on('unhandledRejection', (e) => console.error('[unhandledRejection]', e));
process.on('uncaughtException', (e) => console.error('[uncaughtException]', e));
