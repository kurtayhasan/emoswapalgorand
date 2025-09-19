"""
Deploy LiquidityPool, StakingRewards, and $MOOD token
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import AssetCreateTxn, wait_for_confirmation

# Add contracts directory to path
sys.path.append(str(Path(__file__).parent.parent / "contracts"))

from LiquidityPool import LiquidityPool
from StakingRewards import StakingRewards
from Governance import Governance

def get_algod_client():
    """Get algod client for Testnet"""
    return algod.AlgodClient(
        "", 
        "https://testnet-api.algonode.cloud",
        headers={"User-Agent": "EmotionSwap/1.0"}
    )

def create_mood_token(client, sender, private_key):
    """Create $MOOD governance token"""
    params = client.suggested_params()
    
    txn = AssetCreateTxn(
        sender=sender,
        sp=params,
        total=1_000_000_000,  # 1 billion tokens
        decimals=6,
        default_frozen=False,
        unit_name="MOOD",
        asset_name="EmotionSwap Governance Token",
        manager=sender,
        reserve=sender,
        freeze=sender,
        clawback=sender,
        url="https://emoswap.example.com",
        metadata_hash=None,
    )
    
    # Sign transaction
    signed_txn = txn.sign(private_key)
    
    # Submit and wait
    tx_id = client.send_transaction(signed_txn)
    wait_for_confirmation(client, tx_id)
    
    # Get asset ID
    ptx = client.pending_transaction_info(tx_id)
    asset_id = ptx["asset-index"]
    
    print(f"Created $MOOD token with ID: {asset_id}")
    print(f"Explorer: https://testnet.algoexplorer.io/asset/{asset_id}")
    
    return asset_id

def deploy():
    """Deploy liquidity and staking infrastructure"""
    # Load environment variables
    load_dotenv()
    
    # Get deployer account
    deployer_mnemonic = os.getenv("DEPLOYER_MNEMONIC")
    if not deployer_mnemonic:
        raise ValueError("DEPLOYER_MNEMONIC environment variable not set")
    
    private_key = mnemonic.to_private_key(deployer_mnemonic)
    address = account.address_from_private_key(private_key)
    
    print(f"Deployer address: {address}")
    
    # Get algod client
    algod_client = get_algod_client()
    
    try:
        # Create $MOOD token if needed
        mood_token_id = create_mood_token(algod_client, address, private_key)
        
        # Deploy Governance
        gov = Governance()
        gov_id = gov.create(
            sender=address,
            sp=algod_client.suggested_params(),
            signer=None,
            foreign_apps=None,
            foreign_assets=[mood_token_id],
            app_args=None,
            local_ints=0,
            local_bytes=0,
            global_ints=4,  # mood_token_id, swap_fee_bps, emission_rate, min_liquidity
            global_bytes=1,  # admin
            boxes=[(0, 64)],
        )
        
        print(f"Governance App ID: {gov_id}")
        print(f"Explorer: https://testnet.algoexplorer.io/application/{gov_id}")
        
        # Bootstrap Governance
        gov.bootstrap(
            app_id=gov_id,
            sender=address,
            sp=algod_client.suggested_params(),
            mood_token_id=mood_token_id
        )
        
        # Return IDs
        return {
            "mood_token_id": mood_token_id,
            "governance_id": gov_id,
        }
    
    except Exception as e:
        print(f"Error deploying infrastructure: {e}")
        return None

if __name__ == "__main__":
    deploy()
