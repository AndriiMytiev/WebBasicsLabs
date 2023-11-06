const express = require('express');
const http = require('http');
const {Server} = require('socket.io');
const app = express();
const server = http.createServer(app);
const io = new Server(server);
app.use(express.static(__dirname + '/public'));
app.get('/', function (req, res) {
    res.sendFile(__dirname + '/index.html');
});
let userCounter = 0;
io.on('connection', (socket) => {
    userCounter++;
    const userId = userCounter;
    console.log(`User ${userId} connected`);
    socket.on('chat message', (message) => {
        io.emit('chat message', {userId, message});
    });
    socket.on('disconnect', () => {
        console.log(`User ${userId} disconnected`);
    });
});
server.listen(3000, () => {
    console.log('Server is running on port 3000');
});
