# Crawl_branch_data
### 透過scrapy+selenium爬取玩股網券商分點資訊
## 流程 ：
1. 透過selenium登錄網站，並獲取cookies
2. 透過cookies進行request
3. 擷取分點卷商資訊json
4. pipline到mogodb資料庫中
## 使用：

```
cd Crawl_branch_data

scrapy crawl branch_buy_sell -a start_year="2021-06-01" -a end_year="2021-06-05" -a stock_id="2330"

```
