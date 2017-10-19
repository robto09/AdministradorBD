# coding=utf-8
from services import usuario
from resources import const
from utils import helper

lista_opciones = const.MENU.keys()

count = 0


def menu():
    print "Menú Principal"
    for k in lista_opciones:
        print "{llave}. {valor}".format(llave=k, valor=const.MENU.get(k))


def switcher(opc):
    acciones = {
        1: usuario.registrar_usuario,
        2: usuario.iniciar_sesion
    }
    if opc in acciones:
        helper.limpiar_pantalla()
        return acciones[opc]()
    print "Saliendo del sistema..."
    helper.tiempo_espera()


def start():
    while True:
        opc = int
        helper.limpiar_pantalla()
        print "Consola de Python para conexión a base de datos postgres"
        print "--------------------------------------------------------"
        while opc not in lista_opciones:
            menu()
            opc = int(raw_input())
            if opc not in lista_opciones:
                print "Por favor selecciona una opción válida"
                helper.tiempo_espera()
                helper.limpiar_pantalla()
            else:
                switcher(opc)
        if opc == const.EXIT:
            return False

if __name__ == '__main__':
    start()

