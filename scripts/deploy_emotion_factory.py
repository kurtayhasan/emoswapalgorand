"""
Deploy EmotionFactory contract to Algorand Testnet
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from algosdk import account, mnemonic
from algosdk.v2client import algod

# Add contracts directory to path
sys.path.append(str(Path(__file__).parent.parent / "contracts"))

from EmotionFactory import EmotionFactory

def get_algod_client():
    """Get algod client for Testnet"""
    return algod.AlgodClient(
        "", 
        "https://testnet-api.algonode.cloud",
        headers={"User-Agent": "EmotionFactory/1.0"}
    )

def deploy():
    """Deploy EmotionFactory contract"""
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
    
    # Get suggested params
    params = algod_client.suggested_params()
    
    # Create app
    app = EmotionFactory()
    approval, clear = app.build()
    
    # Get current round
    status = algod_client.status()
    current_round = status["last-round"]
    
    print(f"Current round: {current_round}")
    
    try:
        # Create application
        app_id = app.create(
            sender=address,
            sp=params,
            signer=None,  # Use default signer
            foreign_apps=None,
            foreign_assets=None,
            app_args=None,
            local_ints=1,  # For last_mint_day
            local_bytes=1,  # For last_mint_day key
            global_ints=3,  # emotion_count, mint_amount, paused
            global_bytes=1,  # admin
            boxes=[(0, 64)],  # 64 bytes box size for emotion -> assetId mapping
        )
        
        print(f"Application ID: {app_id}")
        print(f"Explorer: https://testnet.algoexplorer.io/application/{app_id}")
        
        return app_id
    
    except Exception as e:
        print(f"Error deploying contract: {e}")
        return None

if __name__ == "__main__":
    deploy()
