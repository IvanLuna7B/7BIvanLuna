from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector

# Configuración de la conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

# Página principal
@app.route("/")
def index():
    return render_template("App.html")

# Ruta para ver la lista de contactos registrados
@app.route("/contactos")
def contactos():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_contacto ORDER BY id_Contacto DESC")
    registros = cursor.fetchall()

    return render_template("app.html", registros=registros)

# Ruta para obtener un contacto específico para edición
@app.route("/contactos/<int:id>/editar")
def editarContacto(id):
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_contacto WHERE id_Contacto = %s", (id,))
    contacto = cursor.fetchone()

    return jsonify({
        "id": contacto[0],
        "correo": contacto[1],
        "nombre": contacto[2],
        "asunto": contacto[3]
    })

# Ruta para actualizar un contacto existente
@app.route("/contactos/actualizar/<int:id>", methods=["POST"])
def actualizarContacto(id):
    if not con.is_connected():
        con.reconnect()

    nombre = request.form["nombre"]
    asunto = request.form["asunto"]

    cursor = con.cursor()
    sql = "UPDATE tst0_contacto SET Nombre = %s, Asunto = %s WHERE id_Contacto = %s"
    val = (nombre, asunto, id)
    cursor.execute(sql, val)

    con.commit()

    pusher_client = pusher.Pusher(
        app_id='1872732',
        key='f02935829e1f1f02e7a1',
        secret='34625fc852703cc297ae',
        cluster='us2',
        ssl=True
    )
    pusher_client.trigger('my-channel', 'my-event', {'message': 'Contacto actualizado'})

    return f"Contacto {id} actualizado con éxito"

# Ruta para buscar contactos en la base de datos
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_contacto ORDER BY id_Contacto DESC")
    registros = cursor.fetchall()
    con.close()

    return jsonify(registros)

if __name__ == "__main__":
    app.run(debug=True)
