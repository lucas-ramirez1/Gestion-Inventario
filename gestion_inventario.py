import sqlite3
import os

# Función para crear la base de datos y las tablas
def crear_bd():
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()

    # Crear tabla Producto
    cursor.execute('''CREATE TABLE IF NOT EXISTS Producto (
                        id_producto INTEGER PRIMARY KEY,
                        nombre TEXT,
                        descripcion TEXT,
                        precio REAL,
                        stock INTEGER,
                        id_categoria INTEGER,
                        FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria)
                    )''')

    # Crear tabla Categoria
    cursor.execute('''CREATE TABLE IF NOT EXISTS Categoria (
                        id_categoria INTEGER PRIMARY KEY,
                        nombre TEXT,
                        descripcion TEXT
                    )''')

    # Crear tabla Proveedor
    cursor.execute('''CREATE TABLE IF NOT EXISTS Proveedor (
                        id_proveedor INTEGER PRIMARY KEY,
                        nombre TEXT,
                        direccion TEXT,
                        telefono TEXT
                    )''')

    # Crear tabla Bodega
    cursor.execute('''CREATE TABLE IF NOT EXISTS Bodega (
                        id_bodega INTEGER PRIMARY KEY,
                        nombre TEXT,
                        ubicacion TEXT,
                        capacidad INTEGER
                    )''')

    # Crear tabla ProductoProveedor (relación muchos a muchos entre Producto y Proveedor)
    cursor.execute('''CREATE TABLE IF NOT EXISTS ProductoProveedor (
                        id_proveedor INTEGER,
                        id_producto INTEGER,
                        FOREIGN KEY (id_proveedor) REFERENCES Proveedor(id_proveedor),
                        FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
                        PRIMARY KEY (id_proveedor, id_producto)
                    )''')

    # Crear tabla ProductoBodega (relación muchos a muchos entre Producto y Bodega)
    cursor.execute('''CREATE TABLE IF NOT EXISTS ProductoBodega (
                        id_bodega INTEGER,
                        id_producto INTEGER,
                        cantidad INTEGER,
                        FOREIGN KEY (id_bodega) REFERENCES Bodega(id_bodega),
                        FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
                        PRIMARY KEY (id_bodega, id_producto)
                    )''')

    # Crear tabla InformeStock
    cursor.execute('''CREATE TABLE IF NOT EXISTS InformeStock (
                        id_informe INTEGER PRIMARY KEY,
                        fecha_informe DATE,
                        stock_total INTEGER,
                        stock_categoria TEXT,
                        stock_proveedor TEXT,
                        stock_bodega TEXT
                    )''')

    conn.commit()
    conn.close()

# Función para registrar un producto en la base de datos
def registrar_producto(nombre, descripcion, precio, stock, id_categoria):
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO Producto (nombre, descripcion, precio, stock, id_categoria)
                      VALUES (?, ?, ?, ?, ?)''', (nombre, descripcion, precio, stock, id_categoria))

    conn.commit()
    conn.close()

# Función para registrar una categoría en la base de datos
def registrar_categoria(nombre, descripcion):
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO Categoria (nombre, descripcion)
                      VALUES (?, ?)''', (nombre, descripcion))

    conn.commit()
    conn.close()

# Función para registrar un proveedor en la base de datos
def registrar_proveedor(nombre, direccion, telefono):
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO Proveedor (nombre, direccion, telefono)
                      VALUES (?, ?, ?)''', (nombre, direccion, telefono))

    conn.commit()
    conn.close()

# Función para registrar una bodega en la base de datos
def registrar_bodega(nombre, ubicacion, capacidad):
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO Bodega (nombre, ubicacion, capacidad)
                      VALUES (?, ?, ?)''', (nombre, ubicacion, capacidad))

    conn.commit()
    conn.close()

# Función para agregar stock a un producto existente
def agregar_stock(id_producto, cantidad):
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()

    cursor.execute('''UPDATE Producto
                      SET stock = stock + ?
                      WHERE id_producto = ?''', (cantidad, id_producto))

    conn.commit()
    conn.close()

# Función para retirar stock de un producto existente
def retirar_stock(id_producto, cantidad):
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()

    cursor.execute('''UPDATE Producto
                      SET stock = stock - ?
                      WHERE id_producto = ?''', (cantidad, id_producto))

    conn.commit()
    conn.close()

# Función para calcular el valor total del stock
def calcular_valor_total_stock():
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT SUM(precio * stock)
                      FROM Producto''')
    total_valor_stock = cursor.fetchone()[0]

    conn.close()

    return total_valor_stock

# Función para imprimir los datos de una tabla
def imprimir_tabla(tabla):
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {tabla};")
    rows = cursor.fetchall()

    print(f"\nDatos de la tabla {tabla}:")
    for row in rows:
        print(row)

    conn.close()

#FUNCIONES CORRESPONDIENTES A RELACIONES ENTRE ENTIDADES

def agregar_producto_a_categoria(id_producto, id_categoria):
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''UPDATE Producto
                          SET id_categoria = ?
                          WHERE id_producto = ?''', (id_categoria, id_producto))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error:", e)
        conn.close()
        return False

def eliminar_producto_de_categoria(id_producto):
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''UPDATE Producto
                          SET id_categoria = NULL
                          WHERE id_producto = ?''', (id_producto,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error:", e)
        conn.close()
        return False

def agregar_producto_a_proveedor(id_producto, id_proveedor):
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO ProductoProveedor (id_producto, id_proveedor)
                          VALUES (?, ?)''', (id_producto, id_proveedor))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error:", e)
        conn.close()
        return False

def eliminar_producto_de_proveedor(id_producto, id_proveedor):
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''DELETE FROM ProductoProveedor
                          WHERE id_producto = ? AND id_proveedor = ?''', (id_producto, id_proveedor))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error:", e)
        conn.close()
        return False

def agregar_producto_a_bodega(id_producto, id_bodega, cantidad):
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT SUM(cantidad) FROM ProductoBodega WHERE id_bodega = ?''', (id_bodega,))
        total_cantidad_bodega = cursor.fetchone()[0]
        if total_cantidad_bodega is None:
            total_cantidad_bodega = 0
        cursor.execute('''SELECT capacidad FROM Bodega WHERE id_bodega = ?''', (id_bodega,))
        capacidad_bodega = cursor.fetchone()[0]
        if total_cantidad_bodega + cantidad > capacidad_bodega:
            print("No hay suficiente espacio en la bodega para agregar el producto.")
            return False
        cursor.execute('''INSERT INTO ProductoBodega (id_bodega, id_producto, cantidad)
                          VALUES (?, ?, ?)''', (id_bodega, id_producto, cantidad))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error:", e)
        conn.close()
        return False

def retirar_producto_de_bodega(id_producto, id_bodega, cantidad):
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT cantidad FROM ProductoBodega
                          WHERE id_producto = ? AND id_bodega = ?''', (id_producto, id_bodega))
        cantidad_en_bodega = cursor.fetchone()[0]
        if cantidad_en_bodega >= cantidad:
            cursor.execute('''UPDATE ProductoBodega
                              SET cantidad = cantidad - ?
                              WHERE id_producto = ? AND id_bodega = ?''', (cantidad, id_producto, id_bodega))
            conn.commit()
            conn.close()
            return True
        else:
            print("No hay suficiente cantidad del producto en la bodega.")
            conn.close()
            return False
    except Exception as e:
        print("Error:", e)
        conn.close()
        return False

def consultar_disponibilidad_en_bodega(id_producto, id_bodega):
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT cantidad FROM ProductoBodega
                          WHERE id_producto = ? AND id_bodega = ?''', (id_producto, id_bodega))
        cantidad_en_bodega = cursor.fetchone()
        conn.close()
        if cantidad_en_bodega is None:
            return 0
        else:
            return cantidad_en_bodega[0]
    except Exception as e:
        print("Error:", e)
        conn.close()
        return 0

#CONSULTAS Y REPORTES:

def consultar_info_producto(id_producto):
    conexion = sqlite3.connect('gestion_inventario.db')
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Producto WHERE id_producto = ?", (id_producto,))
    producto = cursor.fetchone()
    conexion.close()
    if producto:
        return dict(producto)
    return None

def consultar_info_categoria(id_categoria):
    conexion = sqlite3.connect('gestion_inventario.db')
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Categoria WHERE id_categoria = ?", (id_categoria,))
    categoria = cursor.fetchone()
    cursor.execute("SELECT * FROM Producto WHERE id_categoria = ?", (id_categoria,))
    productos = [dict(producto) for producto in cursor.fetchall()]
    conexion.close()
    if categoria:
        return {"nombre": categoria["nombre"], "descripcion": categoria["descripcion"], "productos": productos}
    return None

def consultar_info_proveedor(id_proveedor):
    conexion = sqlite3.connect('gestion_inventario.db')
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Proveedor WHERE id_proveedor = ?", (id_proveedor,))
    proveedor = cursor.fetchone()
    cursor.execute("SELECT * FROM ProductoProveedor WHERE id_proveedor = ?", (id_proveedor,))
    productos = [dict(producto) for producto in cursor.fetchall()]
    conexion.close()
    if proveedor:
        return {"nombre": proveedor["nombre"], "direccion": proveedor["direccion"], "telefono": proveedor["telefono"], "productos": productos}
    return None


def consultar_info_bodega(id_bodega):
    conexion = sqlite3.connect('gestion_inventario.db')
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Bodega WHERE id_bodega = ?", (id_bodega,))
    bodega = cursor.fetchone()
    cursor.execute("""
        SELECT p.id_producto, p.nombre, pb.cantidad 
        FROM ProductoBodega pb 
        JOIN Producto p ON pb.id_producto = p.id_producto 
        WHERE pb.id_bodega = ?
    """, (id_bodega,))
    productos_bodega = [dict(producto) for producto in cursor.fetchall()]
    conexion.close()
    if bodega:
        return {"nombre": bodega["nombre"], "ubicacion": bodega["ubicacion"], "capacidad": bodega["capacidad"], "productos": productos_bodega}
    return None

def generar_informe_stock():
    conn = sqlite3.connect('gestion_inventario.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT SUM(stock) FROM Producto''')
    stock_total = cursor.fetchone()[0]
    
    cursor.execute('''SELECT c.nombre, SUM(p.stock)
                      FROM Producto p
                      LEFT JOIN Categoria c ON p.id_categoria = c.id_categoria
                      GROUP BY c.nombre''')
    stock_por_categoria_data = cursor.fetchall()
    stock_por_categoria = {nombre: stock for nombre, stock in stock_por_categoria_data}

    cursor.execute('''SELECT pr.nombre, SUM(p.stock)
                      FROM Producto p
                      LEFT JOIN ProductoProveedor pp ON p.id_producto = pp.id_producto
                      LEFT JOIN Proveedor pr ON pp.id_proveedor = pr.id_proveedor
                      GROUP BY pr.nombre''')
    stock_por_proveedor_data = cursor.fetchall()
    stock_por_proveedor = {nombre: stock for nombre, stock in stock_por_proveedor_data}

    cursor.execute('''SELECT b.nombre, SUM(pb.cantidad)
                      FROM Bodega b
                      LEFT JOIN ProductoBodega pb ON b.id_bodega = pb.id_bodega
                      GROUP BY b.nombre''')
    stock_por_bodega_data = cursor.fetchall()
    stock_por_bodega = {nombre: cantidad for nombre, cantidad in stock_por_bodega_data}

    conn.close()
    return stock_total, stock_por_categoria, stock_por_proveedor, stock_por_bodega



#ESTA FUNCIÓN ELIMINA LA BASE DE DATOS, EL OBJETIVO DE ELLA ES PARA PODER REALIZAR PRUEBAS
def eliminar_bd():
    if os.path.exists('gestion_inventario.db'):
        os.remove('gestion_inventario.db')
        print("Base de datos eliminada con éxito.")
    else:
        print("La base de datos no existe.")

#                               **PROGRAMA PRINCIPAL**

# Eliminar la base de datos si existe
eliminar_bd()

# Crear la base de datos y las tablas
crear_bd()

#                         **PRUEBAS PARA EL CORRECTO USO DE LAS FUNCIONES**

# Verificar si se crearon las tablas imprimiendo sus datos
#imprimir_tabla("Producto")
#imprimir_tabla("Categoria")
#imprimir_tabla("Proveedor")
#imprimir_tabla("Bodega")
#imprimir_tabla("ProductoProveedor")
#imprimir_tabla("ProductoBodega")
#imprimir_tabla("InformeStock")
#print(f"\nTodo lo anterior debe estar vacio.")


# REGISTRO DE ENTIDADES EJEMPLO
#registrar_producto("Producto1", "Descripción del Producto 1", 10.99, 100, 1)
#registrar_categoria("Categoria1", "Descripción de la Categoría 1")
#registrar_proveedor("Proveedor1", "Dirección del Proveedor 1", "123456789")
#registrar_bodega("Bodega1", "Ubicación de la Bodega 1", 1000)

#Verifica si se registro la wea en las tablas:
#imprimir_tabla("Producto")
#imprimir_tabla("Categoria")
#imprimir_tabla("Proveedor")
#imprimir_tabla("Bodega")
#imprimir_tabla("ProductoProveedor")
#imprimir_tabla("ProductoBodega")
#imprimir_tabla("InformeStock")
#print(f"\nEntidades registradas con éxito.")

# GESTIÓN DE STOCK EJEMPLO

#print(f"\nStock INICIAL: ")
#total_valor_stock = calcular_valor_total_stock()
#print(f"El valor total del stock es: {total_valor_stock}")

# Agregar stock a un producto existente
#print(f"\nStock AGREGADO: ")
#agregar_stock(1, 50)
#total_valor_stock = calcular_valor_total_stock()
#print(f"El valor total del stock es: {total_valor_stock}")

# Retirar stock de un producto existente
#print(f"\nStock RETIRADO:")
#retirar_stock(2, 10)
#total_valor_stock = calcular_valor_total_stock()
#print(f"El valor total del stock es: {total_valor_stock}")

# RELACIONES ENTRE ENTIDADES

#Las funciones devolverán un valor específico true/false el cual indica si la operación se hizo con éxito o no.
#a = agregar_producto_a_categoria(1, 1)
#print(a)
#b = eliminar_producto_de_categoria(1)
#print(b)
#c = agregar_producto_a_proveedor(1, 1)
#print(c)
#d = eliminar_producto_de_proveedor(1, 1)
#print(d)
#e = agregar_producto_a_bodega(1, 1, 10)
#print(e)
#f = retirar_producto_de_bodega(1, 1, 10)
#print(f)

#g = consultar_disponibilidad_en_bodega(1, 1)
#print(f"La cantidad en bodega es: {g}")

#CONSULTAS Y REPORTES EJEMPLOS:

# Prueba de consultar_info_producto
#print("Consultar información del producto con ID 1:")
#info_producto = consultar_info_producto(1)
#print(info_producto)

# Prueba de consultar_info_categoria
#print("Consultar información de la categoría con ID 1:")
#info_categoria = consultar_info_categoria(1)
#print(info_categoria)

# Prueba de consultar_info_proveedor
#print("Consultar información del proveedor con ID 1:")
#info_proveedor = consultar_info_proveedor(1)
#print(info_proveedor)

# Prueba de consultar_info_bodega
#print("Consultar información de la bodega con ID 1:")
#info_bodega = consultar_info_bodega(1)
#print(info_bodega)

# Prueba de generar_informe_stock
#print("Generar informe de stock:")
#informe_stock = generar_informe_stock()
#print(informe_stock)