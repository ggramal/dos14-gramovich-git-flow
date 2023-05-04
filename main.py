import yaml
from flask import Flask, abort, make_response, request

app = Flask(__name__)

class TransactionError(Exception):
  pass

class WithdrawalBlocked(Exception):
  pass

class CommonAccount:
  def __init__(self,client_id, type, withdraw=False, amount=0):
    self.__client_id = client_id
    self.withdraw = withdraw
    self.type = type

  @property
  def client_id(self):
    return self.__client_id

  def amount(self):
    pass

  def transaction(self, substract, add):
    pass

class DebitAccount(CommonAccount):
  """This is a debit account class"""

  def __init__(self, client_id, type, withdraw=False, amount=0):
    self.__amount = amount
    super().__init__(client_id, type, withdraw)
   
  @property
  def amount(self):
    return self.__amount

  
  def to_dict(self):
    return {
      "client_id": self.client_id,
      "amount": self.amount,
      "type": self.type,
      "withdraw": self.withdraw
    }

  def transaction(self, substract=0, add=0):
    trx = self.__amount
    if substract > 0:
      if not self.withdraw:
        raise WithdrawalBlocked("Withdrawal blocked. For this account")
      trx = self.__amount - substract

    if add > 0:
      trx = self.__amount + add
   
    if trx < 0:
      raise TransactionError("Debit account cant be less than 0")

    self.__amount = trx


class CreditAccount(CommonAccount):
  """This is a credit account class"""

  def __init__(self, client_id, type, withdraw=False, amount=0):
    self.__amount = amount
    super().__init__(client_id, type, withdraw)

  @property
  def amount(self):
    return self.__amount

  def to_dict(self):
    return {
      "client_id": self.client_id,
      "amount": self.amount,
      "type": self.type,
      "withdraw": self.withdraw
    }

  def transaction(self, substract=0, add=0):
    if substract > 0:
      self.__amount = self.__amount - substract

    if add > 0:
      self.__amount = self.__amount + add

def read_accounts_file(account_file):
  with open(account_file, "r") as f:
    return yaml.safe_load(f)
  
def write_accounts_file(account_file, accounts):
  accs = [account.to_dict() for client_id, account in accounts.items()]
  with open(account_file,"w") as f:
    yaml.dump(accs, f, allow_unicode=True)

def init():
  accounts = read_accounts_file(account_file)
  account_dict = {}
  for account in accounts:
      client_id = int(account["client_id"])
      if account["type"] == "credit":
        account_dict[client_id] = CreditAccount(**account)
      elif account["type"] == "debit":
        account_dict[client_id] = DebitAccount(**account)
  return account_dict

account_file = "account.yaml"
accounts = init()

@app.route("/api/v1/accounts", methods=["GET"])
def read_accounts():
  return [account.to_dict() for client_id, account in accounts.items()]

@app.route("/api/v1/accounts/<int:client_id>", methods=["GET"])
def read_account(client_id):
  try:
    response = make_response(accounts[client_id].to_dict())
  except KeyError:
    response = make_response({"status": "error", "message": "Client not found"})
    response.status = 404 
  
  return response

@app.route("/api/v1/accounts/<int:client_id>/transaction", methods=["POST"])
def transaction(client_id):
  r = request.json
  try:
    account = accounts[client_id]
    account.transaction(**r)
    write_accounts_file(account_file, accounts)
    response = make_response(account.to_dict())
  except KeyError as ek:
    response = make_response({"status": "error", "message": "Client not found"})
    response.status = 404 
  except TransactionError as e:
    response = make_response({"status": "error", "message": f"{e}"})
    response.status = 400
  except WithdrawalBlocked as e:
    response = make_response({"status": "error", "message": f"{e}"})
    response.status = 403
        
  return response

@app.route("/api/v1/accounts", methods=["PUT"])
def create_account():
  account = request.json
  response = make_response({"status": "error", "message": "Client already has an account"})
  response.status = 406 
  if account["client_id"] not in accounts.keys():
    if account["type"] == "credit":
      accounts[client_id] = CreditAccount(**account)
    elif account["type"] == "debit":
      accounts[client_id] = DebitAccount(**account)

    write_accounts_file(account_file, accounts)

    response = make_response({"status": "ok", "message": f"Account for {client_id} created"})
    response.status = 201
    
  return response
