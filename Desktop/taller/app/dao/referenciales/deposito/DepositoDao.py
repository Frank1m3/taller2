from flask import current_app as app
from app.conexion.Conexion import Conexion

class DepositoDao:

    def getDepositos(self):
        sql = """
        SELECT d.id_deposito, d.descripcion,
               d.id_sucursal, s.descripcion AS sucursal_nombre
        FROM depositos d
        LEFT JOIN sucursales s ON d.id_sucursal = s.id_sucursal
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            filas = cur.fetchall()
            resultados = []
            for f in filas:
                resultados.append({
                    "id_deposito": f[0],
                    "descripcion": f[1],
                    "id_sucursal": f[2],
                    "sucursal_nombre": f[3]
                })
            return resultados
        except Exception as e:
            app.logger.error(e)
            return []
        finally:
            cur.close()
            con.close()

    def getSucursales(self):
        sql = "SELECT id_sucursal, descripcion FROM sucursales ORDER BY descripcion"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            filas = cur.fetchall()
            resultado = []
            for f in filas:
                resultado.append({
                    "id_sucursal": f[0],
                    "descripcion": f[1]
                })
            return resultado
        except Exception as e:
            app.logger.error(f"Error al obtener sucursales: {e}")
            return []
        finally:
            cur.close()
            con.close()

    def getDepositoById(self, id_deposito):
        sql = """
        SELECT d.id_deposito, d.descripcion,
               d.id_sucursal, s.descripcion AS sucursal_nombre
        FROM depositos d
        LEFT JOIN sucursales s ON d.id_sucursal = s.id_sucursal
        WHERE d.id_deposito = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_deposito,))
            fila = cur.fetchone()
            if fila:
                return {
                    "id_deposito": fila[0],
                    "descripcion": fila[1],
                    "id_sucursal": fila[2],
                    "sucursal_nombre": fila[3]
                }
            return None
        except Exception as e:
            app.logger.error(e)
            return None
        finally:
            cur.close()
            con.close()

    def guardarDeposito(self, descripcion, id_sucursal):
        sql = """
        INSERT INTO depositos(descripcion, id_sucursal)
        VALUES (%s, %s)
        RETURNING id_deposito
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (descripcion, id_sucursal))
            id_deposito = cur.fetchone()[0]
            con.commit()
            return id_deposito
        except Exception as e:
            con.rollback()
            app.logger.error(e)
            return None
        finally:
            cur.close()
            con.close()

    def updateDeposito(self, id_deposito, descripcion, id_sucursal):
        sql = """
        UPDATE depositos
        SET descripcion = %s,
            id_sucursal = %s
        WHERE id_deposito = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (descripcion, id_sucursal, id_deposito))
            con.commit()
            return True
        except Exception as e:
            con.rollback()
            app.logger.error(e)
            return False
        finally:
            cur.close()
            con.close()

    def deleteDeposito(self, id_deposito):
        sql = "DELETE FROM depositos WHERE id_deposito = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_deposito,))
            con.commit()
            return True
        except Exception as e:
            con.rollback()
            app.logger.error(e)
            return False
        finally:
            cur.close()
            con.close()
