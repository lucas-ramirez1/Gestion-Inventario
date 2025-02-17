from flask import Flask, render_template, request, redirect
import sqlite3
import gestion_inventario

app = Flask(__name__)

@app.route('/')
def ruta_raiz():
    return render_template('index.html')

# Rutas para registrar entidades
@app.route('/registrar_producto', methods=['GET', 'POST'])
def registrar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        id_categoria = int(request.form['id_categoria'])
        gestion_inventario.registrar_producto(nombre, descripcion, precio, stock, id_categoria)
        return redirect('/')
    return render_template('registrar_producto.html')

@app.route('/registrar_categoria', methods=['GET', 'POST'])
def registrar_categoria():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        gestion_inventario.registrar_categoria(nombre, descripcion)
        return redirect('/')
    return render_template('registrar_categoria.html')

@app.route('/registrar_proveedor', methods=['GET', 'POST'])
def registrar_proveedor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        gestion_inventario.registrar_proveedor(nombre, direccion, telefono)
        return redirect('/')
    return render_template('registrar_proveedor.html')

@app.route('/registrar_bodega', methods=['GET', 'POST'])
def registrar_bodega():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ubicacion = request.form['ubicacion']
        capacidad = int(request.form['capacidad'])
        gestion_inventario.registrar_bodega(nombre, ubicacion, capacidad)
        return redirect('/')
    return render_template('registrar_bodega.html')

# Rutas para gestionar stock
@app.route('/gestionar_stock', methods=['GET', 'POST'])
def gestionar_stock():
    if request.method == 'POST':
        operacion = request.form['operacion']
        id_producto = int(request.form['id_producto'])
        cantidad = int(request.form['cantidad'])
        if operacion == 'agregar':
            gestion_inventario.agregar_stock(id_producto, cantidad)
        elif operacion == 'retirar':
            gestion_inventario.retirar_stock(id_producto, cantidad)
        return redirect('/')
    return render_template('gestionar_stock.html')

# Rutas para consultas y reportes
@app.route('/consultar_info', methods=['GET', 'POST'])
def consultar_info():
    if request.method == 'POST':
        tipo_consulta = request.form['tipo_consulta']
        id_entidad = int(request.form['id_entidad'])
        if tipo_consulta == 'producto':
            info = gestion_inventario.consultar_info_producto(id_entidad)
        elif tipo_consulta == 'categoria':
            info = gestion_inventario.consultar_info_categoria(id_entidad)
        elif tipo_consulta == 'proveedor':
            info = gestion_inventario.consultar_info_proveedor(id_entidad)
        elif tipo_consulta == 'bodega':
            info = gestion_inventario.consultar_info_bodega(id_entidad)
        return render_template('consultar_info.html', info=info)
    return render_template('consultar_info.html')

@app.route('/informe_stock')
def informe_stock():
    stock_total, stock_por_categoria, stock_por_proveedor, stock_por_bodega = gestion_inventario.generar_informe_stock()
    return render_template('informe_stock.html', stock_total=stock_total, stock_por_categoria=stock_por_categoria, stock_por_proveedor=stock_por_proveedor, stock_por_bodega=stock_por_bodega)


@app.route('/producto/<int:id>')
def mostrar_producto(id):
    producto = gestion_inventario.consultar_info_producto(id)
    if producto:
        return render_template('producto.html', producto=producto)
    return "Producto no encontrado", 404

@app.route('/categoria/<int:id>')
def mostrar_categoria(id):
    categoria = gestion_inventario.consultar_info_categoria(id)
    if categoria:
        return render_template('categoria.html', categoria=categoria)
    return "Categoría no encontrada", 404

@app.route('/proveedor/<int:id>')
def mostrar_proveedor(id):
    proveedor = gestion_inventario.consultar_info_proveedor(id)
    if proveedor:
        return render_template('proveedor.html', proveedor=proveedor)
    return "Proveedor no encontrado", 404

@app.route('/bodega/<int:id>')
def mostrar_bodega(id):
    bodega = gestion_inventario.consultar_info_bodega(id)
    if bodega:
        return render_template('bodega.html', bodega=bodega)
    return "Bodega no encontrada", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


