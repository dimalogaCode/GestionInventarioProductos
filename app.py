from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1634",  # Cambia esto por tu contraseña de MySQL
    database="Inventario"
)

# Crear cursor para interactuar con la base de datos
cursor = db.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()  # Trae todos los productos de la base de datos
    return render_template('index.html', productos=productos)

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        
        # Ejecutar consulta para insertar nuevo producto
        cursor.execute("INSERT INTO productos (nombre, descripcion, cantidad, precio) VALUES (%s, %s, %s, %s)", 
                       (nombre, descripcion, cantidad, precio))
        db.commit()  # Guardar cambios
        return redirect('/')

@app.route('/actualizar_producto/<int:id>', methods=['GET', 'POST'])
def actualizar_producto(id):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        
        # Actualizar en la base de datos
        cursor = db.cursor()
        cursor.execute("""
            UPDATE productos 
            SET nombre=%s, descripcion=%s, cantidad=%s, precio=%s
            WHERE id=%s
        """, (nombre, descripcion, cantidad, precio, id))
        db.commit()
        cursor.close()

        return redirect('/')
    else:
        # Si el método es GET, renderizar el formulario con los datos actuales del producto
        cursor = db.cursor()
        cursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
        producto = cursor.fetchone()
        cursor.close()

        return render_template('editar_producto.html', producto=producto)
    
    

@app.route('/eliminar_producto/<int:id>')
def eliminar_producto(id):
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    db.commit()  # Guardar cambios
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
