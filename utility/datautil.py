import random

import pandas as pd
from data_assessment.main import portfolios
# for i in portfolios["Investor Name"]:
#     print(i)
def randomProjection(current):
    range = random.uniform(-10, 20)
    return (current * ((100 + range) / 100))


df = pd.read_excel("data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="Instrument Master Price")
def fundProjection():
    fund_data = df[df["Instrument_Type"] == "FUND"]
    # print(fund_data)
    ret = {}
    temp = []
    rows = []
    # fund_projected_df = pd.DataFrame(columns=["Fund","Symbol","one_month","three_month","six_month","one_year","two_year","three_year"])
    for fund, symbol, j in zip(fund_data["Security_Description"], fund_data["Symbol"], fund_data["Price 12/31/2022"]):
        om = randomProjection(j)
        one_month = ((om - j) / j) * 100
        tm = randomProjection(om)
        three_month = ((tm - j) * 100) / j
        sm = randomProjection(tm)
        six_month = ((sm - j) * 100) / j
        oy = randomProjection(sm)
        one_year = ((oy - j) * 100) / j
        ty = randomProjection(oy)
        two_year = ((ty - j) * 100) / j
        thy = randomProjection(ty)
        three_year = ((thy - j) * 100) / j
        new_row = pd.DataFrame({"Fund": [fund], "Symbol": [symbol], "one_month": [round(one_month, 2)], "three_month": [round(three_month, 2)],"six_month": [round(six_month, 2)], "one_year": [round(one_year, 2)], "two_year": [round(two_year, 2)],"three_year": [round(three_year, 2)]})
        rows.append(new_row)
    fund_projected_df = pd.concat(rows)
    fund_projected = fund_projected_df.sort_values('three_year', ascending=False)
    for index,i in fund_projected.iterrows():
        temp.append({"Fund": i["Fund"], "Symbol": i["Symbol"], "one_month": i["one_month"], "three_month": i["three_month"],"six_month": i["six_month"], "one_year": i["one_year"], "two_year": i["two_year"],"three_year": i["three_year"]})
    ret["data"] = temp
    return ret
def fetchMarketValue(client, instrument):
    index = 0
    for cli in portfolios["Investor_Name"]:
        if cli == client and portfolios["Security_Description"][index] == instrument:
            return round(portfolios["Market_Value"][index],2)
        index+=1


def calculateMarketValue(client, instrument, input):
    index = 0
    type = input.split('%')
    current_market_value = fetchMarketValue(client, instrument)
    for cli in portfolios["Investor_Name"]:
        if cli == client and portfolios["Security_Description"][index] == instrument:
            if len(type) == 1:
                return round(current_market_value + float(input),2)
            elif len(type) == 2:
                return round(((float(type[0])/100)*current_market_value) + current_market_value,2)
            else:
                return "PLease Enter value in Proper Format"
        index+=1

def totalMarketValue(client):
    total_market_value = 0
    index=0
    for cli in portfolios["Investor_Name"]:
        if cli == client:
            total_market_value += portfolios["Market_Value"][index]
        index+=1
    return round(total_market_value,2)

def totalBookValue(client):
    total_book_value = 0
    index = 0
    for cli in portfolios["Investor_Name"]:
        if cli == client:
            total_book_value += portfolios["Account_Investment_Book_Value"][index]
        index += 1
    return round(total_book_value,2)

def newTotalMarketValue(client, instrument, input):
    current_total_market_value = totalMarketValue(client)
    current_instrument_market_value = fetchMarketValue(client,instrument)
    new_instrument_market_value = calculateMarketValue(client,instrument,input)
    return round(current_total_market_value-current_instrument_market_value+new_instrument_market_value,2)

def clientTotalValueAnalysis(book_value,old_value,new_value):
    res = {}
    market_value_change = round(((new_value-old_value)/old_value)*100,2)
    original_market_to_book_value = round(((old_value-book_value)/book_value)*100,2)
    new_market_to_book_value = round(((new_value-book_value)/book_value)*100,2)
    res["market_value_change"] = market_value_change
    res["original_market_to_book_value"] = original_market_to_book_value
    res["new_market_to_book_value"] = new_market_to_book_value
    return res

def overallCalculations(data):
    cmv = []
    nmv = []
    ctmv = totalMarketValue(data[0]['client'])
    ctbv = totalBookValue(data[0]['client'])
    for i in data:
        cmv.append(fetchMarketValue(i['client'], i['instrument']))
        nmv.append(calculateMarketValue(i['client'], i['instrument'], i['input']))
    dmv = [a - b for a, b in zip(nmv, cmv)]
    ocmv = sum(dmv)
    ntmv = ctmv + ocmv
    percent_change_mv = round((ocmv/ctmv)*100,2)
    nmv_to_bv = round(((ntmv-ctbv)/ctbv)*100,2)
    res = {'percent_change_mv':percent_change_mv, 'nmv_to_bv':nmv_to_bv}
    return res

def fetchMarketValuePercentage(client, instrument):
    totalMV = totalMarketValue(client)
    instrumentMV = fetchMarketValue(client,instrument)
    return round(((instrumentMV/totalMV)*100),2)

def percentageImpact(market_value, projected_value):
    if market_value != 0:
        return round((((projected_value-market_value)/market_value)*100),2)
    else:
        return 0

def getClientForInstrument(instrument, advisor):
    filter_df = portfolios[portfolios["Security_Description"] == instrument]
    filter_df = filter_df[filter_df["Advisor"] == advisor]
    # print(filter_df[["Investor_Name","Investor_Type_Desc","Account","Security_Description", "Account_Investment_Book_Value", "Market_Value"]])
    return filter_df[["Investor_Name","Investor_Type_Desc","Account","Security_Description", "Account_Investment_Book_Value", "Market_Value"]]

def impactOnAccount(account, instrument, projected_market_value):
    data = portfolios[portfolios["Account"] == account]
    index = data.index
    total_market_value = data["Market_Value"].sum()
    currrent_market_value = fetchMarketValue(data["Investor_Name"][index[0]],instrument)
    diff = projected_market_value - currrent_market_value
    percentage_impact = (diff/total_market_value)*100
    return round(percentage_impact,3)
def marketSignalImpact(instrument, advisor, input):
    data = getClientForInstrument(instrument,advisor)
    index = data.index
    pointer = 0
    temp = {}
    return_data = []
    for i in data["Investor_Name"]:
        projected_value = calculateMarketValue(i, instrument, input)
        if projected_value > data["Market_Value"][index[pointer]]:
            up_down = "Up"
        elif projected_value < data["Market_Value"][index[pointer]]:
            up_down = "Down"
        else:
            up_down = "No Impact"
        percentage_impact = impactOnAccount(data["Account"][index[pointer]],instrument,projected_value)
        temp["Investor_Name"] = i
        temp["Account"] = data["Account"][index[pointer]]
        temp["Market_Value"] = data["Market_Value"][index[pointer]]
        temp["Projected_Value"] = projected_value
        temp["upDownIndicator"] = up_down
        temp["Percentage_Impact"] = str(percentage_impact) + "%"
        return_data.append(temp.copy())
        pointer+=1
    return {"data": return_data}

def getAdvisorInstruments(advisor):
    df = portfolios[portfolios["Advisor"] == advisor]
    instruments = []
    for ins in df["Security_Description"]:
        if ins not in instruments:
            instruments.append(ins)
    return {advisor: instruments}

def getInstrumentData():
    ret = {}
    for index,i in df.iterrows():
        ret[i["Security_Description"]] = {"Symbol":i["Symbol"], "12/31/2018":i["Price 12/31/2018"], "12/31/2019":i["Price 12/31/2019"], "12/31/2020":i["Price 12/31/2020"], "12/31/2021":i["Price 12/31/2021"], "03/31/2022":i["Price 03/31/2022"], "06/30/2022":i["Price 06/30/2022"], "09/30/2022":i["Price 09/30/2022"], "12/31/2022":i["Price 12/31/2022"], "Price-As of date":i["Price-As of date"]}
    return ret

