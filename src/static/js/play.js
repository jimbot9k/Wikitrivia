const URL = "http://localhost:5000";
const playerName = document.cookie.split(';')[1].split('=')[1]
const roomID = document.cookie.split(';')[0].split('=')[1]
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
    document.getElementById("playerListText").innerHTML = players;
}

function updateAnswers(answer1, answer2, answer3, answer4, previousAnswer) {
    document.getElementById("answer1").innerHTML = answer1;
    document.getElementById("answer2").innerHTML = answer2;
    document.getElementById("answer3").innerHTML = answer3;
    document.getElementById("answer4").innerHTML = answer4;
    document.getElementById("previousAnswer").innerHTML = "Previous Answer: " + previousAnswer;

}

function endRound(roomID) {
    console.log("end pls")
    const questionSets = document.getElementById("questionTypes")
    const questionSet = questionSets.options[questionSets.selectedIndex].value;
    const msg = {roomID:roomID, questionSet:questionSet};
    socket.emit("endRound", msg);
}

function sendAnswer(roomID, playerName, option) {
    const msg = {roomID:roomID, playerName:playerName, answer:option};
    socket.emit("sendAnswer", msg);
}

function getPlayers(roomID) {
    const msg = {roomID:roomID};
    response = socket.emit("getPlayers", msg);
}

function createGame(playerName, roomID) {
    const msg = {roomID:roomID, playerName:playerName};
    console.log(msg)
    socket.emit("createGame", msg);
}

function joinGame(playerName, roomID) {
    const msg = {roomID:roomID, playerName:playerName};
    socket.emit("joinGame", msg);
}

function initialise(type, playerName, roomID) {
    console.log(type)
    if (type == "Create") {
        createGame(playerName, roomID);
    } else if (type == "Join") {
        joinGame(playerName, roomID);
    }
}

socket.connect();
console.log(type)
initialise(type, playerName, roomID)

socket.on("updatePlayers", (data) => {
    newPlayers = JSON.parse(data)['players']
    updatePlayers(newPlayers)
});

socket.on("updateQuestion", (data) => {
    question = JSON.parse(data)['question']
    answer1 = JSON.parse(data)['answer1']
    answer2 = JSON.parse(data)['answer2']
    answer3 = JSON.parse(data)['answer3']
    answer4 = JSON.parse(data)['answer4']
    previousAnswer = JSON.parse(data)['previousAnswer']

    updateQuestion(question)
    updateAnswers(answer1, answer2, answer3, answer4, previousAnswer)
});






