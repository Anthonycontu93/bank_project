from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from cs50 import SQL
import random
import pandas as pd
from pandasql import sqldf
import os
import csv
from sqlite3 import Error
import sqlite3 as sql
import re


db = SQL("sqlite:///banca.db")

conn = sql.connect("/workspaces/76244869/project_bank/banca.db")



# classe cliente, inizilizzo il cliente, con attributi necessari
class Cliente:
        def __init__(self, name, lastname, taxID, salary, balance=0):

            self.name = name
            self.lastname = lastname
            self.taxID = taxID
            self.salary = salary
            self._balance = balance

        def __str__(self):
             return f" nome:{self.name}\n congnome:{self.lastname}\n cc:{self.taxID}\n income:{self.salary}\n balance:{self.balance}\n"

        # metodo per costruire l'oggetto cliente
        @classmethod
        def get(cls):

            print("Client's data:",end="\n")
            name = input("Name: ")
            lastname = input("lastname: ")
            while True:
                 try:
                    codice_fiscale = input("TaxID:").upper()

                    taxID = codice_fiscale
                    patter = re.compile(r'^[A-Z]{6}[0-9]{2}[A-Z]{1}[0-9]{2}[A-Z]{1}[0-9]{3}[A-Z]{1}$')
                    match = patter.search(f"{taxID}")
                    if match:
                         print("Valid TaxID")
                         break
                    else:
                         raise ValueError
                 except:
                    print("Invalid TaxID")
                    continue

            salary = input("salary:")
            balance = input("Account balance:")

            # controllo se mancano attributi chiamo l'error
            if not name or not lastname or not codice_fiscale or not salary or not balance:
                raise ValueError
            return cls(name, lastname, codice_fiscale, salary, balance)



        #getter
        @property
        def balance(self):
             return self._balance
        #getter
        @property
        def get_cc(self):
             return self.taxID

        #set in case the cc doesn't match
        def update_cc(self, new_cc):
             self.taxID = new_cc


        # metodo per depositare
        def deposit(self, n, Cc):
             add = n
             add = int(add)
             bag = int(self._balance)
             bag += add
             self._balance = bag
             Cc = Cc
             update = db.execute("UPDATE Persons SET Balance = ? WHERE Cc = ? ", self.balance, Cc)

        # metodo per prelevare
        def withdraw(self, n, Cc):
             min = n
             min = int(min)
             bag = int(self._balance)
             bag -= min
             self._balance = bag
             Cc = Cc
             update = db.execute("UPDATE Persons SET Balance = ? WHERE Cc = ? ", self.balance, Cc)


        def insert_into_db(self):
              insert = db.execute("INSERT INTO Persons (LastName, FirstName, Cc, Salary, Balance) VALUES (?,?,?,?,?)", self.lastname, self.name, self.taxID, self.salary, self.balance)



        def add_newloan_db(Cc,bank):
              id_loan = Loan.get_id()
              taxID = Cc
              bank = bank
              ammount = input("total loan:")
              rate = input("total rates:")
              question_on_startTime = input("Do you want to start pay from this month? y/n:").lower()
              if question_on_startTime == "yes" or question_on_startTime == "y":
                   start_date = date.today()
                   start_date = start_date.strftime("%d/%m/%Y")
              else:
                   d = int(input("day:"))
                   m = int(input("month:"))
                   y = int(input("year: "))
                   start_time = date(y, m, d)
                   start_date = start_time.strftime("%d/%m/%Y")


                   if not d or not m or not y:
                        raise ValueError


              end_date = date.today() + relativedelta(months=int(rate))
              end_date = end_date.strftime("%d/%m/%Y")

              # controllo se mancano attributi chiamo l'error
              if not taxID or not ammount or not rate: #not id_loan or
                    raise ValueError

              insert = db.execute("INSERT INTO Loans_ (LoanID, Cc, Ammount, Rates, Start_Date, End_date, Bank_name) VALUES (?,?,?,?,?,?,?)", id_loan, taxID, ammount, rate, start_date, end_date, bank)


# classe prestiti, qui inizializzo il prestito con tempo e rate, e controllo se il cliente è della banca.
class Loan:
     def __init__(self, id_loan, taxID, ammount, rate, start_date, end_date):

        self.id_loan = id_loan
        self.taxID = taxID
        self.ammount = ammount
        self.rate = rate
        self.start_date = start_date
        self.end_date = end_date

     def __str__(self):
         return f" id_prestito:{self.id_loan}\n client_cc:{self.taxID}\n ammount:{self.ammount}\n rate:{self.rate}\n start_date:{self.start_date}\n end_date:{self.end_date}\n"

     # unique ID for loan
     def get_id():
          id = random.getrandbits(16)
          return id

     # metodo per costruire l'oggetto loan
     @classmethod
     def get_loan(cls):
          print("Loan details:", end="\n")
          id_loan = Loan.get_id()
          taxID = input("taxID: ").upper()
          ammount = input("total loan:")
          rate = input("total rates:")
          question_on_startTime = input("Do you want to start pay from this month? y/n:").lower()
          if question_on_startTime == "yes" or question_on_startTime == "y":
               start_date = date.today()
               start_date = start_date.strftime("%d/%m/%Y")
          else:
               d = int(input("day:"))
               m = int(input("month:"))
               y = int(input("year: "))
               start_time = date(y, m, d)
               start_date = start_time.strftime("%d/%m/%Y")


               if not d or not m or not y:
                    raise ValueError


          end_date = date.today() + relativedelta(months=int(rate))
          end_date = end_date.strftime("%d/%m/%Y")

          # controllo se mancano attributi chiamo l'error
          if not taxID or not ammount or not rate: #not id_loan or
                raise ValueError
          return cls(id_loan, taxID, ammount, rate, start_date, end_date)


     #getter
     @property
     def starting_date(self):
          return self.start_date
     #getter
     @property
     def ending_date(self):
          return self.end_date
     #getter
     @property
     def get_cc(self):
          return self.taxID

     # set in case the cc doesn't match

     def update_cc(self, new_cc):
          self.taxID = new_cc

     def insert_into_db(self, name_istituto):
              bank = str(name_istituto)
              insert = db.execute("INSERT INTO Loans_ (LoanID, Cc, Ammount, Rates, Start_Date, End_date, Bank_name) VALUES (?,?,?,?,?,?,?)", self.id_loan, self.taxID, self.ammount, self.rate, self.start_date, self.end_date, bank)




class Bank:

    clients = []
    loans = []

    def __init__(self, bank_name):
        self.bank_name = bank_name

    # print client and loan
    def __str__(self):
         return f" client's details:\n{Bank.clients[0]} loan detail's:\n{Bank.loans[0]}"

    @property
    def get_names_bank(self):
        return self.bank_name

    def add_cliente(self, customer):
        Bank.clients.append(customer)

    def add_loan(self, loan):
        Bank.loans.append(loan)

    def remove_client(self, Cc):
         Cc = Cc
         q = input("Are you sure you want to delete the customer form for the loan? y/n:").lower()

         if q == "yes" or q == "y":
              remove = db.execute("DELETE FROM Loans_ WHERE Cc = ?", Cc)
              remove = db.execute("DELETE FROM Persons WHERE Cc = ?", Cc)
         else:
              return

    def search_client(self):
         taxID = str(input("Input taxID to find the client:")).upper()
         #estrapoolo info per file csv
         try:
              cursor = conn.cursor()
              cursor.execute("SELECT Loans_.LoanID, Loans_.Ammount, Loans_.Rates, Loans_.Start_Date, Loans_.End_date, Loans_.Bank_name, Loans_.Cc, Persons.Balance FROM Loans_ JOIN Persons ON Persons.Cc = Loans_.Cc WHERE Persons.Cc = (?)", (taxID,))
              with open("Loans_data_client.csv", "w") as csv_file:
                   csv_writer = csv.writer(csv_file, delimiter=",")
                   csv_writer.writerow([i[0] for i in cursor.description])
                   csv_writer.writerows(cursor)

              dirpath = os.getcwd() + "/Loans_data_client.csv"
              print("Data exported Successfully into {}".format(dirpath))

         except Error as e:
              print(e)




    def add_loan_to_client(self):

         taxID = input("TaxID:")
         check_if_client = db.execute("SELECT * FROM Loans_ WHERE Cc = ?", taxID)
         print(check_if_client)
         n_loan = len(check_if_client)
         if n_loan >= 1:
              for _ in range(n_loan):
                   Cc = check_if_client[_]['Cc']
                   print(Cc)
                   bank = check_if_client[_]['Bank_name']
                   print(bank)
                   Cliente.add_newloan_db(Cc, bank)
         else:
              print("This taxID is not a client")
              return



# funzione che genera una banca casuale
def name_a_bank():
         banks = ["Unicredit", "Intesa San Paolo", "BNP", "Mediolanum", "N26"]
         bank = random.choice(banks)
         return bank






def main():

     while True:
        try:

            #random name bank
            istituto_di_credito = name_a_bank()

            #crea oggetto bank
            bank = Bank(istituto_di_credito)

            print("Welcome to our bank, application form to register a new client.\n")
            #crea oggetto Cliente
            cliente=Cliente.get()

            #aggiungiamo alla lista il primo cliente
            bank.add_cliente(cliente)

            q1 = input("Would you like a loan?:").lower()
            if q1 == "yes" or q1 == "y":

                    #crea oggetto Loan
                    loan=Loan.get_loan()
                    cc1 = cliente.get_cc
                    cc2 = loan.get_cc


                    #aggiungiamo alla lista il primo loan
                    bank.add_loan(loan)


                    while True:
                         if cc1 == cc2:
                              break
                         else:
                              print("TaxID doesn't match", end="\n\n")
                              #modify the taxID and if it respect the patter update
                              modify_data = input("Modify the TaxID:").upper()
                              confirm = input("Confirm TaxID:").upper()
                              patter = re.compile(r'^[A-Z]{6}[0-9]{2}[A-Z]{1}[0-9]{2}[A-Z]{1}[0-9]{3}[A-Z]{1}$')
                              match = patter.search(f"{confirm}")
                              if confirm == modify_data and match:
                                   cliente.update_cc(confirm)
                                   loan.update_cc(confirm)
                                   break

                    print(cliente)
                    print(loan)
                    print(bank)




                    remove_client = input("Do you want to delete a client from the db? y/n:").lower()

                    if remove_client == "yes" or remove_client == "y":
                         cc= input("Input the client's taxID:").upper()
                         clients = db.execute("SELECT * FROM Persons WHERE Cc = ?", cc)
                         print(clients)
                         n = len(clients)
                         for _ in range(n):
                            if cc in clients[_]['Cc']:
                                 bank.remove_client(cc)
                                 print("Client deleted.")
                    else:
                         print("You didn't delete any client.")



                    #controllo se è tutto corretto e poi
                    # inseriamo nel db il cliente e il loan e prendiamo il nome della banca random

                    are_you_sure = input("Are you sure you want to add the client and the loan? y/n:").lower()

                    if are_you_sure == "yes" or are_you_sure == "y":
                        cliente.insert_into_db()
                        name_istituto = bank.get_names_bank
                        loan.insert_into_db(name_istituto)
                        print("The client is added!")
                    else:
                         print("Delete the form")


                    modify_balance = input("Do you want to depoist or withdraw? y/n:").lower()

                    if modify_balance == "yes" or modify_balance == "y":
                         which_operation = input("Deposit or withdraw? d/w:").lower()
                         # + o - su balnca del db
                         while True:
                              if which_operation =="d":
                                   cc = input("Whats the Cc number?:").upper()
                                   balance = db.execute("SELECT * FROM Loans_ WHERE Cc = ?", cc)
                                   money = int(input("How much?:"))
                                   cliente.deposit(money, cc)
                                   break

                              elif which_operation =="w":
                                   cc = input("Whats the Cc number?:").upper()
                                   balance = db.execute("SELECT * FROM Persons WHERE Cc = ?", cc)
                                   print(balance)
                                   n = len(balance)
                                   for _ in range(n):
                                        balance = balance[_]['Balance']
                                        print(balance)
                                   money = int(input("How much?:"))
                                   if int(balance) < money:
                                        print("Not enough credit")
                                        continue
                                   cliente.withdraw(money, cc)
                                   break
                              else:
                                   break


            else:
               # taxID cliente
               cc1 = cliente.get_cc

               #chied se volgio modificare il balace
               modify_balance = input("Do you want to depoist or withdraw? y/n:").lower()

               if modify_balance == "yes" or modify_balance == "y":
                    which_operation = input("Deposit or withdraw? d/w:").lower()
                    # + o - su balnca del db
                    while True:
                         if which_operation =="d":
                              cc = input("Whats the Cc number?:").upper()
                              balance = db.execute("SELECT * FROM Loans_ WHERE Cc = ?", cc)
                              money = int(input("How much?:"))
                              cliente.deposit(money, cc)
                              break

                         elif which_operation =="w":
                              cc = input("Whats the Cc number?:").upper()
                              balance = db.execute("SELECT * FROM Persons WHERE Cc = ?", cc)
                              n = len(balance)
                              print(balance)
                              for _ in range(n):
                                   balance = balance[_]['Balance']
                                   money = int(input("How much?:"))
                                   if int(balance) < money:
                                        print("Not enough credit!")
                                        continue
                                   else:
                                        cliente.withdraw(money, cc)
                                        new_bal = int(cliente.balance)
                                        print(f"Thank you, your balance is: {new_bal}!")
                                        break
                              break

                         else:
                              continue

               remove_client = input("Do you want to delete a client from the db? y/n:").lower()

               if remove_client == "yes" or remove_client == "y":
                    cc= input("Input the client's taxID:").upper()
                    clients = db.execute("SELECT * FROM Persons WHERE Cc = ?", cc)
                    print(clients)
                    n = len(clients)
                    for _ in range(n):
                         if cc in clients[_]['Cc']:
                              bank.remove_client(cc)
                              print("Client deleted.")
                         else:
                              print("You didn't delete any client.")
                              return



        except ValueError:
            print("Missing attributes")
            continue
        break

     #estrapoolo info per file csv
     try:
          cursor = conn.cursor()
          cursor.execute("select * from Loans_")
          with open("Loans_data.csv", "w") as csv_file:
               csv_writer = csv.writer(csv_file, delimiter=",")
               csv_writer.writerow([i[0] for i in cursor.description])
               csv_writer.writerows(cursor)

          dirpath = os.getcwd() + "/Loans_data.csv"
          print("Data exported Successfully into {}".format(dirpath))

          cursor = conn.cursor()
          cursor.execute("select * from Persons")
          with open("Persons_data.csv", "w") as csv_file:
               csv_writer = csv.writer(csv_file, delimiter=",")
               csv_writer.writerow([i[0] for i in cursor.description])
               csv_writer.writerows(cursor)

          dirpath = os.getcwd() + "/Persons_data.csv"
          print("Data exported Successfully into {}".format(dirpath))


     except Error as e:
          print(e)


     while True:
          try:

               search = input("Would you like to search a customer? y/n:").lower()
               if search == "yes" or search == "y":
                    #aggiunge un prestito ad un cliente esistente
                    bank.search_client()
                    break

               else:
                    print("")


               adding = input("Would you like to add a loan to a customer? y/n:").lower()
               if adding == "yes" or adding == "y":
                    #aggiunge un prestito ad un cliente esistente
                    bank.add_loan_to_client()
                    break

               else:
                    print("Thank you, is been a pleasure to help you!")
                    return






          finally:
               conn.close()

if __name__ == "__main__":
    main()