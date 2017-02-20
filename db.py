import sqlite3


class DB:
    __dbname = None
    __dbhandle = None
    __cursor = None

    # Constructor
    def __init__(self, dbname, attributes_file):
        self.__dbname = dbname + "db"
        # Create first table with same name as the DB name
        self.create_initial_table(dbname, attributes_file)

    # Connect to a DB and set the cursor
    def connect(self):
        self.__dbhandle = sqlite3.connect("data/" + self.__dbname)
        self.__cursor = self.__dbhandle.cursor()

    # Commit and disconnect from DB
    def disconnect(self):
        self.__dbhandle.commit()
        self.__dbhandle.close()

    # Function to clear a table
    def clear_table(self, table_name):
        self.connect()
        cursor = self.__cursor
        cursor.execute("DROP TABLE " + table_name)
        self.disconnect()

    # Function to drop a view
    def drop_view(self,view_name):
        self.connect()
        cursor = self.__cursor
        cursor.execute("DROP VIEW " + view_name)
        self.disconnect()

    # Create an initial table to hold all data
    def create_initial_table(self, table_name, attributes_file):
        lines = []
        columns = []
        fhandle = open("resource/" + attributes_file, 'r')
        for line in fhandle:
            stripped_line = line.strip()
            if stripped_line != "":
                lines.append(stripped_line)
        fhandle.close()

        for line in lines:
            columns.append(line.split(" ")[0])

        # Create table if it doesn't exist
        self.connect()
        cursor = self.__cursor
        tablecheckstmt = "select count(*) from sqlite_master where type='table' and name='" + table_name + "'"
        tablecheck = cursor.execute(tablecheckstmt).fetchone()[0]
        if tablecheck == 0:  # Table doesn't exist. Create it
            stmt = "CREATE TABLE IF NOT EXISTS " + table_name + "(" + columns[0] + " TEXT)"
            cursor.execute(stmt)
            for i in range(1, len(columns)):
                stmt = "ALTER TABLE " + table_name + " ADD COLUMN " + columns[i] + " TEXT"
                cursor.execute(stmt)
        self.disconnect()

    # Load initial data from data file to the initial table
    def load_initial_data(self, table_name, data_file):
        # Load data into table
        fhandle = open("resource/" + data_file, 'r')
        lines = []
        for line in fhandle:
            lines.append(tuple(line.strip().split(' ')))
        fhandle.close()

        self.connect()
        cursor = self.__cursor
        insertstmt = "INSERT INTO " + table_name + " VALUES (?, ?, ?, ?, ?)"
        cursor.executemany(insertstmt, lines)
        self.disconnect()

    # Fetch column names
    def column_names(self, table_name):
        self.connect()
        columns = []
        lines = []
        cursor = self.__cursor
        cursor.execute("PRAGMA table_info([" + table_name + "])")
        lines = cursor.fetchall()
        self.disconnect()
        for line in lines:
            columns.append(line[1])
        return columns

    # Fetch last column
    def last_column(self, table_name):
        self.connect()
        columns = []
        lines = []
        cursor = self.__cursor
        cursor.execute("PRAGMA table_info([" + table_name + "])")
        lines = cursor.fetchall()
        self.disconnect()
        for line in lines:
            columns.append(line[1])
        return columns[-1]

    # Fetch the possible values for an attribute
    def possible_attribute_values(self, table_name, attribute):
        self.connect()
        cursor = self.__cursor
        possible_values = []
        cursor.execute("SELECT DISTINCT " + attribute + " FROM " + table_name)
        output_tuple_list = cursor.fetchall()
        possible_values = [t[0] for t in output_tuple_list]
        self.disconnect()
        return possible_values

    # Fetch matching rows
    def fetch_matching_rows(self, table_name, attribute, value):
        self.connect()
        cursor = self.__cursor
        cursor.execute("SELECT * FROM " + table_name + " WHERE " + attribute + "='" + value + "'")
        rows = cursor.fetchall()
        self.disconnect()
        return rows

    # Fetch all rows
    def fetch_all_rows(self,table_name):
        self.connect()
        cursor = self.__cursor
        cursor.execute("SELECT * FROM " + table_name)
        rows = cursor.fetchall()
        self.disconnect()
        return rows

    # Create a view
    def create_view(self, source_table, attribute_dict):
        #attribs = ",".join(attribute_dict.keys())
        viewname = []
        stmtcond = []
        for k in attribute_dict.keys():
            viewname.append(k + "_" + attribute_dict[k])
            stmtcond.append(k + "='" + attribute_dict[k] + "'")
        viewname = source_table + "_" + ("_".join(viewname))
        stmtcond = " AND ".join(stmtcond)
        viewcolumns = self.column_names(source_table)
        for k in attribute_dict.keys():
            viewcolumns.remove(k)
        viewcolumns = ",".join(viewcolumns)
        stmt = "CREATE VIEW " + viewname + "(" + viewcolumns + ") AS SELECT " + viewcolumns + " FROM " \
               + source_table + " WHERE " + stmtcond
        self.connect()
        cursor = self.__cursor
        cursor.execute(stmt)
        self.disconnect()
        return viewname


# db = DB("tennis", "tennis-attr.txt")
# db.load_initial_data("tennis","booktennis-train.txt")
# # print(db.fetch_matching_rows("tennis", "PlayTennis", "Yes"))
# a = {"Outlook" : "Sunny"}
# db.create_view("tennis", a)
# print(db.column_names("tennis_Outlook_Sunny"))
# b = {"Temperature": "Hot"}
# db.create_view("tennis_Outlook_Sunny",b)