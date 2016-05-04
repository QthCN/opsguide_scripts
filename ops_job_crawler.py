# 用于从拉钩网上抓取和运维相关职位的职位要求和职位标题

import json
import re
import time

import requests

POSITIONS_LIST_URL_TEMPLATE = "http://www.lagou.com/jobs/positionAjax.json?" \
                              "city=全国&first=false&kd={kw}&pn={pn}"
POSITION_DETAIL_TEMPLATE = "http://www.lagou.com/jobs/{position_id}.html"
TOTAL_PAGES = 20
KW = ["运维", "DBA", "网络工程师", "系统工程师", "IT支持", "IDC",
      "CDN", "F5", "系统管理员", "病毒分析", "WEB安全", "网络安全",
      "系统安全"]
OUTPUT_NAME = "运维类职位信息.txt"
OUTPUT_COLS = ("职位名称", "职位说明")
OUTPUT_COLS_SPLIT_TOKEN = "$$$$"
OUTPUT_ROWS_SPLIT_TOKEN = "@@@@"


def save_data(position_name, jd):
    with open(OUTPUT_NAME, "a") as f:
        row = "{pn}{ct}{jd}{rt}".format(
            pn=position_name,
            ct=OUTPUT_COLS_SPLIT_TOKEN,
            jd=jd,
            rt=OUTPUT_ROWS_SPLIT_TOKEN
        )
        row = row.replace("\n", "").replace("\r", "")
        f.write(row)


def sleep(s=5):
    time.sleep(s)


def crawl_simple_html(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response.content
    except Exception as e:
        raise


def get_jd(html):
    jd = ""
    get_it = False
    try:
        for line in html.split("\n"):
            if get_it or "job_bt" in line:
                get_it = True
                jd += line
            if "</dd>" in line:
                get_it = False
    except Exception as e:
        print(e)
        jd = ""
    return re.compile(r"<[^>]+>")\
             .sub(" ", jd)\
             .replace("\n", " ")\
             .replace("\r", " ")


def do_crawl(kw):
    for pn in range(1, TOTAL_PAGES):
        try:
            position_list_url = POSITIONS_LIST_URL_TEMPLATE.format(pn=pn,
                                                                   kw=kw)
            position_list = crawl_simple_html(position_list_url)
            if position_list is None:
                continue
            position_list = json.loads(position_list.decode("utf-8"))
            positions = position_list["content"]["result"]

            for position in positions:
                position_id = position["positionId"]
                position_name = position["positionName"]
                print("正在抓取{pid} {pname}的信息...".format(
                    pid=position_id, pname=position_name))
                position_detail_url = POSITION_DETAIL_TEMPLATE.format(
                    position_id=position_id)
                position_detail_html = crawl_simple_html(
                    position_detail_url).decode("utf-8")
                jd = get_jd(position_detail_html)
                save_data(position_name, jd)
                sleep(1)
            sleep(3)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    for kw in KW:
        print("正在抓取 {kw} 的信息...".format(kw=kw))
        do_crawl(kw)
