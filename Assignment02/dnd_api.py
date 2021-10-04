import requests


class DND:
    base_url = "https://www.dnd5eapi.co/api/"

    @classmethod
    def _query(cls, endpoint):
        r = requests.get(f"{cls.base_url}{endpoint}")
        if r.status_code != 200:
            print(endpoint, r.status_code)
            return None
        return r.json()

    @classmethod
    def get_resource_list(cls, resource, keep_raw=False):
        raw = cls._query(resource)
        if keep_raw or raw is None:
            return raw
        return [(result["index"], result["name"], result["url"]) for result in raw["results"]]

    @classmethod
    def get_resource(cls, res_type, res_index):
        raw = cls._query(f"{res_type}/{res_index}")
        return raw
