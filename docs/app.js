const svg = d3.select("#plot");
const width = +svg.attr("width");
const height = +svg.attr("height");
const originX = width / 2;  // x = 0 point
const originY = height / 2;  // y = 0 point

// Track whether coordinates are visible or not
let showCoordinates = true;

// Function to draw gridlines (with center as origin)
function drawGridlines() {
    const gridSize = 10;  // Set smaller grid size
    
    // Draw vertical lines
    for (let x = 0; x <= width; x += gridSize) {
        svg.append("line")
            .attr("x1", x)
            .attr("y1", 0)
            .attr("x2", x)
            .attr("y2", height)
            .attr("stroke", "#ddd")
            .attr("stroke-width", 1);
    }

    // Draw horizontal lines
    for (let y = 0; y <= height; y += gridSize) {
        svg.append("line")
            .attr("x1", 0)
            .attr("y1", y)
            .attr("x2", width)
            .attr("y2", y)
            .attr("stroke", "#ddd")
            .attr("stroke-width", 1);
    }

    // Draw x and y axes
    svg.append("line")
        .attr("x1", originX)
        .attr("y1", 0)
        .attr("x2", originX)
        .attr("y2", height)
        .attr("stroke", "black")
        .attr("stroke-width", 2);

    svg.append("line")
        .attr("x1", 0)
        .attr("y1", originY)
        .attr("x2", width)
        .attr("y2", originY)
        .attr("stroke", "black")
        .attr("stroke-width", 2);
}

// Draw the gridlines
drawGridlines();

// Function to add a point
function addPoint(x, y) {
    const pointGroup = svg.append("g").attr("class", "point-group");

    pointGroup.append("circle")
        .attr("cx", originX + x)  // Offset by origin
        .attr("cy", originY - y)  // Invert y for correct position
        .attr("r", 3)  // Smaller circle radius
        .attr("fill", "red")
        .style("cursor", "pointer")
        .on("click", function(event) {
            pointGroup.remove();
            event.stopPropagation();  // Prevent adding a new point while removing
        });

    pointGroup.append("text")
        .attr("x", originX + x + 10)  // Offset by origin
        .attr("y", originY - y)  // Invert y for correct position
        .attr("fill", "black")
        .attr("class", "coordinates")
        .attr("visibility", showCoordinates ? "visible" : "hidden")
        .text(`(${Math.round(x)}, ${Math.round(y)})`)
        .style("pointer-events", "none");
}

// Click to add points manually
svg.on("click", function(event) {
    const [mouseX, mouseY] = d3.pointer(event);
    const x = mouseX - originX;  // Calculate x relative to origin
    const y = originY - mouseY;  // Calculate y relative to origin
    addPoint(x, y);
});

// Function to clear polygons
function clearPolygons() {
    svg.selectAll("polygon").remove();  // Remove all polygons
}

// Event listener for the "Clear Points" button
document.getElementById("clear-button").addEventListener("click", () => {
    svg.selectAll(".point-group").remove();  // Remove all point groups
    clearPolygons();  // Clear polygons as well
});

// Event listener for the "Toggle Coordinates" button
document.getElementById("toggle-coords").addEventListener("click", () => {
    showCoordinates = !showCoordinates;  // Toggle the state

    // Toggle the visibility of all text elements with class 'coordinates'
    svg.selectAll(".coordinates")
        .attr("visibility", showCoordinates ? "visible" : "hidden");
});

// Event listener for the "Randomize" button
document.getElementById("randomize-button").addEventListener("click", () => {
    const input = document.getElementById("point-count");
    let numPoints = +input.value;

    // Ensure the number is between 1 and 1000
    if (numPoints > 1000) {
        numPoints = 1000;
        input.value = 1000;  // Reset input to 1000 if above
    } else if (numPoints < 1 || isNaN(numPoints)) {
        numPoints = 1;  // Set default to 1 if invalid input
        input.value = 1;
    }

    // Clear previous points and polygons before adding new ones
    svg.selectAll(".point-group").remove();
    clearPolygons();

    // Generate random points
    for (let i = 0; i < numPoints; i++) {
        // Generate random coordinates relative to the center
        const randomX = (Math.random() * (width-10)) - ((width-10) / 2);  // Range [-width-10/2, width-10/2]
        const randomY = (Math.random() * (height-10)) - ((height-10) / 2); // Range [-height-10/2, height-10/2]
        addPoint(randomX, randomY);
    }
});

// Event listener for the "Generate" button
document.getElementById("generate-button").addEventListener("click", () => {
    const points = [];

    // Gather all points from the SVG
    svg.selectAll(".point-group").each(function() {
        const pointGroup = d3.select(this);
        const circle = pointGroup.select("circle");
        const cx = +circle.attr("cx") - originX;
        const cy = originY - +circle.attr("cy");
        points.push([cx, cy]);
    });

    // Clear polygons before generating new ones
    clearPolygons();

    // Send points to the back end via a POST request
    fetch('https://delaunay-triangulation-aid.onrender.com/api/triangulate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ points: points })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);

        if (data.triangles) {
            data.triangles.forEach(triangle => {
                const [i1, i2, i3] = triangle;
                const p1 = points[i1];
                const p2 = points[i2];
                const p3 = points[i3];

                svg.append("polygon")
                    .attr("points", `${originX + p1[0]},${originY - p1[1]} ${originX + p2[0]},${originY - p2[1]} ${originX + p3[0]},${originY - p3[1]}`)
                    .attr("fill", "blue")
                    .attr("stroke", "black")
                    .attr("stroke-width", 1);
            });
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
