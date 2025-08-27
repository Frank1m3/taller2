from flask import current_app as app
from app.conexion.Conexion import Conexion

class AperturaDao:

    def getAperturas(self):
        aperturaSQL = """
        SELECT a.id_apertura, a.nro_turno, 
               upper(p.nombres || ' ' || p.apellidos) as fiscal, 
               upper(p2.nombres || ' ' || p2.apellidos) as cajero, 
               to_char(a.registro, 'DD/MM/YYYY HH24:MI:SS') as registro, 
               a.monto_inicial, a.estado
        FROM aperturas a
        LEFT JOIN personas p ON a.clave_fiscal = p.fun_id
        LEFT JOIN personas p2 ON a.cajero = p2.fun_id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(aperturaSQL)
            lista_aperturas = cur.fetchall()
            lista_ordenada = []
            ultimo_turno = None
            for item in lista_aperturas:
                lista_ordenada.append({
                    "id_apertura": item[0],
                    "nro_turno": item[1],
                    "clave_fiscal": item[2],
                    "cajero": item[3],
                    "registro": item[4],
                    "monto_inicial": item[5],
                    "estado": item[6]
                })
                if ultimo_turno is None or item[1] > ultimo_turno:
                    ultimo_turno = item[1]
            return lista_ordenada, ultimo_turno
        except con.Error as e:
            app.logger.error(f"Error al obtener aperturas: {e}")
            return [], None
        finally:
            cur.close()
            con.close()

    def getAperturaById(self, id_apertura):
        aperturaSQL = """
        SELECT id_apertura, nro_turno, clave_fiscal, cajero, registro, estado
        FROM aperturas WHERE id_apertura = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(aperturaSQL, (id_apertura,))
            aperturaEncontrada = cur.fetchone()
            if aperturaEncontrada:
                return {
                    "id_apertura": aperturaEncontrada[0],
                    "nro_turno": aperturaEncontrada[1],
                    "clave_fiscal": aperturaEncontrada[2],
                    "cajero": aperturaEncontrada[3],
                    "registro": aperturaEncontrada[4],
                    "estado": aperturaEncontrada[5]
                }
            return None
        except con.Error as e:
            app.logger.error(f"Error al obtener apertura por ID: {e}")
            return None
        finally:
            cur.close()
            con.close()

    def guardarApertura(self, clave_fiscal, cajero, monto_inicial):
        insertAperturaSQL = """
        INSERT INTO aperturas (clave_fiscal, cajero, monto_inicial)
        SELECT %s, %s, %s
        WHERE EXISTS (
            SELECT 1 FROM funcionarios f
            WHERE f.fun_id = %s AND f.es_fiscal = TRUE
        )
        AND EXISTS (
            SELECT 1 FROM funcionarios f2
            WHERE f2.fun_id = %s AND f2.es_cajero = TRUE
        )
        AND %s != %s
        AND NOT EXISTS (
            SELECT 1 FROM funcionarios f_check
            WHERE f_check.fun_id = %s AND f_check.es_fiscal = TRUE AND f_check.es_cajero = TRUE
        )
        RETURNING id_apertura;
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(insertAperturaSQL, (clave_fiscal, cajero, monto_inicial, clave_fiscal, cajero, clave_fiscal, cajero, clave_fiscal))
            result = cur.fetchone()
            if result:
                id_apertura = result[0]
                con.commit()
                return {"id_apertura": id_apertura}
            return None
        except Exception as e:
            app.logger.error(f"Error al insertar apertura: {e}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()

    def anularApertura(self, id_apertura):
        """
        Cambia el estado de la apertura a 'anulado'.
        También actualiza automáticamente el cierre relacionado.
        Funciona con estado inicial 'abierto' o 'activo'.
        """
        updateSQL = """
        UPDATE aperturas a
        SET estado = 'anulado'
        FROM cierres c
        WHERE a.id_apertura = %s
          AND a.id_apertura = c.id_apertura
          AND a.estado IN ('abierto', 'activo')
        RETURNING a.id_apertura;
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(updateSQL, (id_apertura,))
            if cur.rowcount > 0:
                # Actualizar cierres directamente por seguridad
                updateCierreSQL = """
                UPDATE cierres
                SET estado = 'anulado'
                WHERE id_apertura = %s;
                """
                cur.execute(updateCierreSQL, (id_apertura,))
                con.commit()
                return True
            return False
        except Exception as e:
            app.logger.error(f"Error al anular apertura: {e}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
