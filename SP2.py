from Db import Db
from Gui import Gui

def main():
    db = Db(init=False, dbName='ToDoList.csv')
    app = Gui(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()