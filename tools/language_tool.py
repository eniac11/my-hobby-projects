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
import json
import os
import pickle
from collections import namedtuple
from pprint import pprint

import requests

FALLBACK_LANGUAGE = "en-GB"
Category = namedtuple("Category", "id name")


class Rule:

    def __init__(self, data: dict):
        self.category = Category(data["category"]["id"], data["category"]["name"])
        self.description: str = data["description"]
        self.id: str = data["id"]
        self.issue: str = data["issueType"]


class MatchContext:

    def __init__(self, data: dict):
        self.text = data["text"]
        self.offset = int(data["offset"])
        self.length = int(data["length"])


class Match:

    def __init__(self, data: dict):
        # pprint(data)
        self.data = data
        self.message: str = data["message"]
        self.shortMessage: str = data["shortMessage"]
        self.offset = int(data["offset"])
        self.length = int(data["length"])
        self.replacements: list[str] = [replacement["value"] for replacement in data["replacements"]]
        self.rule = Rule(data["rule"])
        self.sentence: str = data["sentence"]
        self.type: str = data["type"]["typeName"]
        self.contextForSureMatch = int(data["contextForSureMatch"])

    def __str__(self):
        s = "Match\n"
        s += "Offset {}, Length {}, Rule: {}\n".format(self.offset, self.length, self.rule.id)
        s += "Message: {}\n".format(self.message)
        s += "Replacements: {}".format(', '.join(self.replacements))
        return s


class Language:

    def __init__(self, data: dict):
        self.name = data['name']
        self.code = data['code']
        self.detected_language = None
        if 'detectedLanguage' in data.keys():
            self.detected_language = Language(data['detectedLanguage'])


class CheckResponse:

    def __init__(self, data: dict):
        # print(json.dumps(data))
        # pprint(data)
        software = data['software']
        self.name = software["name"]
        self.version = float(software["version"])
        self.build_date = datetime.datetime.strptime(software["buildDate"], "%Y-%m-%d %H:%M:%S %z")
        # self.build_date = datetime.datetime.fromtimestamp(software["buildDate"])
        # self.build_date = software["buildDate"]
        self.api_version = int(software['apiVersion'])
        self.premium = software['premium']
        self.premium_hint = software["premiumHint"]
        self.status = software["status"]

        self.language = Language(data['language'])

        self.matches = [Match(match) for match in data['matches']]


class LanguageTool:

    def __init__(self, remote_address: str):
        self.remote_address = remote_address
        self.language = FALLBACK_LANGUAGE

    def make_request(self):
        pass

    def check(self, text):
        req = requests.get(self.remote_address + "/v2/check",
                           params={"language": self.language, "text": text, 'level': 'picky'})
        # print(req.text)
        # pprint(req.json())
        return [Match(match) for match in req.json()["matches"]]

    def check_full(self, text):
        req = requests.get(self.remote_address + "/v2/check", params={"language": self.language, "text": text})
        # print(req.text)
        return CheckResponse(req.json())


class MeaningfulMatch:

    def __init__(self, match: Match):
        self.match = match
        self.title, self.subtitle, self.description = self.process_message()

    def process_message(self):
        match = self.match
        if match.rule.id == "EN_A_VS_AN":
            return match.shortMessage, match.rule.description, match.message
        if match.rule.id == "UPPERCASE_SENTENCE_START":
            return match.rule.category.name, match.message, None
        if match.rule.id == "MORFOLOGIK_RULE_EN_GB":
            if match.rule.issue == 'misspelling':
                if match.rule.category.id == "TYPOS":
                    return match.rule.category.name, match.shortMessage, None
                return match.shortMessage, None, None
        if match.rule.id == "COMMA_COMPOUND_SENTENCE":
            return match.rule.description.capitalize(), None, match.message
        return match.message, match.shortMessage, None


def main():
    os.environ["NO_PROXY"] = "localhost"
    tool = LanguageTool('http://localhost:8081')

    # check_resp = tool.check_full("hello thsi has a error")
    # print(check_resp.name)
    # print(check_resp.version)
    # print(check_resp.build_date)
    # for match in check_resp.matches:
    #     print(match)

    matches = tool.check(
        "We stand up and walk to the window of our flat. A pterodactyl flies passed, and We watch it land on an air taxi pad transforming into an extremely gangly humanoid.")
    print(len(matches))
    match = matches[0]

    # print(MeaningfulMatch(match))

    processed_match = MeaningfulMatch(match)
    print(json.dumps(processed_match.match.data))
    print(match.sentence)
    print(processed_match.title)
    print(processed_match.subtitle)
    print(processed_match.description)
    print(', '.join(map(repr, processed_match.match.replacements)))


if __name__ == "__main__":
    main()
