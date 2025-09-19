#!/usr/bin/env python3
"""
Get real Application IDs from testnet using AlgoSDK
"""

from algosdk import account, mnemonic
from algosdk.v2client import algod
import json

def get_real_application_ids():
    """Get real Application IDs from testnet"""
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
            app_ids = []
            for i, app in enumerate(created_apps, 1):
                app_id = app['id']
                app_ids.append(app_id)
                print(f"   {i}. Application ID: {app_id}")
                print(f"      Explorer: https://testnet.algoexplorer.io/application/{app_id}")
                print(f"      AlgoExplorer: https://explorer.perawallet.app/application/{app_id}")
            
            return app_ids
        else:
            print("❌ No applications found")
            return []
            
    except Exception as e:
        print(f"❌ Error checking account: {e}")
        return []

def create_real_contracts():
    """Create real contract data based on existing apps"""
    print("\n🔧 Creating real contract data...")
    
    # Get existing apps
    existing_apps = get_real_application_ids()
    
    if existing_apps:
        print(f"\n✅ Found {len(existing_apps)} existing contracts!")
        
        # Use existing apps
        data = {
            'emotion_factory_id': existing_apps[0] if len(existing_apps) > 0 else 0,
            'governance_id': existing_apps[1] if len(existing_apps) > 1 else 0,
            'staking_rewards_id': existing_apps[2] if len(existing_apps) > 2 else 0,
            'swap_pool_ids': {
                'Happy': existing_apps[3] if len(existing_apps) > 3 else 0,
                'Sad': existing_apps[4] if len(existing_apps) > 4 else 0,
                'Angry': existing_apps[5] if len(existing_apps) > 5 else 0,
                'Excited': existing_apps[6] if len(existing_apps) > 6 else 0,
                'Calm': existing_apps[7] if len(existing_apps) > 7 else 0,
                'Anxious': existing_apps[8] if len(existing_apps) > 8 else 0,
                'Grateful': existing_apps[9] if len(existing_apps) > 9 else 0,
                'Loved': existing_apps[10] if len(existing_apps) > 10 else 0,
            },
            'liquidity_pool_ids': {
                'Happy': existing_apps[11] if len(existing_apps) > 11 else 0,
                'Sad': existing_apps[12] if len(existing_apps) > 12 else 0,
                'Angry': existing_apps[13] if len(existing_apps) > 13 else 0,
                'Excited': existing_apps[14] if len(existing_apps) > 14 else 0,
                'Calm': existing_apps[15] if len(existing_apps) > 15 else 0,
                'Anxious': existing_apps[16] if len(existing_apps) > 16 else 0,
                'Grateful': existing_apps[17] if len(existing_apps) > 17 else 0,
                'Loved': existing_apps[18] if len(existing_apps) > 18 else 0,
            }
        }
    else:
        print("❌ No existing contracts found. Creating mock data...")
        
        # Create mock data with realistic IDs
        data = {
            'emotion_factory_id': 0,  # Will be updated when deployed
            'governance_id': 0,
            'staking_rewards_id': 0,
            'swap_pool_ids': {
                'Happy': 0,
                'Sad': 0,
                'Angry': 0,
                'Excited': 0,
                'Calm': 0,
                'Anxious': 0,
                'Grateful': 0,
                'Loved': 0,
            },
            'liquidity_pool_ids': {
                'Happy': 0,
                'Sad': 0,
                'Angry': 0,
                'Excited': 0,
                'Calm': 0,
                'Anxious': 0,
                'Grateful': 0,
                'Loved': 0,
            }
        }
    
    # Save to file
    with open('deployed_contracts.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("✅ Contract data created!")
    print(f"📱 EmotionFactory: {data['emotion_factory_id']}")
    print(f"📱 Governance: {data['governance_id']}")
    print(f"📱 StakingRewards: {data['staking_rewards_id']}")
    
    return data

def main():
    """Main function"""
    print("🚀 Getting real Application IDs from testnet...")
    print("=" * 60)
    
    # Check existing contracts
    existing_ids = get_real_application_ids()
    
    if existing_ids:
        print(f"\n✅ Found {len(existing_ids)} existing contracts!")
        return create_real_contracts()
    else:
        print("\n❌ No existing contracts found.")
        print("🔧 Creating mock contract data for testing...")
        return create_real_contracts()

if __name__ == "__main__":
    result = main()
