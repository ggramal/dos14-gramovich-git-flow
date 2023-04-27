class CommonAccount:
  def __init__(self,client_id, amount=0):
    self.client_id = client_id
    self.__amount = amount 


  def get_amount(self):
    return self.__amount

  def transaction(self, substract, add):
    pass

class DebitAccount(CommonAccount):
  """This is an account class"""

  def __init__(self, client_id, amount=0):
     
    super().__init__(client_id, amount)
    
  def transaction(self, substract=0, add=0):
    trx = 0
    if substract > 0:
      trx = self._CommonAccount__amount - substract

    if add > 0:
      trx = self._CommonAccount__amount + add
   
    if trx < 0:
      raise ValueError("Debit account cant be less than 0")

    self._CommonAccount__amount = trx


class CreditAccount(CommonAccount):
  """This is a credit account class"""

  def __init__(self, client_id, amount=0):
    super().__init__(self)


  def transaction(self, substract=0, add=0):
    if substract > 0:
      self.__amount = self.__amount - substract

    if add > 0:
      self.__amount = self.__amount + add




def some_main():
  account = DebitAccount(client_id=1, amount=100)
  print(account.__dict__)
  print(account.get_amount())
  try:
    account.transaction(add=100)
  except ValueError as e:
    pass

  print(account.get_amount())


if __name__ == "__main__":
  some_main()
