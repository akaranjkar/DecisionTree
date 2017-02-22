import sqlite3
import os
from random import randint
from collections import OrderedDict

class DB:

    # Constructor
    def __init__(self, dbname, attributes_file,collection_type):
        self.collection_type = collection_type
        self.attributes_file = attributes_file
        self.table_name = dbname
        self.dbhandle = None
        self.cursor = None
        dbfile = dbname + "db"
        # Clear database file if it exists
        if os.path.exists("data/" + dbfile):
            os.remove("data/" + dbfile)
        self.dbname = dbfile
        # Create first table with same name as the DB name
        self.create_initial_table(self.table_name, attributes_file,self.collection_type)

    # Connect to a DB and set the cursor
    def connect(self):
        self.dbhandle = sqlite3.connect("data/" + self.dbname)
        self.cursor = self.dbhandle.cursor()

    # Commit and disconnect from DB
    def disconnect(self):
        self.dbhandle.commit()
        self.dbhandle.close()

    # Function to clear a table
    def clear_table(self, table_name):
        self.connect()
        cursor = self.cursor
        cursor.execute("DROP TABLE '" + table_name + "'")
        self.disconnect()

    # Function to drop a view
    def drop_view(self,view_name):
        self.connect()
        cursor = self.cursor
        cursor.execute("DROP VIEW '" + view_name + "'")
        self.disconnect()

    # Create an initial table to hold all data
    def create_initial_table(self, table_name, attributes_file,collection_type):
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
        cursor = self.cursor
        tablecheckstmt = "select count(*) from sqlite_master where type='table' and name='" + table_name + "'"
        tablecheck = cursor.execute(tablecheckstmt).fetchone()[0]
        if tablecheck == 0:  # Table doesn't exist. Create it
            if collection_type == "discrete":
                stmt = "CREATE TABLE IF NOT EXISTS " + table_name + "(" + columns[0] + " TEXT)"
                cursor.execute(stmt)
                for i in range(1, len(columns)):
                    stmt = "ALTER TABLE " + table_name + " ADD COLUMN " + columns[i] + " TEXT"
                    cursor.execute(stmt)
            elif collection_type == "real":
                stmt = "CREATE TABLE IF NOT EXISTS " + table_name + "('" + columns[0] + "' REAL)"
                cursor.execute(stmt)
                for i in range(1, len(columns) -1 ):
                    stmt = "ALTER TABLE " + table_name + " ADD COLUMN '" + columns[i] + "' REAL"
                    cursor.execute(stmt)
                stmt = "ALTER TABLE " + table_name + " ADD COLUMN '" + columns[-1] + "' TEXT"
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

        self.load_lines_to_table(table_name,lines)
        # line_columns = len(lines[0])
        # q = ['?'] * line_columns
        # self.connect()
        # cursor = self.cursor
        # insertstmt = "INSERT INTO " + table_name + " VALUES (" + ",".join(q) + ")"
        # cursor.executemany(insertstmt, lines)
        # self.disconnect()

    # Load data from rows to table
    def load_lines_to_table(self,table_name,lines):
        line_columns = len(lines[0])
        q = ['?'] * line_columns
        self.connect()
        cursor = self.cursor
        insertstmt = "INSERT INTO " + table_name + " VALUES (" + ",".join(q) + ")"
        cursor.executemany(insertstmt, lines)
        self.disconnect()

    # Fetch column names
    def column_names(self, table_name):
        self.connect()
        columns = []
        lines = []
        cursor = self.cursor
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
        cursor = self.cursor
        cursor.execute("PRAGMA table_info([" + table_name + "])")
        lines = cursor.fetchall()
        self.disconnect()
        for line in lines:
            columns.append(line[1])
        return columns[-1]

    # Fetch the possible values for an attribute
    def possible_attribute_values(self, table_name, attribute):
        self.connect()
        cursor = self.cursor
        possible_values = []
        cursor.execute("SELECT DISTINCT \"" + attribute + "\" FROM '" + table_name + "'")
        output_tuple_list = cursor.fetchall()
        possible_values = [t[0] for t in output_tuple_list]
        self.disconnect()
        return possible_values

    # Fetch matching rows
    def fetch_matching_rows(self, table_name, attribute, value):
        self.connect()
        cursor = self.cursor
        cursor.execute("SELECT * FROM '" + table_name + "' WHERE \"" + attribute + "\"='" + value + "'")
        rows = cursor.fetchall()
        self.disconnect()
        return rows

    # Fetch all rows
    def fetch_all_rows(self,table_name):
        self.connect()
        cursor = self.cursor
        cursor.execute("SELECT * FROM '" + table_name + "'")
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
            stmtcond.append("\"" + k + "\"='" + attribute_dict[k] + "'")
        viewname = source_table + "_" + ("_".join(viewname))
        stmtcond = " AND ".join(stmtcond)
        viewcolumns = self.column_names(source_table)
        for k in attribute_dict.keys():
            viewcolumns.remove(k)
        for i in range(0,len(viewcolumns)):
            viewcolumns[i] = "\"" + viewcolumns[i] + "\""
        viewcolumns = ",".join(viewcolumns)
        stmt = "CREATE VIEW '" + viewname + "'(" + viewcolumns + ") AS SELECT " + viewcolumns + " FROM '" \
               + source_table + "' WHERE " + stmtcond
        self.connect()
        cursor = self.cursor
        cursor.execute(stmt)
        self.disconnect()
        return viewname

    def transform_real_data(self,source_table):
        columns = self.column_names(source_table)
        for i in range(0,len(columns)-1):
            new_table = self.transform_column(source_table,columns[i])
            source_table = new_table
        return source_table

    def transform_column(self,source_table,column_name):
        last_column = self.last_column(source_table)
        columns = self.column_names(source_table)
        column_name_index = None
        for i in range(0,len(columns)):
            if columns[i] == column_name:
                column_name_index = i

        sort_stmt = "SELECT * FROM '" + source_table + "' ORDER BY \"" + column_name + "\""
        # create a new table with sorted by column
        new_table_name = source_table + "_transformed"
        temp_new_table_name = source_table + "_" + column_name + "_sorted_tmp"
        self.connect()
        cursor = self.cursor
        tablecheckstmt = "select count(*) from sqlite_master where type='table' and name='" + temp_new_table_name + "'"
        tablecheck = cursor.execute(tablecheckstmt).fetchone()[0]
        if tablecheck == 0:  # Table doesn't exist. Create it
            stmt = "CREATE TABLE IF NOT EXISTS '" + temp_new_table_name + "' AS " + sort_stmt
            cursor.execute(stmt)
        self.disconnect()
        # get all rows in a list
        sorted_rows = self.fetch_all_rows(temp_new_table_name)
        change_points = []
        # find spots where the class changes and calculate average. add to a set
        for i in range(0,len(sorted_rows)-1):
            if sorted_rows[i][-1] != sorted_rows[i+1][-1]:
                avg = (sorted_rows[i][column_name_index] + sorted_rows[i+1][column_name_index]) / 2
                change_points.append(avg)
        new_columns = sorted(set(change_points))
        # print(new_columns)
        # add a new column to the table and update values in this table
        for column in new_columns:
            new_column_name = column_name + " >= " + str(column)
            stmt1 = "ALTER TABLE '" + temp_new_table_name + "'ADD COLUMN '" + new_column_name + "' TEXT"
            stmt2 = "UPDATE '" + temp_new_table_name + "' SET \"" + new_column_name + "\" = 't' WHERE \"" + column_name + "\" >= " + str(column)
            stmt3 = "UPDATE '" + temp_new_table_name + "' SET \"" + new_column_name + "\" = 'f' WHERE \"" + column_name + "\" < " + str(column)
            self.connect()
            cursor = self.cursor
            cursor.execute(stmt1)
            cursor.execute(stmt2)
            cursor.execute(stmt3)
            self.disconnect()
        # remove temp table and create new one
        column_dict = OrderedDict()
        self.connect()
        cursor = self.cursor
        stmt = "PRAGMA TABLE_INFO([" + temp_new_table_name + "])"
        cursor.execute(stmt)
        op = cursor.fetchall()
        self.disconnect()
        for line in op:
            if line[1] == column_name:
                continue
            if line[1] == last_column:
                continue
            column_dict[line[1]] = line[2]
        column_dict[last_column] = 'TEXT'
        # print(column_dict)
        dict_keys = list(column_dict.keys())
        self.connect()
        cursor = self.cursor
        tablecheckstmt = "select count(*) from sqlite_master where type='table' and name='" + new_table_name + "'"
        tablecheck = cursor.execute(tablecheckstmt).fetchone()[0]
        if tablecheck == 0:  # Table doesn't exist. Create it
            stmt = "CREATE TABLE IF NOT EXISTS '" + new_table_name + "'(\"" + dict_keys[0] + "\" " + column_dict[dict_keys[0]] + ")"
            cursor.execute(stmt)
            for i in range(1, len(dict_keys)):
                stmt = "ALTER TABLE '" + new_table_name + "' ADD COLUMN \"" + dict_keys[i] + "\" " + column_dict[dict_keys[i]]
                cursor.execute(stmt)
        self.disconnect()

        for i in range(0,len(dict_keys)):
            dict_keys[i] = "\"" + dict_keys[i] + "\""
        self.connect()
        cursor = self.cursor
        stmt = "INSERT INTO '" + new_table_name + "' SELECT " + ",".join(dict_keys) + " FROM '" + temp_new_table_name + "'"
        cursor.execute(stmt)
        self.disconnect()
        self.clear_table(temp_new_table_name)
        return new_table_name


    # # Corrupt data and return new table
    # def corrupt_table(self,source_table,percentage):
    #     all_rows = self.fetch_all_rows(source_table)
    #     total_rows = len(all_rows)
    #     class_labels = self.possible_attribute_values(source_table,self.last_column(source_table))
    #     rows_to_corrupt = int(round(total_rows * percentage / 100))
    #     new_table_name = source_table + "_corrupt_" + str(percentage)
    #     for i in range(0,rows_to_corrupt):
    #         random_row_index = randint(0,total_rows)
    #         random_row = all_rows[random_row_index]
    #         random_row_class_value = random_row[-1]
    #         new_class_labels = class_labels.remove(random_row_class_value)
    #         new_random_row_class_value = new_class_labels[randint(0,len(new_class_labels))]
    #         random_row[-1] = new_random_row_class_value
    #         all_rows[random_row_index] = random_row
    #     self.connect()
    #     self.create_initial_table(new_table_name,self.attributes_file,self.collection_type)
    #     self.load_lines_to_table(new_table_name,all_rows)
    #     self.disconnect()
    #     return new_table_name



# db = DB("iris", "iris-attr.txt", "real")
# db.load_initial_data("iris","iris-train.txt")
# # print(db.fetch_matching_rows("tennis", "PlayTennis", "Yes"))
# a = {"Outlook" : "Sunny"}
# db.create_view("tennis", a)
# print(db.column_names("tennis_Outlook_Sunny"))
# b = {"Temperature": "Hot"}
# db.create_view("tennis_Outlook_Sunny",b)

# db = DB("tennis", "tennis-attr.txt", "discrete")
# db.load_initial_data("tennis","tennis-train.txt")
# print(db.fetch_all_rows("tennis"))
# ct = db.corrupt_table("tennis",30)
# print(db.fetch_all_rows(ct))

# db = DB("iris", "iris-attr.txt", "real")
# db.load_initial_data("iris","iris-train.txt")
# # db.transform_column("iris","sepal-length")
# print(db.transform_real_data("iris"))