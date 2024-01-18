import sqlite3
from DbEntry import DbEntry

class Db:
    def __init__(self, init=False, dbName='ToDoListDb'):
        # CSV filename
        self.csvFile = dbName + ".csv"
        self.dbName = dbName + ".db"
        # initialize container of database entries 
        self.table_name = "ToDoList"
        self.create_table()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    taskno TEXT PRIMARY KEY,
                    name TEXT,
                    description TEXT,
                    deadline TEXT,
                    priority TEXT,
                    progress TEXT)''')
        self.column_names = ['taskno', 'name', 'description', 'deadline', 'priority', 'progress']
        self.commit_close()

    def fetch_data(self):
        self.connect_cursor()
        query = f'''SELECT * FROM {self.table_name}'''
        self.cursor.execute(query)
        tupleList = self.cursor.fetchall()
        self.conn.close()

        return tupleList

    def insert_data(self, taskno, name, description, deadline, priority, progress):
        newEntry = DbEntry(taskno=taskno, name=name, description=description, deadline=deadline, priority=priority, progress=progress)
        newEntryDict = newEntry.__dict__
        self.connect_cursor()
        query = f'''INSERT INTO {self.table_name} ({",".join(newEntryDict.keys())}) VALUES (?,?,?,?,?,?)'''
        self.cursor.execute(query, list(newEntryDict.values()))
        self.commit_close()

    def delete_data(self, taskno):
        self.connect_cursor()
        query = f'''DELETE FROM {self.table_name} WHERE taskno = "{taskno}"'''
        self.cursor.execute(query)
        self.commit_close()

    def update_data(self, new_name, new_description, new_deadline, new_priority, new_progress, taskno):
        if not self.id_exists(taskno):
            return

        self.connect_cursor()
        entry = DbEntry(taskno, new_name, new_description, new_deadline, new_priority, new_progress)
        query = f'''UPDATE {self.table_name} SET '''
        query += f'''{",".join([f"{key}='{value}'" for key,value in list(entry.__dict__.items())])}'''
        query += f''' WHERE taskno = {taskno}'''
        
        self.cursor.execute(query)
        self.commit_close()

    def export_csv(self):
        data = self.fetch_data()
        if data:
            with open(self.csvFile, 'w') as csv:
                for i in data:
                    csv.write(f"{','.join(i)}\n")

    def id_exists(self, taskno):
        result = False

        self.connect_cursor()
        query = f'''SELECT taskno FROM {self.table_name} WHERE taskno = "{taskno}" LIMIT 1'''
        self.cursor.execute(query)
        fetched = self.cursor.fetchone()
        self.conn.close()
        
        if fetched:
            result = True
        
        return result