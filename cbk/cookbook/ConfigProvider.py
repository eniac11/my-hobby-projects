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
import abc
import json
import zipfile
from dataclasses import dataclass, field
from typing import Optional, Literal

from cbk.cookbook.Stores import Provider, Store, StoredItem, T
from tools.htmls import Element


@dataclass
class ConfigItem:
    name: str
    _value: str
    accepted_values: list[Literal]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value in self.accepted_values:
            self._value = value
        else:
            raise ValueError(f'"{value}" not an accepted value. Value must be one of [{", ".join(self.accepted_values)}]')


class ConfigStore(Store[ConfigItem], abc.ABC):

    def get(self, *args, name: Optional[str] = None, **kwargs) -> StoredItem[ConfigItem]:
        if name is not None:
            for key, value in self.values.items():
                if value.name == name:
                    return StoredItem(self, key)

    @abc.abstractmethod
    def serialize(self) -> dict:
        pass


class DefaultConfig(ConfigStore):
    values: dict[ConfigItem]

    def __init__(self, name: str):
        super().__init__("default")
        self.add(ConfigItem('unit_system', 'imperial', ['imperial', 'metric']))

    def serialize(self) -> dict:
        config = {}
        for value in self.values.values():
            config[value.name] = value.value
        return config


class ConfigProvider(Provider[ConfigStore]):
    stores: list[ConfigStore]

    def __init__(self):
        super().__init__("config", DefaultConfig)

    def save(self, zip_file: zipfile.ZipFile):
        config = {}
        for config_store in self.stores:
            data = config_store.serialize()
            config[config_store.name] = data
        stringified_config = json.dumps(config)
        zip_file.writestr('conig.json', stringified_config)

    @classmethod
    def load(cls, zip_file: zipfile.ZipFile, provider_manifest: Element):
        raise NotImplementedError
