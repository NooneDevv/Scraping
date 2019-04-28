import MySQLdb


class DbUtils:
    """Features all Database related needs for this project"""

    def __init__(self, username, password, host, db_name):
        """Initialize connection specific variables and establish initial connection"""

        self.username = username
        self.password = password
        self.host = host
        self.db_name = db_name
        self.db = None
        self.c = None
        self.connect()

    def connect(self):
        """Connects to the specified Database"""

        try:
            self.db = MySQLdb.connect(self.host, self.username, self.password, self.db_name)
        except MySQLdb.OperationalError:
            return False
        self.c = self.db.cursor()
        return True

    def execute_query(self, query):
        """Executes specified SQL Query, will attempt to re-connect if the connection was closed"""

        print("Executing query: " + query)
        try:
            self.c.execute(query)
        except MySQLdb.OperationalError:
            if self.connect():
                print("Reconnected.")
                self.c.execute(query)
            else:
                print("Failed to reconnect - aborting.")
                quit()
        except MySQLdb.ProgrammingError:
            print("No specified table found in the database.")

    def insert_many(self, dest, values):
        """Builds an insert multiple values SQL Query based on given Values, and executes it"""
        query = 'INSERT INTO {}({}) VALUES'.format(dest,dest)

        for v in values:
            query += '("' + v + '"),'
        self.execute_query(query[:-1])

    def get_count(self, table):
        """Gets the count of rows in specified database table"""
        query = "SELECT COUNT(*) FROM {}".format(table)

        self.execute_query(query)
        return self.c.fetchone()[0]

    def check_exists(self, table, data):
        """Checks whether specified record is already in the table"""
        query = 'SELECT * FROM {} WHERE {}="{}"'.format(table, table, data)

        self.execute_query(query)
        if len(self.c.fetchall()) >= 1:
            return True
        return False

    def append_hit(self, hit):
        """Appends a 'hit' into the hits table"""
        query = 'INSERT INTO hits(hits) VALUES("{}")'.format(hit)

        if self.check_exists("hits", hit):
            print(hit + " already exists in the DB.")
        else:
            self.execute_query(query)
            print("Added hit to database: {}".format(hit))




