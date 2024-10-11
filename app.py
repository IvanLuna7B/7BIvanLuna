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

# Ruta para guardar un nuevo contacto en la base de datos
@app.route("/contactos/guardar", methods=["POST"])
def contactosGuardar():
    if not con.is_connected():
        con.reconnect()

    correo = request.form["txtCorreoElectronico"]
    nombre = request.form["txtNombre"]
    asunto = request.form["txtAsunto"]

    cursor = con.cursor()
    sql = "INSERT INTO tst0_contacto (Correo_Electronico, Nombre, Asunto) VALUES (%s, %s, %s)"
    val = (correo, nombre, asunto)
    cursor.execute(sql, val)

    con.commit()

    pusher_client = pusher.Pusher(
        app_id='1872732',
        key='f02935829e1f1f02e7a1',
        secret='34625fc852703cc297ae',
        cluster='us2',
        ssl=True
    )
    pusher_client.trigger('my-channel', 'my-event', {'message': 'Nuevo contacto registrado'})

    return f"Contacto guardado: {nombre}, Correo: {correo}, Asunto: {asunto}"

# Ruta para actualizar un contacto existente
@app.route("/contactos/actualizar/<int:id>", methods=["POST"])
def actualizarContacto(id):
    if not con.is_connected():
        con.reconnect()

    correo = request.form["txtCorreoElectronico"]
    nombre = request.form["txtNombre"]
    asunto = request.form["txtAsunto"]

    cursor = con.cursor()
    sql = "UPDATE tst0_contacto SET Correo_Electronico = %s, Nombre = %s, Asunto = %s WHERE id_Contacto = %s"
    val = (correo, nombre, asunto, id)
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

# Ruta para eliminar un contacto
@app.route("/contactos/eliminar/<int:id>", methods=["POST"])
def eliminarContacto(id):
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "DELETE FROM tst0_contacto WHERE id_Contacto = %s"
    cursor.execute(sql, (id,))

    con.commit()

    pusher_client = pusher.Pusher(
        app_id='1872732',
        key='f02935829e1f1f02e7a1',
        secret='34625fc852703cc297ae',
        cluster='us2',
        ssl=True
    )
    pusher_client.trigger('my-channel', 'my-event', {'message': 'Contacto eliminado'})

    return f"Contacto {id} eliminado con éxito"

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
