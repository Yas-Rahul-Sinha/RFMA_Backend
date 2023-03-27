import pandas as pd
from data_assessment.client_portfolio import *
from data_assessment.impact_calculation import *
from data_assessment.portfolio_info import *

market_research = pd.read_excel("../data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="Market Research")
market_news = pd.read_excel("../data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="Market News")
def byMarketReview(advisor, category,type,threshold,portfolio_size):
    category_filter = market_research[market_research["Category"] == category]
    type_filter = category_filter[category_filter["Type"] == type]
    accounts = getClientAccounts(advisor)
    temp = []
    temp2 = {}
    for acc in accounts:
        ins = getAccountInstruments(acc)
        for ch in type_filter["Security_Description"]:
            if ch in ins:
                imp = impactOnPortfolio(acc,ch)
                if imp >= threshold and getPortfolioMarketValue(acc) > portfolio_size:
                    temp2["Client"] = accountOwner(acc)
                    temp2["Impact"] = imp
                    temp2["Reason"] = f"Impact of {imp} on portfolio due to change in {category} of {type}"
                    temp.append(temp2.copy())
                    # temp.append({"Client":accountOwner(acc),"Impact":imp,"Reason":f"Impact of {imp} on portfolio due to change in {category} of {type}"})
    temp.sort(key=lambda x:x["Impact"])
    return temp

def byMarketNews(advisor, category, type, portfolio_size):
    category_filter = market_news[market_news["Category"] == category]
    type_filter = category_filter[category_filter["Impacts"] == type]
    accounts = getClientAccounts(advisor)
    temp = []
    temp2 = {}
    for acc in accounts:
        ins = getAccountInstruments(acc)
        for ch in type_filter["Description"]:
            if ch in ins:
                if getPortfolioMarketValue(acc) > portfolio_size:
                    temp2["Client"] = accountOwner(acc)
                    temp2["Impact"] = type
                    temp2["Reason"] = f"{type} impact on portfolio as per {category} related market news"
                    temp.append(temp2.copy())
    return temp

def byInvestmentReview(advisor, type, portfolio_size):
    accounts = getClientAccounts(advisor)
    temp = []
    temp2 = {}
    if type == 'Portfolio Performance Related':
        for acc in accounts:
            # current = performanceAnalysis(acc,"Market Value","Market_Value_as_of_31st_Dec_2022")
            # prev = performanceAnalysis(acc,"Market_Value_as_of_31st_Dec_2022","Market_Value_as_of_30th_Sept_2022")
            # pre_prev = performanceAnalysis(acc, "Market_Value_as_of_30th_Sept_2022", "Market_Value_as_of_30th_June_2022")
            prev_value = getPortfolioMarketValueAtTime(acc,"Market_Value_as_of_30th_Sept_2022")
            current_value = getPortfolioMarketValueAtTime(acc, "Market_Value_as_of_31st_Dec_2022")
            result = ((current_value - prev_value)/prev_value) * 100
            result = round(result,2)
            if result < 0.2 and getPortfolioMarketValue(acc) > portfolio_size:
                temp2["Client"] = accountOwner(acc)
                temp2["Impact"] = result
                temp2["Reason"] = f"client account {acc} is performing poorly with yield of {result}%"
                temp.append(temp2.copy())
        return temp
    elif type == "Periodic Portfolio Review":
        all_clients = pd.read_excel("../data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="Periodic Performance Review")
        # print(all_clients)
        relevent_clients = all_clients[all_clients["Advisor"] == advisor]
        # print(relevent_clients)
        for client,total_investment in zip(relevent_clients["Client"],relevent_clients["Total_Investment"]):
            temp2["Client"] = client
            temp2["Impact"] = total_investment
            temp2["Reason"] = f"Periodic Portfolio Review of {client} whose total investment is {total_investment}"
            temp.append(temp2.copy())
        return temp
    elif type == "Personal Events":
        all_clients = pd.read_excel("../data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="Personal Events")
        # print(all_clients)
        temp_client = all_clients[all_clients["Event_Type"] == "Investment Review"]
        # print(temp_client)
        relevent_client = temp_client[temp_client["Advisor"] == advisor]
        # print(relevent_client)
        for client,event in zip(relevent_client["Client_Name"], relevent_client["Event"]):
            temp2["Client"] = client
            temp2["Impact"] = event
            temp2["Reason"] = f"{client} has an event {event}"
            temp.append(temp2.copy())
        return temp
    elif type == "Portfolio Recommendation":
        products = pd.read_excel("../data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="New Products")
        client_list = getClientList(advisor)
        for client in client_list:
            current_investment = getClientTotalInvestment(client)
            filter_products = products[products["Probability_Customer_Portfolio_Amount"] <= current_investment]
            recommended_product_df = filter_products[filter_products["Min_Investment_Required"] == filter_products["Min_Investment_Required"].max()]
            recommended_product = recommended_product_df["Product_Name"].iloc[0]
            temp2["Client"] = client
            temp2["Impact"] = recommended_product
            temp2["Reason"] = f"Product Recommendation to {client} of product {recommended_product} who is having a total investment of {current_investment}"
            temp.append(temp2.copy())
        return temp
    if type == "Additional Investment":
        data = pd.read_excel("../data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="Client Requested Meetings")
        filter_data = data[data["Reason"] == "Additional Investment"]
        required_data = filter_data[filter_data["Advisor"] == advisor]
        for client in required_data["Client"]:
            temp2["Client"] = client
            temp2["Impact"] = type
            temp2["Reason"] = f"{client} wants to do Additional Investment"
            temp.append(temp2.copy())
        return temp
# print(byMarketNews("Gunasiri","Financial","Negative",10000))
# print(byInvestmentReview("Gunasiri","Periodic Portfolio Review",10000))
# print(byInvestmentReview("Gunasiri","Personal Events",10000))
# print(byInvestmentReview("Gunasiri","Portfolio Recommendation",10000))
# print(byInvestmentReview("Sukant","Additional Investment",10000))

def byClientEscalation(advisor, type, porrtfolio_threshold):
    temp = []
    temp2 = {}
    data = pd.read_excel("../data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="Client Requested Meetings")
    escalation_data = data[data["Type"] == "Client Escalation"]
    relevent_data = escalation_data[escalation_data["Advisor"] == advisor]
    for client,esc_type in zip(relevent_data["Client"],relevent_data["Reason"]):
        worth = getClientTotalInvestment(client)
        if worth >= porrtfolio_threshold and type == esc_type :
            temp2["Client"] = client
            temp2["Impact"] = esc_type
            temp2["Reason"] = f"Client Escalation of {esc_type} by client {client} whose total investment is {worth}"
            temp.append(temp2.copy())
        return temp

# print(byClientEscalation("Gunasiri","Account Closure",100000))

def byOtherClientCommunication(advisor, reason, portfolio_threshold):
    temp = []
    temp2 = {}
    data = pd.read_excel("../data/WM Manager Dashboard Data SetV2.xlsx", sheet_name="Client Requested Meetings")
    filter_data1 = data[data["Type"] == "Other Client Communication"]
    filter_data2 = filter_data1[filter_data1["Advisor"] == advisor]
    required_data = filter_data2[filter_data2["Reason"] == reason]
    for cli,res in zip(required_data["Client"],required_data["Reason"]):
        inv = getClientTotalInvestment(cli)
        if inv >= portfolio_threshold:
            temp2["Client"] = cli
            temp2["Impact"] = res
            temp2["Reason"] = f"{cli} requested meeting for {res}"
            temp.append(temp2.copy())
    return temp

# print(byOtherClientCommunication("Gunasiri","Service Issue",100000))