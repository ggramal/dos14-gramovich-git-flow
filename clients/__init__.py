import csv

class AccountClient:
  def __init__(self, client_id):
    self.__client_id = client_id
    self.__withdraw = False

  @property
  def withdraw(self):
    return slef.__withdraw

  @withdraw.setter
  def withdraw(self, value):
    self.__withdraw = value


  def transaction(self, substract=0, add=0):
    with open('transactions.csv', mode='a', newline='') as file:
      writer = csv.writer(file)
      if substract > 0:
        writer.writerow([self.__client_id, substract, 'substract'])
      elif add > 0:
        writer.writerow([self.__client_id, add, 'add'])
