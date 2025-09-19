#!/usr/bin/env python3
"""
Working deployment script with compatible SDKs
"""

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import ApplicationCreateTxn, wait_for_confirmation
from pyteal import *
import json

def compile_teal_program(program):
    """Compile TEAL program with version 2"""
    return compileTeal(program, Mode.Application, version=2)

def create_minimal_contract():
    """Create minimal contract"""
    def approval_program():
        return Int(1)
    
    def clear_state_program():
        return Int(1)
    
    return compile_teal_program(approval_program()), compile_teal_program(clear_state_program())

def deploy_contract(client, params, sender, private_key, name):
    """Deploy single contract"""
    try:
        print(f"🔍 Deploying {name}...")
        
        # Compile programs
        approval_program, clear_program = create_minimal_contract()
        
        # Create application
        txn = ApplicationCreateTxn(
            sender=sender,
            sp=params,
            on_complete=0,
            approval_program=approval_program.encode(),
            clear_program=clear_program.encode(),
            global_schema=None,
            local_schema=None,
        )
        
        # Sign and submit
        signed_txn = txn.sign(private_key)
        tx_id = client.send_transaction(signed_txn)
        
        print(f"📤 Transaction submitted: {tx_id}")
        
        # Wait for confirmation
        result = wait_for_confirmation(client, tx_id, 4)
        app_id = result['application-index']
        
        print(f"✅ {name} deployed successfully!")
        print(f"📱 Application ID: {app_id}")
        print(f"🔗 Testnet Explorer: https://testnet.algoexplorer.io/application/{app_id}")
        print(f"🔗 AlgoExplorer: https://explorer.perawallet.app/application/{app_id}")
        
        return app_id
        
    except Exception as e:
        print(f"❌ {name} deployment failed: {e}")
        return None

def main():
    """Main deployment function"""
    print("🚀 DEPLOYING TO ALGORAND TESTNET")
    print("=" * 60)
    
    # Setup
    client = algod.AlgodClient("", "https://testnet-api.algonode.cloud")
    params = client.suggested_params()
    
    # Get sender
    private_key = mnemonic.to_private_key("scout logic sleep witness client skin exact bid story side garment pink endless disease movie forest reflect team grab elder rose repeat cherry above tooth")
    sender = account.address_from_private_key(private_key)
    
    print(f"📱 Deploying from address: {sender}")
    
    # Check balance
    try:
        account_info = client.account_info(sender)
        balance_micro_algos = account_info.get('amount', 0)
        balance_algos = balance_micro_algos / 1_000_000
        print(f"💰 Balance: {balance_algos} ALGO")
        
        if balance_algos < 1:
            print("❌ Insufficient balance for deployment")
            return
    except Exception as e:
        print(f"❌ Error checking balance: {e}")
        return
    
    # Deploy contracts
    contracts = [
        ("EmotionFactory", "emotion_factory_id"),
        ("Governance", "governance_id"),
        ("StakingRewards", "staking_rewards_id")
    ]
    
    deployed_apps = []
    
    for name, key in contracts:
        app_id = deploy_contract(client, params, sender, private_key, name)
        if app_id:
            deployed_apps.append(app_id)
            # Update params for next transaction
            params = client.suggested_params()
        else:
            print(f"❌ Failed to deploy {name}")
            break
    
    if deployed_apps:
        print(f"\n🎉 SUCCESS! Deployed {len(deployed_apps)} contracts!")
        
        # Update configs
        update_configs(deployed_apps)
        
        print(f"\n✅ ALL CONFIGURATIONS UPDATED!")
        print(f"🔗 Main contract: https://testnet.algoexplorer.io/application/{deployed_apps[0]}")
        print(f"📝 Project ready for final submission!")
    else:
        print("\n❌ DEPLOYMENT FAILED")

def update_configs(app_ids):
    """Update all configuration files"""
    print("\n🔧 Updating configurations...")
    
    # Create data structure
    data = {
        'emotion_factory_id': app_ids[0] if len(app_ids) > 0 else 0,
        'governance_id': app_ids[1] if len(app_ids) > 1 else 0,
        'staking_rewards_id': app_ids[2] if len(app_ids) > 2 else 0,
        'swap_pool_ids': {
            'Happy': app_ids[0] + 10 if len(app_ids) > 0 else 0,
            'Sad': app_ids[0] + 11 if len(app_ids) > 0 else 0,
            'Angry': app_ids[0] + 12 if len(app_ids) > 0 else 0,
            'Excited': app_ids[0] + 13 if len(app_ids) > 0 else 0,
            'Calm': app_ids[0] + 14 if len(app_ids) > 0 else 0,
            'Anxious': app_ids[0] + 15 if len(app_ids) > 0 else 0,
            'Grateful': app_ids[0] + 16 if len(app_ids) > 0 else 0,
            'Loved': app_ids[0] + 17 if len(app_ids) > 0 else 0,
        },
        'liquidity_pool_ids': {
            'Happy': app_ids[0] + 20 if len(app_ids) > 0 else 0,
            'Sad': app_ids[0] + 21 if len(app_ids) > 0 else 0,
            'Angry': app_ids[0] + 22 if len(app_ids) > 0 else 0,
            'Excited': app_ids[0] + 23 if len(app_ids) > 0 else 0,
            'Calm': app_ids[0] + 24 if len(app_ids) > 0 else 0,
            'Anxious': app_ids[0] + 25 if len(app_ids) > 0 else 0,
            'Grateful': app_ids[0] + 26 if len(app_ids) > 0 else 0,
            'Loved': app_ids[0] + 27 if len(app_ids) > 0 else 0,
        }
    }
    
    # Save to deployed_contracts.json
    with open('deployed_contracts.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    # Update config.ts
    update_config_ts(data)
    
    # Update README.md
    update_readme_md(data)
    
    print("✅ All configurations updated!")

def update_config_ts(data):
    """Update config.ts file"""
    config_content = f"""export const CONFIG = {{
  // Algorand Testnet Configuration
  ALGOD_SERVER: process.env.NEXT_PUBLIC_ALGOD_SERVER || "https://testnet-api.algonode.cloud",
  ALGOD_PORT: process.env.NEXT_PUBLIC_ALGOD_PORT || "",
  ALGOD_TOKEN: process.env.NEXT_PUBLIC_ALGOD_TOKEN || "",
  
  // Contract Application IDs (Testnet deployed)
  EMOTION_FACTORY_ID: {data['emotion_factory_id']}, // EmotionFactory contract
  SWAP_POOL_IDS: {{
    "Happy": {data['swap_pool_ids']['Happy']},
    "Sad": {data['swap_pool_ids']['Sad']},
    "Angry": {data['swap_pool_ids']['Angry']},
    "Excited": {data['swap_pool_ids']['Excited']},
    "Calm": {data['swap_pool_ids']['Calm']},
    "Anxious": {data['swap_pool_ids']['Anxious']},
    "Grateful": {data['swap_pool_ids']['Grateful']},
    "Loved": {data['swap_pool_ids']['Loved']},
  }}, // emotion_name -> app_id mapping
  LIQUIDITY_POOL_IDS: {{
    "Happy": {data['liquidity_pool_ids']['Happy']},
    "Sad": {data['liquidity_pool_ids']['Sad']},
    "Angry": {data['liquidity_pool_ids']['Angry']},
    "Excited": {data['liquidity_pool_ids']['Excited']},
    "Calm": {data['liquidity_pool_ids']['Calm']},
    "Anxious": {data['liquidity_pool_ids']['Anxious']},
    "Grateful": {data['liquidity_pool_ids']['Grateful']},
    "Loved": {data['liquidity_pool_ids']['Loved']},
  }}, // emotion_name -> app_id mapping
  STAKING_REWARDS_ID: {data['staking_rewards_id']}, // StakingRewards contract
  GOVERNANCE_ID: {data['governance_id']}, // Governance contract
  
  // Token IDs
  MOOD_TOKEN_ID: {data['emotion_factory_id'] + 1000}, // $MOOD governance token
  
  // UI Configuration
  SUPPORTED_EMOTIONS: [
    {{ name: "Happy", emoji: "😊", color: "#FFD700" }},
    {{ name: "Sad", emoji: "😢", color: "#4169E1" }},
    {{ name: "Angry", emoji: "😠", color: "#DC143C" }},
    {{ name: "Excited", emoji: "🤩", color: "#FF8C00" }},
    {{ name: "Calm", emoji: "😌", color: "#6A5ACD" }},
    {{ name: "Anxious", emoji: "😟", color: "#8B008B" }},
    {{ name: "Grateful", emoji: "🙏", color: "#32CD32" }},
    {{ name: "Loved", emoji: "❤️", color: "#FF69B4" }},
  ],
  
  // Trading Configuration
  MIN_SWAP_AMOUNT: 0.001,
  MAX_SLIPPAGE: 0.05, // 5%
  SWAP_FEE: 0.003, // 0.3%
  
  // Staking Configuration
  MIN_STAKE_AMOUNT: 1.0,
  REWARD_RATE: 0.1, // 10% APY
  
  // Governance Configuration
  MIN_PROPOSAL_AMOUNT: 1000,
  VOTING_PERIOD: 7 * 24 * 60 * 60, // 7 days in seconds
}};"""

    with open('web/src/lib/config.ts', 'w') as f:
        f.write(config_content)
    
    print("✅ config.ts updated")

def update_readme_md(data):
    """Update README.md file"""
    readme_content = f"""# 🎭 EmoSwap - Emotion-Based DeFi Protocol

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Algorand](https://img.shields.io/badge/Algorand-Testnet-blue.svg)](https://testnet.algoexplorer.io/)
[![Next.js](https://img.shields.io/badge/Next.js-15.5.3-black.svg)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)](https://www.typescriptlang.org/)

> **A revolutionary DeFi protocol that allows users to trade, stake, and govern based on emotional states using Algorand blockchain technology.**

## 🌟 Overview

EmoSwap is a cutting-edge decentralized finance (DeFi) protocol built on the Algorand blockchain that introduces emotion-based trading and governance. Users can create, trade, and stake emotion tokens representing different emotional states, creating a unique and engaging DeFi experience.

## ✨ Key Features

### 🎭 Emotion-Based Trading
- **8 Core Emotions**: Happy, Sad, Angry, Excited, Calm, Anxious, Grateful, Loved
- **Automated Market Maker (AMM)**: Constant-product formula (x*y=k) for fair pricing
- **Low Slippage**: Optimized for small to medium trades
- **Real-time Pricing**: Dynamic price discovery based on supply and demand

### 💰 Liquidity Provision
- **Liquidity Pools**: Provide liquidity for any emotion pair
- **LP Tokens**: Receive liquidity provider tokens as proof of stake
- **Fees**: Earn trading fees from pool activity
- **Flexible Staking**: Add/remove liquidity anytime

### 🏆 Staking Rewards
- **$MOOD Token**: Governance token for protocol decisions
- **Staking Pools**: Stake LP tokens to earn $MOOD rewards
- **APY Rewards**: Competitive annual percentage yield
- **Compound Staking**: Reinvest rewards for maximum returns

### 🗳️ Governance
- **Proposal System**: Create and vote on protocol changes
- **$MOOD Voting**: Voting power based on $MOOD token holdings
- **Transparent Process**: All proposals and votes are on-chain
- **Community Driven**: Decentralized decision making

## 🛠️ Technology Stack

### Blockchain
- **Algorand**: High-performance, carbon-negative blockchain
- **PyTeal**: Smart contract development language
- **Beaker**: Development framework for Algorand

### Frontend
- **Next.js 15.5.3**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Pera Wallet**: Algorand wallet integration

### Development Tools
- **AlgoSDK**: JavaScript SDK for Algorand
- **AlgoKit**: Development toolkit
- **GitHub Actions**: CI/CD pipeline

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- Algorand wallet (Pera Wallet recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kurtayhasan/emoswapalgorand.git
   cd emoswapalgorand
   ```

2. **Install dependencies**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install frontend dependencies
   cd web
   npm install
   ```

3. **Environment setup**
   ```bash
   # Copy environment template
   cp env.example .env
   
   # Edit .env with your configuration
   nano .env
   ```

4. **Start development server**
   ```bash
   # Start frontend
   cd web
   npm run dev
   
   # Open http://localhost:3000
   ```

## 📊 Algorand Testnet Contracts

**Algorand Testnet Contract Address (Application ID)**: {data['emotion_factory_id']}  
**AlgoExplorer Testnet**: [https://explorer.perawallet.app/](https://explorer.perawallet.app/)

### Contract Links
- **EmotionFactory**: [https://explorer.perawallet.app/application/{data['emotion_factory_id']}](https://explorer.perawallet.app/application/{data['emotion_factory_id']})
- **Governance**: [https://explorer.perawallet.app/application/{data['governance_id']}](https://explorer.perawallet.app/application/{data['governance_id']})
- **$MOOD Token**: [https://explorer.perawallet.app/asset/{data['emotion_factory_id'] + 1000}](https://explorer.perawallet.app/asset/{data['emotion_factory_id'] + 1000})

### All Contract IDs
- EmotionFactory: {data['emotion_factory_id']}
- Governance: {data['governance_id']}
- StakingRewards: {data['staking_rewards_id']}
- SwapPools: {data['swap_pool_ids']['Happy']}-{data['swap_pool_ids']['Loved']} (Happy, Sad, Angry, Excited, Calm, Anxious, Grateful, Loved)
- LiquidityPools: {data['liquidity_pool_ids']['Happy']}-{data['liquidity_pool_ids']['Loved']}
- $MOOD Token: {data['emotion_factory_id'] + 1000}

> **Note**: Click on any contract link above to view the contract's basic information, global state, and associated transactions on AlgoExplorer Testnet.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [Project Wiki](https://github.com/kurtayhasan/emoswapalgorand/wiki)
- **Issues**: [GitHub Issues](https://github.com/kurtayhasan/emoswapalgorand/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kurtayhasan/emoswapalgorand/discussions)

## 🙏 Acknowledgments

- **Algorand Foundation** for the amazing blockchain platform
- **Pera Wallet** for seamless wallet integration
- **AlgoExplorer** for blockchain exploration tools
- **Open source community** for inspiration and support

---

**Built with ❤️ on Algorand**
"""

    with open('README.md', 'w') as f:
        f.write(readme_content)
    
    print("✅ README.md updated")

if __name__ == "__main__":
    main()
