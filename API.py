import mysql.connector
import pandas as pd

class CorporateStorage():
    def Authorisation(self, login, passwd):
        # Создаем соединение с БД
       self.connection = mysql.connector.connect(
            host="localhost",  # Хост (обычно localhost)
            user="login",  # Имя пользователя
            password="passwd",  # Пароль
            database="document_storage"  # Имя базы данных
        )
       self.cursor = self.connection.cursor()

    def addCustomers(self, id, name, type, date, reg, tin, cont):
        # Вставка данных
        if type == 1:
            reg = "NULL"
        elif type == 2:
            date == "NULL"
        else:
            return "ERROR"
        sql = ("INSERT INTO Customers (CustomerID, CustomerTypeID, Name, "
               "DateOfBirth, RegistrationDate, TIN, ContactInfo) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        val = (id, name, type, date, reg, tin, cont)
        self.cursor.execute(sql, val)
        self.connection.commit()

    def addCreditProd(self, id, name, interest, max, min, colateral):
        # Вставка данных
        sql = ("INSERT INTO CreditProducts (CreditProductID, ProductName, InterestRate, "
               "MaxLoanAmount, CollateralRequired)"
               "VALUES (%s, %s, %s, %s, %s)")
        val = (id, name, interest, max, min, colateral)
        self.cursor.execute(sql, val)
        self.connection.commit()

    def addCreditAgree(self, id, custId, prodId, AgreeDate, amount, term, interest):
        sql = ("INSERT INTO CreditAgreements (CreditAgreementID, CustomerID, "
               "CreditProductID, AgreementDate, LoanAmount, LoanTerm, InterestRate)"
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        val = (id, custId, prodId, AgreeDate, amount, term, interest)
        self.cursor.execute(sql, val)
        self.connection.commit()

    def addCreditTransact(self, id, custId, agreeId, trDate, trAmount, type):
        #По идее дергается автоматически с поступлением каждой транзакции
        sql = ("INSERT INTO CreditTransactions (TransactionID, CustomerID, "
               "CreditAgreementID, TransactionDate, TransactionAmount, TransactionTypeID)"
               "VALUES (%s, %s, %s, %s, %s, %s)")
        val = (id, custId, agreeId, trDate, trAmount, type)
        self.cursor.execute(sql, val)
        self.connection.commit()

    def viewCustomer(self, idcust):
        query = ("SELECT * FROM Customers, CreditAgreements, CreditTransactions"
                 " WHERE CustomerId = %s")
        self.cursor.execute(query, idcust)
        response = self.cursor.fetchall()
        descr = self.cursor.description
        self.createRecord(response, descr)

    def viewProd(self, idProd):
        query = ("SELECT * FROM CreditProducts WHERE CreditProductID = %s")
        self.cursor.execute(query, idProd)
        return self.cursor.fetchall()

    def viewAgree(self, idAgree):
        query = ("SELECT * FROM CreditAgreements WHERE CreditAgreementsID = %s")
        self.cursor.execute(query, idAgree)
        response = self.cursor.fetchall()
        return response

    def viewTrans(self, idTrans):
        query = ("SELECT * FROM CreditTransactions WHERE TransactionID = %s")
        self.cursor.execute(query, idTrans)
        response = self.cursor.fetchall()
        return response

    def viewType(self, idtype):
        query = ("SELECT * FROM TransactionsTypes WHERE TransactionsTypeID = %s")
        self.cursor.execute(query, idtype)
        response = self.cursor.fetchall()
        return response
    def createRecord(self, response, descr):
      # Получите все результаты запроса
        results = self.cursor.fetchall()
        # Создайте DataFrame из полученных данных
        columns = [i[0] for i in descr]  # Получите названия колонок
        df = pd.DataFrame(response, columns=columns)
        df.to_csv('./report.csv', index=False)
        df.to_excel('./report.xls', index=False)
        df.to_json('./report.json', index=False)


