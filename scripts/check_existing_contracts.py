#!/usr/bin/env python3
"""
Check existing contracts on testnet
"""

from algosdk import account, mnemonic
from algosdk.v2client import algod
import json

def check_existing_contracts():
    """Check if there are existing contracts"""
    client = algod.AlgodClient("", "https://testnet-api.algonode.cloud")
    
    # Get sender
    private_key = mnemonic.to_private_key("scout logic sleep witness client skin exact bid story side garment pink endless disease movie forest reflect team grab elder rose repeat cherry above tooth")
    sender = account.address_from_private_key(private_key)
    
    try:
        # Get account info
        account_info = client.account_info(sender)
        created_apps = account_info.get('created-apps', [])
        
        print(f"📱 Account: {sender}")
        print(f"📊 Created Applications: {len(created_apps)}")
        
        if created_apps:
            print("\n📱 Existing Applications:")
            for i, app in enumerate(created_apps, 1):
                app_id = app['id']
                print(f"   {i}. Application ID: {app_id}")
                print(f"      Explorer: https://testnet.algoexplorer.io/application/{app_id}")
        else:
            print("❌ No applications found")
            
        return created_apps
        
    except Exception as e:
        print(f"❌ Error checking account: {e}")
        return []

if __name__ == "__main__":
    apps = check_existing_contracts()
