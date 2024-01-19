class DbEntry:
    def __init__(self,
                 taskno=1,
                 name='Task',
                 description='Revise',
                 deadline='01/01/24',
                 priority='Low Priority',
                 progress='Not Yet Started'):
        self.taskno = taskno
        self.name = name
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.progress = progress
