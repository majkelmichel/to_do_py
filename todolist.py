from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# new_row = Table(task="Do cleaning", date=datetime.strptime('07-04-2020', '%m-%d-%Y').date())
# session.add(new_row)
# session.commit()


menu = """1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit"""

while True:
    print(menu)
    user_answer = input()
    print()
    if user_answer == "1":
        print(f"Today {datetime.today().day} {datetime.today().strftime('%b')}:")
        rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
        if len(rows) == 0:
            print("Nothing to do!\n")
        else:
            for task in rows:
                print(f'{task.id}. {task}')
            print()
    elif user_answer == "2":
        for i in range(7):
            today = datetime.today() + timedelta(days=i)
            print(f"{today.strftime('%A')} {today.day} {today.strftime('%b')}:")
            rows = session.query(Table).filter(Table.deadline == today.date()).all()
            if len(rows) == 0:
                print("Nothing to do!\n")
            else:
                for task in rows:
                    print(f'{task.id}. {task}')
                print()
    elif user_answer == "3":
        rows = session.query(Table).all()
        for row in rows:
            print(f"{row.id}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        print()
    elif user_answer == "4":
        rows = session.query(Table).filter(Table.deadline < datetime.today())
        print("Missed tasks:")
        for row in rows:
            print(f"{row.id}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        print()
    elif user_answer == "5":
        print("Enter task")
        user_task = input()
        print("Enter deadline")
        user_deadline = input()
        new_task = Table(task=user_task, deadline=datetime.strptime(user_deadline, '%Y-%m-%d'))
        session.add(new_task)
        session.commit()
        print("Task has been added!\n")
    elif user_answer == "6":
        rows = session.query(Table).all()
        print("Choose the number of the task you want to delete:")
        for row in rows:
            print(f"{row.id}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        task_to_delete = input()
        session.delete(rows[int(task_to_delete) - 1])
        session.commit()
        print()
    elif user_answer == "0":
        print("Bye!")
        break