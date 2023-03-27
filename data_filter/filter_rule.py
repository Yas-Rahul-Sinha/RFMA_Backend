from data_filter.sorting_rules import *
category_list = {
    "Market News":{
        "Elections":["Positive","Negative","Neutral"],
        "Political":["Unrest", "Government Failure"],
    },
    "Market Research":{
        "Market Sector":["Communication Services","Consumer Discretionary","Consumer Staples","Energy","Financials","Health Care","Industrials","Information Technology","Materials","Real Estate","Utilities"],
        "Industry Group":["Automobiles and Components","Banks","Capital Goods","Commercial and Professional Services","Consumer Durables and Apparel","Consumer Services","Diversified Financials","Energy","Food, Beverage, and Tobacco","Food and Staples Retailing","Health Care Equipment and Services","Household and Personal Products","Insurance","Materials","Media and Entertainment","Pharmaceuticals","Biotechnology and Life Sciences","Real Estate","Retailing","Semiconductors and Semiconductor Equipment","Software and Services","Technology Hardware and Equipment","Telecommunication Services","Transportation","Utilities"],
        "Financial Instrument":[],
        "Corporate House":[],
        "Regional Investments":["Mutual fund Investments"]
    },
    "Ratings":{
        "Corporate House":[],
        "Industry Sector":[],
        "Financial Instrument":[],
        "Region":[],
        "Country":[]
    },
    "Client Escalations":{
        "Account Closure":[],
        "Service Issue":[],
    },
    "Other Client Communication":{
        "Service Issue":[],
        "Personal Events": [],
        "Business Inquiry": [],
        "New Investment": []
    },
    "Investment Review":{
        "Periodic Portfolio Review":[],
        "Portfolio Performance Related":[],
        "Personal events":[],
        "Portfolio Recommendation":[],
        "Additional Investment":[]
    }
}
# rule = {
#     "Rule1":[{"Market Research":{"Market Sector":"Communication Services","Threshold":"5%","Portfolio Size":"10000000"}},{"Market Research":{"Industry Group":"Banks","Threshold":"9%","Portfolio Size":"10000000"}},{"Market News":{"Elections":"Negative"}}],
#     "Rule2":[{"Client Escalation":{"Service Issue":"no_sub"}},{"Investment Review":{"Portfolio Performance Related":"no_sub"}},{"Market News":{"Elections":"Positive"}}]
# }
rule = {
    "Advisor":"Gunasiri",
    "Rule1":{
        "Priority":1,
        "isActive":True,
        "Condition1":{"MainCategory":"Market Research", "SubCategory":"Market Sector", "SpecificImpact":"Communication Services", "Threshold":0, "PortfolioSize":1000000},
        "Condition2":{"MainCategory":"Market News","SubCategory":"Financial","SpecificImpact":"Negative","PortfolioSize":10000000}
    },
    # "Rule2":[{}]
}

def filter(rules):
    adv = rules["Advisor"]
    res = []
    temp = {}
    for key in rules:
        if key != "Advisor" and rules[key]["isActive"] == True:
            temp2 = filterByRule(adv,rules[key])
            temp["Priority"] = rules[key]["Priority"]
            temp["Result"] = temp2
            res.append(temp.copy())
    # res.sort(key=lambda x:x.Priority)
    return res

# def finalSorting(res_array):
#     sorted_array =

def filterByRule(advisor,rule):
    result = []
    for key in rule:
        if key != "Priority" and key != "isActive":
            res = filterByCondition(advisor,rule[key])
            # res["SatisfyingConditions"] = 1
            result.append(res.copy())
    return result

def filterByCondition(advisor,condition):
    if condition["MainCategory"] == "Market Research":
        res = byMarketReview(advisor,condition["SubCategory"],condition["SpecificImpact"],condition["Threshold"],condition["PortfolioSize"])
    elif condition["MainCategory"] == "Market News":
        res = byMarketNews(advisor,condition["SubCategory"],condition["SpecificImpact"],condition["PortfolioSize"])
    elif condition["MainCategory"] == "Client Escalation":
        res = byClientEscalation(advisor,condition["SubCategory"],condition["PortfolioSize"])
    elif condition["MainCategory"] == "Other Client Communication":
        res = byOtherClientCommunication(advisor,condition["SubCategory"],condition["PortfolioSize"])
    elif condition["MainCategory"] == "Investment Review":
        res = byInvestmentReview(advisor,condition["SubCategory"],condition["PortfolioSize"])
    elif condition["MainCategory"] == "Review":
        res = "Not Implemented Yet"
    return res

print(filter(rule))