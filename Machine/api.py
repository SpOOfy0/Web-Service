from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import eventlet

# Initialiser l'application Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Dictionnaire pour stocker les robots connectés
robots = {}

# Route pour afficher la page HTML
@app.route('/')
def index():
    return render_template('index.html')

# Route pour gérer la soumission du message via HTTP GET
@app.route('/send_message', methods=['GET'])
def send_message():
    robot_id = request.args.get('robot_id')
    message = request.args.get('message')

    # Envoyer un message spécifique à un robot via Socket.IO
    if robot_id in robots:
        socketio.emit('server_to_robot', {'message': message}, room=robots[robot_id])
        return f"Message envoyé au robot {robot_id}: {message}"
    else:
        return f"Robot {robot_id} non connecté", 404

# Socket.IO: Quand un robot se connecte
@socketio.on('connect_robot')
def connect_robot(data):
    robot_id = data['robot_id']
    robots[robot_id] = request.sid  # Associer l'ID du robot à son identifiant de session
    join_room(request.sid)  # Le robot rejoint une salle spécifique
    print(f"Robot {robot_id} connecté")

# Socket.IO: Quand un robot envoie un message de confirmation
@socketio.on('robot_response')
def robot_response(data):
    robot_id = data['robot_id']
    message = data['message']
    print(f"Réponse du robot {robot_id}: {message}")

# Socket.IO: Quand un robot se déconnecte
@socketio.on('disconnect')
def on_disconnect():
    for robot_id, sid in list(robots.items()):
        if sid == request.sid:
            print(f"Robot {robot_id} déconnecté")
            del robots[robot_id]
            break

if __name__ == '__main__':
    # Utilisation d'eventlet pour exécuter le serveur Socket.IO
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
