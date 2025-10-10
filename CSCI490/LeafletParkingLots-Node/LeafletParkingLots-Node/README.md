# Leaflet Parking Lots (Node + Express)

Leaflet + OpenStreetMap app with drawing & server-side GeoJSON persistence.

## Features
- OSM basemap (no API key)
- Draw/edit polygons with Leaflet-Geoman
- Save & load lots to/from server (`/api/lots` -> `data/parking_lots.geojson`)
- Import/Export GeoJSON manually
- Debounced saves during editing

## Run
```bash
npm install
npm run dev   # with nodemon
# or
npm start     # plain node
```
Open http://localhost:3000

## API
- `GET /api/lots` → returns current GeoJSON FeatureCollection
- `POST /api/lots` → body must be FeatureCollection; saves to `data/parking_lots.geojson`

## Structure
- `server.js` — Express server & API
- `public/` — static frontend (Leaflet app)
- `data/parking_lots.geojson` — persisted data file
