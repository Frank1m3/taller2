from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.proveedor.ProveedorDao import ProveedorDao
from app import csrf  # <-- Importa la instancia creada en tu app

provapi = Blueprint('provapi', __name__)

@provapi.route('/proveedores', methods=['GET'])
def getProveedores():
    dao = ProveedorDao()
    try:
        proveedores = dao.getProveedores()
        return jsonify(success=True, data=proveedores, error=None), 200
    except Exception as e:
        app.logger.error(f"Error al obtener proveedores: {e}")
        return jsonify(success=False, error="Error interno."), 500

@provapi.route('/proveedores/<int:id_proveedor>', methods=['GET'])
def getProveedor(id_proveedor):
    dao = ProveedorDao()
    try:
        proveedor = dao.getProveedorById(id_proveedor)
        if proveedor:
            return jsonify(success=True, data=proveedor, error=None), 200
        return jsonify(success=False, error="Proveedor no encontrado."), 404
    except Exception as e:
        app.logger.error(f"Error al obtener proveedor: {e}")
        return jsonify(success=False, error="Error interno."), 500

@provapi.route('/proveedores', methods=['POST'])
@csrf.exempt
def addProveedor():
    data = request.get_json() or {}
    dao = ProveedorDao()
    campos = ['ruc', 'razon_social', 'estado', 'telefono']

    # Validaciones
    for c in campos:
        if not data.get(c) or str(data.get(c)).strip() == '':
            return jsonify(success=False, error=f"El campo {c} es obligatorio."), 400

    estado = data['estado'].lower()
    if estado not in ['activo', 'inactivo', 'pendiente']:
        return jsonify(success=False, error="Estado inválido."), 400

    try:
        exito = dao.guardarProveedor(
            data['ruc'].strip(),
            data['razon_social'].strip().upper(),
            estado,
            data['telefono'].strip()
        )
        if exito:
            return jsonify(success=True, data={
                'ruc': data['ruc'].strip(),
                'razon_social': data['razon_social'].strip().upper(),
                'estado': estado,
                'telefono': data['telefono'].strip()
            }, error=None), 201
        return jsonify(success=False, error="No se pudo guardar el proveedor."), 500
    except Exception as e:
        app.logger.error(f"Error al agregar proveedor: {e}")
        return jsonify(success=False, error="Error interno."), 500

@provapi.route('/proveedores/<int:id_proveedor>', methods=['PUT'])
@csrf.exempt
def updateProveedor(id_proveedor):
    data = request.get_json() or {}
    dao = ProveedorDao()
    campos = ['ruc', 'razon_social', 'estado', 'telefono']

    for c in campos:
        if not data.get(c) or str(data.get(c)).strip() == '':
            return jsonify(success=False, error=f"El campo {c} es obligatorio."), 400

    estado = data['estado'].lower()
    if estado not in ['activo', 'inactivo', 'pendiente']:
        return jsonify(success=False, error="Estado inválido."), 400

    try:
        exito = dao.updateProveedor(
            id_proveedor,
            data['ruc'].strip(),
            data['razon_social'].strip().upper(),
            estado,
            data['telefono'].strip()
        )
        if exito:
            return jsonify(success=True, data={
                'id_proveedor': id_proveedor,
                'ruc': data['ruc'].strip(),
                'razon_social': data['razon_social'].strip().upper(),
                'estado': estado,
                'telefono': data['telefono'].strip()
            }, error=None), 200
        return jsonify(success=False, error="No encontrado o no se pudo actualizar."), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar proveedor: {e}")
        return jsonify(success=False, error="Error interno."), 500

@provapi.route('/proveedores/<int:id_proveedor>', methods=['DELETE'])
@csrf.exempt
def deleteProveedor(id_proveedor):
    dao = ProveedorDao()
    try:
        exito = dao.deleteProveedor(id_proveedor)
        if exito:
            return jsonify(success=True, mensaje=f"Proveedor {id_proveedor} eliminado.", error=None), 200
        return jsonify(success=False, error="Proveedor no encontrado."), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar proveedor: {e}")
        return jsonify(success=False, error="Error interno."), 500
