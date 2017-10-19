# coding=utf-8

from resources import const
from utils import helper
from core import usuario as usuario_core
from services import querys
import re

# conexion

ATRIBUTOS_USUARIO = ["nombre_usuario", "contrasena", "tipo_usuario"]
# Mensajes de información y errores
MENSAJES = {
    "error": {
        "nombre_usuario": "Nombre de usuario inválido o ya existe, intentelo nuevamente",
        "contrasena": "Contraseña inválida, intentelo nuevamente"
    },
    "info": {
        "nombre_usuario": "Ingrese un nombre de usuario, debe tener máximo 10 caracteres alfanumericos",
        "contrasena": "Ingrese una contraseña, de 6 a 8 caracteres alfanumericos",
        "tipo_usuario": "Ingrese el tipo de usuario a registrar"
    }
}

REGEX = {
    "nombre_usuario": u"^[a-zA-Z0-9\sáéíóúÁÉÍÓÚåüñÑ']{1,10}$",
    "contrasena": u"^(?=.*?[a-zA-Z])(?=.*?[0-9]).{8,}$"
}

FUNCIONES_USUARIOS = {
    1: {"create": querys.Create, "alter": querys.Alter, "insert": querys.Insert, "delete": querys.Delete,
        'update': querys.Update, "select": querys.Select},
    2: {"create": querys.Create, "alter": querys.Alter, "insert": querys.Insert, "delete": querys.Delete,
        'update': querys.Update, "select": querys.Select},
    3: {"create": querys.Create, "alter": querys.Alter, "insert": querys.Insert, "delete": querys.Delete,
        'update': querys.Update, "select": querys.Select}
}

MENU_USUARIOS = {
    1: {0: "Volver al menú principal", 1: "Create", 2: "Alter", 3: "Insert", 4: "Delete", 5: "Update", 6: "Select"},
    2: {0: "Volver al menú principal", 1: "Create", 2: "Alter", 3: "Insert", 4: "Delete", 5: "Update", 6: "Select"},
    3: {0: "Volver al menú principal", 1: "Create", 2: "Alter", 3: "Insert", 4: "Delete", 5: "Update", 6: "Select"}
}


def registrar_usuario():
    nuevo_usuario = {}
    print "Registro de Usuario"
    for k in ATRIBUTOS_USUARIO:
        es_valido = False
        while not es_valido:
            if k is not "tipo_usuario":
                print MENSAJES["info"][k]
                text = raw_input()
                es_valido = re.match(REGEX.get(k), text) if k is "contrasena" else re.match(REGEX.get(k),
                                                                                            text) and usuario_core.buscar_usuario_por_nombre(
                    text) is None
                if not es_valido:
                    print MENSAJES["error"][k]
                    helper.tiempo_espera()
                    helper.limpiar_pantalla()
                else:
                    print "Has ingresado como {k} : {v}".format(k=k, v=text)
                    nuevo_usuario[k] = text
            else:
                lista_opciones = const.TIPOS_USUARIO.keys()
                opc = int
                while opc not in lista_opciones:
                    print "Seleccione una opción:"
                    for j in lista_opciones:
                        print "{llave}. {valor}".format(llave=j, valor=const.TIPOS_USUARIO.get(j))
                    opc = int(raw_input())
                    if opc not in lista_opciones:
                        print "Seleccione una opción válida"
                        helper.tiempo_espera()
                        helper.limpiar_pantalla()
                    else:
                        es_valido = True
                        nuevo_usuario[k] = opc
    print "Insertando..."
    usuario_core.insertar_nuevo_usuario(nuevo_usuario)


def iniciar_sesion():
    sesion = False
    print "Inicio de Sesión"
    while not sesion:
        print "Ingresa tu nombre de usuario"
        nombre_usuario = raw_input()
        print "Ingresa tu contraseña"
        contrasena = raw_input()
        usuario = usuario_core.buscar_usuario_por_nombre(nombre_usuario)
        if usuario is not None and usuario.contrasena == contrasena:
            print "Sesión iniciada"
            print "Redireccionando..."
            helper.tiempo_espera()
            helper.limpiar_pantalla()
            while True:
                menu = sesion_menu(usuario)
                if not menu:
                    break
            sesion = True
        else:
            print "Datos incorrectos, intente nuevamente"
            helper.tiempo_espera()
            helper.limpiar_pantalla()


def sesion_menu(usuario):
    lista_menu = MENU_USUARIOS[usuario.tipo_usuario_id].keys()
    opc = int
    print "Menú de Funciones - {}".format(const.TIPOS_USUARIO[usuario.tipo_usuario_id])
    for k in lista_menu:
        print "{llave}. {valor}".format(llave=k, valor=MENU_USUARIOS[usuario.tipo_usuario_id][k])
    while opc not in lista_menu:
        opc = int(raw_input())
        if opc not in lista_menu:
            print "Selecciona una opción valida"
        elif opc != 0:
            while True:
                print "Ejemplo de uso para {}: {}".format(MENU_USUARIOS[usuario.tipo_usuario_id][opc].upper(),
                                                          const.QUERY_EJEMPLOS[
                                                              MENU_USUARIOS[usuario.tipo_usuario_id][opc].lower()])
                print "Ingrese un query"
                query = raw_input()
                funcion = FUNCIONES_USUARIOS[usuario.tipo_usuario_id][
                    MENU_USUARIOS[usuario.tipo_usuario_id][opc].lower()](query)
                funcion.parser()
                if funcion.ejecutar:
                    funcion.execute()
                    try:
                        if funcion.cursor:
                            helper.show_results(funcion.cursor)
                    except Exception:
                        pass
                    helper.tiempo_espera()
                    helper.limpiar_pantalla()
                    break
                else:
                    helper.tiempo_espera()
                    helper.limpiar_pantalla()
        else:
            print "Volviendo al menú principal..."
            helper.tiempo_espera()
            break
    return False if opc == 0 else True
