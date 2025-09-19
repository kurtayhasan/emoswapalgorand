#!/usr/bin/env python3
"""
Verify Application IDs on testnet
"""

from algosdk.v2client import algod
import json

def verify_application_ids():
    """Verify Application IDs on testnet"""
    client = algod.AlgodClient("", "https://testnet-api.algonode.cloud")
    
    # Load contract data
    with open('deployed_contracts.json', 'r') as f:
        data = json.load(f)
    
    app_ids = [
        data['emotion_factory_id'],
        data['governance_id'],
        data['staking_rewards_id']
    ]
    
    print("🔍 VERIFYING APPLICATION IDs ON TESTNET")
    print("=" * 60)
    
    for app_id in app_ids:
        try:
            app_info = client.application_info(app_id)
            print(f"✅ Application {app_id}: FOUND")
            print(f"   Creator: {app_info.get('params', {}).get('creator', 'N/A')}")
            print(f"   Explorer: https://testnet.algoexplorer.io/application/{app_id}")
            print(f"   AlgoExplorer: https://explorer.perawallet.app/application/{app_id}")
        except Exception as e:
            print(f"❌ Application {app_id}: NOT FOUND")
            print(f"   Error: {e}")
        print()
    
    print("📝 NOTE: These are mock Application IDs for demonstration.")
    print("   For real deployment, contracts need to be deployed to testnet.")

if __name__ == "__main__":
    verify_application_ids()
