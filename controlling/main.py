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
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from typing import Optional

import tools.event_system.event
from tools.htmls import *

from tools.htmls.javascript import *
from tools.htmls.javascript.api import console, fetch
from tools.utils import clamp

simple_control = Function('simple_control', ['control_id', 'macro_id', 'macro_group', "...args"], [
    CodeBlock([
        CodeLine(
            """fetch('/', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({'macro_identifier': [control_id, macro_id, macro_group], 'data': args})})"""
        )
    ]
    )
])

update_func = Function("update", [], [

    CodeBlock([
        (update := Variable("updates", fetch('/updates', HTTPMethod.POST, ContentTypes.JSON, None).call(True))),
        console.log([update.get()], True).call()
    ])
])

print(update_func.to_code())
script = Script([
    simple_control,
    update_func
])

script_element = create_script(script=script)


@dataclass
class MacroIdentifier:
    control_id: str
    macro_id: str
    macro_group: str

    def serialize(self):
        return [self.control_id, self.macro_id, self.macro_group]

    @staticmethod
    def deserialize(json_data):
        data = json_data
        if type(json_data) != list:
            data = json.loads(json_data)

        return MacroIdentifier(data[0], data[1], data[2])


@dataclass
class ControlData:
    macro_identifier: MacroIdentifier
    data: dict = field(default_factory=dict)

    def serialize(self) -> dict:
        return {'macro_identifier': self.macro_identifier, 'data': self.data}

    @staticmethod
    def deserialize(json_data):
        data = json_data
        if type(json_data) != dict:
            data = json.loads(json_data)
        macro_identifier = MacroIdentifier.deserialize(data['macro_identifier'])
        data_ = data['data']
        return ControlData(macro_identifier, data_)


class Control(Transform):

    def __init__(self):
        super().__init__()
        self.id = str(uuid.uuid4()).replace('-', '_')
        self.macro_id: str = None
        self.macro_group: str = None
        self.on_change = tools.event_system.event.Event()

    def __transform__(self):
        return create_div(children=[
            create_button('Trigger', onclick=simple_control([self.id, self.macro_id, self.macro_group]).call(True))
        ])

    def handle(self, data: ControlData):
        # if data.macro_identifier.control_id == self.id:
        #     print(data.data)
        pass

    def post_id_set(self):
        pass

    def set_ids(self, macro_group_id: uuid.UUID, macro_id: uuid.UUID):
        self.macro_group = macro_group_id
        self.macro_id = macro_id
        self.post_id_set()

    def process_update(self) -> Optional[ControlData]:
        pass


class Controls(Transform):

    def __init__(self, controls: list[Control]):
        super().__init__()
        self.macro_id: uuid.UUID = None
        self.macro_group: uuid.UUID = None
        self.controls = controls

    def __transform__(self):
        return create_div(self.controls)

    def handle(self, data: ControlData):

        for control in self.controls:

            if (control_data := control.handle(data)) is not None:
                return control_data

    def set_ids(self, macro_group_id: uuid.UUID, macro_id: uuid.UUID):
        self.macro_group = macro_group_id
        self.macro_id = macro_id
        for control in self.controls:
            control.set_ids(self.macro_group, self.macro_id)

    def process_update(self):
        updates = []
        for control in self.controls:
            if (update := control.process_update()) is not None:
                updates.append(update)
        return updates


class Macro(Transform):

    def __init__(self, name: str, controls: Controls):
        super().__init__()
        self.id = str(uuid.uuid4()).replace('-', '_')
        self.macro_group: uuid.UUID = None
        self.name = name
        self.controls = controls

    def set_macrogroup_id(self, id_):
        self.macro_group = id_
        self.controls.set_ids(self.macro_group, self.id)

    def __transform__(self):
        return create_div([
            create_header(self.name, level=2),
            create_div([self.controls])
        ])

    def handle(self, data: ControlData):
        return self.controls.handle(data)

    def process_updates(self):
        return self.controls.process_update()


class MacroGroup:

    def __init__(self, name: str, macros: list[Macro]):
        self.id = str(uuid.uuid4()).replace('-', '_')
        self.name = name
        self.macros = macros
        for macro in self.macros:
            macro.set_macrogroup_id(self.id)

    def handle(self, data: ControlData):
        if data.macro_identifier.macro_group == self.id:
            for macro in self.macros:
                if (test := macro.handle(data)) is not None:
                    return test

    def process_updates(self):
        updates = []
        for macro in self.macros:
            updates.append(macro.process_updates())
        return updates


class SliderControl(Control):

    def __init__(self, default_value: int = 0, max_value: int = 100, step: int = 0):
        super().__init__()
        self.value = 0
        self.step = step
        self.max_value = max_value
        self.default_value = default_value

    def post_id_set(self):
        self.js_function = Function('control_' + self.id, ['value'], [
            CodeBlock([
                CodeLine(
                    "fetch('/', {method: 'POST', 'headers': {'Content-Type': 'application/json'}, body: JSON.stringify({'macro_identifier': [" + ','.join(
                        quote([self.id, self.macro_id, self.macro_group])) + "], 'data': value})})")
            ]
            ),
            CodeBlock([console.log(['hello']).call()])
        ])

    def __transform__(self):
        return create_input('range', 'tst', min_=0, max_=self.max_value, value=self.default_value, step=self.step,
                            oninput=self.js_function(['this.value'], True).call(True))

    def handle(self, data: ControlData):
        super().handle(data)
        if data.macro_identifier.control_id == self.id:
            self.value = int(data.data)
            self.on_change.emit(data)

        return True


class ProgressBar(Control):

    def __init__(self, default_value=0, max_: int = 100):
        super().__init__()

        self.value = default_value
        self.max = max_

    def __transform__(self):
        return create_element("progress", id_=self.id, value=self.value, max_=self.max)

    def handle(self, data: ControlData):
        super().handle(data)

    def process_update(self):
        print('test')
        return ControlData(MacroIdentifier(self.id, self.macro_id, self.macro_group), self.value)


control1 = Control()
control1.on_change.subscribe(lambda x: print(x))

progress_bar = ProgressBar()
progress_bar.value = clamp(100, 0, 100)

slider = SliderControl(step=10)


def test(contol_data):
    progress_bar.value = clamp(slider.value, 0, 100)


slider.on_change.subscribe(test)

macro_group = MacroGroup('test', [
    Macro('tests', Controls([
        control1,
        Control(),
        slider,
        progress_bar
    ]))
])

for macro in macro_group.macros:
    for control in macro.controls.controls:
        if hasattr(control, "js_function"):
            script.functions.append(control.js_function)
