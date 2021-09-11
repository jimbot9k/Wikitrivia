const URL = "http://localhost:5000";
const playerName = document.cookie.split(';')[0].split('=')[1]
const roomID = document.cookie.split(';')[1].split('=')[1]
var socket = io(URL, { autoConnect: false });
console.log(playerName + " " + roomID)

socket.onAny((event, ...args) => {
    console.log(event, args);
});

function updateQuestion() {

}

function updatePlayers() {

}

function sendAnswer() {

}

function createGame() {

}

function joinGame() {
    const msg = {roomID:roomID, playerName:playerName}
    socket.emit('joinGame', msg)
}

function endRound() {

}
 

socket.connect();
socket.on
joinGame()


