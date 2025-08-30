/* Main file for project
    This file is to focus on the user story of a map that shows the status of the parking lots across campus
        - "As a student I want to be able to see a visual reference of the current capacity of the parking 
        lot to easily judge the parking across campus. An example would be a map with green, yellow, or red
        overlayed over the parking lots on campus."

*/
function main() {
    window.onload = function() {
        const canvas = document.getElementById('imageCanvas');
        const ctx = canvas.getContext('2d');
        
        // Load the image
        const img = new Image();
        img.src = '/img/campus.jpg';
        // Courtesy of https://x.com/CCUHousing/status/1039140856673054725
        img.onload = function() {
            // Draw the image on the canvas
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

            // Define the box parameters (x, y, width, height)
            const x = 100;
            const y = 100;
            const width = 150;
            const height = 100;

            // Draw a red box around the selected area
            ctx.beginPath();
            ctx.rect(x, y, width, height);
            ctx.lineWidth = 3;
            ctx.strokeStyle = 'red';
            ctx.stroke();
        }
    }
}