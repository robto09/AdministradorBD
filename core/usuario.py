# coding=utf-8
from resources import sql
from database.db import DB
bd_conn = DB['bd']


def insertar_nuevo_usuario(usuario_dict):
    try:
        query = sql.REGISTRO_USUARIO % (usuario_dict["nombre_usuario"], usuario_dict["contrasena"], usuario_dict["tipo_usuario"])
        bd_conn.insert(query)
        print "Nuevo registro exitoso"
    except Exception:
        print "Ocurrió un error al momento de insertar el nuevo usuario"


def buscar_usuario_por_nombre(nombre):
    return bd_conn.query_one(sql.BUSCAR_USUARIO_POR_NOMBRE % (nombre,))

