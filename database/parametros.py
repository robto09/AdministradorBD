def connector(**opts):
    return ' '.join(["%s=%s" % (key, value) for key, value in opts.iteritems()])


bd_connection = connector(dbname='pythonappdb', user='postgres', password='123456', host='localhost')
