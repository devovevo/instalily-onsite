#!/usr/bin/env python3
from research import research_contractors_by_postal_code, insights_for_contractor
from tasks import summarize_and_crawl_webpage
from subpage_scrape import subpage

from scrape_db import db

contractor_ids = research_contractors_by_postal_code("us", 10013, 50, 50)