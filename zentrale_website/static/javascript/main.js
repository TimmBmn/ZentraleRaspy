// const socket = new WebSocket("ws://127.0.0.1:6000");
const socket = new WebSocket("ws://localhost:6000");

socket.addEventListener("open", (event) => {
    socket.send("Hello Server!");
    console.log("open");
});

socket.addEventListener("message", (event) => {
    console.log(event.data);
});