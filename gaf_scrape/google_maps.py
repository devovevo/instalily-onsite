import requests, os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAP_API_ENDPOINT=os.getenv("GOOGLE_MAP_API_ENDPOINT")
GOOGLE_MAP_QUERY_STRING_DEFAULT_PARAMS=os.getenv("GOOGLE_MAP_QUERY_STRING_DEFAULT_PARAMS")

def geo_info_from_postal(country_code: str, postal_code: int):
    return requests.get(url=f"{GOOGLE_MAP_API_ENDPOINT}?{GOOGLE_MAP_QUERY_STRING_DEFAULT_PARAMS}&components=postal_code:{postal_code}|country:{country_code}").json()["results"][0]