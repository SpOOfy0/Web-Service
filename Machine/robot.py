import socketio

# Créer une instance du client Socket.IO
sio = socketio.Client()

# Identifiant unique du robot (il pourrait être généré ou prédéfini)
robot_id = 'robot_123'

# Lorsque le robot se connecte au serveur
@sio.event
def connect():
    print("Robot connecté au serveur")
    # Envoyer l'ID du robot au serveur lors de la connexion
    sio.emit('connect_robot', {'robot_id': robot_id})

# Lorsque le robot reçoit un message du serveur
@sio.on('server_to_robot')
def handle_message(data):
    print(f"Message reçu du serveur: {data['message']}")
    # Envoyer une réponse au serveur
    sio.emit('robot_response', {'robot_id': robot_id, 'message': "Oui, je reçois votre message"})

# Lorsque le robot se déconnecte du serveur
@sio.event
def disconnect():
    print("Robot déconnecté du serveur")

# Se connecter au serveur Flask-SocketIO
sio.connect('http://localhost:5000')

# Démarrer une boucle pour garder la connexion active
sio.wait()
