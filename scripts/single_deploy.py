#!/usr/bin/env python3
"""
Deploy single contract for testing
"""

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCreateTxn, wait_for_confirmation
import base64

def deploy_single_contract():
    """Deploy a single contract"""
    client = algod.AlgodClient("", "https://testnet-api.algonode.cloud")
    params = client.suggested_params()
    
    # Base64 encoded minimal programs (version 2)
    approval_program = base64.b64decode("ASACAAE=")  # int 1; return
    clear_program = base64.b64decode("ASACAAE=")     # int 1; return
    
    # Get sender
    private_key = mnemonic.to_private_key("scout logic sleep witness client skin exact bid story side garment pink endless disease movie forest reflect team grab elder rose repeat cherry above tooth")
    sender = account.address_from_private_key(private_key)
    
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
    
    # Wait for confirmation
    result = wait_for_confirmation(client, tx_id, 4)
    app_id = result['application-index']
    
    print(f"✅ Contract deployed!")
    print(f"📱 Application ID: {app_id}")
    print(f"🔗 Explorer: https://testnet.algoexplorer.io/application/{app_id}")
    
    return app_id

if __name__ == "__main__":
    app_id = deploy_single_contract()
    print(f"\n🎉 Success! Application ID: {app_id}")
