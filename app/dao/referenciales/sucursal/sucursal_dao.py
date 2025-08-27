from flask import current_app as app
from app.conexion.Conexion import Conexion

class SucursalDao:

    def getSucursales(self):
        sucursalSQL = """
        SELECT id_sucursal, descripcion
        FROM sucursales
        ORDER BY id_sucursal
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sucursalSQL)
            lista_sucursales = cur.fetchall()
            lista_ordenada = []
            for item in lista_sucursales:
                lista_ordenada.append({
                    "id_sucursal": item[0],
                    "descripcion": item[1]
                })
            return lista_ordenada
        except Exception as e:
            app.logger.error(f"Error al obtener sucursales: {e}")
            return []
        finally:
            cur.close()
            con.close()

    def getSucursalById(self, id_sucursal):
        sucursalSQL = """
        SELECT id_sucursal, descripcion
        FROM sucursales WHERE id_sucursal=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sucursalSQL, (id_sucursal,))
            sucursalEncontrada = cur.fetchone()
            if sucursalEncontrada:
                return {
                    "id_sucursal": sucursalEncontrada[0],
                    "descripcion": sucursalEncontrada[1]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener sucursal por ID: {e}")
            return None
        finally:
            cur.close()
            con.close()

    def guardarSucursal(self, descripcion):
        insertSucursalSQL = """
        INSERT INTO sucursales(descripcion)
        VALUES (%s)
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertSucursalSQL, (descripcion,))
            con.commit()
            return True
        except Exception as e:
            app.logger.error(f"Error al insertar sucursal: {e}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateSucursal(self, id_sucursal, descripcion):
        updateSucursalSQL = """
        UPDATE sucursales
        SET descripcion=%s
        WHERE id_sucursal=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateSucursalSQL, (descripcion, id_sucursal))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar sucursal: {e}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteSucursal(self, id_sucursal):
        deleteSucursalSQL = """
        DELETE FROM sucursales
        WHERE id_sucursal=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteSucursalSQL, (id_sucursal,))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar sucursal: {e}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def getDepositosPorSucursal(self, id_sucursal):
        # Obtiene depósitos activos relacionados a una sucursal
        sql = """
        SELECT sd.id_deposito
        FROM sucursal_depositos sd
        WHERE sd.id_sucursal = %s AND sd.estado = true
        ORDER BY sd.id_deposito
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_sucursal,))
            depositos = cur.fetchall()
            # Retornamos lista de IDs de depósitos
            lista_depositos = [row[0] for row in depositos]
            return lista_depositos
        except Exception as e:
            app.logger.error(f"Error al obtener depósitos de la sucursal {id_sucursal}: {e}")
            return []
        finally:
            cur.close()
            con.close()
