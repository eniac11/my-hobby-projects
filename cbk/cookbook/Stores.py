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

import abc
import hashlib
import pickle
import uuid
import weakref
import zipfile
from pathlib import Path
from typing import Generic, TypeVar, Generator, Optional




from tools.htmls import Element, Transform

T = TypeVar("T")


class Store(abc.ABC, Generic[T]):

    def __init__(self, name: str):
        self.name = name
        self.values: dict[str, T] = {}

    def get_by_id(self, id_: str) -> T:
        return self.values[id_]

    @abc.abstractmethod
    def get(self, *args, **kwargs) -> StoredItem[T]:
        pass

    def add(self, item: T):
        self.values[str(uuid.uuid4())] = item

    def __iter__(self) -> Generator[StoredItem[T]]:
        for key in self.values.keys():
            yield StoredItem(self, key)


class StoredItem(Generic[T]):

    def __init__(self, store: Store, id_: str):
        self.store = store
        self.id = id_

    def get(self) -> T:
        return self.store.get_by_id(self.id)


S = TypeVar("S", bound=Store)


class Provider(Generic[S]):

    def __init__(self, provider_name: str, default_store_factory: type[Store]):
        self.provider_name = provider_name
        self.stores: list[Store] = [default_store_factory("default")]

    def get_by_id(self, id_: str) -> T:
        for store in self.stores:
            if value := store.get_by_id(id_):
                return value

    def get(self, *args, store_name: Optional[str] = None, **kwargs) -> StoredItem[T]:
        if store_name is not None:
            if value := self[store_name].get(*args, **kwargs):
                return value
        for store in self.stores:
            if value := store.get(*args, **kwargs):
                return value

    def add(self, item: T, store_name="default"):
        if store_name == "default":
            self.stores[0].add(item)
        else:
            self[store_name].add(item)

    def register_store(self, store: S):
        self.stores.append(store)

    def __getitem__(self, store_name: str):
        for store in self.stores:
            if store_name == store.name:
                return store
        raise IndexError(f"'{store_name}' is not a valid index")

    def __iter__(self) -> Generator[StoredItem[T]]:
        for store in self.stores:
            for item in store:
                yield item

    def save(self, zip_file: zipfile.ZipFile):
        manifest = []
        for store in self.stores:
            dump = pickle.dumps(store)
            zip_file.writestr('stores/' + self.provider_name + '/' + store.name, dump)
            md5 = hashlib.md5(dump).hexdigest()
            manifest.append((store.name, md5))
        return manifest


    @classmethod
    def load(cls, zip_file: zipfile.ZipFile, provider_manifest: Element):
        stores = []
        for store_fest in provider_manifest.get_elements_by_name('store'):
            stores.append(pickle.load(
                zip_file.open('stores/' + provider_manifest.kwargs['name'] + '/' + store_fest.kwargs['name'])))
        provider = Provider(provider_manifest.kwargs['name'], lambda name: None)
        provider.stores = stores
        return provider
