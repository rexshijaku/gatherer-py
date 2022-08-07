import MySQLdb
import csv


class DBHandler:
    __host = None
    __user = None
    __password = None
    __port = None
    __char_set = None
    __collate = None

    __tenant_query = None
    __tenant_query_source = None

    # in case catalog connection is specified explicitly these fields will be used
    __catalog_host = None
    __catalog_db = None
    __catalog_user = None
    __catalog_password = None
    __catalog_port = None
    __catalog_char_set = None
    __catalog_collate = None

    __catalog_query = None

    __debug = False

    def __init__(self, host, user, password, port,
                 tenant_query=None, tenant_query_source=None, debug=False):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__port = port
        self.__tenant_query = tenant_query
        self.__tenant_query_source = tenant_query_source
        self.__debug = debug

    def setCatalog(self, catalog_db, catalog_query,
                   catalog_host=None, catalog_user=None, catalog_password=None, catalog_port=None):
        self.__catalog_db = catalog_db
        self.__catalog_query = catalog_query

        self.__catalog_host = self.__setCatalogSettingValue(catalog_host, self.__host)
        self.__catalog_user = self.__setCatalogSettingValue(catalog_user, self.__user)
        self.__catalog_password = self.__setCatalogSettingValue(catalog_password, self.__password)
        self.__catalog_port = self.__setCatalogSettingValue(catalog_port, self.__port)

    def __setCatalogSettingValue(self, value, when_none_set_this):
        if value is None:
            return when_none_set_this
        return value

    def get_tenants(self):

        self.print('fetching databases...')

        db = MySQLdb.connect(host=self.__catalog_host,
                             user=self.__catalog_user,
                             passwd=self.__catalog_password,
                             port=self.__catalog_port,
                             db=self.__catalog_db)
        cur = db.cursor()
        cur.execute(self.__catalog_query)
        result = []
        for row in cur.fetchall():  # instead tuple return an array
            result.append(row[0])
        db.close()
        return result

    def get_tenant_result(self, db):

        self.print('getting tenant {db} result '.format(db=db))

        db = MySQLdb.connect(host=self.__host,
                             user=self.__user,
                             passwd=self.__password,
                             port=self.__port,
                             db=db)

        if self.__tenant_query_source is not None:
            query_to_execute = open(self.__tenant_query_source, "r").read()
        else:
            query_to_execute = self.__tenant_query

        cur = db.cursor()
        cur.execute(query_to_execute)
        result = cur.fetchall()
        db.close()
        return result

    def saveDBResult(self, data, path):
        self.print('saving tenant {path} result '.format(path=path))
        with open(path, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for tup in data:
                writer.writerow(tup)

    def print(self, message):
        if self.__debug:
            print(message)
