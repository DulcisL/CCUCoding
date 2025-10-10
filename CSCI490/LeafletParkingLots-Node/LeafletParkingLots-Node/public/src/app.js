/* Leaflet Parking Lots (Node backend)
   - Draw polygons
   - Save/load GeoJSON via Express endpoints (/api/lots)
*/
(function(){
  "use strict";

  // ----- Map Init -----
  const DEFAULT_CENTER = [35.0000, -78.9000];
  const DEFAULT_ZOOM   = 16;

  const map = L.map('map').setView(DEFAULT_CENTER, DEFAULT_ZOOM);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  // A feature group to hold editable layers
  const drawnGroup = L.featureGroup().addTo(map);

  // Geoman controls
  map.pm.addControls({
    position: 'bottomleft',
    drawCircle: false,
    drawMarker: false,
    drawCircleMarker: false,
    drawRectangle: false,
    drawPolyline: false,
    drawText: false
  });

  // Style helper
  function lotStyle(feature) {
    const color = feature?.properties?.color || '#2a6';
    const opacity = feature?.properties?.opacity ?? 0.35;
    return { color, weight: 2, fillColor: color, fillOpacity: opacity };
  }

  // selected layer for property editing
  let selectedLayer = null;

  // ----- Load from server -----
  async function loadFromServer() {
    try {
      const r = await fetch('/api/lots');
      const gj = await r.json();
      addGeoJSONToMap(gj);
      try { map.fitBounds(drawnGroup.getBounds()); } catch(e) {}
    } catch (e) {
      console.warn('Failed to load from server, falling back to empty collection', e);
    }
  }

  function addGeoJSONToMap(geojson) {
    L.geoJSON(geojson, {
      style: lotStyle,
      onEachFeature: (feature, layer) => attachLayerHandlers(layer, feature)
    }).eachLayer(l => drawnGroup.addLayer(l));
  }

  function attachLayerHandlers(layer, feature) {
    layer.on('click', () => {
      selectedLayer = layer;
      const props = layer.feature?.properties || {};
      document.getElementById('propName').value = props.name || '';
      document.getElementById('propCapacity').value = props.capacity ?? '';
    });

    // Enable geoman editing
    layer.pm.enable({ allowSelfIntersection: false });

    // Save on edits
    layer.on('pm:edit', debouncePersist);
    layer.on('pm:dragend', debouncePersist);
  }

  // ----- Create new features -----
  map.on('pm:create', e => {
    const layer = e.layer;
    layer.feature = layer.feature || { type: 'Feature', properties: { name:'', capacity:null, color:'#2a6', opacity:0.35 } };
    attachLayerHandlers(layer, layer.feature);
    drawnGroup.addLayer(layer);
    debouncePersist();
  });

  // ----- Build current GeoJSON -----
  function currentGeoJSON() {
    const fc = { type: 'FeatureCollection', features: [] };
    drawnGroup.eachLayer(layer => {
      const feature = layer.toGeoJSON();
      const props = layer.feature?.properties || {};
      feature.properties = { ...props };
      fc.features.push(feature);
    });
    return fc;
  }

  // ----- Persist to server -----
  async function persistToServer() {
    const gj = currentGeoJSON();
    try {
      await fetch('/api/lots', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gj)
      });
    } catch (e) {
      console.error('Failed to persist to server', e);
    }
  }

  // Simple debounce to avoid spamming the server with writes
  let debounceTimer = null;
  function debouncePersist() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(persistToServer, 500);
  }

  // ----- UI: Export -----
  document.getElementById('btnExport').addEventListener('click', () => {
    const gj = currentGeoJSON();
    const blob = new Blob([JSON.stringify(gj, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'parking_lots.geojson';
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 500);
  });

  // ----- UI: Clear -----
  document.getElementById('btnClear').addEventListener('click', () => {
    if (!confirm('Remove all drawn features?')) return;
    drawnGroup.clearLayers();
    debouncePersist();
  });

  // ----- UI: Import (client-side only) -----
  document.getElementById('btnImport').addEventListener('click', async () => {
    const input = document.getElementById('fileImport');
    if (!input.files || !input.files[0]) { alert('Choose a .geojson file first.'); return; }
    const text = await input.files[0].text();
    try {
      const gj = JSON.parse(text);
      drawnGroup.clearLayers();
      addGeoJSONToMap(gj);
      debouncePersist();
      try { map.fitBounds(drawnGroup.getBounds()); } catch(e) {}
    } catch (e) {
      alert('Invalid GeoJSON file.');
    }
  });

  // ----- UI: Recenter -----
  document.getElementById('btnRecenter').addEventListener('click', () => {
    const lat = parseFloat(document.getElementById('centerLat').value);
    const lng = parseFloat(document.getElementById('centerLng').value);
    const zoom = parseInt(document.getElementById('zoomLevel').value, 10);
    if (isFinite(lat) && isFinite(lng)) map.setView([lat, lng], isFinite(zoom) ? zoom : map.getZoom());
  });

  // ----- UI: Update Selected Properties -----
  document.getElementById('btnUpdateProps').addEventListener('click', () => {
    if (!selectedLayer) { alert('Select a shape (click it on the map)'); return; }
    const name = document.getElementById('propName').value || '';
    const capacity = document.getElementById('propCapacity').value;
    selectedLayer.feature = selectedLayer.feature || { type:'Feature', properties:{} };
    const props = selectedLayer.feature.properties;
    props.name = name;
    props.capacity = capacity === '' ? null : Number(capacity);
    props.color = props.capacity && props.capacity > 0 ? '#2262CC' : '#2a6';
    selectedLayer.setStyle(lotStyle({ properties: props }));
    debouncePersist();
  });

  // Initial load
  loadFromServer();

})();