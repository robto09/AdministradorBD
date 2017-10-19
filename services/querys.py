# coding=utf-8
from resources import sql
from database.db import DB
from resources import const

bd_conn = DB['bd']


class Create:
    def __init__(self, query):
        self.sql = query.lower()
        self.nombre_tabla = str
        self.ejecutar = False

    def parser(self):
        palabras_reservadas = ["crear", "tabla"]
        joined = []
        for palabra_reservada in palabras_reservadas:
            index = int
            while index != -1:
                try:
                    index = self.sql.index(palabra_reservada)
                except Exception:
                    index = -1
                if index != -1:
                    if palabra_reservada in joined:
                        print "Error de sintaxis, palabra reservada duplicada \"{}\"".format(palabra_reservada)
                        return False
                    else:
                        self.sql = self.sql.replace(palabra_reservada, '', 1)
                        joined.append(palabra_reservada)

        words = [w for w in self.sql.split(' ') if w.isalpha()]
        if len(words) == 0:
            print "Error de sintaxis, debe ingresar nombre de \"tabla\""
        elif len(words) > 1:
            print "Error de sintaxis, ha ingresado dos o más nombres para la tabla"
        elif bd_conn.query_one(sql.CHECK_TABLE_NAME % words[0]) is None:
            self.nombre_tabla = words[0]
            self.sql = sql.CREAR_TABLA % (self.nombre_tabla,)
            self.ejecutar = True
        else:
            print "Tabla: {} ya existe en la base de datos".format(words[0])

    def execute(self):
        try:
            bd_conn.execute(self.sql)
            print "Se ha creado la tabla: {}".format(self.nombre_tabla)
        except Exception as e:
            print "Ocurrió un error ejecutando el query: {}".format(self.sql)


class Alter:
    def __init__(self, query):
        self.sql = query.lower()
        self.nombre_tabla = str
        self.ejecutar = False

    def parser(self):
        indices = {3: "nombre tabla", 8: "nombre columna", 11: "tipo de dato"}
        try:
            self.sql = self.sql.split(' ')
            message = None
            atributos = []
            try:
                for indice in sorted(indices.keys(), key=int):
                    message = "Error de sintaxis, no se pudo obtener: {}".format(indices[indice])
                    atributo = self.sql[indice]
                    if indices[indice] == "tipo de dato":
                        tipo_de_dato = {
                            "entero": "int",
                            "cadena": "varchar"
                        }
                        atributo = tipo_de_dato[atributo]
                    atributos.append(atributo)
            except Exception:
                print message

            for atributo in atributos:
                if atributo in const.BANNED_TABLES:
                    print "No tienes permisos para alterar la tabla {}".format(atributo)
                    return False
            self.nombre_tabla = atributos[0]

            if bd_conn.query_one(sql.CHECK_TABLE_NAME % self.nombre_tabla) is None:
                print "La tabla a alterar \"{}\" no existe, intente nuevamente".format(self.nombre_tabla)
                return False

            result = bd_conn.query_one(sql.CHECK_COLUMN_NAME % (self.nombre_tabla, atributos[1]))

            if len(atributos) == 3 and result is None:
                self.sql = sql.ALTERAR_TABLA % tuple(atributos)
                print self.sql
                self.ejecutar = True
            else:
                print "La tabla \"{}\" ya posee una columna llamada \"{}\"".format(self.nombre_tabla, atributos[1])
                return False
        except Exception as e:
            print "Error de sintaxis en el query, intente de nuevo"

    def execute(self):
        try:
            bd_conn.execute(self.sql)
            print "Se ha alterado la tabla: {}".format(self.nombre_tabla)
        except Exception as e:
            print "Ocurrió un error ejecutando el query: {}".format(self.sql)


class Insert:
    def __init__(self, query):
        self.sql = query.lower()
        self.nombre_tabla = str
        self.ejecutar = False

    def parser(self):
        palabras_reservadas = ["insertar", "en"]
        try:
            i = 1
            valores = self.sql[self.sql.index("(") + 1: self.sql.index(")")]

            if len(self.sql) > self.sql.index(")") + 1:
                print "Error de sintaxis, no puede añadir caracteres luego de los parentesis"
                return False

            self.sql = self.sql.replace(valores, "").replace("(", "").replace(")", "")

            for palabra in self.sql.split(' '):
                if i > len(palabras_reservadas):
                    self.nombre_tabla = palabra
                    break
                i += 1
            if bd_conn.query_one(sql.CHECK_TABLE_NAME % self.nombre_tabla) is None:
                print "Error, la Tabla {} no existe".format(self.nombre_tabla)
                return False
            else:
                values = "values("
                i = 1
                for valor in valores.split(','):
                    values += "'{}',".format(valor) if i < len(valores.split(',')) else "'{}')".format(valor)
                    i += 1
                self.sql = sql.INSERTAR % self.nombre_tabla + values
                self.ejecutar = True
        except Exception as e:
            print "Error de sintaxis en el query, intente de nuevo"

    def execute(self):
        try:
            bd_conn.insert(self.sql)
            print "Se ha insertado en la tabla: {}".format(self.nombre_tabla)
        except Exception:
            print "Ocurrió un error ejecutando el query: {}".format(self.sql)


class Delete:
    def __init__(self, query):
        self.sql = query.lower()
        self.nombre_tabla = str
        self.ejecutar = False

    def parser(self):
        indices = {1: "nombre tabla", 3: "nombre columna", 6: "valor"}
        try:
            self.sql = self.sql.split(' ')
            message = None
            atributos = []
            try:
                for indice in sorted(indices.keys(), key=int):
                    message = "Error de sintaxis, no se pudo obtener: {}".format(indices[indice])
                    atributo = self.sql[indice]
                    atributos.append(atributo)
            except Exception:
                print message

            for atributo in atributos:
                if atributo in const.BANNED_TABLES:
                    print "No tienes permisos para alterar la tabla {}".format(atributo)
                    return False

            self.nombre_tabla = atributos[0]

            if bd_conn.query_one(sql.CHECK_TABLE_NAME % self.nombre_tabla) is None:
                print "La tabla  \"{}\" no existe, intente nuevamente".format(self.nombre_tabla)
                return False

            result = bd_conn.query_one(sql.CHECK_COLUMN_NAME % (self.nombre_tabla, atributos[1]))

            if len(atributos) == 3 and result is not None:
                self.sql = sql.BORRAR % tuple(atributos)
                self.ejecutar = True
            else:
                print "La tabla \"{}\" no posee una columna llamada \"{}\"".format(self.nombre_tabla, atributos[1])
                return False
        except Exception as e:
            print e
            print "Error de sintaxis en el query, intente de nuevo"

    def execute(self):
        try:
            bd_conn.execute(self.sql)
            print "Se ha borrado el registro de la tabla: {}".format(self.nombre_tabla)
        except Exception:
            print "Ocurrió un error ejecutando el query: {}".format(self.sql)


class Update:
    def __init__(self, query):
        self.sql = query.lower()
        self.nombre_tabla = str
        self.ejecutar = False

    def parser(self):
        indices = {1: "nombre tabla", 4: "nombre columna", 6: "valor"}

        try:
            self.sql = self.sql.split(' ')
            message = None
            atributos = []
            try:
                for indice in sorted(indices.keys(), key=int):
                    message = "Error de sintaxis, no se pudo obtener: {}".format(indices[indice])
                    atributo = self.sql[indice]
                    atributos.append(atributo)
            except Exception:
                print message

            for atributo in atributos:
                if atributo in const.BANNED_TABLES:
                    print "No tienes permisos para alterar la tabla {}".format(atributo)
                    return False

            self.nombre_tabla = atributos[0]

            if bd_conn.query_one(sql.CHECK_TABLE_NAME % self.nombre_tabla) is None:
                print "La tabla a actualizar \"{}\" no existe, intente nuevamente".format(self.nombre_tabla)
                return False

            result = bd_conn.query_one(sql.CHECK_COLUMN_NAME % (self.nombre_tabla, atributos[1]))

            if len(atributos) == 3 and result is not None:
                self.sql = sql.ACTUALIZAR % tuple(atributos)
                self.ejecutar = True
            else:
                print "La tabla \"{}\" no posee una columna llamada \"{}\"".format(self.nombre_tabla, atributos[1])
                return False
        except Exception as e:
            print "Error de sintaxis en el query, intente de nuevo"

    def execute(self):
        try:
            bd_conn.update_flush(self.sql)
            print "Se ha actualizado el registro en la tabla: {}".format(self.nombre_tabla)
        except Exception:
            print "Ocurrió un error ejecutando el query: {}".format(self.sql)


class Select:
    def __init__(self, query):
        self.sql = query.lower()
        self.nombre_tabla = str
        self.ejecutar = False
        self.cursor = None
        self.campos = []

    def parser(self):
        indices = {6: "nombre tabla"}
        try:
            campos = self.sql[self.sql.index("("): self.sql.index(")") + 1]
            self.sql = self.sql.replace(campos, "")
            self.sql = [q for q in self.sql.split(' ') if q.isalnum()]
            message = None
            atributos = []
            try:
                for indice in sorted(indices.keys(), key=int):
                    message = "Error de sintaxis, no se pudo obtener: {}".format(indices[indice])
                    atributo = self.sql[indice]
                    atributos.append(atributo)
            except Exception:
                print message

            for atributo in atributos:
                if atributo in const.BANNED_TABLES:
                    print "No tienes permisos para alterar la tabla {}".format(atributo)
                    return False

            self.nombre_tabla = atributos[0]

            if bd_conn.query_one(sql.CHECK_TABLE_NAME % self.nombre_tabla) is None:
                print "La tabla a alterar \"{}\" no existe, intente nuevamente".format(self.nombre_tabla)
                return False

            campos = campos.replace("(", "").replace(")", "")
            for campo in campos.split(','):
                result = bd_conn.query_one(sql.CHECK_COLUMN_NAME % (self.nombre_tabla, campo))
                if result is None:
                    print "La tabla \"{}\" no posee una columna llamada \"{}\"".format(self.nombre_tabla, campo)
                    return False
                else:
                    self.campos.append(campo)
            self.sql = sql.SELECCIONAR % (campos, self.nombre_tabla)
            self.ejecutar = True

        except Exception as e:
            print e
            print "Error de sintaxis en el query, intente de nuevo"

    def execute(self):
        try:
            self.cursor = bd_conn.query(self.sql)
            print "Se han buscando resultados en la tabla: {}".format(self.nombre_tabla)
        except Exception:
            print "Ocurrió un error ejecutando el query: {}".format(self.sql)