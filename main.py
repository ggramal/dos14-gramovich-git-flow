class CommonAccount:
  def __init__(self,client_id, amount=0):
    self.__client_id = client_id


  def amount(self):
    pass

  def transaction(self, substract, add):
    pass

class DebitAccount(CommonAccount):
  """This is a debit account class"""

  def __init__(self, client_id, amount=0):
    self.__amount = amount
    super().__init__(client_id)
    
  def amount(self):
    return self.__amount

  def transaction(self, substract=0, add=0):
    trx = 0
    if substract > 0:
      trx = self.__amount - substract

    if add > 0:
      trx = self.__amount + add
   
    if trx < 0:
      raise ValueError("Debit account cant be less than 0")

    self.__amount = trx


class CreditAccount(CommonAccount):
  """This is a credit account class"""

  def __init__(self, client_id, amount=0):
    self.__amount = amount
    super().__init__(client_id)


  def amount(self):
    return self.__amount

  def transaction(self, substract=0, add=0):
    if substract > 0:
      self.__amount = self.__amount - substract

    if add > 0:
      self.__amount = self.__amount + add




def some_main():
  account = DebitAccount(client_id=1, amount=100)
  #account._amount = 200
  print(account.amount())
  try:
    account.transaction(-1)
  except ValueError as e:
    pass

  print(account.amount())


if __name__ == "__main__":
  some_main()
