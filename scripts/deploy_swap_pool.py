"""
Deploy SwapPool contract to Algorand Testnet
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from algosdk import account, mnemonic
from algosdk.v2client import algod

# Add contracts directory to path
sys.path.append(str(Path(__file__).parent.parent / "contracts"))

from SwapPool import SwapPool

def get_algod_client():
    """Get algod client for Testnet"""
    return algod.AlgodClient(
        "", 
        "https://testnet-api.algonode.cloud",
        headers={"User-Agent": "SwapPool/1.0"}
    )

def deploy(asset_id: int):
    """Deploy SwapPool contract for an emotion asset"""
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
    app = SwapPool()
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
            foreign_assets=[asset_id],
            app_args=None,
            local_ints=0,
            local_bytes=0,
            global_ints=5,  # asset_id, algo_reserve, asset_reserve, fee_bps, is_bootstrapped
            global_bytes=1,  # fee_sink
            boxes=[(0, 64)],  # 64 bytes box size
        )
        
        print(f"Application ID: {app_id}")
        print(f"Explorer: https://testnet.algoexplorer.io/application/{app_id}")
        
        # Bootstrap pool with asset
        result = app.bootstrap(
            app_id=app_id,
            sender=address,
            sp=params,
            asset_id=asset_id
        )
        
        print(f"Pool bootstrapped with asset {asset_id}")
        
        return app_id
    
    except Exception as e:
        print(f"Error deploying contract: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python deploy_swap_pool.py <asset_id>")
        sys.exit(1)
    
    asset_id = int(sys.argv[1])
    deploy(asset_id)
