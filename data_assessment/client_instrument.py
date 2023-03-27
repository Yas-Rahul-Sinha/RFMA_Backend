from data_assessment.main import portfolios
from data_assessment.main import advisor
from utility.datautil import fetchMarketValuePercentage

adv_investor_investments = {}
investor_investments = {}
temp1 = []
temp2 = {}
temp3 = {}
for adv in advisor:
    for inv in advisor[adv]:
        index = 0
        for investor in portfolios["Investor_Name"]:
            if inv["Investor"] == investor:
                temp2["Instrument_Type"] = portfolios["Instrument_Type"][index]
                temp2["Description"] = portfolios["Security_Description"][index]
                temp2["Units"] = portfolios["Units"][index]
                temp2["Market_Value"] = round(portfolios["Market_Value"][index],2)
                temp2["Book_Value"] = round(portfolios["Account_Investment_Book_Value"][index],2)
                temp2["Portfolio_Weightage"] = fetchMarketValuePercentage(inv["Investor"], portfolios["Security_Description"][index])
                temp2["Account"] = portfolios["Account"][index]
                if index == len(portfolios["Investor_Name"])-1:
                    temp1.append(temp2.copy())
                    temp3[temp2["Account"]] = temp1.copy()
                    temp1.clear()
                elif temp2["Account"] != portfolios["Account"][index+1]:
                    temp1.append(temp2.copy())
                    temp3[temp2["Account"]] = temp1.copy()
                    temp1.clear()
                else:
                    temp1.append(temp2.copy())
            index+=1
        investor_investments[inv["Investor"]] = temp3.copy()
        temp3.clear()
    adv_investor_investments[adv] = investor_investments.copy()
    investor_investments.clear()
# print(adv_investor_investments)
# for i in adv_investor_investments["Advisor 1"]:
#     print(i)


