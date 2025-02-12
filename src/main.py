import requests
import os
import urllib.parse

from bs4 import BeautifulSoup
from labels_mapper import labels_mapper
from tech_list import tech_list
from random import randint
from time import sleep
import sqlite3
import datetime
from db_utils import check_db

db_url = os.environ.get("DB_URL")
con = sqlite3.connect(db_url)
cur = con.cursor()

def db_insert(obj):
    print("OBJECT:", obj)
    table_name: str = "STATS"
    placeholders = ', '.join(['?'] * len(obj))
    columns = ', '.join(obj.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table_name, columns, placeholders)

    cur.execute(sql, list(obj.values()))

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

    # stats_obj = {'DATE': '2025-01-26', 'TECH': 'Python', 'ANY_TIME': 14014, 'PAST_MONTH': 8950, 'PAST_WEEK': 2319, 'PAST_24_HOURS': 110, 'FULL_TIME': 12584, 'PART_TIME': 416, 'CONTRACT': 416, 'TEMPORARY': 53, 'VOLUNTEER': 1, 'INTERNSHIP': 2227, 'ENTRY_LEVEL': 3712, 'ASSOCIATE': 1390, 'MID_SENIOR': 5110, 'DIRECTOR': 112, 'ON_SITE': 7005, 'HYBRID': 4600, 'REMOTE': 2065}

    db_insert(stats_obj)

def main():
    env = os.environ.get("ENV")
    bot_token = os.environ.get("BOT_TOKEN")
    bot_chat_id = os.environ.get("BOT_CHAT_ID")

    bot_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    print(f"Running in {env} mode")

    check_db(con)

    try:
        for i, tech in enumerate(tech_list):
            rand_time = randint(10, 30)
            sleep(rand_time)
            get_page_content(tech)

            if i == len(tech_list) - 1:
                job_finished_time = datetime.datetime.today().isoformat()
                con.commit()

                response = requests.get(bot_url, params={"chat_id": bot_chat_id, "text": f"All positions scraped on {job_finished_time}. Saved in {db_url} database."})

                if response.status_code == 200:
                    print("Message sent successfully!")
                else:
                    print("Failed to send message:", response.text)
    except Exception as e:
        response = requests.get(bot_url, params={"chat_id": bot_chat_id, "text": f"Error happened: {e}"})

        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print("Failed to send message:", response.text)

if __name__ == "__main__":
    main()