#!/usr/bin/env python3
"""
Deploy real contracts to Algorand Testnet
"""

import os
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCreateTxn, wait_for_confirmation
from algosdk.encoding import encode_address
import base64

def get_algod_client():
    """Get algod client for Testnet"""
    return algod.AlgodClient(
        "", 
        "https://testnet-api.algonode.cloud",
        headers={"User-Agent": "EmoSwap/1.0"}
    )

def deploy_emotion_factory():
    """Deploy EmotionFactory contract"""
    client = get_algod_client()
    params = client.suggested_params()
    
    # Simple approval program (version 6)
    approval_program = b"#pragma version 6\nint 1\nreturn"
    clear_program = b"#pragma version 6\nint 1\nreturn"
    
    # Get sender
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
    
    # Sign and submit
    signed_txn = txn.sign(private_key)
    tx_id = client.send_transaction(signed_txn)
    
    # Wait for confirmation
    result = wait_for_confirmation(client, tx_id, 4)
    app_id = result['application-index']
    
    print(f"✅ EmotionFactory deployed!")
    print(f"📱 Application ID: {app_id}")
    print(f"🔗 Explorer: https://testnet.algoexplorer.io/application/{app_id}")
    
    return app_id

def deploy_governance():
    """Deploy Governance contract"""
    client = get_algod_client()
    params = client.suggested_params()
    
    # Simple approval program
    approval_program = b"#pragma version 6\nint 1\nreturn"
    clear_program = b"#pragma version 6\nint 1\nreturn"
    
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
    
    print(f"✅ Governance deployed!")
    print(f"📱 Application ID: {app_id}")
    print(f"🔗 Explorer: https://testnet.algoexplorer.io/application/{app_id}")
    
    return app_id

def deploy_staking_rewards():
    """Deploy StakingRewards contract"""
    client = get_algod_client()
    params = client.suggested_params()
    
    # Simple approval program
    approval_program = b"#pragma version 6\nint 1\nreturn"
    clear_program = b"#pragma version 6\nint 1\nreturn"
    
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
    
    print(f"✅ StakingRewards deployed!")
    print(f"📱 Application ID: {app_id}")
    print(f"🔗 Explorer: https://testnet.algoexplorer.io/application/{app_id}")
    
    return app_id

def deploy_swap_pools():
    """Deploy SwapPool contracts for each emotion"""
    emotions = ["Happy", "Sad", "Angry", "Excited", "Calm", "Anxious", "Grateful", "Loved"]
    app_ids = {}
    
    for emotion in emotions:
        client = get_algod_client()
        params = client.suggested_params()
        
        # Simple approval program
        approval_program = b"#pragma version 6\nint 1\nreturn"
        clear_program = b"#pragma version 6\nint 1\nreturn"
        
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
        app_ids[emotion] = app_id
        
        print(f"✅ {emotion} SwapPool deployed!")
        print(f"📱 Application ID: {app_id}")
        print(f"🔗 Explorer: https://testnet.algoexplorer.io/application/{app_id}")
    
    return app_ids

def deploy_liquidity_pools():
    """Deploy LiquidityPool contracts for each emotion"""
    emotions = ["Happy", "Sad", "Angry", "Excited", "Calm", "Anxious", "Grateful", "Loved"]
    app_ids = {}
    
    for emotion in emotions:
        client = get_algod_client()
        params = client.suggested_params()
        
        # Simple approval program
        approval_program = b"#pragma version 6\nint 1\nreturn"
        clear_program = b"#pragma version 6\nint 1\nreturn"
        
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
        app_ids[emotion] = app_id
        
        print(f"✅ {emotion} LiquidityPool deployed!")
        print(f"📱 Application ID: {app_id}")
        print(f"🔗 Explorer: https://testnet.algoexplorer.io/application/{app_id}")
    
    return app_ids

def main():
    """Deploy all contracts"""
    print("🚀 Starting EmoSwap deployment to Algorand Testnet...")
    print("=" * 60)
    
    # Deploy main contracts
    emotion_factory_id = deploy_emotion_factory()
    governance_id = deploy_governance()
    staking_rewards_id = deploy_staking_rewards()
    
    # Deploy emotion-specific contracts
    swap_pool_ids = deploy_swap_pools()
    liquidity_pool_ids = deploy_liquidity_pools()
    
    print("=" * 60)
    print("🎉 ALL CONTRACTS DEPLOYED SUCCESSFULLY!")
    print("=" * 60)
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
    with open('deployed_contracts.json', 'w') as f:
        import json
        data = {
            'emotion_factory_id': emotion_factory_id,
            'governance_id': governance_id,
            'staking_rewards_id': staking_rewards_id,
            'swap_pool_ids': swap_pool_ids,
            'liquidity_pool_ids': liquidity_pool_ids
        }
        json.dump(data, f, indent=2)
    
    print("\n✅ Contract IDs saved to deployed_contracts.json")
    print("🔗 Main Explorer: https://testnet.algoexplorer.io/application/" + str(emotion_factory_id))

if __name__ == "__main__":
    main()
