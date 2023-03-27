import ast
from flask_cors import CORS
from flask import Flask
from flask_restful import Resource,Api,reqparse

from data_filter.filter_rule import *
from data_assessment.main import advisor
from data_assessment.escalation import temp2
from data_assessment.escalation import temp3
from data_assessment.client_portfolio import getAccountPortfolio
from data_assessment.market_news import adv_market
from data_assessment.client_instrument import adv_investor_investments
from utility.datautil import *

app = app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


post_data = reqparse.RequestParser()
post_data.add_argument('Advisor',help='Advisor Name', required=True)
post_data.add_argument('Instrument',help='Instrument Name', required=True)
post_data.add_argument('Value',help='Value', required=True)

filter_data = reqparse.RequestParser()
filter_data.add_argument('Advisor',help="Advisor Name", required=True)

class ClientList(Resource):
    def get(self, adv):
        return {adv: advisor[adv]}

class MarketNews(Resource):
    def get(self, adv):
        return {adv: adv_market[adv]}

class ClientEscalation(Resource):
    def get(self, adv):
        return {adv:temp2[adv]}

class CRM(Resource):
    def get(self, adv):
        return {adv:temp3[adv]}

class PortfolioData(Resource):
    def get(self,adv,client,account):
        return getAccountPortfolio(adv,client,account)

class MarketSignalImpact2(Resource):
    def post(self):
        response = {}
        temp = {}
        args = post_data.parse_args()
        for i in args["data"]:
            j = ast.literal_eval(i)
            temp["Existing_Value"] = fetchMarketValue(j["investor"], j["instrument"])
            temp["Projected_Value"] = calculateMarketValue(j["investor"], j["instrument"], j["value"])
            temp["Percentage_Impact"] = percentageImpact(temp["Existing_Value"], temp["Projected_Value"])
            if temp["Existing_Value"] > temp["Projected_Value"]:
                temp["Up/Down"] = "Down"
            elif temp["Existing_Value"] < temp["Projected_Value"]:
                temp["Up/Down"] = "Up"
            else:
                temp["Up/Down"] = "No Impact"
            response[j['instrument']] = temp.copy()
        return response

class MarketSignalImpact(Resource):
    def post(self):
        args = post_data.parse_args()
        return marketSignalImpact(args["Instrument"], args["Advisor"], args["Value"])
class ClientInstrumentData(Resource):
    def get(self,adv):
        return adv_investor_investments[adv]

class AdvisorInstruments(Resource):
    def get(self, adv):
        return getAdvisorInstruments(adv)

class FundProjection(Resource):
    def get(self):
        return fundProjection()

class InstrumentData(Resource):
    def get(self):
        return getInstrumentData()

class FilterRule(Resource):
    def post(self):
        args = filter_data.parse_args()
        return filter(args)

api.add_resource(ClientList, '/<string:adv>/clientList')
api.add_resource(MarketNews, '/<string:adv>/marketNews')
api.add_resource(ClientEscalation, '/<string:adv>/clientEscalation')
api.add_resource(CRM, '/<string:adv>/CRM')
api.add_resource(PortfolioData, '/portfolioData/<string:adv>/<string:client>/<int:account>')
api.add_resource(MarketSignalImpact2, '/marketSignalImpact2')
api.add_resource(MarketSignalImpact, '/marketSignalImpact')
api.add_resource(ClientInstrumentData, '/clientInstrumentData/<string:adv>')
api.add_resource(AdvisorInstruments, '/advisorInstruments/<string:adv>')
api.add_resource(FundProjection, '/fundProjection')
api.add_resource(InstrumentData, '/instrumentData')
api.add_resource(FilterRule, '/filterRule')
if __name__ == '__main__':
    app.run(debug=True)