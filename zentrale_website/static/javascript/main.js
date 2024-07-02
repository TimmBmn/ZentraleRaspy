const socket = new WebSocket("ws://localhost:8765");

socket.addEventListener("open", (event) => {
    console.log("open");
    socket.send(JSON.stringify({"type": "connect"}));
});


socket.addEventListener("message", (event) => {
    console.log(event.data);
});

socket.addEventListener("close", (event) => {
    console.log("close");
});
