from flask import current_app as app
from app.conexion.Conexion import Conexion

class ProveedorDao:

    def getProveedores(self):
        sql = """
        SELECT id_proveedor, ruc, razon_social, registro, estado, telefono
        FROM proveedores
        ORDER BY id_proveedor
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            proveedores = cur.fetchall()
            lista = []
            for item in proveedores:
                registro_str = item[3].strftime('%Y-%m-%d') if item[3] else None
                lista.append({
                    "id_proveedor": item[0],
                    "ruc": item[1],
                    "razon_social": item[2],
                    "registro": registro_str,
                    "estado": item[4],
                    "telefono": item[5]
                })
            return lista
        except Exception as e:
            app.logger.error(f"Error en getProveedores: {e}")
            return []
        finally:
            cur.close()
            con.close()

    def getProveedorById(self, id_proveedor):
        sql = """
        SELECT id_proveedor, ruc, razon_social, registro, estado, telefono
        FROM proveedores WHERE id_proveedor = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_proveedor,))
            p = cur.fetchone()
            if p:
                registro_str = p[3].strftime('%Y-%m-%d') if p[3] else None
                return {
                    "id_proveedor": p[0],
                    "ruc": p[1],
                    "razon_social": p[2],
                    "registro": registro_str,
                    "estado": p[4],
                    "telefono": p[5]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error en getProveedorById: {e}")
            return None
        finally:
            cur.close()
            con.close()

    def guardarProveedor(self, ruc, razon_social, estado, telefono):
        # registro NO se envía, se genera automáticamente en la BD con default now()
        sql = """
        INSERT INTO proveedores (ruc, razon_social, estado, telefono)
        VALUES (%s, %s, %s, %s)
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (ruc, razon_social, estado, telefono))
            con.commit()
            return True
        except Exception as e:
            app.logger.error(f"Error en guardarProveedor: {e}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateProveedor(self, id_proveedor, ruc, razon_social, estado, telefono):
        sql = """
        UPDATE proveedores
        SET ruc = %s,
            razon_social = %s,
            estado = %s,
            telefono = %s
        WHERE id_proveedor = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (ruc, razon_social, estado, telefono, id_proveedor))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error en updateProveedor: {e}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteProveedor(self, id_proveedor):
        sql = "DELETE FROM proveedores WHERE id_proveedor = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_proveedor,))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error en deleteProveedor: {e}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
