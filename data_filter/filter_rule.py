import pandas as pd

from data_filter.sorting_rules import *
from openpyxl import load_workbook
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
    "Advisor": "Gunasiri",
    "Rule": [
        {
            "Priority": 1,
            "isActive": "True",
            "Condition": [
                {
                    "MainCategory": "Market Research",
                    "SubCategory": "Market Sector",
                    "SpecificImpact": "Communication Services",
                    "Threshold": 0,
                    "PortfolioSize": 100000
                },
                {
                    "MainCategory": "Market News",
                    "SubCategory": "Financial",
                    "SpecificImpact": "Negative",
                    "PortfolioSize": 10000000
                }
            ]
        },
        {
            "Priority": 1,
            "isActive": "True",
            "Condition": [
                {
                    "MainCategory": "Market Research",
                    "SubCategory": "Market Sector",
                    "SpecificImpact": "Communication Services",
                    "Threshold": 0,
                    "PortfolioSize": 1000000
                },
                {
                    "MainCategory": "Market News",
                    "SubCategory": "Financial",
                    "SpecificImpact": "Negative",
                    "PortfolioSize": 10000000
                }
            ]
        }
    ]
}

def writeToSheet(rules):
    df_json = pd.DataFrame(rules)
    with pd.ExcelWriter('data/WM Manager Dashboard Data SetV2.xlsx', mode='a',if_sheet_exists='replace', engine='openpyxl') as writer:
        df_json.to_excel(writer, sheet_name='Filter Rule', index=None)
    # file_path = 'data/WM Manager Dashboard Data SetV2.xlsx'
    # wb = load_workbook(file_path)
    # ws = wb["Filter Rule"]

def filter(rules):
    adv = rules["Advisor"]
    res = []
    temp = {}
    for rule in rules["Rule"]:
        if rule["isActive"] == "True":
            temp2 = filterByRule(adv,rule)
            temp["Priority"] = rule["Priority"]
            temp["Result"] = temp2
            res.append(temp.copy())
    # res.sort(key=lambda x:x.Priority)
    sorting = finalSorting(res)
    final = multipleReasonMerger(sorting)
    return final

def finalSorting(res_array):
    sorted_array = []
    res_array.sort(key=lambda x:x["Priority"])
    for rule_select in res_array:
        for condition_select in rule_select["Result"]:
            for results in condition_select:
                sorted_array.append(results)
    return sorted_array

def filterByRule(advisor,rule):
    result = []
    for condition in rule["Condition"]:
        res = filterByCondition(advisor,condition)
        # res["SatisfyingConditions"] = 1
        result.append(res.copy())
    return result

def ifPresentCheck(ans_array, obj):
    match_count = 0
    if len(ans_array) == 0:
        obj["Conditions Satisfying"] = 1
        ans_array.append(obj)
    else:
        for anss in ans_array:
            if anss["Client"] == obj["Client"]:
                anss["Conditions Satisfying"] += 1
                anss["Reason"] = anss["Reason"] + ", " + obj["Reason"]
                match_count += 1
        if match_count == 0:
            obj["Conditions Satisfying"] = 1
            ans_array.append(obj)
    return ans_array


def multipleReasonMerger(data):
    ans = []
    for obj in data:
        ans = ifPresentCheck(ans,obj)
    return ans

def filterByCondition(advisor,condition):
    res = []
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

# arr = filter(rule)
# print(finalSorting(arr))