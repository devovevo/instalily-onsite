import requests, os, random
from dotenv import load_dotenv

from common import DUMMY_USER_AGENTS

load_dotenv()

GAF_REVIEWS_API_ENDPOINT=os.getenv("GAF_REVIEWS_API_ENDPOINT")
GAF_REVIEWS_QUERY_STRING_DEFAULT_PARAMS=os.getenv("GAF_REVIEWS_QUERY_STRING_DEFAULT_PARAMS")

def scrape_contractor_reviews(id: str, num_reviews: int):
    headers = {
        "User-Agent": random.choice(DUMMY_USER_AGENTS)
    }

    url = f"{GAF_REVIEWS_API_ENDPOINT}/{id}?{GAF_REVIEWS_QUERY_STRING_DEFAULT_PARAMS}&pagesize={num_reviews}"

    return requests.get(url=url, headers=headers).json()