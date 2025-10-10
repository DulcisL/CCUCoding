import express from 'express';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json({ limit: '5mb' })); // for POST JSON
app.use(express.static(path.join(__dirname, 'public')));

// Simple health endpoint
app.get('/api/health', (_req, res) => res.json({ ok: true }));

// Data file path
const dataDir = path.join(__dirname, 'data');
const lotsPath = path.join(dataDir, 'parking_lots.geojson');

// Ensure data dir exists
if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });

// Load initial file or create an empty FeatureCollection
function initFile() {
  if (!fs.existsSync(lotsPath)) {
    const empty = { type: 'FeatureCollection', features: [] };
    fs.writeFileSync(lotsPath, JSON.stringify(empty, null, 2));
  }
}
initFile();

// GET lots
app.get('/api/lots', (_req, res) => {
  try {
    const text = fs.readFileSync(lotsPath, 'utf-8');
    res.setHeader('Content-Type', 'application/json');
    res.send(text);
  } catch (e) {
    res.status(500).json({ error: 'Failed to read lots file.' });
  }
});

// POST lots (save)
app.post('/api/lots', (req, res) => {
  const body = req.body;
  // Basic validation
  if (!body || body.type !== 'FeatureCollection' || !Array.isArray(body.features)) {
    return res.status(400).json({ error: 'Body must be a GeoJSON FeatureCollection.' });
  }
  try {
    fs.writeFileSync(lotsPath, JSON.stringify(body, null, 2));
    res.status(204).end();
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: 'Failed to write lots file.' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
