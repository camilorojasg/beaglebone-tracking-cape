
//Load the TCP Library
net = require('net');
 
//Start a TCP Server
net.createServer(function (socket) {
 
        //Identify this client
        socket.name = socket.remoteAddress + ":" + socket.remotePort
 
        console.log('Tracking Cape connected (' + socket.name + ')\n');

        //Handle incoming messages from clients.
        socket.on('data', function (data) {
                console.log("Tracking Cape> " + data);
        });
 
        socket.on('end', function () {
                console.log("Tracking Cape disconnected.\n");
        });
 
}).listen(5000);
 
console.log("Waiting for BeagleBone Tracking Cape. Port 5000\n");