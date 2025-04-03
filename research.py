import time
from agents import insights
from datetime import datetime
from gaf_scrape import gaf_contractors, google_maps
from scrape_db import db

def research_contractors_by_postal_code(country_code: str, postal_code: int, distance: int, num_contractors: int):
    lat, long = google_maps.geo_info_from_postal(country_code, postal_code)["geometry"]["location"].values()
    contractor_search_results = gaf_contractors.residential_contractors_near_lat_long(lat, long, distance, num_contractors)

    researched_contractor_ids = []

    for contractor in contractor_search_results:
        contractor_info = contractor
        contractor_id = contractor_info["raw"]["gaf_contractor_id"]

        now = datetime.now()
        if db.get_contractor_info(contractor_id) == {} or (now - datetime.fromisoformat(db.get_contractor_info(contractor_id)["date"])).days > 5:
            
            contractor_page_info = gaf_contractors.scrape_contractor_page(contractor_info["uri"])
            contractor_info["website"] = contractor_page_info["url"]

            contractor_info["date"] = now.isoformat()

            if contractor_info["website"] is not None:
                db.add_contractor_subpage(contractor_id, contractor_info["website"])

            db.set_contractor_info(contractor_id, contractor_info)

        for subpage in db.get_contractor_subpages(contractor_id):
            if db.get_subpage_info(subpage) == {} or (now - datetime.fromisoformat(db.get_subpage_info(subpage)["date"])).days > 5:
                db.push_subpage_queue(contractor_id, subpage)

        researched_contractor_ids.append(contractor_id)

    return researched_contractor_ids

def insights_for_contractor(contractor_id: str):
    if db.get_contractor_info(contractor_id) == {}:
        print("Contractor has not yet been found!")
        return
    
    if not db.get_contractor_subpages(contractor_id):
        print("Contractor has no website, so can't get insights!")
        return
    
    subpages = db.get_contractor_subpages(contractor_id)

    now = datetime.now()
    for subpage in subpages:
        if db.get_subpage_info(subpage) == {} or (now - datetime.fromisoformat(db.get_subpage_info(subpage)["date"])).days > 5:
            db.push_subpage_queue(contractor_id, subpage)

    while db.get_subpage_queue().intersection(subpages):
        time.sleep(5)

    insight_list = [db.get_subpage_info(url) for url in db.get_contractor_subpages(contractor_id)]
    batched_insight_list = [insight_list[i: i + 5] for i in range(0, len(subpages), 5)]

    while len(batched_insight_list) > 1:
        insight_list = []

        for batched_insight in batched_insight_list:
            combined_insight = insights.gen("\n".join(batched_insight))
            insight_list.append(combined_insight)

        batched_insight_list = [insight_list[i: i + 5] for i in range(0, len(subpages), 5)]

    return batched_insight_list[0]