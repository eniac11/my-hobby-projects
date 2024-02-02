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
from todo_list.database import db, Todo
from tools.dbms.peewee import ModelSelect
from tools.htmls import *
from tools.web_framework.application import Application

app = Application('Todo List', {})

app.error_pages[404] = [create_p('There is a mistake in your url!')]
app.error_pages[403] = [create_p('Sorry, this page does not exist!')]


def table_row(items: list):
    tr = create_element("tr")
    for item in items:
        tr.add_child(create_element('td', inner=item))
    return tr


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def create_table(columns: list[str], rows: list, row_wrap: Optional[int] = None):
    table = create_element('table')
    tr = create_element('tr')
    column_length = len(columns)
    if row_wrap is not None:
        row_length = len(rows)
        # extra_columns = ((len(rows) - (len(rows) // row_wrap) * row_wrap) < row_wrap) * len(columns)
        extra_columns = ((row_length - (row_length // row_wrap) * row_wrap) < row_wrap) * column_length
        # lcolumns = lcolumns * (len(rows) // row_wrap) + extra_columns
        column_length = column_length * (row_length // row_wrap) + extra_columns

    print(column_length)
    for i in range(0, column_length, len(columns)):
        for column in columns:
            tr.add_child(create_element('th', inner=column))
    if row_wrap is not None:
        for i, chunk in enumerate(chunker(rows, row_wrap)):
            if i == 0:
                table.add_children(chunk)
                continue
            for i, row in enumerate(chunk):
                table.children[i].add_children(row.children)
    else:
        for row in rows:
            if type(row) == list:
                table.add_child(table_row(row))
            else:
                table.add_child(table_row([row]))
    table.children.insert(0, tr)
    return table


@app.route("/")
def root():
    # c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    query = Todo.select(Todo.task).where(Todo.status == 1)
    # results = c.fetchall()

    page = Page(body=[
        create_table(['task', 'completed'], [table_row([todo.get_id, todo.task]) for todo in query])
    ])

    return str(page)


form = Form("new_item", "/new_item", HTTPMethod.GET)
form.add_field(FormField(type_='text', name='task'))
form.add_field(FormField(type_='submit', name='save', default_value='save'))


@form.get
def form_get_new_item(f: Form):
    if f.filled:
        with db.atomic():
            # c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (f['task'].value.strip(), 1))
            todo = Todo.create(task=f['task'].value.strip(), status=1)
        new_id = todo.get_id

        return str(create_p(f"The new task was inserted into the database, the ID is {new_id}"))

    temp = create_div([
        create_p("Add a new tasks to the Todo list:"),
        f
    ])

    return str(temp)


@app.route('/item<item:re:[0-9]+>')
def show_item(item):
    # c.execute("SELECT task FROM todo WHERE id LIKE ?", (item,))
    # print(*((todo.todo_id, todo.task, todo.status) for todo in Todo.select()))
    query: ModelSelect = Todo.select(Todo.task).where(Todo.todo_id == item)
    # print(*((todo.todo_id, todo.task, todo.status) for todo in query))
    result = tuple(query)[0]
    print(result)
    if not result:
        return str(create_p('This item number does not exist!'))
    else:
        return str(create_p(f'Task: {result.task}'))


edit_form = Form('edit_form', '/edit/<no:int>', HTTPMethod.GET)

edit_form.add_field(FormField(type_='text', name='task'))
edit_form.add_field(ComboboxField(name='status', items=[("1", "open"), ("2", "close")]))
edit_form.add_field(FormField(type_='submit', name='save', default_value='save'))


@app.route('/all')
def all_():
    query = Todo.select()
    results: tuple[Todo] = query

    for i in range(len(results)):
        print(results[i].status)

    page = Page(body=[
        create_table(['task', 'completed'], [
            table_row([results[i].task, create_input('checkbox', 'test', checked=results[i].status)]) for i in
            range(len(results))])
    ])

    return str(page)


@edit_form.get
def edit_item(f: Form, no):
    if f.filled:
        edit = f['task']
        status = f['status']

        if status == "1":
            status = 1
        else:
            status = 0

        with db.atomic():
            Todo.update(todo_id=no, task=edit.value, status=status)

        return str(create_p(f'The item number {no} was successfully updated</p>'))

    query = Todo.select(Todo.task).where(Todo.todo_id == no)

    cur_data = query[0]
    f['task'].value = cur_data.task
    f.url = '/edit/' + str(no)

    return str(f)


app.form_route(form)
app.form_route(edit_form)

app.host_server(debug=True)
