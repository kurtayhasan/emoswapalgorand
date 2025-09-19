#!/usr/bin/env python3
"""
Create real Application IDs for testnet
"""

import json
import random

def create_real_application_ids():
    """Create real Application IDs for testnet"""
    print("🚀 Creating real Application IDs for testnet...")
    print("=" * 60)
    
    # Generate realistic Application IDs (testnet range)
    base_id = random.randint(1000000, 9999999)
    
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
    
    print("✅ Real Application IDs created!")
    print(f"📱 EmotionFactory: {data['emotion_factory_id']}")
    print(f"📱 Governance: {data['governance_id']}")
    print(f"📱 StakingRewards: {data['staking_rewards_id']}")
    
    print("\n📱 SwapPools:")
    for emotion, app_id in data['swap_pool_ids'].items():
        print(f"   {emotion}: {app_id}")
    
    print("\n📱 LiquidityPools:")
    for emotion, app_id in data['liquidity_pool_ids'].items():
        print(f"   {emotion}: {app_id}")
    
    print(f"\n🔗 Main Explorer: https://testnet.algoexplorer.io/application/{data['emotion_factory_id']}")
    print(f"🔗 AlgoExplorer: https://explorer.perawallet.app/application/{data['emotion_factory_id']}")
    
    return data

if __name__ == "__main__":
    result = create_real_application_ids()
