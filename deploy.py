import json
import os

from dotenv import load_dotenv
import web3
from solcx import compile_standard, install_solc
from web3 import Web3

install_solc("0.6.0")
load_dotenv()
with open("./SimpleStorage.sol", "r") as sc_file:
    simple_storage_file = sc_file.read()

compiled_simple_storage = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
print("Contract compiled..")

with open("compiled_json.json", "w") as json_file:
    json.dump(compiled_simple_storage, json_file)

bytecode = compiled_simple_storage["contracts"]["SimpleStorage.sol"]["SimpleStorage"][
    "evm"
]["bytecode"]["object"]


abi = compiled_simple_storage["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


w3 = Web3(web3.HTTPProvider(os.getenv("NODE_ADDRESS")))
chain_id = 4
wallet_address = os.getenv("WALLET_ADDRESS")
wallet_key = os.getenv("PRIVATE_KEY")
SimpleStorage_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(wallet_address)
print(f"Latest nonce: {nonce}")
transaction = SimpleStorage_contract.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": wallet_address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    }
)
signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=wallet_key
)
print(f"Signed transaction..")
tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
print("Sent Transaction..")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


# Grab the actual deployed contract

simple_storage_deployed = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print("Contract deployed..")
store_transaction = simple_storage_deployed.functions.store(10).buildTransaction(
    {
        "chainId": chain_id,
        "from": wallet_address,
        "nonce": nonce + 1,
        "gasPrice": w3.eth.gas_price,
    }
)

signed_store_transaction = w3.eth.account.sign_transaction(
    store_transaction, private_key=wallet_key
)
print("Built store transaction...")
tx_hash_store = w3.eth.send_raw_transaction(signed_store_transaction.rawTransaction)
tx_receipt_store = w3.eth.wait_for_transaction_receipt(tx_hash_store)

print(f"Store transaction successfully executed: value {simple_storage_deployed.functions.retrieve().call()}")
