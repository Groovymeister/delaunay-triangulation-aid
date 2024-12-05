const svg = d3.select("#plot");
const width = +svg.attr("width");
const height = +svg.attr("height");
const originX = width / 2;  // x = 0 point
const originY = height / 2;  // y = 0 point
const autoModeToggle = document.getElementById("auto-mode-toggle");
const autoModeSlider = document.getElementById("auto-mode-slider");
const sliderValueDisplay = document.getElementById("slider-value");

let steps = [];
let currentStep = 0;
let triangulationComplete = false;
let autoModeEnabled = false;
let autoModeInterval = null;

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
            if (triangulationComplete || currentStep > 0) {return;}
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
    if (triangulationComplete || (currentStep < steps.length && currentStep != 0)) return;
    const [mouseX, mouseY] = d3.pointer(event);
    const x = mouseX - originX;  // Calculate x relative to origin
    const y = originY - mouseY;  // Calculate y relative to origin
    addPoint(x, y);
});

// Function to clear edges
function clearEdges() {
    svg.selectAll(".edge-line").remove();
    steps = [];
    currentStep = 0;
    triangulationComplete = false;
}

// Event listener for the "Clear Points" button
document.getElementById("clear-button").addEventListener("click", () => {
    svg.selectAll(".point-group").remove();  // Remove all point groups
    clearEdges();  // Clear polygons as well
    steps = [];
    currentStep = 0;
    triangulationComplete = false;
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
    steps = [];
    currentStep = 0;
    clearEdges();

    // Generate random points
    for (let i = 0; i < numPoints; i++) {
        // Generate random coordinates relative to the center
        const randomX = (Math.random() * (width-10)) - ((width-10) / 2);  // Range [-width-10/2, width-10/2]
        const randomY = (Math.random() * (height-10)) - ((height-10) / 2); // Range [-height-10/2, height-10/2]
        addPoint(randomX, randomY);
    }
});

document.getElementById("generate-button").addEventListener("click", () => {
    if (autoModeEnabled) { startAutoMode();}
    else{
    const points = [];
    

    svg.selectAll(".point-group").each(function() {
        const pointGroup = d3.select(this);
        const circle = pointGroup.select("circle");
        const cx = +circle.attr("cx") - originX;
        const cy = originY - +circle.attr("cy");
        points.push([cx, cy]);
    });

    clearEdges();

    fetch('https://delaunay-triangulation-aid.onrender.com/api/triangulate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ points: points })
    })
    .then(response => response.json())
    .then(data => {
        if (data.triangles) {
            data.triangles.forEach(edge => {
                const p1 = edge.p1;
                const p2 = edge.p2;

                svg.append("line")
                    .attr("x1", originX + p1.x)
                    .attr("y1", originY - p1.y)
                    .attr("x2", originX + p2.x)
                    .attr("y2", originY - p2.y)
                    .attr("stroke", "blue")
                    .attr("stroke-width", 2)
                    .attr("class", "edge-line");
            });
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
    triangulationComplete = true;
}
});

function fetchSteps(points) {
    // return fetch('http://127.0.0.1:5000/api/step', {
    return fetch('https://delaunay-triangulation-aid.onrender.com/api/step', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ points: points })
    })
    .then(response => response.json())
    .then(data => {
        steps = data.steps;
        console.log("Fetched Steps: ", steps);
    })
    .catch((error) => {
        console.error('Error fetching steps:', error);
    });
}

function getAllPoints() {
    const points = [];
    svg.selectAll(".point-group").each(function() {
        const pointGroup = d3.select(this);
        const circle = pointGroup.select("circle");
        const cx = +circle.attr("cx") - originX;
        const cy = originY - +circle.attr("cy");
        points.push([cx, cy]);
    });
    return points;
}

document.getElementById("step-button").addEventListener("click", () => {
    if (currentStep === 0) {
        fetchSteps(getAllPoints()).then(() => {
            if (steps.length > 0) {
                processStep();
            } else {
                console.log("No steps available.");
            }
        });
    } else if (currentStep < steps.length && !(triangulationComplete)) {
        processStep();
    } else {
        console.log("No more steps to perform.");
        triangulationComplete = true;
    }
});

function processStep() {
    const step = steps[currentStep];
    switch (step.type) {
        case "add":
            step.edges.forEach(edge => {
                svg.append("line")
                    .attr("x1", originX + edge.p1.x)
                    .attr("y1", originY - edge.p1.y)
                    .attr("x2", originX + edge.p2.x)
                    .attr("y2", originY - edge.p2.y)
                    .attr("stroke", "blue")
                    .attr("stroke-width", 2)
                    .attr("class", "edge-line");
            });
            section = document.getElementById("add");
     
            section.scrollIntoView({
                behavior: "smooth", 
                block: "nearest",   
                inline: "nearest"  
            });
            break;
        case "remove":
            step.edges.forEach(edge => {
                svg.selectAll(".edge-line")
                    .filter(function() {
                        const line = d3.select(this);
                        const x1 = +line.attr("x1");
                        const y1 = +line.attr("y1");
                        const x2 = +line.attr("x2");
                        const y2 = +line.attr("y2");
                        return (x1 === originX + edge.p1.x && y1 === originY - edge.p1.y &&
                            x2 === originX + edge.p2.x && y2 === originY - edge.p2.y);
                    })
                    .remove();
            });
            section = document.getElementById("remove");
         
            section.scrollIntoView({
                behavior: "smooth", 
                block: "nearest",   
                inline: "nearest"  
            });
            break;
        case "initial_edges":
            step.edges.forEach(edge => {
                svg.append("line")
                    .attr("x1", originX + edge.p1.x)
                    .attr("y1", originY - edge.p1.y)
                    .attr("x2", originX + edge.p2.x)
                    .attr("y2", originY - edge.p2.y)
                    .attr("stroke", "blue")
                    .attr("stroke-width", 2)
                    .attr("class", "edge-line");
            });
            section = document.getElementById("initial_edges");
            section.scrollIntoView({
                behavior: "smooth", 
                block: "nearest",   
                inline: "nearest"  
            });
            break;

    }
    currentStep++;
}

// Slider value display
autoModeSlider.addEventListener("input", () => {
    sliderValueDisplay.textContent = `${autoModeSlider.value}ms`;
});

// Toggle auto mode on/off
autoModeToggle.addEventListener("change", () => {
    autoModeEnabled = autoModeToggle.checked;
    if (!autoModeEnabled && autoModeInterval) {
        clearInterval(autoModeInterval);
        autoModeInterval = null;
    }
});

function startAutoMode() {
    fetchSteps(getAllPoints()).then(() => {
        if (steps.length > 0) {
            function executeStep() {
                if (!autoModeEnabled) {return;}
                if (currentStep < steps.length) {
                    processStep();
                    setTimeout(executeStep, parseInt(autoModeSlider.value));
                } else {
                    triangulationComplete = true;
                }
            }
            executeStep();
        }
    });
}
