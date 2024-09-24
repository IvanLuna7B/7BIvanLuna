from flask import Flask, render_template, request

app = Flask(__name__)

# Ruta para la página principal
@app.route("/")
def index():
    return "<p>Hola, Mundo!</p>"

# Ruta para la página de alumnos
@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

# Ruta para guardar los datos de los alumnos (recibe datos por POST)
@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar(): 
    matricula = request.form['txtMatriculaFA']
    nombre_apellido = request.form['txtNombreApellidoFA']
    return f"Matrícula: {matricula}, Nombre y Apellido: {nombre_apellido}"

if __name__ == "__main__":
    app.run(debug=True)
