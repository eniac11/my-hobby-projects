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
import difflib
import importlib.resources

from pprint import pprint

import server3.main as main2
from tools import semantic, htmls
from .StoryClassess import Sentence

semantic.config.minified = True
from tools.htmls import *
from tools.semantic import Semantic
from tools.web_framework.application import Application
from tools.web_framework.bottle import request

from . import config

from .story import chapters
# print(__name__)



app = Application(__name__,
                  {"semantic": Semantic.static_semantic_root, "default": importlib.resources.path("server3", "static")})

semantic_ = Semantic()
semantic.load_component_if_needed("sticky")
semantic.load_component_if_needed("rail")
semantic.load_component_if_needed("visibility")

links = [
    Link('/', "Story"),
    Link('/items', 'Story Reference'),
    Link('/chapters', 'Chapters'),
    Link('/markdown_example', 'Markdown Example')
]


# main2.scripts.append(create_element("script", inner="""
# $('.reference')
#   .popup({
#     popup: 'div#hover'
#   })
# ;
# """))


def create_navbar():
    return semantic.menu([
        semantic.item(["Story"], class_=["header"]),
        *[semantic.item([link]) for link in links],
        semantic.menu([
            semantic.item([create_link("/print", inner="Print")])
        ], class_=["right"])
    ], class_=["ui", "sticky"])


def create_context_menu():
    return semantic.menu([
        semantic.item(['test'], class_=['header']),
        semantic.button('primary', inner='History', onclick='show_history()')
    ], class_=['ui', 'vertical', 'context'], id_='context-menu')







# @app.route("/static/<path:path>")
# def static(path):
#     if semantic.check(path):
#         return bottle.static_file(str(semantic.static_file(path)), semantic.static_root(path))
#     return bottle.static_file(path, Path(__file__).parent / "static")


if config.active_grammar:
    from server3.grammaring import check, popups

    links.append(Link('/check_grammar', 'Grammar'))


    @app.route("/check_grammar")
    def check_grammar():
        grammar_page = Page(head=[

            *main2.scripts,
            create_script(url="/static/grammar.js"),
            semantic_,
            htmls.config.style_sheet
        ],
            body=[
                # semantic.dimmer(children=[
                #
                #     semantic.progress("", total=len(chapters),
                #                       styles=[width := Style('width', '400px')], id_="prog1"),
                #     semantic.progress("",
                #                       total=len(chapters[0].get_elements_by_element_name("p")), styles=[width], id_="prog2")
                # ]),
                create_navbar(),
                create_div([], class_=["ui", "container"], id_="lazy"),
                create_div([], id_="data"),
                semantic.ui(id_="hover", class_=["popup", "flowing"], styles=[Style("max-width", "20%")])
            ])
        return str(grammar_page)


    @app.route("/lazy")
    def lazy():
        yield from map(str, check())


    @app.route("/popup")
    def popups_():
        yield from map(str, popups)
        # print(*map(str, popups))


    @app.route("/stats")
    def stats():
        return {
            "chapters": len(chapters),
            "paragraphs": [len(chapter.get_elements_by_name("p")) for chapter in chapters]
        }


copy_page = copy.deepcopy(main2.page)

main2.page.head.children.append(semantic_)

main2.page.body.children.insert(0, create_navbar())

main2.page.body.children.insert(-1, main2.status_bar())
main2.page.body.get_element_by_id('ters').children.insert(0, main2.toc)
# main2.page.body.children.append(create_context_menu())

categorys = main2.display_categories()
categorys.body.children.insert(0, create_navbar())
categorys.head.children.append(semantic_)


#@app.route('/editor', method='POST')
#def editor_():
    #if request.method == "POST":
        #json = request.json
        #pprint(json)
        #q = editor.EditorQuery(json)
        #return str(transform(editor.run_query(q)))

@app.route("/")
def hello_world():
    return str(main2.page)


@app.route('/items', methods=["GET"])
def items():
    if len(request.query) > 0:
        if request.query["category"]:
            category = main2.display_category(request.query['category'])
            category.body.children.insert(0, create_navbar())
            category.head.children.append(semantic_)
            return str(category)

    return str(categorys)


@app.route('/chapters/<index>', methods=["GET"])
@app.route('/chapters')
def view_chapters(index=None):
    if index is not None:
        chapter = chapters[int(index)]
        page = Page(head=[
            htmls.config.style_sheet,
            *main2.scripts,
        ], body=chapter.page_view(),
            onload="setupPopupCallbacks()")
        page.body.children.insert(0, create_navbar())
        page.body.children.append(create_div([], id_="hover"))
        page.body.children.append(create_div(
            main2.create_help_text(),
            styles=[
                Style('display', 'none')
            ]
        ))
        page.head.children.append(semantic_)
        return str(page)
    page = Page(head=[
        htmls.config.style_sheet,
        *main2.scripts
    ], body=[
        create_element('ul', children=[
            create_list_item(children=[
                Link(f"/chapters/{i}", chapter.format())
            ]) for i, chapter in enumerate(chapters)
        ])
    ], onload="setupPopupCallbacks()")
    page.body.children.insert(0, create_navbar())
    page.head.children.append(semantic_)
    return str(page)


@app.route("/print")
def view_print():
    return str(copy_page)


word_count = main2.get_word_count()


@app.route("/word_count")
def word_count_():
    return str(word_count)


from tools.markdown import convert_markdown

with open("README.md") as f:
    
    markdown_page = Page(head=[
        htmls.config.style_sheet,
        *main2.scripts
    ], body=[
        *convert_markdown(f.read())
    ], onload="setupPopupCallbacks()")
    markdown_page.body.children.insert(0, create_navbar())
    markdown_page.head.children.append(semantic_)


@app.route("/markdown_example")
def markdown_example():
    return str(markdown_page)

# print(chapters[0].children[0].children[0])


# print(chapters[0].link_.elem)


# def transform_text(transformer: TextBlock | str, func):
#     transformer = transform_block_to_text_block(transformer)
#     return TextBlock(func(transformer.elem))
app.host_server(debug=True)
