from flask import Flask, render_template, request, redirect, url_for,session
import sqlite3

#Libreria para la gestion de los has en passwords
from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps

app = Flask(__name__)

# Conexión a la base de datos
#
def init_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    #Tabla ususario
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """
    )

    # Tabla de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            direccion TEXT
        )
        ''')

    # Tabla de mascotas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mascotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            especie TEXT,
            raza TEXT,
            edad INTEGER,
            id_cliente INTEGER,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id)
        )
        ''')

    # Tabla de citas (para consultas médicas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            motivo TEXT,
            id_cliente INTEGER,
            id_mascota INTEGER,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id),
            FOREIGN KEY (id_mascota) REFERENCES mascotas(id)
        )
        ''')

    # Tabla de peluquería
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS peluqueria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            servicio TEXT,
            precio REAL,
            id_mascota INTEGER,
            fecha TEXT,
            FOREIGN KEY (id_mascota) REFERENCES mascotas(id)
        )
        ''')

    # Tabla de productos (artículos, comidas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            categoria TEXT,
            cantidad INTEGER,
            precio REAL
        )
        ''')

    conn.commit()
    conn.close()

init_database()
#########################################################
"""
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
    
@app.route("/")
def inde():
    return render_template("inde.html")

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST':
        nombre =  request.form['nombre']
        username = request.form['username']
        password = request.form['password']
        # Encriptar el password
        password_encriptado =  generate_password_hash(password)
        # Almacenar en la base de datos
        conn =  sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre,username,password) VALUES (?,?,?)",(nombre, username,password_encriptado))
        conn.commit()
        conn.close()
        return redirect("/login")
        
    return render_template('auth/register.html')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn =  sqlite3.connect("database.db")
        # Permite obtener registros como diccionario
        conn.row_factory =  sqlite3.Row
        cursor =  conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = ?",(username,))
        usuario = cursor.fetchone()
        conn.close()
        
        if usuario and check_password_hash(usuario['password'],password):
            session['user_id'] = usuario['id']
            return redirect('/admin/dashboard')
                
    return render_template('auth/login.html')
    
@app.route("/logout")
def logout():
    session.pop('user_id',None)
    return redirect("/")



"""
#########################################################
# Ruta principal: Mostrar clientes
@app.route('/')
def index():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return render_template('index.html', clientes=clientes)

# Ruta para agregar un cliente
@app.route('/agregar_cliente', methods=['GET', 'POST'])
def agregar_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']

        #conn = obtener_conexion()
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nombre, telefono, direccion)
            VALUES (?, ?, ?)
        ''', (nombre, telefono, direccion))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('agregar_cliente.html')
#mostrar mascota
# 
@app.route('/mascota')
def mascota():
    #conn = obtener_conexion()
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mascotas")
    servicios = cursor.fetchall()
    conn.close()
    return render_template('mascota.html', servicios=servicios)

# Ruta para agregar una mascota
@app.route('/agregar_mascota', methods=['GET', 'POST'])
def agregar_mascota():
    if request.method == 'POST':
        nombre = request.form['nombre']
        especie = request.form['especie']
        raza = request.form['raza']
        edad = request.form['edad']
        id_cliente = request.form['id_cliente']

        #conn = obtener_conexion()
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mascotas (nombre, especie, raza, edad, id_cliente)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, especie, raza, edad, id_cliente))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('agregar_mascota.html')

# Ruta para mostrar peluquería
@app.route('/peluqueria')
def peluqueria():
    #conn = obtener_conexion()
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM peluqueria")
    servicios = cursor.fetchall()
    conn.close()
    return render_template('peluqueria.html', servicios=servicios)

# Ruta para agregar servicio de peluquería
@app.route('/agregar_peluqueria', methods=['GET', 'POST'])
def agregar_peluqueria():
    if request.method == 'POST':
        servicio = request.form['servicio']
        precio = request.form['precio']
        id_mascota = request.form['id_mascota']
        fecha = request.form['fecha']

        #conn = obtener_conexion()
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO peluqueria (servicio, precio, id_mascota, fecha)
            VALUES (?, ?, ?, ?)
        ''', (servicio, precio, id_mascota, fecha))
        conn.commit()
        conn.close()
        return redirect(url_for('peluqueria'))
    return render_template('agregar_peluqueria.html')

# Ruta para ver inventario (productos)
@app.route('/inventario')
def inventario():
    #conn = obtener_conexion()
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template('inventario.html', productos=productos)

# Ruta para agregar un producto (artículos, comida, etc.)
@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        #conn = obtener_conexion()
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, categoria, cantidad, precio)
            VALUES (?, ?, ?, ?)
        ''', (nombre, categoria, cantidad, precio))
        conn.commit()
        conn.close()
        return redirect(url_for('inventario'))
    return render_template('agregar_producto.html')

# Ruta para mostrar los servicios médicos
@app.route('/servicios_medicos')
def servicios_medicos():
    #conn = obtener_conexion()
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM citas")
    citas = cursor.fetchall()
    conn.close()
    return render_template('servicios_medicos.html', citas=citas)

# Ruta para agregar una cita médica
@app.route('/agregar_cita', methods=['GET', 'POST'])
def agregar_cita():
    if request.method == 'POST':
        fecha = request.form['fecha']
        motivo = request.form['motivo']
        id_cliente = request.form['id_cliente']
        id_mascota = request.form['id_mascota']

        #conn = obtener_conexion()
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO citas (fecha, motivo, id_cliente, id_mascota)
            VALUES (?, ?, ?, ?)
        ''', (fecha, motivo, id_cliente, id_mascota))
        conn.commit()
        conn.close()
        return redirect(url_for('servicios_medicos'))
    return render_template('agregar_cita.html')

if __name__ == '__main__':
    app.run(debug=True)