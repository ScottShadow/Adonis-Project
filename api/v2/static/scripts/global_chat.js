var socket = io.connect('http://127.0.0.1:5000', { transports: ['websocket'] });
var room_id = "{{ room.id }}";

// Join the global room
socket.emit('join', { room_id: room_id });

// Send message
document.getElementById('chat-form').onsubmit = function (e) {
  e.preventDefault();
  var message = document.getElementById('message-input').value;
  if (message.trim() === '') return;
  socket.emit('message', { room_id: room_id, message: message });
  document.getElementById('message-input').value = '';
};

// Receive message
socket.on('message', function (data) {
  var chatWindow = document.getElementById('chat-window');
  var messageDiv = document.createElement('div');
  messageDiv.className = 'message ' + (data.username === "{{ user.username }}" ? 'self' : 'other');
  messageDiv.innerHTML = '<strong>' + data.username + ': ' + '<em>' + data.created_at + '</em>' + '</strong>' + data.message;
  chatWindow.appendChild(messageDiv);
  chatWindow.scrollTop = chatWindow.scrollHeight;
});
socket.on('status', (data) => {
  var chatWindow = document.getElementById('chat-window');
  var messageDiv = document.createElement('div');
  messageDiv.className = 'message ' + ('other');
  messageDiv.innerHTML = '<strong>' + "System" + ': ' + '<em>' + data.created_at + '</em>' + '</strong>' + data.message;
  chatWindow.appendChild(messageDiv);
  chatWindow.scrollTop = chatWindow.scrollHeight;
});

socket.on('error', function (data) {
  alert(data.message);
});

