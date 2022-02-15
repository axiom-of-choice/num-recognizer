const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
let coord = { x: 0, y: 0 };

document.addEventListener("mousedown", start);
document.addEventListener("mouseup", stop);
window.addEventListener("resize", resize);

// Set up touch events for mobile, etc
canvas.addEventListener("touchstart", function (e) {
  mousePos = getTouchPos(canvas, e);
var touch = e.touches[0];
var mouseEvent = new MouseEvent("mousedown", {
x = touch.clientX,
y = touch.clientY
});
canvas.dispatchEvent(mouseEvent);
}, false);
canvas.addEventListener("touchend", function (e) {
var mouseEvent = new MouseEvent("mouseup", {});
canvas.dispatchEvent(mouseEvent);
}, false);
canvas.addEventListener("touchmove", function (e) {
var touch = e.touches[0];
var mouseEvent = new MouseEvent("mousemove", {
x =  touch.clientX,
y = touch.clientY
});
canvas.dispatchEvent(mouseEvent);
}, false);

// Get the position of a touch relative to the canvas
function getTouchPos(canvasDom, touchEvent) {
var rect = canvasDom.getBoundingClientRect();
return {
x = touchEvent.touches[0].clientX - rect.left,
y =  touchEvent.touches[0].clientY - rect.top
};
}

// Prevent scrolling when touching the canvas
document.body.addEventListener("touchstart", function (e) {
  if (e.target == canvas) {
    e.preventDefault();
  }
}, false);
document.body.addEventListener("touchend", function (e) {
  if (e.target == canvas) {
    e.preventDefault();
  }
}, false);
document.body.addEventListener("touchmove", function (e) {
  if (e.target == canvas) {
    e.preventDefault();
  }
}, false);


resize();


function resize() {
  ctx.canvas.width = 28*10;
  ctx.canvas.height = 28*10;
}
function reposition(event) {
  x = event.clientX - canvas.offsetLeft;
  y = event.clientY - canvas.offsetTop;
}
function start(event) {
  document.addEventListener("mousemove", draw);
  reposition(event);
}
function stop(event) {
  document.removeEventListener("mousemove", draw);
}


function draw(event) {
  ctx.beginPath();
  ctx.lineWidth = 10;
  ctx.lineCap = "round";
  ctx.strokeStyle = "white";
  ctx.moveTo(x, y);
  reposition(event);
  ctx.lineTo(x, y);
  ctx.stroke();
}

function enviarApi(){
    d3.select("#respuesta").attr("style","visibility:visible")

    let imagen_64 = canvas.toDataURL()
    console.log("Imagen base64:",imagen_64)
    d3.json("/api",{
        method:"POST",
        body:JSON.stringify({
            imagen:imagen_64
        }), 
        headers:{
            "Content-type":"application/json"
        }})
        .then(json=>{
            console.log(json)
            d3.select("#respuesta").text(`Estimación: ${json.etiqueta}`)
        })

}
