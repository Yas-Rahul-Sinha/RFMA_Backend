from data_assessment.client_instrument import adv_investor_investments
from utility.datautil import *
from data_assessment.main import portfolios


weights = [1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,12,10,10,10,12,12,10,12,11,11,10,11,10,10,10,9,8,7,6,5,4]
projected_value = random.choices(range(-20,21), weights=weights, k=1)
# print(projected_value)

def getClientAccounts(advisor):
    data = portfolios[portfolios["Advisor"] == advisor]
    accounts = data["Account"].unique()
    return accounts

def getAccountInstruments(account_no):
    data = portfolios[portfolios["Account"] == account_no]
    return data["Security_Description"].unique()


def getAccountPortfolio(advisor, investor, account):
    K = len(adv_investor_investments[advisor][investor][account])
    projection = random.choices(range(-20,21), weights=weights, k=K)
    print(projection)
    temp = {}
    portfolio_data = {}
    temp2 = []
    index = 0
    total_market_value = 0
    total_projected_value = 0
    updn = ""
    for i in adv_investor_investments[advisor][investor][account]:
        temp['Description'] = i['Description']
        temp['Instrument_Type'] = i['Instrument_Type']
        temp['Market_Value'] = i['Market_Value']
        # print(str(projection[index])+'%')
        temp['Projected_Value'] = calculateMarketValue(investor, i['Description'], str(projection[index])+'%')
        if temp['Market_Value'] > temp['Projected_Value']:
            temp['upDownIndicator'] = 'Down'
        elif temp['Market_Value'] < temp['Projected_Value']:
            temp['upDownIndicator'] = 'Up'
        else:
            temp['upDownIndicator'] = 'No Impact'
        temp['Percentage_Impact'] = str(percentageImpact(temp['Market_Value'], temp['Projected_Value'])) + "%"
        # portfolio_data[i['Description']] = temp.copy()
        temp2.append(temp.copy())
        total_market_value += temp['Market_Value']
        total_projected_value += temp['Projected_Value']
        index+=1
    if total_projected_value > total_market_value:
        updn = 'Up'
    elif total_market_value > total_projected_value:
        updn = "Down"
    else:
        updn = "No Impact"
    temp['Description'] = "Total"
    temp['Instrument_Type'] = "Total"
    temp['Market_Value'] = total_market_value
    temp['Projected_Value'] = total_projected_value
    temp['upDownIndicator'] = updn
    temp['Percentage_Impact'] = str(percentageImpact(total_market_value, total_projected_value)) + "%"
    temp2.append(temp.copy())

    portfolio_data["data"] = temp2.copy()
    return portfolio_data


