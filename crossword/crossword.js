const gridSize = 5; // or 15
const cellSize = 50;
const width = gridSize * cellSize + 300;
const height = gridSize * cellSize;

const canvas = document.createElement("canvas");
canvas.width = width;
canvas.height = height;
document.body.appendChild(canvas);
const ctx = canvas.getContext("2d");

const WHITE = "#FFFFFF", BLACK = "#000000", GRAY = "#C8C8C8", BLUE = "#0000FF", GREEN = "#00FF00", RED = "#FF0000";

const solutionCrossword = gridSize === 5 ? [
    ["P", "E", "R", "U", ""],
    ["O", "M", "A", "N", ""],
    ["T", "U", "P", "", ""],
    ["", "", "", "", ""],
    ["", "", "", "", ""]
] : [];

let editableGrid = solutionCrossword.map(row => row.map(cell => cell ? " " : ""));
let selectedCell = null;
let startTime = Date.now();
let gameWon = false;
let incorrectMessage = false;

function generateNumbers() {
    let numbering = Array.from({ length: gridSize }, () => Array(gridSize).fill(null));
    let num = 1;
    let hintsAcross = { 1: "A country in South America", 5: "A country in the Middle East", 6: "Animal that goes 'mahhhhh'" };
    let hintsDown = { 1: "Smoking it makes people high", 2: "A bird that can't fly", 3: "Expected from the Blacks", 4: "One in Spanish" };
    
    for (let row = 0; row < gridSize; row++) {
        for (let col = 0; col < gridSize; col++) {
            if (solutionCrossword[row][col] !== "" && (!row || !col || solutionCrossword[row - 1][col] === "" || solutionCrossword[row][col - 1] === "")) {
                numbering[row][col] = num++;
            }
        }
    }
    return { numbering, hintsAcross, hintsDown };
}

const { numbering, hintsAcross, hintsDown } = generateNumbers();

function drawGrid() {
    ctx.clearRect(0, 0, width, height);
    for (let row = 0; row < gridSize; row++) {
        for (let col = 0; col < gridSize; col++) {
            let x = col * cellSize, y = row * cellSize;
            ctx.fillStyle = solutionCrossword[row][col] === "" ? BLACK : (selectedCell?.[0] === row && selectedCell?.[1] === col ? BLUE : WHITE);
            ctx.fillRect(x, y, cellSize, cellSize);
            ctx.strokeStyle = GRAY;
            ctx.strokeRect(x, y, cellSize, cellSize);
            if (numbering[row][col]) {
                ctx.fillStyle = BLACK;
                ctx.font = "12px Arial";
                ctx.fillText(numbering[row][col], x + 3, y + 12);
            }
            if (editableGrid[row][col] !== " ") {
                ctx.fillStyle = BLACK;
                ctx.font = "36px Arial";
                ctx.fillText(editableGrid[row][col], x + 15, y + 35);
            }
        }
    }
    ctx.fillStyle = BLACK;
    ctx.font = "20px Arial";
    ctx.fillText(`Time: ${((Date.now() - startTime) / 1000).toFixed(1)}s`, gridSize * cellSize + 10, 30);
    
    if (gameWon) {
        ctx.fillStyle = GREEN;
        ctx.font = "48px Arial";
        ctx.fillText("You Win!", width / 2 - 60, height / 2);
    }
    if (incorrectMessage) {
        ctx.fillStyle = RED;
        ctx.font = "20px Arial";
        ctx.fillText("Not quite correct!", gridSize * cellSize + 10, height - 20);
    }
    
    let yOffset = 50;
    ctx.font = "14px Arial";
    for (let [num, hint] of Object.entries(hintsAcross)) {
        ctx.fillText(`${num}A: ${hint}`, gridSize * cellSize + 10, yOffset);
        yOffset += 20;
    }
    yOffset += 10;
    for (let [num, hint] of Object.entries(hintsDown)) {
        ctx.fillText(`${num}D: ${hint}`, gridSize * cellSize + 10, yOffset);
        yOffset += 20;
    }
}

document.addEventListener("click", (e) => {
    let col = Math.floor(e.offsetX / cellSize);
    let row = Math.floor(e.offsetY / cellSize);
    if (col < gridSize && solutionCrossword[row][col] !== "") selectedCell = [row, col];
});

document.addEventListener("keydown", (e) => {
    if (selectedCell && !gameWon) {
        let [row, col] = selectedCell;
        if (e.key.match(/^[a-zA-Z]$/)) {
            editableGrid[row][col] = e.key.toUpperCase();
        } else if (e.key === "Backspace") {
            editableGrid[row][col] = " ";
            incorrectMessage = false;
        }
        checkCompletion();
    }
});

function checkCompletion() {
    gameWon = solutionCrossword.every((row, rIdx) => row.every((cell, cIdx) => cell === "" || editableGrid[rIdx][cIdx] === cell));
    incorrectMessage = !gameWon && editableGrid.flat().every((cell, i) => solutionCrossword.flat()[i] === "" || cell !== " ");
}

function gameLoop() {
    drawGrid();
    requestAnimationFrame(gameLoop);
}
gameLoop();
