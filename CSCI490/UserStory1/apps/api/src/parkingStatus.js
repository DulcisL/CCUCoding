/* parkingStatus file used for creating and updating the web page showing parking lot status.
  Desc: This will take the map and given data from SQL and change the parking lot color based on the 
  current fill of the parking lot at the given time.
  
  User Story: As a student I want to be able to see a visual reference of the current capacity 
  of the parking lot to easily judge the parking across campus. An example would be a map with 
  green, yellow, or red overlayed over the parking lots on campus.
*/

//Get map and layers
const map = L.map('map', {
  preferCanvas: true // faster for many polygons
}).setView([40.0, -75.0], 14); // set to your campus center

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap & friends'
}).addTo(map);


//Helper functions
function clamp255(n) { return Math.max(0, Math.min(255, Math.round(n))); }

function fillToColor(fill, isEvent) {
  const red = clamp255(255 * fill);
  const green = clamp255(255 * (1 - fill));
  return isEvent ? 'rgb(255,0,0)' : `rgb(${red},0,${green})`;
}


/*Lot
  Desc: Class that will be used to store the needed information after being pulled from database
  Variables:
    _id(int) : the private lot ID 
    name (string) : the name of the parking lot
    capacity(int) : the capacity of the lot
    fill(float) : the percent filled of lot (between 0-1)
    location(geojson) : stores the polygon location information
    color(array) : the color based on the current fill of the parking lot
  
  Helpers:
    setColor() : sets the color based on the fill of the parking lot
  
*/
class Lot {
<<<<<<< HEAD
  constructor(lotId, lotName, lotCapacity, lotGeom, lotfill) {
=======
  constructor(lotId, lotName, lotCapacity, lotfill, lotLocation) {
>>>>>>> 1597a5aa940e3c5dde53dc8ea972ba9146e3ffb4
    this._id = lotId;
    this.name = lotName;
    this.capacity = lotCapacity;
    this.fill = lotfill;
<<<<<<< HEAD
    this.geom = lotGeom
    //set color automatically
=======
    this.location = lotLocation
>>>>>>> 1597a5aa940e3c5dde53dc8ea972ba9146e3ffb4
    this.color = this.setColor();
    this.event = false;
  }

  setColor() {
<<<<<<< HEAD
    // Assuming fill will be a number between 0 and 1
    //Red and green will be inversely proportional
    var red = 255 * this.fill;
    var green = 255 * (1 - this.fill);
    //set color of polygon for lot
    if (this.event == false){
      this.color = (red, 0, green);
    }
    if (this.event == true){
      this.color = (255, 0, 0);
    }
    return this.color
  }
  setEvent(bool){
    if (bool){
      this.event = bool;
      this.setColor();
    }
=======
    //Red and green will be inversely proportional round to 2 decimals
    var red = round((255 * this.fill), 2);
    var green = round((255 * (1 - this.fill)), 2);

    //Set color of polygon for lot
    return rgb(red, 0, green);
>>>>>>> 1597a5aa940e3c5dde53dc8ea972ba9146e3ffb4
  }
};

/*getLots()
Desc: This will collect the information that is needed from the SQL database and return the lots 
        in and array.
Params: none
Returns: lots(array) - will return the array of the lots with the needed information
*/
<<<<<<< HEAD
async function getLots() {
  const resp = await fetch('/api/lots', { headers: { 'Accept': 'application/json' } });
  if (!resp.ok) throw new Error(`API error ${resp.status}`);
  const data = await resp.json();
  return Array.isArray(data) ? data : [];
}

function lotsToFeatureCollection(lots) {
  return {
    type: 'FeatureCollection',
    features: lots.map(d => ({
      type: 'Feature',
      geometry: d.geom, // <- your DB-provided GeoJSON geometry
      properties: {
        lotId: String(d.id),
        name: d.name ?? `Lot ${d.id}`,
        capacity: d.capacity ?? null,
        fill: Number(d.fill ?? 0),
        event: Boolean(d.event)
      }
    }))
  };
}

function paintLayerFromProps(layer, props) {
  const color = fillToColor(props.fill, props.event);
  layer.setStyle({ fillColor: color, color: color, weight: 1, fillOpacity: 0.7, opacity: 1 });

  const pct = isFinite(props.fill) ? Math.round(props.fill * 100) : 0;
  const cap = props.capacity ?? '?';
  const badge = props.event ? ' • Event' : '';
  layer.bindTooltip(`${props.name}${badge}\n${pct}% full (${cap} cap)`, { sticky: true });
}

// First-time build of the layer and the id->layer map
function buildGeoJsonLayer(featureCollection) {
  lotGeoJsonLayer = L.geoJSON(featureCollection, {
    style: DEFAULT_STYLE,
    onEachFeature: (feature, layer) => {
      const id = feature.properties.lotId;
      lotLayerById.set(id, layer);

      // hover highlight (optional)
      layer.on('mouseover', () => layer.setStyle({ weight: 2 }));
      layer.on('mouseout', () => layer.setStyle({ weight: 1 }));

      paintLayerFromProps(layer, feature.properties);
    }
  }).addTo(map);

  map.fitBounds(lotGeoJsonLayer.getBounds(), { padding: [20, 20] });
}

// If a new lot appears, add it; if one disappears, gray it out.
function refreshStyles(featureCollection) {
  const seen = new Set();

  for (const feature of featureCollection.features) {
    const id = feature.properties.lotId;
    let layer = lotLayerById.get(id);

    if (layer) {
      // update existing
      paintLayerFromProps(layer, feature.properties);
    } else {
      // brand new lot—add it and track
      layer = L.geoJSON(feature, { style: DEFAULT_STYLE }).addTo(map);
      lotLayerById.set(id, layer.getLayers()[0] ?? layer);
      paintLayerFromProps(lotLayerById.get(id), feature.properties);
    }
    seen.add(id);
  }

  // Any polygon we didn’t see this cycle gets greyed out
  for (const [id, layer] of lotLayerById.entries()) {
    if (!seen.has(id)) layer.setStyle(DEFAULT_STYLE);
  }
}
=======
function getLots() {
  //Initialize
  let lots = {};
  var id, name, cap, fill, geojson;

  //Get data from PGSQL DB

  //Store as object with keyword pairs name:data into array

  //Return the lots array
  return lots
}

function main() {
  //Initialize
  let lots = {};

  //Get lots
  lots = getLots();

  //Set color of lot polygon
  for (const lot of lots) {
    //Update lots from DB over a certain amount of time

    //Set the new color
    lot.setColor();
  }

   //Push to leaflet

}
/* To Do
 - Data base implementation
    - 3 x 3 row x columns
 - Need to make data read from database (SQL)
    - Take string and parse into dict like name- pairs
 - Special events closes parking lots
 - Sending back to the leaflet
 - Front end (interactive map and UI)
 - Testing
>>>>>>> 1597a5aa940e3c5dde53dc8ea972ba9146e3ffb4



async function main() {
  try {
    const lots = await getLots();
    const fc = lotsToFeatureCollection(lots);

    if (!lotGeoJsonLayer) {
      buildGeoJsonLayer(fc);     // first run
    } else {
      refreshStyles(fc);         // subsequent runs
    }
  } catch (e) {
    console.error('Failed to load/paint lots:', e);
  }
}

//Set to refresh ever N seconds
function boot() {
  main();
  //Refreshes every 10 minutes
   setInterval(main, 600000);
}
document.addEventListener('DOMContentLoaded', boot);