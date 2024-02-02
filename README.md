# Python HTML generator and various projects

This repository contains various bit of half baked projects around the concept of define html directly in python.
This is my hobby project and as such it is in no way organised.

The design guide that I have used for the various projects is that of minimal externally installed dependencies.
This means that if I need an external library it should at most be one file dependency. This was because I needed it 
portable on a usb flash stick which would be used on both Linux and Windows. So it would have been difficult to use 
Virtual Environment.

Each project is contained within it own folder as a module which can be run using `python -m <project_name>`.

The only folder that is not a project is the **tools** folder which contains all the custom framework code that is used 
in the each project. The reason for the name **tools** is for the unimaginative reason of diffuculty in naming it.

Of course the project is not without its external dependencies.

- (LanguageTool (for the grammar server) in java)[https://languagetool.org/] not required can be disabled
- (NLTK - nlp)[nltk.org] (Not required)
- (Matplotlib)[https://matplotlib.org/] - for specific projects

: Note that the `working directory` needs to be the root of the git repo.

## Project List

## server3

This project is my custom tooling for writing a creative work in the form of a story. Orginally used *flask* as its
server framwork but then ported to (bottlepy - a single file web-framework)[https://bottlepy.org/]. The story behind
is that tradtional editing such as markdown or LibreOffice were not flexible enough to do what I needed which was
embed references to varouis story elements so that I could hover over or click on a referenced word and it would pull 
up information about the reference. This was needed for note taking. This project is by far the most featurefull.

`server3/test.py` was my attempt at performance analysis of transforming `Element()` to `str`

### Requirements to run.

- NLTK - sentence tokenising (Not required)
  - Only when used along side LanguageTool and for serialisation in `server3/serialize.py (run as module)`

grammar checking can be toggled in `server3/config.py`

## python_in_webbrowser

This project is a probably a secondary goal of the entire frameworks minimal large dependencies. This project 
archive the entire `tools` package along with its own source code and serves a webpage that runs 
(pyscript)[https://pyscript.net/] that loads the archive and using the `tools.htmls` module generates the entire
web page in the browser in python. Of this was implemented to eases my development process but could for production 
use python `wheels` instead. It is my hope that this would bring python into the webbrowser.

Another feature which could be achieved is constructing a virtual dom out of python `Element()` with say a 
reference to html objects in the instance. This is the purpose of `Element_Constructor` which would allow 
the base class of all Elements to be tailored for the browser or perhaps a desktop gui framework like Qt or gtk.

## ipc_bus

This was my attempt at remote function calling but with added advantage of interfaces that are defined in the source
rather than at runtime like xmlrpc in the standard library so that code completion workds. There are three 
major problems with problems with the implementation first is security, the protocol shunts around pickled objects. 
Second is method chaining it not possible to `rpc.method1().some_property` as this needs to be send two requests to 
the server but python can't handle it and errors. Finnaly, to the best of my knowledege the server code is
able to handle request - process - response in a single request but it takes multiple request to feed the response 
back up the chain.

## todo_list

Quite self explanatory. I think I followed a tutorial somewhere not sure where though.

### Internal dependencies

- (Peewee ORM - single file)[http://docs.peewee-orm.com/en/latest/] - `tools/dbms/peewee.py`

## cbk

This project has been in the pipeline for a long time and been rewritten serveral times. It is a Recipe book editor,
viewer and framework. Started out as a simple gui written in tkinter to generate ReStructuredText for sphinx. Then a 
PyQt application with xml recipe storage. Now it is a fully pythonized storage system of pickling objects. It is an
attempt to use what I call the Provider Pattern where a Provider object is created and DataStores are registered on it. 
Thus allowing for a single collated view of multiple sources.

The reason for this is say the user enters some ingredients before a cookbook is loaded then those ingredients are stored
in the application user-data folder or a more concretely the application can provide a datastore of commonly used ingredients
that are then collated along with cookbook specific ingredients so that the user would not need to re-enter all 
the ingredient data each time a new a cookbook is created.


