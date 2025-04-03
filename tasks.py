import os

from celery import Celery
from datetime import datetime
from dotenv import load_dotenv

from subpage_scrape import subpage
from scrape_db import db
from agents import insights

load_dotenv()

REDIS_HOST=os.getenv("REDIS_HOST")
REDIS_PORT=os.getenv("REDIS_PORT")
REDIS_DB_ID=os.getenv("REDIS_DB_ID")

app = Celery("tasks", broker_url=f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_ID}")

@app.task
def summarize_and_crawl_webpage(contractor_id: str, url: str):
    db.add_contractor_subpage(contractor_id, url)

    text_list, link_list = subpage.scrape(url)
    analysis = insights.gen("\n".join(text_list))

    db.set_subpage_info(url, {
        "analysis": analysis,
        "date": datetime.now().isoformat()
    })

    for link in link_list:
        db.push_subpage_queue(contractor_id, link)
    
    return True