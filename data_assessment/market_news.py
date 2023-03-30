import pandas as pd
from data_assessment.main import portfolios

market = pd.read_excel('data/WM Manager Dashboard Data SetV2.xlsx', sheet_name='Market News')
advisor_list = ["Gunasiri", "Chris", "John", "Sukant"]
temp = []
adv_market_temp = {}
adv_market = {}
market = market.transpose()

for i in advisor_list:
    index = 0
    for j in portfolios["Advisor"]:
        if i == j and portfolios["Security_Description"][index] not in temp:
            temp.append(portfolios["Security_Description"][index])
        index+=1
    adv_market_temp[i] = temp.copy()
    temp.clear()
for advisor in adv_market_temp:
    for security in adv_market_temp[advisor]:
        for sec in market:
            if market[sec]["Description"] == security:
                market[sec]["Market_News_Date"] = str(market[sec]["Market_News_Date"])
                temp.append(market[sec].to_dict())
    adv_market[advisor] = temp.copy()
    temp.clear()
print(adv_market['Gunasiri'])



