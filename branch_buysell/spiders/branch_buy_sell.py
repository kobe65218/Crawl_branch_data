import scrapy
import urllib
import json
import pandas as pd
from selenium import webdriver
import time
import numpy as np
import datetime
class BranchBullSell(scrapy.Spider):

    name = "branch_buy_sell"
    # 透過selenium登錄網站,並獲取cookies
    def login(self):
        driver = webdriver.Chrome()
        driver.get("https://www.wantgoo.com/")
        driver.find_element_by_css_selector("a#aLogin").click()
        driver.find_element_by_css_selector("input#idUserName").send_keys("shine655218@gmail.com")
        driver.find_element_by_css_selector("input#idPassword").send_keys("kobe910018")
        driver.find_element_by_css_selector("button#btnLogIn").click()
        time.sleep(3)
        return driver.get_cookies()

    def start_requests(self):
        cookies = self.login()
        start_time = self.start_year
        end_time = self.end_year
        stock_id = self.stock_id
        # creat date
        all_day = np.arange(start_time,end_time , dtype = "M8[D]")
        # not include holiday
        busy_day = np.is_busday(np.arange(start_time,end_time , dtype = "M8[D]"))
        times = all_day[busy_day]

        for time in times:
            url = f"https://www.wantgoo.com/stock/{stock_id}/major-investors/branch-buysell-data?isOverBuy=true&endDate={time}&beginDate={time}&v=326177"
            yield scrapy.Request(url = url , cookies = cookies,dont_filter=True , cb_kwargs=dict( id=stock_id, t=time) )
    def parse(self,response , id , t):
        branch_data = json.loads(response.text)
        branch_df = pd.DataFrame(branch_data["data"])
        branch_df.set_index(branch_df["agentName"] , inplace=True )
        branch_df.rename(columns={"buyQuantities" : "(buy)" , "sellQuantities": "(sell)" } , inplace=True)
        branch_df = branch_df[["(buy)","(sell)"]].stack()
        branch_df.index = branch_df.index.get_level_values(0) + branch_df.index.get_level_values(1)
        branch_dict = branch_df.to_dict()
        branch_dict["stock_id"] = id
        branch_dict["time"] = datetime.datetime.strptime(t.astype(str),"%Y-%m-%d")
        return branch_dict