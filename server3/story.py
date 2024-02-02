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
from .StoryClassess import *
from .lore import *

story_title = InternalLink(create_header("My Story"))

Chapter.format_spec = "{title}"

chapters = []


languagetool = Link("languagetool.org", "LanguageTool (for the grammar server) in java", external=True)
NLTK = Link("nltk.org", "NLTK - nlp", external=True)
Matplotlib = Link('matplotlib.org', "Matplotlib", external=True)

chapter1 = Chapter(
    "Introduction",
    [
        create_p(children=[
            "This repository contains various bit of half baked projects around the concept of define html directly in python. ",
            "This is my hobby project and as such it is in no way organised."
        ]),
        create_p(children=[
            "The design guide that I have used for the various projects is that of minimal externally installed dependencies. ",
            "This means that if I need an external library it should at most be one file dependency. This was because I needed it ",
            "portable on a usb flash stick which would be used on both Linux and Windows. So it would have been difficult to use ",
            "Virtual Environment."
        ]),
        create_p(children=[
            "Each project is contained within it own folder as a module which can be run using `python -m <project_name>`."
        ]),
        create_p(children=[
            "The only folder that is not a project is the **tools** folder which contains all the custom framework code that is used ",
            "in the each project. The reason for the name **tools** is for the unimaginative reason of diffuculty in naming it."
        ]),

        create_p(children=[
            "Of course the project is not without its external dependencies.",
            create_element("ul", children=[
                create_list_item(children=[languagetool, " not required can be disabled"]),
                create_list_item(children=[NLTK, " (Not required)"]),
                create_list_item(children=[Matplotlib, " - for specific projects"]),
            ])
        ]),
        create_p(children=[": Note that the `working directory` needs to be the root of the git repo."])
    ])
chapters.append(chapter1)

chapter2 = Chapter(
    "Projects",
    [
        create_header("server3", level=2),
        create_p(children=[
            
"This project is my custom tooling for writing a creative work in the form of a story. Orginally used *flask* as its ",
"server framwork but then ported to (bottlepy - a single file web-framework)[https://bottlepy.org/]. The story behind ",
"is that tradtional editing such as markdown or LibreOffice were not flexible enough to do what I needed which was ",
"embed references to varouis story elements so that I could hover over or click on a referenced word and it would pull ",
"up information about the reference. This was needed for note taking. This project is by far the most featurefull. ",

"`server3/test.py` was my attempt at performance analysis of transforming `Element()` to `str`"
    ])
])



chapters.append(chapter2)

chapter3 = Chapter(
    "An example of using LoreItems",
    [
        create_p(children=[
            "This is a lore item about the aura magic system", aura, "from the ", aura, " system it can be broken down into ",
            "multiple systems such as ", magic_Aura, visacality, " this is the a titled (ie. capitalised) variant of ", aura, 
            " -> ", Aura
        ])
    ])
chapters.append(chapter3)

internal_links = [
    story_title.link("My Story"),
    *list(map(lambda x: x.link(), chapters))
]


story = [story_title, *chapters] 
