# python.exe -m venv .venv
# cd .venv/Scripts
# activate.bat
# py -m ensurepip --upgrade
# pip install -r requirements.txt

from flask import Flask

from flask import render_template
from flask import request
from flask import jsonify, make_response
from equipos_service import equipos_bp 

import mysql.connector
import pusher
import datetime
import pytz

from flask_cors import CORS, cross_origin

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_23005014_bd",
    user="u760464709_23005014_usr",
    password="B|7k3UPs3&P"
)

app = Flask(__name__)
CORS(app)

app.register_blueprint(equipos_bp)

def pusherIntegrantes():
    pusher_client = pusher.Pusher(
        app_id='2048639',
        key='85576a197a0fb5c211de',
        secret='bbd4afc18e15b3760912',
        cluster='us2',
        ssl=True
    )
    pusher_client.trigger('integranteschannel', 'integrantesevent', {'message': 'hello Integrantes'})
    return make_response(jsonify({}))

def pusherEquiposIntegrantes():
    pusher_client = pusher.Pusher(
        app_id='2048639',
        key='85576a197a0fb5c211de',
        secret='bbd4afc18e15b3760912',
        cluster='us2',
        ssl=True
    )
    pusher_client.trigger('equiposIntegranteschannel', 'equiposIntegrantesevent', {'message': 'hello Equipos Integrantes'})
    return make_response(jsonify({}))

def pusherEquipos():
    pusher_client = pusher.Pusher(
        app_id='2048639',
        key='85576a197a0fb5c211de',
        secret='bbd4afc18e15b3760912',
        cluster='us2',
        ssl=True
    )
    pusher_client.trigger('equiposchannel', 'equiposevent', {'message': 'hello Equipos'})
    return make_response(jsonify({}))

def pusherProyectos():
    pusher_client = pusher.Pusher(
        app_id='2048639',
        key='85576a197a0fb5c211de',
        secret='bbd4afc18e15b3760912',
        cluster='us2',
        ssl=True
    )
    pusher_client.trigger('proyectoschannel', 'proyectosevent', {'message': 'hello Proyectos'})
    return make_response(jsonify({}))

def pusherProyectosAvances():
    pusher_client = pusher.Pusher(
        app_id='2048639',
        key='85576a197a0fb5c211de',
        secret='bbd4afc18e15b3760912',
        cluster='us2',
        ssl=True
    )
    pusher_client.trigger('proyectosAvanceschannel', 'proyectosAvancesevent', {'message': 'hello Proyectos Avances'})
    return make_response(jsonify({}))

@app.route("/")
def index():
    if not con.is_connected():
        con.reconnect()
    con.close()

    return render_template("index.html")

@app.route("/app")
def app2():
    if not con.is_connected():
        con.reconnect()
    con.close()

    return render_template("login.html")

@app.route("/iniciarSesion", methods=["POST"])
def iniciarSesion():
    if not con.is_connected():
        con.reconnect()

    usuario    = request.form["txtUsuario"].strip()
    contrasena = request.form["txtContrasena"].strip()

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT IdUsuario
    FROM usuarios
    
    WHERE Nombre = %s 
    AND Contrasena = %s
    """
    val = (usuario, contrasena)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

#   Rutas  De  Integrantes    
@app.route("/integrantes")
def integrantes():
    
    return render_template("integrantes.html")

@app.route("/tbodyIntegrantes")
def tbodyProductos():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT idIntegrante,
           nombreIntegrante

    FROM integrantes

    ORDER BY idIntegrante DESC
    LIMIT 10 OFFSET 0
    """

    cursor.execute(sql)
    registros = cursor.fetchall()
    
    return render_template("tbodyIntegrantes.html", integrantes=registros)

@app.route("/integrantes/buscar", methods=["GET"])
def buscarIntegrantes():
    if not con.is_connected():
        con.reconnect()

    args     = request.args
    busqueda = args["busqueda"]
    busqueda = f"%{busqueda}%"

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT idIntegrante,
           nombreIntegrante

    FROM integrantes

    WHERE nombreIntegrante LIKE %s

    ORDER BY idIntegrante DESC
    LIMIT 10 OFFSET 0
    """
    val = (busqueda,)

    try:
        cursor.execute(sql, val)
        registros = cursor.fetchall()

    except mysql.connector.errors.ProgrammingError as error:
        print(f"Ocurrió un error de programación en MySQL: {error}")
        registros = []

    finally:
        con.close()

    return make_response(jsonify(registros))


@app.route("/integrante", methods=["POST"])
def guardarIntegrante():
    if not con.is_connected():
        con.reconnect()

    idIntegrante = request.form["idIntegrante"]
    nombreIntegrante = request.form["nombreIntegrante"]

    cursor = con.cursor()

    if idIntegrante:
        sql = """
        UPDATE integrantes
        SET nombreIntegrante = %s
        WHERE idIntegrante = %s
        """
        val = (nombreIntegrante, idIntegrante)
    else:
        sql = """
        INSERT INTO integrantes (nombreIntegrante)
        VALUES (%s)
        """
        val = (nombreIntegrante,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    pusherIntegrantes()
    return make_response(jsonify({"mensaje": "Integrante guardado"}))




@app.route("/integrante/<int:id>")
def editarIntegrante(id):
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql = """
    
    SELECT idIntegrante, nombreIntegrante
    
    FROM integrantes
    
    WHERE idIntegrante = %s
    """
    val = (id,)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))


@app.route("/integrante/eliminar", methods=["POST"])
def eliminarIntegrante():
    if not con.is_connected():
        con.reconnect()

    id = request.form.get("id")

    cursor = con.cursor(dictionary=True)
    sql = """
    DELETE FROM integrantes 
    WHERE idIntegrante = %s
    """
    
    val = (id,)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    pusherIntegrantes()
    return make_response(jsonify({"mensaje": "Integrante eliminado"}))

@app.route("/proyectos/lista")
def listaProyectos():
    try:
        if not con.is_connected():
            con.reconnect()

        cursor = con.cursor(dictionary=True)
        sql = """
        SELECT idProyecto, tituloProyecto
        FROM proyectos
        ORDER BY tituloProyecto ASC
        """
        cursor.execute(sql)
        proyectos = cursor.fetchall()
        con.close()
        
        return make_response(jsonify(proyectos))
        
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
#   Rutas  De  Proyectos Avances    
@app.route("/proyectosavances")
def proyectosavances():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    # Traer proyectos para el select
    sql = """
    SELECT idProyecto, tituloProyecto
    FROM proyectos
    ORDER BY tituloProyecto ASC
    """
    cursor.execute(sql)
    proyectos = cursor.fetchall()
    con.close()

    # Mandamos también los proyectos para el select
    return render_template("proyectosavances.html", proyectos=proyectos)


@app.route("/tbodyProyectosAvances")
def tbodyProyectosAvances():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql = """
    SELECT pa.idProyectoAvance,
           pa.progreso,
           pa.descripcion,
           pa.fechaHora,
           p.tituloProyecto
    FROM proyectosavances pa
    INNER JOIN proyectos p ON pa.idProyecto = p.idProyecto
    ORDER BY pa.idProyectoAvance DESC
    LIMIT 10 OFFSET 0
    """
    cursor.execute(sql)
    registros = cursor.fetchall()
    con.close()
    
    return render_template("tbodyProyectosAvances.html", proyectosavances=registros)


@app.route("/proyectoavance", methods=["POST"])
def guardarProyectoAvance():
    if not con.is_connected():
        con.reconnect()

    idProyectoAvance = request.form.get("idProyectoAvance")
    idProyecto       = request.form.get("idProyecto")   # 👈 debe coincidir con el name del select
    progreso         = request.form.get("txtProgreso")
    descripcion      = request.form.get("txtDescripcion")

    cursor = con.cursor()

    if idProyectoAvance:  # Update
        sql = """
        UPDATE proyectosavances
        SET idProyecto = %s,
            progreso   = %s,
            descripcion = %s,
            fechaHora = NOW()
        WHERE idProyectoAvance = %s
        """
        val = (idProyecto, progreso, descripcion, idProyectoAvance)
    else:  # Insert
        sql = """
        INSERT INTO proyectosavances (idProyecto, progreso, descripcion, fechaHora)
        VALUES (%s, %s, %s, NOW())
        """
        val = (idProyecto, progreso, descripcion)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    pusherProyectosAvances()
    return make_response(jsonify({"mensaje": "Proyecto Avance guardado"}))


@app.route("/proyectoavance/eliminar", methods=["POST"])
def eliminarProyectoAvance():
    if not con.is_connected():
        con.reconnect()

    id = request.form.get("id")

    cursor = con.cursor(dictionary=True)
    sql = """
    DELETE FROM proyectosavances 
    WHERE idProyectoAvance = %s
    """
    val = (id,)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    pusherProyectosAvances()
    return make_response(jsonify({"mensaje": "Proyecto Avance eliminado"}))

#/////////////////////Equipos/////////////////////////////
  
#/// Lo borre pk no se comentar

#////////////////////////////////////////////////////    


@app.route("/proyectos")
def proyectos():
    return render_template("proyectos.html")

@app.route("/tbodyProyectos")
def tbodyProyectos():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT 
            p.idProyecto,
            p.tituloProyecto,
            e.nombreEquipo,
            p.objetivo,
            p.estado

    FROM proyectos AS p

    INNER JOIN equipos AS e
            ON p.idEquipo = e.idEquipo
    
    ORDER BY p.estado DESC

    LIMIT 10 OFFSET 0
    """

    cursor.execute(sql)
    registros = cursor.fetchall()
    
    return render_template("tbodyProyectos.html", proyectos=registros)

@app.route("/proyectos/buscar", methods=["GET"])
def buscarProyectos():
    if not con.is_connected():
        con.reconnect()

    args     = request.args
    busqueda = args["busqueda"]
    busqueda = f"%{busqueda}%"

    cursor = con.cursor(dictionary=True)
    sql    = """

    SELECT p.idProyecto, p.tituloProyecto, p.objetivo, p.estado
    FROM proyectos AS p
    INNER JOIN equipos AS e ON p.idEquipo = e.idEquipo
    WHERE p.tituloProyecto LIKE %s    -- FALTA ESTA LÍNEA
    ORDER BY p.estado DESC
    LIMIT 10 OFFSET 0
    
    """
    val = (busqueda,)

    try:
        cursor.execute(sql, val)
        registros = cursor.fetchall()

    except mysql.connector.errors.ProgrammingError as error:
        print(f"Ocurrió un error de programación en MySQL: {error}")
        registros = []

    finally:
        con.close()

    return make_response(jsonify(registros))

@app.route("/proyectos", methods=["POST"])
def guardarProyectos():
    if not con.is_connected():
        con.reconnect()

    idProyecto = request.form["idProyecto"]
    tituloProyecto = request.form["tituloProyecto"]
    idEquipo = request.form["idEquipo"]
    objetivo = request.form["objetivo"]
    estado = request.form["estado"]
    
    cursor = con.cursor()

    if idProyecto:
        sql = """
        UPDATE proyectos
        SET tituloProyecto = %s,
            idEquipo = %s,
            objetivo = %s,
            estado = %s
        WHERE idProyecto = %s
        """
        val = (tituloProyecto, idEquipo, objetivo, estado, idProyecto)
    else:
        sql = """
        INSERT INTO proyectos (tituloProyecto, idEquipo, objetivo, estado)
        VALUES (%s, %s, %s, %s)
        """
        val = (tituloProyecto, idEquipo, objetivo, estado)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    pusherProyectos()
    return make_response(jsonify({"mensaje": "Proyecto guardado"}))

############# Eliminar
@app.route("/proyectos/eliminar", methods=["POST"])
def eliminarProyecto():
    if not con.is_connected():
        con.reconnect()

    id = request.form["id"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    DELETE FROM proyectos
    WHERE idProyecto = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({}))



#//////////////esta wea me trae una lista pal inerjoin //////////////////////////////////////////////////////////
@app.route("/equipos/lista")
def cargarEquipos():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql = """
    SELECT idEquipo, nombreEquipo
    FROM equipos
    ORDER BY nombreEquipo ASC
    """
    
    cursor.execute(sql)
    registros = cursor.fetchall()
    con.close()
    
    return make_response(jsonify(registros))
#/////////////////////////////////////////////////////////equiposintegrante///////////////////////////////////////
@app.route("/equiposintegrantes")
def equiposintegrantes():
    return render_template("equiposintegrantes.html")


@app.route("/tbodyequiposintegrantes")
def tbodyequiposintegrantes():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql = """
    SELECT
    ei.idEquipoIntegrante,
    e.idEquipo,
    i.idIntegrante,
    e.nombreEquipo,
    i.nombreIntegrante,
    ei.fechaUnion
FROM equiposintegrantes AS ei
INNER JOIN equipos AS e ON ei.idEquipo = e.idEquipo
INNER JOIN integrantes AS i ON ei.idIntegrante = i.idIntegrante
ORDER BY ei.fechaUnion DESC
LIMIT 10 OFFSET 0;

     
    """
    cursor.execute(sql)
    registros = cursor.fetchall()
    con.close()

    return render_template("tbodyequiposintegrantes.html", equiposintegrantes=registros)


@app.route("/productos/buscar", methods=["GET"])
def buscarProductos():
    if not con.is_connected():
        con.reconnect()

    args     = request.args
    busqueda = args["busqueda"]
    busqueda = f"%{busqueda}%"
    
    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT Id_Producto,
           Nombre_Producto,
           Precio,
           Existencias

    FROM productos

    WHERE Nombre_Producto LIKE %s
    OR    Precio          LIKE %s
    OR    Existencias     LIKE %s

    ORDER BY Id_Producto DESC

    LIMIT 10 OFFSET 0
    """
    val    = (busqueda, busqueda, busqueda)

    try:
        cursor.execute(sql, val)
        registros = cursor.fetchall()

        # Si manejas fechas y horas
        """
        for registro in registros:
            fecha_hora = registro["Fecha_Hora"]

            registro["Fecha_Hora"] = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
            registro["Fecha"]      = fecha_hora.strftime("%d/%m/%Y")
            registro["Hora"]       = fecha_hora.strftime("%H:%M:%S")
        """

    except mysql.connector.errors.ProgrammingError as error:
        print(f"Ocurrió un error de programación en MySQL: {error}")
        registros = []

    finally:
        con.close()

    return make_response(jsonify(registros))

@app.route("/producto", methods=["POST"])
# Usar cuando solo se quiera usar CORS en rutas específicas
# @cross_origin()
def guardarProducto():
    if not con.is_connected():
        con.reconnect()

    id          = request.form["id"]
    nombre      = request.form["nombre"]
    precio      = request.form["precio"]
    existencias = request.form["existencias"]
    # fechahora   = datetime.datetime.now(pytz.timezone("America/Matamoros"))
    
    cursor = con.cursor()

    if id:
        sql = """
        UPDATE productos

        SET Nombre_Producto = %s,
            Precio          = %s,
            Existencias     = %s

        WHERE Id_Producto = %s
        """
        val = (nombre, precio, existencias, id)
    else:
        sql = """
        INSERT INTO productos (Nombre_Producto, Precio, Existencias)
                    VALUES    (%s,          %s,      %s)
        """
        val =                 (nombre, precio, existencias)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    pusherProductos()
    
    return make_response(jsonify({}))

@app.route("/producto/<int:id>")
def editarProducto(id):
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT Id_Producto, Nombre_Producto, Precio, Existencias

    FROM productos

    WHERE Id_Producto = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/producto/eliminar", methods=["POST"])
def eliminarProducto():
    if not con.is_connected():
        con.reconnect()

    id = request.form["id"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    DELETE FROM productos
    WHERE Id_Producto = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({}))

if __name__ == "__main__":
    app.run(debug=True, port=5000)






