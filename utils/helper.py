import time
import sys
from resources import const


def limpiar_pantalla():
    print "\n" * 1000
    print "------------------------------------"


def tiempo_espera():
    for i in reversed(xrange(const.TIEMPO_ESPERA)):
        time.sleep(1)
        sys.stdout.write(str(i + 1) + '\n')
        sys.stdout.flush()


def show_results(cursor):
    widths = []
    columns = []
    tavnit = '|'
    separator = '+'
    results = cursor.fetchall()

    for cd in cursor.description:
        widths.append(max(cd[2], len(cd[0])))
        columns.append(cd[0])

    for w in widths:
        tavnit += " %-" + "%ss |" % (w,)
        separator += '-' * w + '--+'

    print(separator)
    print(tavnit % tuple(columns))
    print(separator)
    for row in results:
        print(tavnit % row)
    print(separator)