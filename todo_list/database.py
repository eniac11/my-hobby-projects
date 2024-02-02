"""Copyright (C) 2024 Hadley Epstein

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from tools.dbms.peewee import *

db = SqliteDatabase('people.db')


class BaseModel(Model):
    class Meta:
        database = db


class Todo(BaseModel):
    todo_id = AutoField()
    task = CharField(max_length=100)
    status = BooleanField(null=True)

def setup():
    db.create_tables([Todo])
    # conn.execute(
    #     "INSERT INTO todo (task,status) VALUES ('Read A-byte-of-python to get a good introduction into Python',0)")
    # conn.execute("INSERT INTO todo (task,status) VALUES ('Visit the Python website',1)")
    # conn.execute(
    #     "INSERT INTO todo (task,status) VALUES ('Test various editors for and check the syntax highlighting',1)")
    # conn.execute("INSERT INTO todo (task,status) VALUES ('Choose your favorite WSGI-Framework',0)")
    with db.atomic():
        todo1 = Todo.create(task='Read A-byte-of-python to get a good introduction into Python', status=0)
        todo2 = Todo.create(task='Visit the Python website', status=1)
        todo3 = Todo.create(task='Test various editors for and check the syntax highlighting', status=1)
        todo4 = Todo.create(task='Choose your favorite WSGI-Framework', status=0)


# setup()


