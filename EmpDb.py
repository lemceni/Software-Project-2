import sqlite3
from EmpDbEntry import EmpDbEntry

class EmpDb:
    def __init__(self, init=False, dbName='EmpDb'):
        # CSV filename
        self.csvFile = dbName + ".csv"
        self.dbName = dbName + ".db"
        # initialize container of database entries 
        self.table_name = "Employees"
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
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    role TEXT,
                    gender TEXT,
                    status TEXT)''')
        self.column_names = ['ID', 'Name', 'Role', 'Gender', 'Status']
        self.commit_close()

    def fetch_employees(self):
        self.connect_cursor()
        query = f'''SELECT * FROM {self.table_name}'''
        self.cursor.execute(query)
        tupleList = self.cursor.fetchall()
        self.conn.close()

        return tupleList

    def insert_employee(self, id, name, role, gender, status):
        newEntry = EmpDbEntry(id=id, name=name, role=role, gender=gender, status=status)
        newEntryDict = newEntry.__dict__
        self.connect_cursor()
        query = f'''INSERT INTO {self.table_name} ({",".join(newEntryDict.keys())}) VALUES (?,?,?,?,?)'''
        self.cursor.execute(query, list(newEntryDict.values()))
        self.commit_close()

    def delete_employee(self, id):
        self.connect_cursor()
        query = f'''DELETE FROM {self.table_name} WHERE id = "{id}"'''
        self.cursor.execute(query)
        self.commit_close()

    def update_employee(self, new_name, new_role, new_gender, new_status, id):
        if not self.id_exists(id):
            return

        self.connect_cursor()
        entry = EmpDbEntry(id, new_name, new_gender, new_role, new_status)
        query = f'''UPDATE {self.table_name} SET '''
        query += f'''{",".join([f"{key}='{value}'" for key,value in list(entry.__dict__.items())])}'''
        query += f''' WHERE id = {id}'''
        
        self.cursor.execute(query)
        self.commit_close()

    def export_csv(self):
        employees = self.fetch_employees()
        if employees:
            with open(self.csvFile, 'w') as csv:
                for employee in employees:
                    csv.write(f"{','.join(employee)}\n")

    def id_exists(self, id):
        result = False

        self.connect_cursor()
        query = f'''SELECT id FROM {self.table_name} WHERE id = "{id}" LIMIT 1'''
        self.cursor.execute(query)
        fetched = self.cursor.fetchone()
        self.conn.close()
        
        if fetched:
            result = True
        
        return result