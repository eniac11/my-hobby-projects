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
from tools.htmls import *
from blog.database import db, Question, create_tables
from tools.dbms import peewee
from tools.web_framework.application import Application

from tools.web_framework.bottle import abort

app = Application('Blog', {})

# create_tables()

@app.app.hook("before_request")
def before_request():
    db.connect()

@app.app.hook("after_request")
def after_request():
    db.close()

def index_template(latest_question_list: list[Question]):
    if len(latest_question_list) > 0:
        return create_element("ul", children=[create_list_item(inner=create_link(f"/{question.get_id()}", inner=question.question_text)) for question in latest_question_list])
    return create_p("No polls are available.")

@app.route("/")
def index():
    query = Question.select().order_by(Question.pub_data)
    print(query)

    return str(index_template(query))

def detail_template(question: Question):
    return create_div([
        create_header(question.question_text),
        create_element("ul", children=[
            create_list_item(inner=choice.choice_text) for choice in question.choices
        ])
    ])

vote_form = Form("vote", '/<question_id:int>/vote', HTTPMethod.POST)
vote_form.add_field(FormField("radio", "choice"))

@app.route("/<question_id:int>")
def detail(question_id: int):
    try:
        question = Question.get_by_id(question_id)
    except peewee.DoesNotExist:
        abort(404, "Question does not exist")
    return str(detail_template(question))

@app.route("/<question_id:int>/results")
def results(question_id: int):
    return str(create_p(f"You're looking at results of question {question_id}."))


@app.route("/<question_id:int>/vote")
def vote(question_id: int):
    return str(create_p(f"You're voting on question {question_id}."))


app.host_server(debug=True)

