from EmpDb import EmpDb
from EmpGuiCtk import EmpGuiCtk

def main():
    db = EmpDb(init=False, dbName='EmpDb.csv')
    app = EmpGuiCtk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()