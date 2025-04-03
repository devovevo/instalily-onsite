import requests, os, random
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from uuid import uuid4

from common import DUMMY_USER_AGENTS

load_dotenv()

GAF_CONTRACTORS_API_ENDPOINT=os.getenv("GAF_CONTRACTORS_API_ENDPOINT")
GAF_CONTRACTORS_API_KEY=os.getenv("GAF_CONTRACTORS_API_KEY")
GAF_CONTRACTORS_QUERY_STRING_DEFAULT_PARAMS=os.getenv("GAF_CONTRACTORS_QUERY_STRING_DEFAULT_PARAMS")

def residential_contractors_near_lat_long(latitude: float, longitude: float, distance: int, num_results: int):
    headers = {
        "Authorization": f"Bearer {GAF_CONTRACTORS_API_KEY}",
        "Content-Type": "application/json",
        'User-Agent': random.choice(DUMMY_USER_AGENTS)
    }

    visitor_id = str(uuid4())
    payload = {
        "locale":"en-US",
        "debug":False,
        "tab":"default",
        "referrer":"none",
        "timezone":"America/New_York",
        "visitorId":visitor_id,
        "actionsHistory":[],
        "aq":f"@distanceinmiles <= {distance} AND @gaf_f_country_code = USA",
        "context":{
            "sortingStrategy":"gafrecommended-initial"
        },
        "fieldsToInclude":[
            "author",
            "language",
            "urihash",
            "objecttype",
            "collection",
            "source",
            "permanentid",
            "gaf_featured_image_src",
            "gaf_featured_image_alt",
            "gaf_contractor_id",
            "gaf_contractor_type",
            "gaf_contractor_dba",
            "gaf_navigation_title",
            "gaf_rating",
            "gaf_number_of_reviews",
            "gaf_f_city",
            "gaf_f_state_code",
            "gaf_f_contractor_certifications_and_awards",
            "gaf_phone",
            "uri",
            "gaf_f_contractor_technologies",
            "gaf_latitude",
            "gaf_longitude",
            "distance",
            "distanceinmiles",
            "gaf_postal_code",
            "gaf_f_country_code",
            "gaf_enrolled_in_gaf_leads",
            "UniqueId",
            "Uri"
        ],
        "pipeline":"prod-gaf-recommended-residential-contractors",
        "q":"",
        "enableQuerySyntax":True,
        "searchHub":"prod-gaf-recommended-residential-contractors",
        "sortCriteria":"relevancy",
        "analytics":{
            "clientId":visitor_id,
            "clientTimestamp":datetime.now().isoformat(),
            "documentReferrer":"none",
            "originContext":"Search",
            "actionCause":"interfaceChange",
            "customData":{
                "context_sortingStrategy":"gafrecommended-initial",
                "coveoHeadlessVersion":"2.19.0","interfaceChangeTo":"default"
                }
        },
        "facets":[
            {
                "filterFacetCount":True,
                "injectionDepth":1000,
                "numberOfValues":999,
                "sortCriteria":"automatic",
                "type":"specific",
                "currentValues":[],
                "freezeCurrentValues":False,
                "isFieldExpanded":True,
                "preventAutoSelect":False,
                "field":"gaf_f_contractor_technologies",
                "facetId":"gaf_f_contractor_technologies"
            },
            {
                "filterFacetCount":True,
                "injectionDepth":1000,
                "numberOfValues":4,
                "sortCriteria":"descending",
                "rangeAlgorithm":"even",
                "currentValues":[
                    {
                        "start":4,
                        "end":5,
                        "endInclusive":True,
                        "state":"idle"
                    },
                    {
                        "start":3,
                        "end":5,
                        "endInclusive":True,
                        "state":"idle"
                    },
                    {
                        "start":2,
                        "end":5,
                        "endInclusive":True,
                        "state":"idle"
                    },
                    {
                        "start":1,
                        "end":5,
                        "endInclusive":True,
                        "state":"idle"
                    }
                ],
                "preventAutoSelect":False,
                "type":"numericalRange",
                "field":"gaf_rating",
                "generateAutomaticRanges":False,
                "facetId":"gaf_rating"
            },
            {
                "filterFacetCount":True,
                "injectionDepth":1000,
                "numberOfValues":0,
                "sortCriteria":"ascending",
                "rangeAlgorithm":"even",
                "currentValues":[],
                "preventAutoSelect":False,
                "type":"dateRange",
                "field":"date",
                "generateAutomaticRanges":False,
                "facetId":"date"
            }
        ],
        "numberOfResults":num_results,
        "firstResult":0,
        "facetOptions":{
            "freezeFacetOrder":False
        },
        "queryFunctions":[
            {
                "fieldName":"@distanceinmiles",
                "function":f"dist(@gaf_latitude, @gaf_longitude, {latitude}, {longitude})*0.000621371"
            }
        ]
    }

    return requests.post(url=GAF_CONTRACTORS_API_ENDPOINT, headers=headers, json=payload).json()["results"]

def scrape_contractor_page(page_url: str):
    headers = {
        "User-Agent": random.choice(DUMMY_USER_AGENTS)
    }
    page = requests.get(url=page_url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    link_elem = soup.find("div", class_="image-masthead-carousel__links")
    website_link = link_elem.find("a").get("href")
    info = {
        "name": soup.find("h1", class_="image-masthead-carousel__heading").string,
        "address": soup.find("address", class_="image-masthead-carousel__address").string,
        "url": website_link if website_link[:3] != "tel" else None,
        "phone_number": link_elem.find("a", class_="link--icon-left").get("href"),
        # "summary": soup.find("div", class_="about-us-block__description").find("p").text,
        "business_since": soup.find("p", class_="contractor-details__description").string,
        # "id": soup.find_all("p", class_="contractor-details__description")[1].string
    }

    return info