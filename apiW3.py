import web3
import json
import pandas as pd
class CorporateStorage():
    url = "HTTP://127.0.0.1:8545"
    with open("abi.json", 'r') as file:
        abi = json.load(file)
    storage = ""
    address = web3.Web3.to_checksum_address("0xE90F67394351f0168c2D0ef781302Ed060A14a3E")#адрес контракта
    def __init__(self):
        self.w3 = web3.Web3(web3.Web3.HTTPProvider(self.url))
        self.w3.eth.defaultAccount = self.w3.eth.accounts[0]
        self.storage = self.w3.eth.contract(address=self.address, abi=self.abi)


    def addCustomers(self, id, name, type, date, reg, tin, cont):
        log = (self.storage.functions.addCustomer(id, name, type, date, reg, tin, cont).
               transact({"from": self.w3.eth.defaultAccount}))
        return log

    def addCreditProd(self, id, name, interest, max, min, colateral):
        log = (self.storage.functions.addCreditProduct(id, name, interest, max, min, colateral).
               transact({"from": self.w3.eth.defaultAccount}))
        return log

    def addCreditAgree(self, id, custId, prodId, AgreeDate, amount, term, interest):
        log = (self.storage.functions.addCreditAgreement(id, custId, prodId, AgreeDate, amount, term, interest).
               transact({"from": self.w3.eth.defaultAccount}))
        return log

    def addCreditTransact(self, id, custId, agreeId, trDate, trAmount, type):
        log = (self.storage.functions.addCreditTransaction(id, custId, agreeId, trDate, trAmount, type).
               transact({"from": self.w3.eth.defaultAccount}))
        return log

    def viewCustomers(self, id):
        inf = self.storage.functions.Customers(id - 1).call()
        return inf

    def viewProd(self, id):
        inf = self.storage.functions.CreditProducts(id-1).call()
        return inf

    def viewAgree(self, id):
        inf = self.storage.functions.CreditAgreements(id-1).call()
        return inf

    def viewTrans(self, id):
        inf = self.storage.functions.CreditTransactions(id-1).call()
        return inf

    def viewType(self, id):
        inf = self.storage.functions.TransactionTypes(id-1).call()
        return inf

    def Authorisation(self, login, passw):
        user = self.storage.functions.auth(login).call()
        try:
            self.w3.eth.personal.unlockAccount(self.w3.to_checksum_address(user.id), passw, 0)
            self.w3.eth.default_account = user.id
            return True
        except (Exception):
            return (False)

    def createReport(self, idCust):
        report = (self.storage.functions.createReport(idCust).
               transact({"from": self.w3.eth.defaultAccount}))
        df = pd.DataFrame(report, columns=20)
        df.to_csv ('./report.csv', index=False)
        df.to_excel('./report.xls', index=False)
        df.to_json('./report.json', index=False)

#####################################