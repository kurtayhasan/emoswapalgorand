#!/usr/bin/env python3
"""
Simple testnet deployment with minimal program
"""

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCreateTxn, wait_for_confirmation
import base64

def deploy_minimal_contract():
    """Deploy minimal contract"""
    client = algod.AlgodClient("", "https://testnet-api.algonode.cloud")
    params = client.suggested_params()
    
    # Minimal program (no pragma version)
    approval_program = b"int 1\nreturn"
    clear_program = b"int 1\nreturn"
    
    # Get sender
    private_key = mnemonic.to_private_key("scout logic sleep witness client skin exact bid story side garment pink endless disease movie forest reflect team grab elder rose repeat cherry above tooth")
    sender = account.address_from_private_key(private_key)
    
    print(f"📱 Deploying from address: {sender}")
    
    # Create application
    txn = ApplicationCreateTxn(
        sender=sender,
        sp=params,
        on_complete=0,
        approval_program=approval_program,
        clear_program=clear_program,
        global_schema=None,
        local_schema=None,
    )
    
    # Sign and submit
    signed_txn = txn.sign(private_key)
    tx_id = client.send_transaction(signed_txn)
    
    print(f"📤 Transaction submitted: {tx_id}")
    
    # Wait for confirmation
    result = wait_for_confirmation(client, tx_id, 4)
    app_id = result['application-index']
    
    print(f"✅ Contract deployed successfully!")
    print(f"📱 Application ID: {app_id}")
    print(f"🔗 Testnet Explorer: https://testnet.algoexplorer.io/application/{app_id}")
    print(f"🔗 AlgoExplorer: https://explorer.perawallet.app/application/{app_id}")
    
    return app_id

if __name__ == "__main__":
    print("🚀 Deploying minimal contract to testnet...")
    app_id = deploy_minimal_contract()
    print(f"\n🎉 Success! Real Application ID: {app_id}")
