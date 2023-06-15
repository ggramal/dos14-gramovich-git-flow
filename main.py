import yaml
from flask import Flask, abort, make_response, request
from time import sleep

app = Flask(__name__)

class TransactionError(Exception):
  pass

class WithdrawalBlocked(Exception):
  pass

class CommonAccount:
  def __init__(self,client_id, type, withdraw=True, amount=0):
    self.__client_id = client_id
    self.withdraw = withdraw
    self._amount = amount
    self.__type = type

  def to_dict(self):
    return {
      "client_id": self.client_id,
      "amount": self.amount,
      "type": self.type,
      "withdraw": self.withdraw
    }

  @property
  def client_id(self):
    return self.__client_id

  @property
  def type(self):
    return self.__type

  @property
  def amount(self):
    return self._amount

  def transaction(self, substract, add):
    pass

class DebitAccount(CommonAccount):
  """This is a debit account class"""

  def __init__(self, client_id, type, withdraw=True, amount=0):
    super().__init__(client_id, type, withdraw, amount)

  def transaction(self, substract=0, add=0):
    trx = self._amount
    if substract > 0:
      if not self.withdraw:
        raise WithdrawalBlocked("Withdrawal blocked. For this account")
      trx = self._amount - substract

    if add > 0:
      trx = self._amount + add

    if trx < 0:
      raise TransactionError("Debit account cant be less than 0")

    self._amount = trx


class CreditAccount(CommonAccount):
  """This is a credit account class"""

  def __init__(self, client_id, type, withdraw=True, amount=0):
    super().__init__(client_id, type, withdraw, amount)

  def transaction(self, substract=0, add=0):
    if substract > 0:
      self._amount = self._amount - substract

    if add > 0:
      self._amount = self._amount + add

def read_accounts_file(account_file):
  with open(account_file, "r") as f:
    return yaml.safe_load(f)

def write_accounts_file(account_file):
  accounts = {
    **all_accounts["creditaccounts"],
    **all_accounts["debitaccounts"]
  }
  accs = [account.to_dict() for client_id, account in accounts.items()]
  with open(account_file,"w") as f:
    yaml.dump(accs, f, allow_unicode=True)

def init():
  accounts = read_accounts_file(account_file)
  debit_account_dict = {}
  credit_account_dict = {}
  for account in accounts:
      client_id = int(account["client_id"])
      if account["type"] == "credit":
        credit_account_dict[client_id] = CreditAccount(**account)
      elif account["type"] == "debit":
        debit_account_dict[client_id] = DebitAccount(**account)
  return debit_account_dict, credit_account_dict

@app.route("/api/v1/<string:account_type>", methods=["GET"])
def read_accounts(account_type):
  try:
    accounts = all_accounts[account_type]
  except KeyError as ek:
    response = make_response(
      {
        "status": "error",
        "message": f"account type - {account_type}. Is a wrong account type. Must be one of {','.join(accounts.keys())}"
      }
    )
    response.status = 404
    return response

  return [account.to_dict() for client_id, account in accounts.items()]

@app.route("/api/v1/<string:account_type>/<int:client_id>", methods=["GET"])
def read_account(account_type, client_id):
  try:
    accounts = all_accounts[account_type]
  except KeyError as ek:
    response = make_response(
      {
        "status": "error",
        "message": f"account type - {account_type}. Is a wrong account type. Must be one of {','.join(accounts.keys())}"
      }
    )
    response.status = 404
    return response

  try:
    response = make_response(accounts[client_id].to_dict())
  except KeyError:
    response = make_response({"status": "error", "message": "Client not found"})
    response.status = 404

  return response

@app.route("/api/v1/<string:account_type>/<int:client_id>/transaction", methods=["POST"])
def transaction(account_type, client_id):
  try:
    accounts = all_accounts[account_type]
  except KeyError as ek:
    response = make_response(
      {
        "status": "error",
        "message": f"account type - {account_type}. Is a wrong account type. Must be one of {','.join(accounts.keys())}"
      }
    )
    response.status = 404
    return response

  r = request.json
  try:
    account = accounts[client_id]
    account.transaction(**r)
    write_accounts_file(account_file)
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

@app.route("/api/v1/<string:account_type>", methods=["PUT"])
def create_account(account_type):
  accounts = {
    **all_accounts["creditaccounts"],
    **all_accounts["debitaccounts"]
  }
  account = request.json

  if account["client_id"] in accounts.keys():
    response = make_response({"status": "error", "message": "Client already has an account"})
    response.status = 406
    return response

  client_id = account["client_id"]
  if account_type == "creditaccounts":
    account["type"] = "credit"
    all_accounts[account_type][client_id] = CreditAccount(**account)
  elif account_type == "debitaccounts":
    account["type"] = "debit"
    all_accounts[account_type][client_id] = DebitAccount(**account)

  write_accounts_file(account_file)

  response = make_response({"status": "ok", "message": f"Account for {client_id} created"})
  response.status = 201

  return response


all_accounts = {}
account_file = "account.yaml"
debit_accounts, credit_accounts = init()
all_accounts["debitaccounts"] = debit_accounts
all_accounts["creditaccounts"] = credit_accounts
