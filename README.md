# web3py-storagesc

This repo contains a project for a simple storage contract.

## How to use

1. Create a .env file containing the three following variables:


`export WALLET_ADDRESS` with your wallet hash

`export PRIVATE_KEY` with your wallet private key

`export NODE_ADDRESS` with the address of the node you are using, which can be localhost (ganache) or remote (Infura)

2. Create a venv and run `pip install -r requirements.txt`
3. `python deploy.py` 
