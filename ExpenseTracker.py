#expenses tracker
import re
import datetime
import os
import csv
import pandas as pd


todaydate=datetime.datetime.today().strftime("%d-%m-%Y")
todaydate=datetime.datetime.strptime(todaydate,"%d-%m-%Y").date()



class Income():
  def __init__(self,name=None,Type="Income",amount=None,category=None,date=None):
    self.__name=name
    self.__amount=amount
    self.__category=category
    self.__type=Type
    #Seting Date as today's Date if not given
    if  date is None:
      self.__date=datetime.datetime.today().date()
    else:
      try:
        self.__date=pd.to_datetime(date,format="%d-%m-%Y").date()
      except ValueError:
        print("\nInvalid date! so current day is taken\n")
        self.__date=datetime.datetime.today().date()
  def getdate(self):
    return self.__date
  def getcategory(self):
    return self.__category
  def gettype(self):
    return self.__type

  def getname(self):
    return self.__name

  def getamount(self):
    return self.__amount






class Expense():


    def __init__(self,name=None,Type="Expense",amount=None,category=None,date=None):
      self.__name=name
      self.__amount=amount
      self.__category=category
      self.__type=Type




      if date is None:
        self.__date= datetime.datetime.today().date()
      else:

        try:
          self.__date= pd.to_datetime(date,format="%d-%m-%Y").date()
        except ValueError:
          print("\nInvalid date! so current day is taken")
          self.__date= datetime.datetime.today().date()

    def getname(self):
      return self.__name

    def gettype(self):
      return self.__type

    def getamount(self):
      return self.__amount
    def getdate(self):
      return self.__date

    def getcategory(self):
      return self.__category


class Expensetracker():

  columns=["Name","Amount","Type","Category","Date"]



  @staticmethod
  def validate_amount(amount_str):
      try:
          amount = float(amount_str)
          if amount <= 0:
              print("Amount must be positive")
              return None
          return amount
      except ValueError:
          print("Invalid amount")
          return None

  @staticmethod
  def validate_date(date_strr):
      try:
          date=datetime.datetime.strptime(date_strr,"%d-%m-%Y").date()

          if date > todaydate:
              print("Date cannot be in future")
              return None
          return date
      except ValueError:
          print("Invalid date so today date is taken")
          return todaydate

  @staticmethod
  def validate_string(value, field_name):
      if not isinstance(value, str) or not value.strip():
          print(f"{field_name} must be a non-empty string.")
          return None
      return value.strip()

  def __init__(self):
    try:
      self.df=pd.read_csv("ExpenseTrackerData.csv",parse_dates=["Date"],date_format="%d-%m-%Y")
    except FileNotFoundError:
      #creates csv file if not exists
      self.df=pd.DataFrame(columns=self.columns)
      self.df.to_csv("ExpenseTrackerData.csv",index=False)

  def refreshlist(self):

    self.df=pd.read_csv("ExpenseTrackerData.csv",parse_dates=["Date"],date_format="%d-%m-%Y")




  def additem(self,item):
    duplicate=self.df[(self.df["Name"]==item.getname())&
               (self.df["Amount"]==item.getamount())&
               (self.df["Type"]==item.gettype())&
               (self.df["Category"]==item.getcategory())&
               (self.df["Date"]==item.getdate())]

    if not duplicate.empty:
      print("Item already exists!")
      return

    temp_df=pd.DataFrame([{"Name":item.getname(), "Amount":item.getamount() , "Type":item.gettype(),"Category":item.getcategory(),"Date":item.getdate()}])
    self.df=pd.concat([self.df,temp_df],ignore_index=True)
    self.df.to_csv("ExpenseTrackerData.csv",index=False)

    print("\n Added Successfully.\n")


  def removeitem(self,temp_df):
    if temp_df.empty:
      print(" No Items to remove!")
      return
    while True:
        print("Items: ")
        temp_df.reset_index(drop=True)
        temp_df["index"]=range(0,len(temp_df))



        print(temp_df.to_string(index=False))
        try:
          userinput = int(input("Enter the index of the expense to remove:(-1 to cancel) "))
          if userinput== -1:
            break
          elif userinput < 0 or userinput >= len(temp_df):
            print("Invalid index!")
            continue

          else:

              original_index = temp_df.loc[userinput, 'index']
              self.df=self.df.drop(original_index).reset_index(drop=True)
              self.df.to_csv("ExpenseTrackerData.csv",index=False)
              print("Item removed successfully!")

              break

        except ValueError:
          print("Invalid input! Please enter correct number.")
          continue



  def viewexpenses(self):
    if self.df[self.df["Type"]=="Expense"].empty:
      print("No expenses found!")
      return

    print(self.df[self.df["Type"]=="Expense"].to_string(index=False))

  def viewincomes(self):
    if self.df[self.df["Type"]=="Income"].empty:
      print("No incomes found!")
      return

    print(self.df[self.df["Type"]=="Income"].to_string(index=False))

  def viewbycategory(self,category,Type):

     print("Items in Category. ")
     print(self.df[(self.df["Type"]==Type) & (self.df["Category"]==category)])

  def filterbydate(self,fromdates,todates,Type):
      #formating given datas
      fromdate=self.validate_date(fromdates)
      todate=self.validate_date(todates)
      if fromdate is None or todate is None:
          print("Invalid date input. Please ensure dates are in dd-mm-yyyy format.")
          return

      if fromdate > todate:
        print("Invalid date range!")
        return

      filtereddf=self.df[(self.df["Type"]==Type) & (self.df["Date"]>=fromdate) & (self.df["Date"]<=todate)]
      if not filtereddf.empty:
        df_sorted=filtereddf.sort_values(by="Date")


        print(df_sorted.to_string(index=False))


      else:
        print("No expenses found in the specified date range.")

  def gettotal(self,Type):
    total=self.df[self.df["Type"]==Type]["Amount"].sum()
    return total








  def viewjournal(self):
    print(self.df.to_string(index=False))

  def input(self):
          while True:

              name_input=input("Enter the name of the income: ")
              name = self.validate_string(name_input, "Name")
              if name is None:
                continue

              amount_input = input("Enter the amount of the income: ")
              amount=self.validate_amount(amount_input)
              if amount is None:
                continue

              date_input=input("Enter the date of the income (dd-mm-yyyy): ")
              date=self.validate_date(date_input)


              category_input=input("Enter category: ")
              category = self.validate_string(category_input, "Category")
              if category is None:
                continue



              return name,amount,category,date

  def filter(self,Type=None):


    if Type=="Expense":
      temp_df=self.df[self.df["Type"]=="Expense"]
    elif Type=="Income":
      temp_df=self.df[self.df["Type"]=="Income"]
    else:
      temp_df=self.df

    while True:
      print("1. Filterbycategory")
      print("2. Filterbydate")
      print("3.sortvalue")
      print("4.RemoveItem")
      print("5.To Edit items")
      print("0.To Go Back")
      try:
        choice=int(input("Press number: "))

        if choice==1:


          self.viewbycategory(category=input("Enter category:"),Type=Type)
        elif choice==2:
          fromdate=input("Enter the start date (dd-mm-yyyy): ")
          todate=input("Enter the end date (dd-mm-yyyy): ")

          self.filterbydate(fromdates=fromdate,todates=todate,Type=Type)
        elif choice==3:
          print("1.By Date(-1 for decending order)")
          print("2.By Amount(-2 for decending order)")

          print("0.To Go Back")
          choice=int(input("Press number: "))

          if choice==1:
            print(temp_df.sort_values(by="Date"))
            break
          elif choice==-1:
            print(temp_df.sort_values(by="Date",ascending=False))
            break
          elif choice==2:
            print(temp_df.sort_values(by="Amount"))
            break
          elif choice==-2:
            print(temp_df.sort_values(by="Amount",ascending=False))
            break


          elif choice==0:
            break
        elif choice==5:
          print("Items: ")
          temp_df.reset_index(drop=True)
          temp_df["index"]=range(0,len(temp_df))
          print(temp_df.to_string())
          userinput = int(input("Enter the index of the expense to edit:(-1 to cancel) "))
          if userinput== -1:
            break
          elif userinput < 0 or userinput >= len(temp_df):
            print("Invalid index!")
            continue
          else:
            while True:
              print("1.Edit Name")
              print("2.Edit Amount")
              print("3.Edit Category")
              print("4.Edit Date")
              print("0.To Go Back")
              choice=int(input("Press number: "))
              if choice ==1:
                new_value=input("Enter new value: ")
                new_value=self.validate_string(new_value,"Name")
                if new_value is None:
                  continue

                original_index = temp_df.loc[userinput, 'index']
                self.df.at[original_index, 'Name'] = new_value
                self.df.to_csv("ExpenseTrackerData.csv",index=False)
                print("Item edited successfully!")
                self.refreshlist()
                break
              elif choice==2:
                new_value=input("Enter new value: ")
                new_value=self.validate_amount(new_value)
                if new_value is None:
                  continue

                original_index = temp_df.loc[userinput, 'index']
                self.df.at[original_index, 'Amount'] = new_value
                self.df.to_csv("ExpenseTrackerData.csv",index=False)
                print("Item edited successfully!")
                self.refreshlist()
                break

              elif choice==3:
                new_value=input("Enter new value: ")
                new_value=self.validate_string(new_value,"Category")
                if new_value is None:
                  continue

                original_index = temp_df.loc[userinput, 'index']
                self.df.at[original_index, 'Category'] = new_value
                self.df.to_csv("ExpenseTrackerData.csv",index=False)
                print("Item edited successfully!")
                self.refreshlist()
                break
              elif choice==4:
                new_value=input("Enter new value: ")
                new_value=self.validate_date(new_value)
                if new_value is None:
                  continue

                original_index = temp_df.loc[userinput, 'index']
                self.df.at[original_index, 'Date'] = new_value
                self.df.to_csv("ExpenseTrackerData.csv",index=False)
                print("Item edited successfully!")
                self.refreshlist()
                break



              elif choice==0:
                break
              else:
                print("Invalid choice!")
                continue

        elif choice==4:
          self.removeitem(temp_df)
        elif choice==0:
          break
        else:
          print("Invalid choice!")
          continue

      except ValueError:
        print("Invalid input! Please enter correct number.")
        continue

def main():

  tracker=Expensetracker()


  while True:
    print("\nWelcome to Expense Tracker!")
    currentstatus=tracker.gettotal("Income")-tracker.gettotal("Expense")
    print(f"Current Status :Rs:{currentstatus}\n")

    print("1.To add item")
    print("2.To view item")
    print("0. Exit")
    try:
      choice=int(input("Enter your choice: "))
      if choice==0:
        print("\nThank you for using Expense Tracker!\n")
        break
      if choice==1:
        while True:
          print("1.To Add Income")
          print("2.To Add Expense")
          print("0.To Go Back")
          try:
            choice=int(input("Enter your choice: "))
            if choice==1:
              while True:
                confirmation=input("Press Any key to confirm or Press enter to Cancel \n")
                if confirmation =="":
                  break
                else:
                  name,amount,category,date=tracker.input()

                  income=Income(name=name,amount=amount,category=category,date=date,Type="Income")

                  tracker.additem(income)
                  break



            elif choice==2:
              while True:
                confirmation=input("Press Any key to confirm or Press enter to Cancel \n")
                if confirmation =="":
                  break
                else:
                  name,amount,category,date=tracker.input()

                  expense=Expense(name=name,amount=amount,category=category,date=date,Type="Expense")

                  tracker.additem(expense)
                  break

            elif choice==0:
              break
            else:
              print("Invalid choice!")
          except ValueError:
            print("Invalid input! Please enter correct number.")
            continue

      if choice==2:

          while True:

            print("1. View Expenses")
            print("2. View Income")
            print("3. View journal")
            print("0. To Back")
            try:
              choice=int(input("Enter your choice: "))
              if choice==1:
                tracker.viewexpenses()
                wanna_filer=input("Do you want to filter? (y/n): ")
                if wanna_filer.lower()=="y":
                  tracker.filter(Type="Expense")

                break
              elif choice==2:
                tracker.viewincomes()
                wanna_filer=input("Do you want to filter? (y/n): ")
                if wanna_filer.lower()=="y":
                  tracker.filter(Type="Income")
                break
              elif choice==3:
                tracker.viewjournal()
                wanna_filer=input("Do you want to filter? (y/n): ")
                if wanna_filer.lower()=="y":
                  tracker.filter()
                break


              elif choice==0:
                break
              else:
                print("Invalid choice!")
            except ValueError:
              print("Invalid input! Please enter correct number.")
              continue


    except ValueError:
      print("Invalid input! Please enter valid number.")


if __name__=="__main__":
  main()
