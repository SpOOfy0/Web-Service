from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')  # Charge le template HTML

@socketio.on('submit_code')
def handle_code_submission(data):
    code = data['code']  # Récupère le code soumis
    language = data['language']  # Récupère le langage choisi
    output = execute_code_in_docker(code, language)  # Exécute le code dans Docker
    emit('code_output', {'output': output}, broadcast=True)  # Émet le résultat

def execute_code_in_docker(code, language):
    script_name = ""
    
    # Définit le script et l'image Docker selon le langage
    if language == "python":
        script_name = "script.py"
        with open(script_name, "w") as f:
            f.write(code)
        image_name = "python:3.9"
        command = ["python", script_name]
    elif language == "javascript":
        script_name = "script.js"
        with open(script_name, "w") as f:
            f.write(code)
        image_name = "node:14"
        command = ["node", script_name]
    else:
        return "Langage non supporté."

    try:
        # Exécute le code dans un conteneur Docker
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{os.getcwd()}:/app", "-w", "/app", image_name] + command,
            capture_output=True,
            text=True
        )
        output = result.stdout + result.stderr
    finally:
        os.remove(script_name)  # Supprime le fichier script après l'exécution

    return output

if __name__ == '__main__':  
    socketio.run(app, host='127.0.0.1', port=5000, debug=True, use_reloader=False)  # Lance le serveur
