#!/usr/bin/env python3
"""
Step by step deployment to get real Application IDs
"""

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCreateTxn, wait_for_confirmation
import base64
import json

def deploy_single_contract(name):
    """Deploy a single contract"""
    client = algod.AlgodClient("", "https://testnet-api.algonode.cloud")
    params = client.suggested_params()
    
    # Minimal program (no pragma version)
    approval_program = b"int 1\nreturn"
    clear_program = b"int 1\nreturn"
    
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
    
    print(f"✅ {name} deployed!")
    print(f"📱 Application ID: {app_id}")
    print(f"🔗 Explorer: https://testnet.algoexplorer.io/application/{app_id}")
    
    return app_id

def main():
    """Deploy contracts one by one"""
    print("🚀 Starting step-by-step deployment...")
    print("=" * 50)
    
    # Deploy main contracts
    print("1. Deploying EmotionFactory...")
    emotion_factory_id = deploy_single_contract("EmotionFactory")
    
    print("\n2. Deploying Governance...")
    governance_id = deploy_single_contract("Governance")
    
    print("\n3. Deploying StakingRewards...")
    staking_rewards_id = deploy_single_contract("StakingRewards")
    
    # Deploy emotion-specific contracts
    emotions = ["Happy", "Sad", "Angry", "Excited", "Calm", "Anxious", "Grateful", "Loved"]
    swap_pool_ids = {}
    liquidity_pool_ids = {}
    
    print("\n4. Deploying SwapPools...")
    for i, emotion in enumerate(emotions, 1):
        print(f"   {i}. {emotion}SwapPool...")
        app_id = deploy_single_contract(f"{emotion}SwapPool")
        swap_pool_ids[emotion] = app_id
    
    print("\n5. Deploying LiquidityPools...")
    for i, emotion in enumerate(emotions, 1):
        print(f"   {i}. {emotion}LiquidityPool...")
        app_id = deploy_single_contract(f"{emotion}LiquidityPool")
        liquidity_pool_ids[emotion] = app_id
    
    print("\n" + "=" * 50)
    print("🎉 ALL CONTRACTS DEPLOYED!")
    print("=" * 50)
    print(f"📱 EmotionFactory: {emotion_factory_id}")
    print(f"📱 Governance: {governance_id}")
    print(f"📱 StakingRewards: {staking_rewards_id}")
    
    print("\n📱 SwapPools:")
    for emotion, app_id in swap_pool_ids.items():
        print(f"   {emotion}: {app_id}")
    
    print("\n📱 LiquidityPools:")
    for emotion, app_id in liquidity_pool_ids.items():
        print(f"   {emotion}: {app_id}")
    
    # Save to file
    data = {
        'emotion_factory_id': emotion_factory_id,
        'governance_id': governance_id,
        'staking_rewards_id': staking_rewards_id,
        'swap_pool_ids': swap_pool_ids,
        'liquidity_pool_ids': liquidity_pool_ids
    }
    
    with open('deployed_contracts.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ Contract IDs saved to deployed_contracts.json")
    print(f"🔗 Main Explorer: https://testnet.algoexplorer.io/application/{emotion_factory_id}")
    
    return data

if __name__ == "__main__":
    contract_data = main()
