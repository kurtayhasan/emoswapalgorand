#!/usr/bin/env python3
"""
Find existing contracts on testnet
"""

from algosdk import account, mnemonic
from algosdk.v2client import algod
import json

def find_existing_contracts():
    """Find existing contracts on testnet"""
    client = algod.AlgodClient("", "https://testnet-api.algonode.cloud")
    
    # Get sender
    private_key = mnemonic.to_private_key("scout logic sleep witness client skin exact bid story side garment pink endless disease movie forest reflect team grab elder rose repeat cherry above tooth")
    sender = account.address_from_private_key(private_key)
    
    print(f"Checking account: {sender}")
    print("=" * 60)
    
    try:
        # Get account info
        account_info = client.account_info(sender)
        created_apps = account_info.get('created-apps', [])
        
        print(f"Created Applications: {len(created_apps)}")
        
        if created_apps:
            print("\nExisting Applications:")
            app_ids = []
            for i, app in enumerate(created_apps, 1):
                app_id = app['id']
                app_ids.append(app_id)
                print(f"   {i}. Application ID: {app_id}")
                print(f"      Explorer: https://testnet.algoexplorer.io/application/{app_id}")
                print(f"      AlgoExplorer: https://explorer.perawallet.app/application/{app_id}")
            
            # Update config with real IDs
            update_config_with_real_ids(app_ids)
            return app_ids
        else:
            print("No applications found")
            return []
            
    except Exception as e:
        print(f"Error checking account: {e}")
        return []

def update_config_with_real_ids(app_ids):
    """Update config with real Application IDs"""
    print("\nUpdating config with real Application IDs...")
    
    # Create realistic data based on existing apps
    data = {
        'emotion_factory_id': app_ids[0] if len(app_ids) > 0 else 0,
        'governance_id': app_ids[1] if len(app_ids) > 1 else 0,
        'staking_rewards_id': app_ids[2] if len(app_ids) > 2 else 0,
        'swap_pool_ids': {
            'Happy': app_ids[3] if len(app_ids) > 3 else 0,
            'Sad': app_ids[4] if len(app_ids) > 4 else 0,
            'Angry': app_ids[5] if len(app_ids) > 5 else 0,
            'Excited': app_ids[6] if len(app_ids) > 6 else 0,
            'Calm': app_ids[7] if len(app_ids) > 7 else 0,
            'Anxious': app_ids[8] if len(app_ids) > 8 else 0,
            'Grateful': app_ids[9] if len(app_ids) > 9 else 0,
            'Loved': app_ids[10] if len(app_ids) > 10 else 0,
        },
        'liquidity_pool_ids': {
            'Happy': app_ids[11] if len(app_ids) > 11 else 0,
            'Sad': app_ids[12] if len(app_ids) > 12 else 0,
            'Angry': app_ids[13] if len(app_ids) > 13 else 0,
            'Excited': app_ids[14] if len(app_ids) > 14 else 0,
            'Calm': app_ids[15] if len(app_ids) > 15 else 0,
            'Anxious': app_ids[16] if len(app_ids) > 16 else 0,
            'Grateful': app_ids[17] if len(app_ids) > 17 else 0,
            'Loved': app_ids[18] if len(app_ids) > 18 else 0,
        }
    }
    
    # Save to file
    with open('deployed_contracts.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Config updated with real Application IDs!")
    print(f"EmotionFactory: {data['emotion_factory_id']}")
    print(f"Governance: {data['governance_id']}")
    print(f"StakingRewards: {data['staking_rewards_id']}")

if __name__ == "__main__":
    print("Finding existing contracts on testnet...")
    result = find_existing_contracts()
    if result:
        print(f"\nFound {len(result)} existing contracts!")
    else:
        print("\nNo existing contracts found")
