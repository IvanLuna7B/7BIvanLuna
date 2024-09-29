from flask import Flask, render_template, request
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
    return render_template("App.html")  # Asegúrate de que sea el nombre correcto

# Ruta para ver la lista de contactos registrados
@app.route("/contactos")
def contactos():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_contacto ORDER BY id_Contacto DESC")
    registros = cursor.fetchall()
    con.close()

    # Regresamos los registros de contactos para mostrarlos en la plantilla app.html
    return render_template("app.html", registros=registros)

# Ruta para guardar un nuevo contacto en la base de datos
@app.route("/contactos/guardar", methods=["POST"])
def contactosGuardar():
    if not con.is_connected():
        con.reconnect()

    # Se extraen los datos del formulario enviado por POST
    correo = request.form["txtCorreoElectronico"]
    nombre = request.form["txtNombre"]
    asunto = request.form["txtAsunto"]

    cursor = con.cursor()

    # Sentencia SQL para insertar un nuevo contacto
    sql = "INSERT INTO tst0_contacto (Correo_Electronico, Nombre, Asunto) VALUES (%s, %s, %s)"
    val = (correo, nombre, asunto)
    cursor.execute(sql, val)

    con.commit()
    con.close()

    # Activar el evento Pusher para notificar del nuevo contacto
    pusher_client = pusher.Pusher(
        app_id='1872732',
        key='f02935829e1f1f02e7a1',
        secret='34625fc852703cc297ae',
        cluster='us2',
        ssl=True
    )
    pusher_client.trigger('my-channel', 'my-event', {'message': 'Nuevo contacto registrado'})

    return f"Contacto guardado: {nombre}, Correo: {correo}, Asunto: {asunto}"

# Ruta para buscar contactos en la base de datos
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_contacto ORDER BY id_Contacto DESC")
    registros = cursor.fetchall()
    con.close()

    return registros

# Ruta para registrar un nuevo contacto usando parámetros GET
@app.route("/contactos/registrar", methods=["GET"])
def registrar():
    args = request.args

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()

    # Inserción del contacto usando los argumentos de la URL
    sql = "INSERT INTO tst0_contacto (Correo_Electronico, Nombre, Asunto) VALUES (%s, %s, %s)"
    val = (args.get("correo"), args.get("nombre"), args.get("asunto"))
    cursor.execute(sql, val)

    con.commit()
    con.close()

    # Activar el evento Pusher para notificar del nuevo contacto
    pusher_client = pusher.Pusher(
        app_id='1872732',
        key='f02935829e1f1f02e7a1',
        secret='34625fc852703cc297ae',
        cluster='us2',
        ssl=True
    )
    pusher_client.trigger('my-channel', 'my-event', {'message': 'Nuevo contacto registrado'})

    return f"Nuevo contacto registrado: {args.get('nombre')} - {args.get('correo')}"

if __name__ == "__main__":
    app.run(debug=True)
