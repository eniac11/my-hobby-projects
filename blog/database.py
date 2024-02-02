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
import datetime

from tools.dbms.peewee import *

db = SqliteDatabase("blog.sqlite3")

class BaseModel(Model):

    class Meta:
        database = db

class Question(BaseModel):
    question_text = CharField(max_length=200)
    pub_data = DateTimeField(default=datetime.datetime.now)

class Choice(BaseModel):
    question = ForeignKeyField(Question, on_delete="CASCADE", backref="choices")
    choice_text = CharField(max_length=200)
    votes = IntegerField(default=0)

def create_tables():
    with db:
        db.create_tables([Question, Choice])