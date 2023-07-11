import yaml
import config
from flask import Flask, abort, make_response, request
from time import sleep
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    f"postgresql://{config.PG_USER}:{config.PG_PASSWORD}@{config.PG_HOST}:{config.PG_PORT}/{config.PG_DATABASE}",
)

Base = declarative_base()

app = Flask(__name__)

class TransactionError(Exception):
  pass

class WithdrawalBlocked(Exception):
  pass

class CommonAccount(Base):
  __tablename__ = "accounts"

  client_id = Column(Integer, primary_key=True)
  withdraw = Column(Boolean)
  amount = Column(Float)
  type = Column(String)

  def __init__(self,client_id, type, withdraw=True, amount=0):
    self.client_id = client_id
    self.withdraw = withdraw
    self.amount = amount
    self.type = type

  def to_dict(self):
    return {
      "client_id": self.client_id,
      "amount": self.amount,
      "type": self.type,
      "withdraw": self.withdraw
    }

  def transaction(self, substract, add):
    pass

class DebitAccount(CommonAccount):
  """This is a debit account class"""

  def __init__(self, client_id, type, withdraw=True, amount=0):
    super().__init__(client_id, type, withdraw, amount)

  def transaction(self, substract=0, add=0):
    trx = self.amount
    if substract > 0:
      if not self.withdraw:
        raise WithdrawalBlocked("Withdrawal blocked. For this account")
      trx = self.amount - substract

    if add > 0:
      trx = self.amount + add

    if trx < 0:
      raise TransactionError("Debit account cant be less than 0")

    self.amount = trx


class CreditAccount(CommonAccount):
  """This is a credit account class"""

  def __init__(self, client_id, type, withdraw=True, amount=0):
    super().__init__(client_id, type, withdraw, amount)

  def transaction(self, substract=0, add=0):
    if substract > 0:
      self.amount = self.amount - substract

    if add > 0:
      self.amount = self.amount + add

def read_accounts(account_file):
  accounts = session.query(CommonAccount).all()
  if not accounts:
    with open(account_file, "r") as f:
      accounts_dict = yaml.safe_load(f)
    for acc in accounts_dict:
      accounts.append(CommonAccount(**acc))
    try:
        session.add_all(accounts)
        session.commit()
    except IntegrityError as err:
        session.rollback()
  return [acc.to_dict() for acc in accounts]




def write_accounts(account_file):
  accounts = {
    **all_accounts["creditaccounts"],
    **all_accounts["debitaccounts"]
  }
  accs = [account for client_id, account in accounts.items()]
  try:
      session.add(accs)
      session.commit()
  except IntegrityError as err:
      session.rollback()

def init():
  accounts = read_accounts(account_file)
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
def read_accs(account_type):
  try:
    accounts = all_accounts[account_type]
    response = [account.to_dict() for client_id, account in accounts.items()]
  except KeyError as ek:
    response = make_response(
      {
        "status": "error",
        "message": f"account type - {account_type}. Is a wrong account type. Must be one of {','.join(all_accounts.keys())}"
      }
    )
    response.status = 404

  return response

@app.route("/api/v1/<string:account_type>/<int:client_id>", methods=["GET"])
def read_acc(account_type, client_id):
  try:
    accounts = all_accounts[account_type]
    try:
      response = make_response(accounts[client_id].to_dict())
    except KeyError:
      response = make_response({"status": "error", "message": "Client not found"})
      response.status = 404
  except KeyError as ek:
    response = make_response(
      {
        "status": "error",
        "message": f"account type - {account_type}. Is a wrong account type. Must be one of {','.join(all_accounts.keys())}"
      }
    )
    response.status = 404

  return response

@app.route("/api/v1/<string:account_type>/<int:client_id>/transaction", methods=["POST"])
def transaction(account_type, client_id):
  try:
    accounts = all_accounts[account_type]
    r = request.json
    try:
      account = accounts[client_id]
      account.transaction(**r)
      write_accounts(account_file)
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
  except KeyError as ek:
    response = make_response(
      {
        "status": "error",
        "message": f"account type - {account_type}. Is a wrong account type. Must be one of {','.join(all_accounts.keys())}"
      }
    )
    response.status = 404

  return response

@app.route("/api/v1/<string:account_type>", methods=["PUT"])
def create_acc(account_type):
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
  else:
    response = make_response(
      {
        "status": "error",
        "message": f"account type - {account_type}. Is a wrong account type. Must be one of {','.join(all_accounts.keys())}"
      }
    )
    response.status = 404
    return response

  write_accounts(account_file)

  response = make_response({"status": "ok", "message": f"Account for {client_id} created"})
  response.status = 201

  return response



Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

all_accounts = {}
account_file = "account.yaml"

debit_accounts, credit_accounts = init()
all_accounts["debitaccounts"] = debit_accounts
all_accounts["creditaccounts"] = credit_accounts
