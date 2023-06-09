# -*- coding: utf-8 -*-
"""Banking.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p6WoSKZOQsfxFNcS6os-iQrwioOAjMJa

# **Please execute the first block which create a new database called Bank.db**
"""

import sqlite3

# Connect to the database (creates the database file if it doesn't exist)
conn = sqlite3.connect('bank.db')

# Create a cursor
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    CustomerName TEXT,
    Age INTEGER,
    Mobile INTEGER,
    AccountNumber INTEGER,
    Balance INTEGER,
    PIN INTEGER
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

"""# **Run the Bank Application code and enter the choices accordingly in the output console**"""

#Importing random to auto generate 6 digit account number for new accounts
import random

# Open Account function use to get customer basic information and create a new account number
# Negative Deposit is not allowed
# If auto generated account number already exists, system throw an error and ask user to try again
def openAccount():
        print("Welcome to Create a new account portal")
        cusname=str(input('Enter your FullName:'))
        age=int(input('Enter your age:'))
        mobile=int(input('Enter your phone number:'))
        balance=int(input('Enter your intial deposit money:'))
        if balance<=0:
          print("Negative deposit is not allowed, please try again")
          main()
        else:
            pin1=int(input("Enter a 4-digit number: "))
            pin2=int(input("Confirm your 4-digit number: "))
            if pin1==pin2:
                  if len(str(pin1)) !=4:
                    print("Invalid PIN! Must be 4 digits, Please Try again.")
                  else:
                    print("PIN is set") 
            else:
                print("Both PIN is not matching, please try again")
            account_number = str(random.randint(100000, 999999))

            # Connect to the database
            conn = sqlite3.connect('bank.db')

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
          
            cursor.execute("SELECT * FROM users WHERE AccountNumber =?", (account_number,))

            # Fetch all the data
            rows = cursor.fetchall()
            if len(rows)>0:
                  print("Account number exists already, Please try again")
            else:
                  # Insert data into the table
                  cursor.execute("INSERT INTO users (CustomerName, Age, Mobile, AccountNumber, Balance, PIN) VALUES (?, ?, ?, ?, ?, ?)", (cusname, age, mobile, account_number, balance, pin1))
                  # Commit the changes and close the connection
                  conn.commit()

                  # Close the connection
                  conn.close()
                      
                  print("Your account is successfully Created")
                  print("Your Name is: ", cusname)
                  print("Your Age is: ", age)
                  print("Your contact number is: ", mobile)
                  print("Your new account number is: ",account_number)
                  print("Your account balance is: $", balance)

                  print("Do you want to create another new account?")
                  ans=str(input('Enter Y for Yes/ N for No:'))
                  if ans=='Y' or ans=='y':
                      openAccount()
                  elif ans == 'N' or ans=='n':
                      main()
                  else:
                    print("Invalid response, please try again")
                  main()

# Deposit Money function is only used for existing customers to deposit money
# If account number doesn't exists in the system, it will throw error message
# User can't deposit the negative value
def depositMoney():
      accountNo=input("Enter your valid account number: ")
      conn = sqlite3.connect('bank.db')
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM users WHERE AccountNumber =?", (accountNo,))
      rows = cursor.fetchone()
      if rows is None:
        print("Account number is invalid, please try again") 
      else:
        print("Welcome back ", rows[0])
        pin=int(input("Enter your PIN:"))
        if pin==rows[5]:
          print("Authentication Successfull")
          dep=float(input("Please enter the amount you want to deposit"))
          if dep>=0:
                newBal=rows[4]+dep
                cursor.execute("UPDATE users set Balance=? WHERE AccountNumber =?", (newBal, accountNo))
                conn.commit()
                cursor.execute("SELECT * FROM users WHERE AccountNumber =?", (accountNo,))
                rows = cursor.fetchone()
                print("Your new account balance is :$", ("%.2f" % rows[4]))
          else:
              print("Seems you have entered the negative value, please try again")
        else:
          print("Authentication is unsuccessfull, please enter valid PIN")
      main()

# Withdrawal function is only to withdraw money from their registered account
# If account number doesn't exists in the system, it will throw error message
# User can't withdraw the more than their current balance
def Withdrawal():
    print("Welcome to withdrawal money screen")
    accountNo=input("Enter your valid account number: ")
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE AccountNumber =?", (accountNo,))
    rows = cursor.fetchone()
    if rows is None:
        print("Account number is invalid, please try again") 
    else:
        print("Welcome back ", rows[0])
        pin=int(input("Enter your PIN:"))
        if pin==rows[5]:
          print("Authentication Successful")
          AccBal=rows[4]
          dep=float(input("Please enter the amount you want to withdraw"))
          if dep<=0:
            print("Negative value is not accepted, please try again")
          else:
              if dep>AccBal:
                print("You don't have sufficient fund in your account, Please check and try other amount")
              else:
                  newBal=rows[4]-dep
                  cursor.execute("UPDATE users set Balance=? WHERE AccountNumber =?", (newBal, accountNo))
                  conn.commit()
                  cursor.execute("SELECT * FROM users WHERE AccountNumber =?", (accountNo,))
                  rows = cursor.fetchone()
                  print("Your remaining account balance is :$", ("%.2f" % rows[4]))
        else:
          print("Authentication is unsuccessful, please enter valid PIN")
        main()

# Transfer fund is to perform fund transfer from one account to another
# Both account should be valid, if not system will throw an error
# Negative value should not be accepted
# If the amount is greater than the current balance, system will throw error

def transferFunds():
    print("Welcome to transfer fund screen")
    accountNo=input("Enter your valid account number: ")
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE AccountNumber =?", (accountNo,))
    rows = cursor.fetchone()
    if rows is None:
        print("Account number doesn't exist, please check and try again") 
    else:
        print("Welcome back ", rows[0])
        pin=int(input("Enter your PIN:"))
        if pin==rows[5]:
            print("Authentication Successful")
            fromAccBal=rows[4]
            accountNo1=input("Enter the valid beneficiary account number: ")
            cursor.execute("SELECT * FROM users WHERE AccountNumber =?", (accountNo1,))
            rows1 = cursor.fetchone()
            if rows1 is None:
                print("Beneficiary account number doesn't exist, please check and try again")
            else:
                print("Funds will be transferred to ", rows1[0])
                toAccBal=rows1[4]
                fund=float(input("Enter the amount you want to transfer"))
                if fund<=0:
                    print("Negative value is not accepted, please try again")
                else:
                    if fund>fromAccBal:
                      print("You don't have sufficient fund in your account, Please check and try other amount")
                    else:
                      updtFromBal=rows[4]-fund
                      updtToBal=rows1[4]+fund
                      cursor.execute("UPDATE users set Balance=? WHERE AccountNumber =?", (updtToBal, accountNo1))
                      conn.commit()
                      cursor.execute("UPDATE users set Balance=? WHERE AccountNumber =?", (updtFromBal, accountNo))
                      conn.commit()
                      cursor.execute("SELECT * FROM users WHERE AccountNumber =?", (accountNo,))
                      rows = cursor.fetchone()
                      print("Your remaining account balance is :$", ("%.2f" % rows[4]))
        else:
            print("Authentication is unsuccessful, please enter valid PIN")
    main()

# Account Balance is to check the current balance
# Account should be valid, if not system will throw an error

def accountBalance():
    print("Welcome to account balance screen")
    accountNo=input("Enter your valid account number: ")
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE AccountNumber =?", (accountNo,))
    rows = cursor.fetchone()
    if rows is None:
        print("Account number doesn't exist, please check and try again") 
    else:
        print("Welcome back ", rows[0])
        pin=int(input("Enter your PIN:"))
        if pin==rows[5]:
          print("Authentication Successful")
          AccBal=rows[4]
          print("Your account balance is $", ("%.2f" % AccBal))
        else:
          print("Authentication is unsuccessful, please enter valid PIN")
    main()

def main():
    print('''Welcome to MyBank
              1. Open New Account
              2. Deposit Account
              3. Withdrawal Money
              4. Transfer Money
              5. Account Balance
              6. Quit''')
    userChoice=input("Choose the menu option")
    print(userChoice)
    if (userChoice=='1'):
      openAccount()
    elif (userChoice=='2'):
      depositMoney()
    elif (userChoice=='3'):
      Withdrawal()
    elif (userChoice=='4'):
      transferFunds()
    elif (userChoice=='5'):
      accountBalance()
    elif (userChoice=='6'):
      print("Thanks for using MyBank service")
    else:
      print("Wrong input, try again")
      main()
main()