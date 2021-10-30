import pandas as pd
import praw
import pandas
import re
import matplotlib.pyplot as plt

stock = re.compile(r'[$]{1}[A-Za-z]{1,3}[\S]')

reddit = praw.Reddit(
    client_id="00wQAtulyk-i0LshRWLtHw",
    client_secret="6lJ2xCCV4ROOpumH6CUI9vKvXr-HQw",
    user_agent="reddit stock market scraper",
    username="Hydraphellian",


)

def tickersArray():
    stockArray = []

    for submission in reddit.subreddit("wallstreetbets").hot(limit=1000):
        if stock.search(submission.title):
            ticker = re.findall(stock, submission.title)
            for element in ticker:
                stockTick = str(element)
                if not stockTick.endswith(")"):
                    if not stockTick.endswith("."):
                        stockTick = stockTick.upper()
                        stockArray.append(stockTick)

    for submission in reddit.subreddit("stocks").hot(limit=1000):
        if stock.search(submission.title):
            ticker = re.findall(stock, submission.title)
            for element in ticker:
                stockTick = str(element)
                if not stockTick.endswith(")"):
                    if not stockTick.endswith("."):
                        stockTick = stockTick.upper()
                        stockArray.append(stockTick)

    return stockArray



def arrayToMap(stockArray):
    stockMap = {}

    for ticker in stockArray:
        if ticker not in stockMap:
            stockMap[ticker] = 1
        else:
            stockMap[ticker] += 1


    stockItems = stockMap.items()
    stockList = list(stockItems)
    stockDf = pd.DataFrame(stockList)

    return stockDf

barMap = arrayToMap(tickersArray())

stocksSorted = barMap.sort_values(1, ascending=False)

stocksSorted[0:10].plot(kind = 'bar',
                  x = 0,
                  y = 1,
                  color = 'purple'
                  )
plt.title("Current Hottest Stocks on Reddit")
plt.xlabel("Stock Tickers")
plt.ylabel("Times Mentioned")
plt.savefig("stockBarPlot.png")
plt.show()
print(stocksSorted)

