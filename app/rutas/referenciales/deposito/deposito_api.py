from flask import Blueprint, request, jsonify, render_template, current_app as app
from app.dao.referenciales.deposito.DepositoDao import DepositoDao
from app import csrf  # instancia csrf de tu app

depoapi = Blueprint('depoapi', __name__)

# NUEVA RUTA: renderiza la página HTML con el select de sucursales
@depoapi.route('/depositos/index', methods=['GET'])
def depositoIndex():
    dao = DepositoDao()
    sucursales = dao.getSucursales()
    return render_template('deposito-index.html', sucursales=sucursales)

# Rutas API JSON
@depoapi.route('/depositos', methods=['GET'])
def getDepositos():
    dao = DepositoDao()
    try:
        depositos = dao.getDepositos()
        return jsonify(success=True, data=depositos, error=None), 200
    except Exception as e:
        app.logger.error(f"Error al obtener depósitos: {e}")
        return jsonify(success=False, error="Error interno."), 500

@depoapi.route('/depositos/<int:id_deposito>', methods=['GET'])
def getDeposito(id_deposito):
    dao = DepositoDao()
    try:
        deposito = dao.getDepositoById(id_deposito)
        if deposito:
            return jsonify(success=True, data=deposito, error=None), 200
        return jsonify(success=False, error="Depósito no encontrado."), 404
    except Exception as e:
        app.logger.error(f"Error al obtener depósito: {e}")
        return jsonify(success=False, error="Error interno."), 500

@depoapi.route('/depositos', methods=['POST'])
@csrf.exempt
def addDeposito():
    data = request.get_json() or {}
    dao = DepositoDao()
    campos = ['descripcion', 'id_sucursal']

    for c in campos:
        if not data.get(c) or (isinstance(data.get(c), str) and data.get(c).strip() == ''):
            return jsonify(success=False, error=f'El campo {c} es obligatorio.'), 400

    try:
        id_deposito = dao.guardarDeposito(
            data['descripcion'].strip(),
            data['id_sucursal']
        )
        if id_deposito:
            return jsonify(success=True, data={'id_deposito': id_deposito}, error=None), 201
        return jsonify(success=False, error="No se pudo guardar el depósito."), 500
    except Exception as e:
        app.logger.error(f"Error al guardar depósito: {e}")
        return jsonify(success=False, error="Error interno."), 500

@depoapi.route('/depositos/<int:id_deposito>', methods=['PUT'])
@csrf.exempt
def updateDeposito(id_deposito):
    data = request.get_json() or {}
    dao = DepositoDao()
    campos = ['descripcion', 'id_sucursal']

    for c in campos:
        if not data.get(c) or (isinstance(data.get(c), str) and data.get(c).strip() == ''):
            return jsonify(success=False, error=f'El campo {c} es obligatorio.'), 400

    try:
        actualizado = dao.updateDeposito(
            id_deposito,
            data['descripcion'].strip(),
            data['id_sucursal']
        )
        if actualizado:
            return jsonify(success=True, data=None, error=None), 200
        return jsonify(success=False, error="Depósito no encontrado o no actualizado."), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar depósito: {e}")
        return jsonify(success=False, error="Error interno."), 500

@depoapi.route('/depositos/<int:id_deposito>', methods=['DELETE'])
@csrf.exempt
def deleteDeposito(id_deposito):
    dao = DepositoDao()
    try:
        eliminado = dao.deleteDeposito(id_deposito)
        if eliminado:
            return jsonify(success=True, mensaje=f"Depósito {id_deposito} eliminado.", error=None), 200
        return jsonify(success=False, error="Depósito no encontrado."), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar depósito: {e}")
        return jsonify(success=False, error="Error interno."), 500
