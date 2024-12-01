import pandas as pd
#from sqlalchemy import create_cursor
import pyodbc

conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER= .;'
    r'DATABASE=document_storage;'
    r'Trusted_Connection=yes;'
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    df = pd.read_csv('./DB/TransactionTypes.csv')
    # Запись DataFrame в таблицу
    df.to_sql('TransactionTypes', con=cursor, index=False, if_exists='append')
    df = pd.read_csv('./DB/Customers.csv')
    # Запись DataFrame в таблицу
    df.to_sql('Customer', con=cursor, index=False, if_exists='append')

    df = pd.read_csv('./DB/CreditTransactions.csv')
    # Запись DataFrame в таблицу
    df.to_sql('CreditTRansactions', con=cursor, index=False, if_exists='append')

    df = pd.read_csv('./DB/CreditProducts.csv')
    # Запись DataFrame в таблицу
    df.to_sql('CreditProducts', con=cursor, index=False, if_exists='append')

    df = pd.read_csv('./DB/CreditAgreements.csv')
    # Запись DataFrame в таблицу
    df.to_sql('CreditAgreements', con=cursor, index=False, if_exists='append')

    print ("It's OK")
    cursor.close()
    conn.close()
    print("Connection closed.")

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    if sqlstate == '28000':
        print("Authentication error. Please check your Windows credentials and SQL Server configuration.")
    else:
        print(f"Database error: {ex}")


