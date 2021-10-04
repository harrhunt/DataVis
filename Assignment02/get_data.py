from dnd_api import DND
import json
from os import path, makedirs

RESOURCE_TYPES = ["ability-scores", "skills", "proficiencies", "languages", "alignments", "backgrounds", "classes",
                  "subclasses", "features", "races", "subraces", "traits", "equipment-categories", "equipment",
                  "magic-items", "weapon-properties", "spells", "feats", "monsters", "conditions", "damage-types",
                  "magic-schools", "rules", "rule-sections"]


def save_all_data():
    for resource_type in RESOURCE_TYPES:
        save_all_resource_type(resource_type)


def save_all_resource_type(resource_type):
    filepath = f"data/{resource_type}"
    if not path.exists(filepath):
        makedirs(filepath)
    resources_list = DND.get_resource_list(resource_type)
    if resources_list is not None:
        for resource in resources_list:
            resource_data = DND.get_resource(resource_type, resource[0])
            if resource_data is not None:
                with open(f"{filepath}/{resource[0]}.json", "w") as file:
                    json.dump(resource_data, file)


if __name__ == '__main__':
    save_all_data()
