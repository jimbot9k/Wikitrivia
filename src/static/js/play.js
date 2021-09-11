const URL = "http://localhost:5000";
const playerName = document.cookie.split(';')[0].split('=')[1]
const roomID = document.cookie.split(';')[1].split('=')[1]
const type = document.cookie.split(';')[2].split('=')[1]
const gameRunning = 1


var socket = io(URL, { autoConnect: false });
socket.onAny((event, ...args) => {
    console.log(event, args);
});

function updateQuestion(question) {
    document.getElementById("questionText").innerHTML = question;
}

function updatePlayers(players) {
    document.getElementById("playerList").innerHTML = players;
}

function updateAnswers(answer1, answer2, answer3, answer4) {
    document.getElementById("answer1").innerHTML = answer1;
    document.getElementById("answer2").innerHTML = answer2;
    document.getElementById("answer3").innerHTML = answer3;
    document.getElementById("answer4").innerHTML = answer4;
}

function sendEndRound(roomID, playerName) {
    const msg = {roomID:roomID, playerName:playerName};
    socket.emit('endRound', msg);
}

function sendAnswer(roomID, playerName, option) {
    const msg = {roomID:roomID, playerName:playerName, option:option};
    socket.emit('sendAnswer', msg);
}

function createGame(playerName, roomID) {
    console.log("2")
}

function sendStartGame(playerName, roomID) {
    console.log("2")
}

function startGame(playerName, roomID) {
    console.log("2")
}

function createGame(playerName, roomID) {
    console.log("2")
}

function joinGame(playerName, roomID) {
    const msg = {roomID:roomID, playerName:playerName};
    socket.emit('joinGame', msg);
}

function initialise(type, playerName, roomID) {
    if (type == "create") {
        createGame(playerName, roomID);
    } else if (type == "join") {
        joinGame(playerName, roomID);
    }
}

function lol(){
    updatePlayers("FUCK YEAH");
    updateAnswers("123", "456", "789", "111");
    updateQuestion("Chase Straight?");
}

function endRound() {
    console.log("1");
}


socket.connect();
initialise(type, playerName, roomID)




