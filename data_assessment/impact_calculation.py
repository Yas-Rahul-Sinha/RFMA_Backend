import pandas as pd
from data_assessment.portfolio_info import *
market_research = pd.read_excel("data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="Market Research")
instrument_master_price = pd.read_excel("data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="Instrument Master Price")
merged = pd.merge(market_research,instrument_master_price, on="Security_Description")

def changeInAllInstrument():
    temp = []
    for ins, change, price in zip(merged["Security_Description"], merged["Change"], merged["Price-As of date"]):
        newPrice = price * (1 - change)
        temp.append(newPrice)
    merged["New_Price"] = temp.copy()
    temp.clear
    return merged[["Security_Description", "Category", "Type", "Change", "Symbol", "Price-As of date", "New_Price"]]

def changePerInstrument(instrument):
    data = changeInAllInstrument()
    return data.loc[data["Security_Description"] == instrument]

def impactOnPortfolio(account_no, instrument):
    total_market_value = getPortfolioMarketValue(account_no)
    changed_unit_market_value = int(changePerInstrument(instrument)["New_Price"])
    units = int(getInstrumentData(account_no,instrument)["Units"])
    market_value = int(getInstrumentData(account_no,instrument)["Market_Value"])
    impact = ((market_value-(units * changed_unit_market_value))/total_market_value) * 100
    return round(impact,2)

# print(impactOnPortfolio(1616655,"BlackRock, Inc."))
# print(getInstrumentData(2019065,"BlackRock, Inc.")["Market_Value"])

