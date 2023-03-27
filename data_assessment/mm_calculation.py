import pandas as pd
portfolios = pd.read_excel('WM Manager Dashboard Data SetV2.xlsx', sheet_name='Portfolio')
master_price = pd.read_excel('WM Manager Dashboard Data SetV2.xlsx', sheet_name='Instrument Master Price')
portfolios = portfolios.transpose()
for port in portfolios:
    index = 0
    for ins in master_price["Security Description"]:
        if(portfolios[port]["Security Description"] == ins):
            portfolios[port]["Market Value"] = portfolios[port]["Units"]*master_price["Price - As of date"][index]
            portfolios[port]["Market Value as of 31st Dec 2022"] = portfolios[port]["Units"]*master_price["Price - 12/31/2022"][index]
            portfolios[port]["Market Value as of 30th Sept 2022"] = portfolios[port]["Units"]*master_price["Price 09/30/2022"][index]
            portfolios[port]["Market Value as of 30th June 2022"] = portfolios[port]["Units"]*master_price["Price 06/30/2022"][index]
            portfolios[port]["Market Value as of 31th March 2022"] = portfolios[port]["Units"]*master_price["Price 03/31/2022"][index]
            portfolios[port]["Market Value as of 31th Dec 2021"] = portfolios[port]["Units"]*master_price["Price 12/31/2021"][index]
            portfolios[port]["Market Value as of 31th Dec 2020"] = portfolios[port]["Units"]*master_price["Price 12/31/2020"][index]
            break
        index+=1
portfolios = portfolios.transpose()