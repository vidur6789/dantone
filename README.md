# Dantone
Data Scraping Project

## Main Scripts

### ScrapeData

Scrapes key ratio data from morningstar and saves in a json format.
Refer to notebooks/MstarDataUsage.ipynb for data usage examples. 

Key points:
1. Specify the list of tickers to scrape in input/Stocklist.xlsx File path/type can be modified in ScrapeData.py
2. Monitor logs/logs.txt for status updates, errors. 
3. On completion of script, #scraped, #pending, #errors printed in logs/progress. Results saved in output/Results-[timestamp].json
4. logs/pending contains list of tickers where error occured. ScrapeData.py first checks for pending stocks in logs/pending before loading StockList.xlsx


### MergeData

Two key standalone functionalities:
1. accumulate_results - Accumulate all result json files in a given directory into a single json results file. 
2. merge_attributes - Merge key stats and fin stats into a single json object/dict for all the stocks in a result file. 
