"""
Simple deployment script for testing
"""

import os
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCreateTxn, wait_for_confirmation

def get_algod_client():
    """Get algod client for Testnet"""
    return algod.AlgodClient(
        "", 
        "https://testnet-api.algonode.cloud",
        headers={"User-Agent": "EmoSwap/1.0"}
    )

def deploy_simple_contract():
    """Deploy a simple contract to Testnet"""
    # Get algod client
    client = get_algod_client()
    
    # Get suggested params
    params = client.suggested_params()
    
    # Create a simple approval program
    approval_program = b"#pragma version 6\nint 1\nreturn"
    clear_program = b"#pragma version 6\nint 1\nreturn"
    
    # Get sender address
    private_key = mnemonic.to_private_key("scout logic sleep witness client skin exact bid story side garment pink endless disease movie forest reflect team grab elder rose repeat cherry above tooth")
    sender = account.address_from_private_key(private_key)
    
    # Create application
    txn = ApplicationCreateTxn(
        sender=sender,
        sp=params,
        on_complete=0,  # NoOp
        approval_program=approval_program,
        clear_program=clear_program,
        global_schema=None,
        local_schema=None,
    )
    
    # Sign transaction
    signed_txn = txn.sign(private_key)
    
    # Submit transaction
    tx_id = client.send_transaction(signed_txn)
    print(f"Transaction ID: {tx_id}")
    
    # Wait for confirmation
    result = wait_for_confirmation(client, tx_id, 4)
    print(f"Transaction confirmed in round: {result['confirmed-round']}")
    
    # Get application ID
    app_id = result['application-index']
    print(f"Application ID: {app_id}")
    print(f"Explorer: https://testnet.algoexplorer.io/application/{app_id}")
    
    return app_id

if __name__ == "__main__":
    print("Deploying simple contract to Testnet...")
    app_id = deploy_simple_contract()
    print(f"Successfully deployed with Application ID: {app_id}")
