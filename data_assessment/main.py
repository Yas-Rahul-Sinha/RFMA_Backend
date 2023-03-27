import math
import pandas as pd
portfolios = pd.read_excel('../data/WM Manager Dashboard Data SetV2.xlsx', sheet_name='Portfolio')
master_price = pd.read_excel('../data/WM Manager Dashboard Data SetV2.xlsx', sheet_name='Instrument Master Price')
portfolios = portfolios.transpose()
for port in portfolios:
    index = 0
    for ins in master_price["Security_Description"]:
        if(portfolios[port]["Security_Description"] == ins):
            portfolios[port]["Market_Value"] = round(portfolios[port]["Units"]*master_price["Price-As of date"][index],2)
            portfolios[port]["Market_Value_as_of_31st_Dec_2022"] = round(portfolios[port]["Units"]*master_price["Price 12/31/2022"][index],2)
            portfolios[port]["Market_Value_as_of_30th_Sept_2022"] = round(portfolios[port]["Units"]*master_price["Price 09/30/2022"][index],2)
            portfolios[port]["Market_Value_as_of_30th_June_2022"] = round(portfolios[port]["Units"]*master_price["Price 06/30/2022"][index],2)
            portfolios[port]["Market_Value_as_of_31th_March_2022"] = round(portfolios[port]["Units"]*master_price["Price 03/31/2022"][index],2)
            portfolios[port]["Market_Value_as_of_31th_Dec_2021"] = round(portfolios[port]["Units"]*master_price["Price 12/31/2021"][index],2)
            portfolios[port]["Market_Value_as_of_31th_Dec_2020"] = round(portfolios[port]["Units"]*master_price["Price 12/31/2020"][index],2)
            break
        index+=1
    if math.isnan(portfolios[port]["Market_Value"]):
        portfolios[port]["Market_Value"] = 0
portfolios = portfolios.transpose()
# print(portfolios["Market Value"][5])
# portfolio = pd.read_excel('WM Manager Dashboard Data SetV2.xlsx', sheet_name='Portfolio', usecols=[0, 1, 5, 11])
temp = portfolios.Advisor[0]
rows, columns = portfolios.shape
# print(rows)
# print(temp)
temp2 = portfolios["Investor_Name"][0]
bookSum = 0
martSum = 0
advisor = {}
investor = []
iterator = 0
for ind in portfolios.Advisor:
    if ind != temp or iterator == rows-1:
        # print(ind != temp)
        investor.append({"Investor":temp2,"Book_Value": round(bookSum,2), "MM": round(martSum,2), "Country_of_Domicile": portfolios["Account_Currency"][iterator]})
        temp2 = portfolios["Investor_Name"][iterator]
        martSum = round(portfolios["Market_Value"][iterator],2)
        bookSum = round(portfolios["Account_Investment_Book_Value"][iterator],2)
        advisor.update({temp:investor.copy()})
        # print(advisor)
        temp = ind
        # print(temp)
        investor.clear()
    elif ind == temp:
        if temp2 != portfolios["Investor_Name"][iterator]:
            # print(temp2)
            investor.append({"Investor":temp2,"Book_Value": round(bookSum,2), "MM": round(martSum,2), "Country_of_Domicile": portfolios["Account_Currency"][iterator]})
            temp2 = portfolios["Investor_Name"][iterator]
            # print(investor)
            martSum = round(portfolios["Market_Value"][iterator],2)
            bookSum = round(portfolios["Account_Investment_Book_Value"][iterator],2)
        elif temp2 == portfolios["Investor_Name"][iterator]:
            martSum += round(portfolios["Market_Value"][iterator],2)
            bookSum += round(portfolios["Account_Investment_Book_Value"][iterator],2)
            # print(bookSum)

    iterator += 1
# for i in advisor["Advisor 1"]:
#     print(i)
