/* parkingStatus file used for creating and updating the web page showing parking lot status.
  Desc: This will take the map and given data from SQL and change the parking lot color based on the 
  current fill of the parking lot at the given time.
  
  User Story: As a student I want to be able to see a visual reference of the current capacity 
  of the parking lot to easily judge the parking across campus. An example would be a map with 
  green, yellow, or red overlayed over the parking lots on campus.
*/

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
  constructor(lotId, lotName, lotCapacity, lotfill, lotLocation) {
    this._id = lotId;
    this.name = lotName;
    this.capacity = lotCapacity;
    this.fill = lotfill;
    this.location = lotLocation
    this.color = this.setColor();
  }

  setColor() {
    //Red and green will be inversely proportional round to 2 decimals
    var red = round((255 * this.fill), 2);
    var green = round((255 * (1 - this.fill)), 2);

    //Set color of polygon for lot
    return rgb(red, 0, green);
  }
};

/*getLots()
Desc: This will collect the information that is needed from the SQL database and return the lots 
        in and array.
Params: none
Returns: lots(array) - will return the array of the lots with the needed information
*/
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


*/