from flask import Flask, render_template, request

app = Flask(__name__)
################## LOGIQUE METIER #################################
# Fonction pour additionner deux nombres
def add(x, y):
    return x + y

# Fonction pour soustraire deux nombres
def subtract(x, y):
    return x - y

# Fonction pour multiplier deux nombres
def multiply(x, y):
    return x * y

# Fonction pour diviser deux nombres
def divide(x, y):
    if y == 0:
        return "Erreur! Division par zéro."
    return x / y
################## FIN DE LOGIQUE METIER #################################


# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour la calculatrice
@app.route('/calculatrice')
def calculatrice():
    return render_template('calculatrice.html')

# Route pour effectuer les calculs
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operation = request.form['operation']

        if operation == 'add':  
            result = add(num1, num2)
        elif operation == 'subtract':
            result = subtract(num1, num2)
        elif operation == 'multiply':
            result = multiply(num1, num2)
        elif operation == 'divide':
            result = divide(num1, num2)
        else:
            result = "Opération invalide."
    except ValueError:
        result = "Erreur! Veuillez entrer des nombres valides."

    return render_template('calculatrice.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
