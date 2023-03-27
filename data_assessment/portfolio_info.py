import math

from data_assessment.main import portfolios
def getPortfolioData(account_no):
    port = portfolios[portfolios["Account"] == account_no]
    return port

def getInstrumentData(account_no,instrument):
    data = getPortfolioData(account_no)
    return data.loc[data["Security_Description"] == instrument]

def getPortfolioMarketValue(account_no):
    port = getPortfolioData(account_no)
    sum = 0
    for val in port["Market_Value"]:
        if not math.isnan(val):
            sum += val
    return sum

def getPortfolioMarketValueAtTime(account_no, time):
    port = getPortfolioData(account_no)
    sum = 0
    for val in port[time]:
        if not math.isnan(val):
            sum += val
    return sum

def getPortfolioBookValue(account_no):
    port = getPortfolioData(account_no)
    sum = 0
    for val in port["Account_Investment_Book_Value"]:
        if not math.isnan(val):
            sum += val
    return sum

def accountOwner(account_no):
    port = portfolios[portfolios["Account"] == account_no]
    investor = port["Investor_Name"]
    return investor.iloc[0]

def performanceAnalysis(account_no, time1, time2):
    port = portfolios[portfolios["Account"] == account_no]
    current_market_value = port[time1].sum()
    previous_market_value = port[time2].sum()
    diff = current_market_value-previous_market_value
    impact = (diff/previous_market_value) * 100
    return impact

def getClientList(advisor):
    port = portfolios[portfolios["Advisor"] == advisor]
    return port["Investor_Name"].unique()

def getClientTotalInvestment(client):
    port = portfolios[portfolios["Investor_Name"] == client]
    return port["Market_Value"].sum()
