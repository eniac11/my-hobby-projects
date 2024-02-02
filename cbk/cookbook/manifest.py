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
import pickle
import zipfile
from typing import TypedDict

from cbk.cookbook.Stores import Provider
from tools.htmls import create_element, Element

""" Manifest Format
<manifest>
    <providers>
        <provider name='recipe'>
            <store name='default' md5='MD5SUM'/>
        </provider>
        <provider name='ingredient'>
            <store name='default' md5='MD5SUM' />
        </provider>
    </providers>
    <config>
        <item name='default'>
            <entry name='unit_system'>
                <accepted_values>
                    <value>imperial</value>
                    <value>metric</value>
                </accepted_values>
            </entry>
        </item>
    </config>
</manifest>

"""


def create_provider(name, *args, **kwargs):
    return create_element('provider', name_=name, *args, **kwargs)


def create_store(name, md5: str):
    return create_element('store', name_=name, md5=md5, single=True)


def save_impl(zfs: zipfile.ZipFile, providers: dict[str, list[tuple[str, str]]]):

    manifest = create_element("manifest", children=[
        create_element('providers', children=[
            create_provider(provider_name, children=[
                create_store(store_name, md5) for store_name, md5 in provider
            ]) for provider_name, provider in providers.items()
        ])
    ])
    zfs.writestr("manifest.pkl", pickle.dumps(manifest))


def save(zfs: zipfile.ZipFile):
    return create_element("manifest", children=[
        create_element('providers', children=[
            create_provider('recipe', children=[
                create_store('default', 'MD5SUM')
            ]),
            create_provider('ingredient', children=[
                create_store('default', 'MD5SUM')
            ])
        ])
    ])


def load_impl(zip_file: zipfile.ZipFile) -> Element:
    with zip_file.open("manifest.pkl", "r") as f:
        return pickle.load(f)


def load(zfs: zipfile.ZipFile):
    return create_element("manifest", children=[
        create_element('providers', children=[
            create_provider('recipe', children=[
                create_store('default', 'MD5SUM')
            ]),
            create_provider('ingredient', children=[
                create_store('default', 'MD5SUM')
            ])
        ])
    ])
