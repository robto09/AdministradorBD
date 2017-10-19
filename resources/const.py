# coding=utf-8
MENU = {
    1: "Registro",
    2: "Inicio de sesión",
    3: "Salir"
}

TIEMPO_ESPERA = 3

TIPOS_USUARIO = {
    1: "SysAdmin",
    2: "SysDBA",
    3: "Developer"
}

EXIT = 3

QUERY_EJEMPLOS = {
    "create": "crear tabla usuario",
    "alter": "alterar la tabla usuario y añadir la columna edad de tipo entero",
    "insert": "Insertar en carros(2007, Honda, Civic)",
    "delete": "eliminar carros donde edad sea = 26",
    'update': "actualizar carros y asignar marca = toyota",
    "select": "seleccionar la columna (marca,modelo) de la tabla carros"
}

BANNED_TABLES = ["usuario", "tipo_usuario"]