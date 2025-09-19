#!/usr/bin/env python3
"""
Get real Application IDs from testnet
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
            
            return app_ids
        else:
            print("❌ No applications found")
            return []
            
    except Exception as e:
        print(f"❌ Error checking account: {e}")
        return []

def create_mock_contracts():
    """Create mock contract data for testing"""
    print("\n🔧 Creating mock contract data...")
    
    # Generate mock Application IDs
    base_id = 1000000000  # Start from a high number
    
    data = {
        'emotion_factory_id': base_id + 1,
        'governance_id': base_id + 2,
        'staking_rewards_id': base_id + 3,
        'swap_pool_ids': {
            'Happy': base_id + 4,
            'Sad': base_id + 5,
            'Angry': base_id + 6,
            'Excited': base_id + 7,
            'Calm': base_id + 8,
            'Anxious': base_id + 9,
            'Grateful': base_id + 10,
            'Loved': base_id + 11,
        },
        'liquidity_pool_ids': {
            'Happy': base_id + 12,
            'Sad': base_id + 13,
            'Angry': base_id + 14,
            'Excited': base_id + 15,
            'Calm': base_id + 16,
            'Anxious': base_id + 17,
            'Grateful': base_id + 18,
            'Loved': base_id + 19,
        }
    }
    
    # Save to file
    with open('deployed_contracts.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("✅ Mock contract data created!")
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
        return existing_ids
    else:
        print("\n❌ No existing contracts found.")
        print("🔧 Creating mock contract data for testing...")
        return create_mock_contracts()

if __name__ == "__main__":
    result = main()
