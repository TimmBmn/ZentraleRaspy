const socket = new WebSocket("ws://localhost:8765");

socket.addEventListener("open", () => {
    console.log("open");
    socket.send(JSON.stringify({"type": "connect"}));
});
socket.addEventListener("close", () => {
    console.log("close");
});


let rooms = {}

socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    console.log(data);

    let room_number = data.room;
    let temperature = data.temp;
    let temp_limit = data.temp_limit;
    let wet = data.wet;

    // wenns ein neuer raum ist
    if (!(room_number in rooms)) {

        let values = create_new_room(room_number);
        rooms[room_number] = {};

        rooms[room_number].entire_div = values[0];
        rooms[room_number].wet_or_dry = values[2];
        rooms[room_number].canvas = new Chart(values[1], {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Temperature',
                    data: [],
                    borderWidth: 1
                }],
            },
                options: {
                    scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }


    add_data_to_chart(rooms[room_number].canvas, temperature);
    if (rooms[room_number].canvas.data.labels.length > 20) {
        remove_data_from_chart(rooms[room_number].canvas);
    }
    
    rooms[room_number].wet_or_dry.innerText = wet ? "Wet" : "Dry";


    if (temperature > temp_limit) {
        rooms[room_number].entire_div.classList.add("alarm");
    } else {
        rooms[room_number].entire_div.classList.remove("alarm");
    }
});


function create_new_room(client_number) {
    let main_box = document.getElementById("main-box");

    let room = document.createElement("div");
    room.classList.add("room");

    let room_number = document.createElement("h2");
    room_number.textContent = client_number;

    let canvas = document.createElement("canvas");

    let room_information = document.createElement("div");
    room_information.classList.add("room-information");

    let room_wet_or_dry = document.createElement("div");
    room_wet_or_dry.classList.add("room-wet-or-dry");

    let shutdown_button = document.createElement("button");
    shutdown_button.classList.add("shutdown-button");
    shutdown_button.innerText = "Shutdown";

    shutdown_button.addEventListener("click", () => {
        console.log("sende bitte meldung")
    });

    room_information.appendChild(room_wet_or_dry);
    room_information.appendChild(shutdown_button);

    room.appendChild(room_number);
    room.appendChild(canvas);
    room.appendChild(room_information);

    main_box.appendChild(room);

    return [room, canvas, room_wet_or_dry];
}

function add_data_to_chart(chart, data) {
    chart.data.labels.push("");
    chart.data.datasets[0].data.push(data);
    chart.update()
}

function remove_data_from_chart(chart) {
    chart.data.labels.shift();
    chart.data.datasets[0].data.shift();
    chart.update();
}

