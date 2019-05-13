import sqlite3
from pprint import pprint
import os
import logger
#from logger import debug_log, level


fields     = ['nacsc_id',  'p_surname',  'p_forename',  's_surname',  's_forename',  'co_name',  'p_tel',  's_tel',  'address',  'postcode',  'email',  'memb_start',  'waste_lic',  'waste_start',  'ins_start', 'region', 'county']
sub_fields = ['nacsc_id',  'p_forename',  'p_surname',  'co_name',  'p_tel',  's_tel',  'address',  'postcode',  'email', 'region', 'county']

class DBHandler():
    def __init__(self, DATABASE):
        if os.path.exists(DATABASE):
           self.db_path = DATABASE
           self.connection  = sqlite3.connect(self.db_path)
           self.cursor      = self.connection.cursor()
           logger.debug_log("Database connection successful.", logger.level.debug)
        else:
           logger.debug_log("Database connection failed.", logger.level.error)

    def _querydb(self,s, count, is_postcode=False):
        f = sub_fields
        columns =  "{},{},{},{},{},{},{},{},{},{},{}".format(f[0],f[1],f[2],f[3],f[4],f[5],f[6],f[7],f[8],f[9],f[10])
        query = "SELECT {} FROM nacsc_members_fts WHERE nacsc_members_fts MATCH ?".format(columns)

        if count > 1:
            split  = s[:count]
            for x in range(0, count):
                qstring = "{}*".format(s[x])
                #query   = "SELECT * FROM nacsc_members_fts WHERE nacsc_members_fts MATCH ?"
                result  = self.cursor.execute(query, (qstring,)).fetchall()
                print(result)
                if result:
                    break
                else:
                    result = None
        else:
          qstring = "{}".format(s[0])
          result  = self.cursor.execute(query, (qstring,)).fetchall()

        return(result)

    def querydb(self,s, is_postcode=False):
        count = len(s)
        result = self._querydb(s, count, is_postcode)
        return(result)


    def change_active_database(self,PATH):
        if not os.path.exists(PATH):
            return
            print("Catastrophic failure: Database path non-existent")

        # check if a current connection is already open
        if self.connection:
            self.connection.close()
            # TODO(jamie): Implement backup of current database file

        # create connection to new database
        self.connection  = sqlite3.connect(PATH)
        self.cursor      = self.connection.cursor()
        if not self.connection:
            logger.debug_log("Database connection failed.", logger.level.error)
        else:
           logger.debug_log("New database [{}] opened".format(PATH), logger.level.debug)




