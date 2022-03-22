# web3py-storagesc

This repo contains a project for a simple storage contract.

## How to use

1. Create a .env file containing the three following variables:


`export WALLET_ADDRESS` with your wallet hash

`export PRIVATE_KEY` with your wallet private key

`export NODE_ADDRESS` with the address of the node you are using, which can be localhost (ganache) or remote (Infura)

`export CHAIN_ID` with the value of the chain_id you want to use. (for e.g, ganache uses 1337)
2. Create a venv and run `pip install -r requirements.txt`
3. `python deploy.py` 
