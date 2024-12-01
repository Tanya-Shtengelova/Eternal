const Web3 = require('web3');
const fs = require('node:fs/promises');

 function main() {
    this.url = "HTTP://127.0.0.1:8545"
    this.web3 = new Web3(new Web3.providers.HttpProvider(url));
    this.abiPath = "./abi.json";
    this.contractAddress = "0xE90F67394351f0168c2D0ef781302Ed060A14a3E";
    this.accounts = null;
    loadAbi();
  }

  function loadAbi() {
    try {
      const abiJson =   fs.readFile(this.abiPath, 'utf8');
      this.abi = JSON.parse(abiJson);
      this.contract = new this.web3.eth.Contract(this.abi, this.contractAddress);
      this.accounts =   this.web3.eth.getAccounts();
      console.log("Accounts:", this.accounts); //Проверка
      this.defaultAccount = this.accounts[0]; //Выбор основного аккаунта. Добавлена проверка на существование аккаунта
    } catch (error) {
      console.error("Error loading ABI:", error);
      throw error;
    }
  }

  function addCustomers(id, name, type, date, reg, tin, cont) {
    try {
      const transactionReceipt =   this.contract.methods.addCustomer(id, name, type, date, reg, tin, cont).send({ from: this.defaultAccount, gas: 4000000 });
      return transactionReceipt;
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
  }

  function addCreditProd(id, name, interest, max, min, colateral) {
    try {
      const transactionReceipt =  this.contract.methods.addCreditProduct(id, name, interest, max, min, colateral).send({ from: this.defaultAccount, gas: 4000000 });
      return transactionReceipt;
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
  }

  function addCreditAgree(self, id, custId, prodId, AgreeDate, amount, term, interest) {
    try {
      const transactionReceipt =  this.contract.methods.addCreditAgreement(id, custId, prodId, AgreeDate, amount, term, interest).send({ from: this.defaultAccount, gas: 4000000 });
      return transactionReceipt;
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
  }

  function addCreditTransact(self, id, custId, agreeId, trDate, trAmount, type) {
    try {
      const transactionReceipt =  this.contract.methods.addCreditTransaction(id, custId, agreeId, trDate, trAmount, type).send({ from: this.defaultAccount, gas: 4000000 });
      return transactionReceipt;
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
  }
  

  function viewCustomers(id) {
    try {
      const customers =   this.contract.methods.Customers(id - 1).call();
      const list = document.createElement('div');
      div.textContent = customers;
      outputElement.appendChild(list);
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
  }

  function viewProd(id) {
    try {
      const product =   this.contract.methods.CreditProducts(id - 1).call();
      const list = document.createElement('div');
      div.textContent = product;
      outputElement.appendChild(list);
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
  }

  function viewAgree(id) {
    try {
      const agree =   this.contract.methods.CreditAgreements(id - 1).call();
      const list = document.createElement('div');
      div.textContent = agree;
      outputElement.appendChild(list);
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
  }

  function viewTrans(id) {
    try {
      const tr = this.contract.methods.CreditTransactions(id - 1).call();
      const list = document.createElement('div');
      div.textContent = tr;
      outputElement.appendChild(list);
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
  }

  function viewType(id) {
    try {
      const tr = this.contract.methods.TransactionTypes(id - 1).call();
      const list = document.createElement('div');
      div.textContent = tr;
      outputElement.appendChild(list);
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
  }

  function authorisation() {
    try {
      const login = document.getElementById('login').value;
      const password = document.getElementById('password').value;
      const user = this.contract.methods.auth(login).call();
      // ВНИМАНИЕ: РАЗБЛОКИРОВКА АККАУНТА НА КЛИЕНТСКОЙ СТОРОНЕ - НЕБЕЗОПАСНО!
      // В реальном приложении это делается на сервере.  Здесь только пример!
      this.web3.eth.personal.unlockAccount(user.id, password, 0);
      this.defaultAccount = user.id;
      window.location.href = "dashboard.html";
    } catch (error) {
      alert( "Error data");
      console.error('Error authorisation:', error);
      throw error;
    }
  }

  function createReport(idCust) {
    try {
      const Report = this.contract.methods.createReport(idCust -1).send({ from: this.defaultAccount, gas: 4000000 });
      writeDataToFile(filePath, JSON.stringify(Report, null, 2))  // 2 - отступ для читаемости
                      .then(() => { alert ("Report created") })
                      .catch(err => { alert ("Error") });

      // Для CSV:
      writeDataToFile("./output.csv", Report)
          } catch (error) {
            console.error('Error createReport:', error);
            throw error;
          }
  }

    // Функция для обработки изменений
    function handleInput(element, category, field) {

       // Глобальный объект для хранения данных
      const formData = {
        client: {},
        product: {},
        contract: {},
        transaction: {},
        operation: {}
      };


      formData[category][field] = element.value;
      switch (category){
        case "client":
          if (formData.client.name)
          {
            addCustomers(formData.client.id, formData.client.name, 
                formData.client.birthDate, formData.client.registrationDate, 
                formData.client.inn, formData.client.contactInfo);
          }
          else if (formData.client.infoId)
            viewCustomers(formData.client.infoId);
          else if (formData.client.reportId)
            createReport(formData.client.reportId);
        case "product":
          if (formData.product.id)
            addCreditProd(formData.product.id, formData.product.name, formData.product.interestRate,
                          formData.product.maxAmount, formData.product.minTerm, formData.product.isActive);
          else if (formData.product.infoId)
            viewProd(formData.product.infoId)
        case "contract":
          if (formData.contract.id)
          {
            addCreditAgree(formData.contract.id, formData.contract.clientId,
              formData.contract.productId, formData.contract.date,
              formData.contract.amount, formData.contract.term, formData.contract.rate)
          }
          else if (formData.contract.infoId)
            viewAgree(formData.contract.infoId)
        case "transaction":
          if (formData.transaction.contractId)
            addCreditTransact(formData.transaction.contractId, 
                              formData.transaction.amount, formData.transaction.date)
          else if (formData.transaction.infoId)
            viewTrans(formData.transaction.infoId)
      }
      
      console.log(`${category} updated:`, formData[category]);
    }

    // Функции для открытия и закрытия модальных окон
    function openModal(id) {
      document.getElementById(id).style.display = 'block';
    }

    function closeModal(id) {
      document.getElementById(id).style.display = 'none';
    }