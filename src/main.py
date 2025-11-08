import requests
import os
import urllib.parse

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from labels_mapper import labels_mapper
from db_utils import db_insert
from tech_list import tech_list
from random import randint
from time import sleep
import datetime
from loguru import logger as log

load_dotenv()


def get_data_by_label_id(soup, label_id: str) -> str:
    return soup.find("label", {"for": label_id}).getText().split('(', 1)[1].split(')')[0]

def get_page_content(tech: str):
    today = datetime.datetime.today().isoformat()

    stats_obj = {
        "DATE": today,
        "TECH": tech
    }

    target_url='https://www.linkedin.com/jobs/search?keywords="{tech}"&location=Germany&geoId=101282230&position=1&pageNum=0'
    res = requests.get(target_url.format(tech=urllib.parse.quote(tech)))

    soup=BeautifulSoup(res.text, 'html.parser')

    # Show raw results of page parsing. Uncomment below for debugging purposes if it cannot get the numbers
    # filter_values_container = soup.find_all("div", {"class": "filter-values-container__filter-value"})
    # print("HTML RESULT:", filter_values_container)

    for key, value in labels_mapper.items():
        try:
            scraped_value = get_data_by_label_id(soup, value)
            no_commas_value = int(scraped_value.replace(",", ""))

            stats_obj[key] = no_commas_value
        except:
            stats_obj[key] = None

    # stats_obj = {'DATE': '2025-08-24 21:03:43.436971', 'TECH': 'Python', 'ANY_TIME': 14014, 'PAST_MONTH': 8950, 'PAST_WEEK': 2319, 'PAST_24_HOURS': 110, 'FULL_TIME': 12584, 'PART_TIME': 416, 'CONTRACT': 416, 'TEMPORARY': 53, 'VOLUNTEER': 1, 'INTERNSHIP': 2227, 'ENTRY_LEVEL': 3712, 'ASSOCIATE': 1390, 'MID_SENIOR': 5110, 'DIRECTOR': 112, 'ON_SITE': 7005, 'HYBRID': 4600, 'REMOTE': 2065}

    return stats_obj

def main():
    env = os.environ.get("ENV")
    db_url = os.getenv("DB_URL", env)
    bot_token = os.getenv("BOT_TOKEN", env)
    bot_chat_id = os.getenv("BOT_CHAT_ID", env)
    bot_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    log.info(f"Running in {env} mode")

    try:
        for i, tech in enumerate(tech_list):
            rand_time = randint(10, 30)
            sleep(rand_time)
            technology_stats_object = get_page_content(tech)
            db_insert(technology_stats_object, db_url)

            if i == len(tech_list) - 1:
                job_finished_time = datetime.datetime.today().isoformat()
                response = requests.get(bot_url, params={"chat_id": bot_chat_id, "text": f"All positions scraped on {job_finished_time}"})

                if response.status_code == 200:
                    print("Message sent successfully!")
                else:
                    print("Failed to send message:", response.text)
    except Exception as e:
        response = requests.get(bot_url, params={"chat_id": bot_chat_id, "text": f"Error happened: {e}"})

        if response.status_code == 200:
            print("Error Message sent successfully!")
        else:
            print("Error message send Failed:", response.text)

if __name__ == "__main__":
    main()