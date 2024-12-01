const mysql = require('mysql2/promise'); // Используем promise-версию для async/await
const fs = require('node:fs/promises'); // Для работы с файлами (async)
const { writeFile } = require('node:fs');
const { parse } = require('csv-parse');
const { stringify } = require('csv-stringify');
const { create } = require('xlsx')

class CorporateStorage {
    constructor(host, user, password, database) {
        this.config = {
            host: host,
            user: user,
            password: password,
            database: database,
            waitForConnections: true,
            connectionLimit: 10,
            queueLimit: 0,
        };
        this.connection = null;
    }

    async connect() {
        this.connection = await mysql.createConnection(this.config);
    }

    async disconnect() {
        await this.connection.end();
    }


    async addCustomers(id, name, type, date, reg, tin, cont) {
        try {
            const [rows] = await this.connection.execute(`
                INSERT INTO Customers (CustomerID, CustomerTypeID, Name, DateOfBirth, RegistrationDate, TIN, ContactInfo) 
                VALUES (?, ?, ?, ?, ?, ?, ?)`,
                [id, name, type, date, type === 1 ? null : reg, type === 2 ? null : date, tin, cont]
            );

            console.log(`${rows.affectedRows} row(s) added`);
        } catch (error) {
            console.error("Error adding customer:", error);
            throw error; // Перебрасываем ошибку для обработки выше
        }
    }

    // Аналогичные методы addCreditProd, addCreditAgree, addCreditTransact  -  добавьте их сами

    async viewCustomer(idcust) {
      try{
        const [rows] = await this.connection.execute(
          `SELECT * FROM Customers WHERE CustomerId = ?`, [idcust]
        );
        return rows;
      } catch(error){
        console.error("Error viewing customer:", error);
        throw error;
      }
    }

    // Аналогичные методы viewProd, viewAgree, viewTrans, viewType -  добавьте их сами

    async createReport(data, columns) {
      try {
          const csvData = stringify(data, { header: true, columns });
          // Добавление создания Excel и JSON файлов
          const wb = createWorkbook({
            sheetNames: ['Report'],
            sheets: [{ data: data }]
          });
          await fs.writeFile('./report.xlsx', wb)
          console.log('Excel report created successfully!')
      } catch (error) {
          console.error('Error creating the report:', error);
          throw error;
      }
    }

}


async function main() {
    const storage = new CorporateStorage('localhost', 'login', 'passwd', 'document_storage');
    await storage.connect();

    try {
        // Пример использования:
        await storage.addCustomers(1, 'Иван Иванов', 1, '1980-05-10', null, '1234567890', 'ivan@example.com');

        // Получение данных:
        const customer = await storage.viewCustomer(1);
        console.log(customer);

        await storage.createReport(customer, ['CustomerID', 'CustomerTypeID', 'Name', 'DateOfBirth', 'RegistrationDate', 'TIN', 'ContactInfo'])
    } catch (error) {
        console.error("Main function error:", error);
    } finally {
      await storage.disconnect();
    }
}



main();