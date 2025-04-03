#!/usr/bin/env python3
import time
from scrape_db import db
from tasks import summarize_and_crawl_webpage

while True:
    next_subpage_to_crawl = db.pop_subpage_queue()
    while next_subpage_to_crawl:
        contractor_id, link = next_subpage_to_crawl
        summarize_and_crawl_webpage.delay(contractor_id, link)

        print(f"Queued the crawling of website {link} from contractor {contractor_id}")

        next_subpage_to_crawl = db.pop_subpage_queue()

    time.sleep(5)