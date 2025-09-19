# EmoSwap Deployment Guide

This guide will help you deploy the EmoSwap protocol to Algorand Testnet.

## Prerequisites

1. **Python 3.9+** installed
2. **Node.js 18+** installed
3. **Pera Wallet** with Testnet account
4. **Testnet ALGOs** from [AlgoFaucet](https://bank.testnet.algorand.network/)

## Step 1: Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/emoswapalgo
cd emoswapalgo
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install frontend dependencies:
```bash
cd web
npm install
cd ..
```

5. Set up environment variables:
```bash
# Copy environment template
cp env.example .env

# Edit .env with your testnet mnemonic
# DEPLOYER_MNEMONIC="your testnet mnemonic phrase here"
```

## Step 2: Deploy Smart Contracts

### 2.1 Deploy EmotionFactory

```bash
python scripts/deploy_emotion_factory.py
```

This will output:
- Application ID for EmotionFactory
- AlgoExplorer link

**Save the Application ID** - you'll need it for the next steps.

### 2.2 Create Emotion Tokens

First, create some emotion tokens using the EmotionFactory:

```python
# You can create a simple script to create emotions
python -c "
import os
from dotenv import load_dotenv
from algosdk import account, mnemonic
from algosdk.v2client import algod
from contracts.EmotionFactory import EmotionFactory

load_dotenv()
client = algod.AlgodClient('', 'https://testnet-api.algonode.cloud')
private_key = mnemonic.to_private_key(os.getenv('DEPLOYER_MNEMONIC'))
address = account.address_from_private_key(private_key)

# Create emotions (this is a simplified example)
emotions = ['Happy', 'Sad', 'Angry', 'Excited']
# You'll need to implement the actual emotion creation logic
"
```

### 2.3 Deploy SwapPools

For each emotion token created, deploy a SwapPool:

```bash
python scripts/deploy_swap_pool.py <emotion_asset_id>
```

**Save all SwapPool Application IDs**.

### 2.4 Deploy Liquidity and Staking Infrastructure

```bash
python scripts/deploy_liquidity_and_stake.py
```

This will create:
- $MOOD governance token
- Governance contract
- LiquidityPool contracts
- StakingRewards contract

**Save all Application IDs and Token IDs**.

## Step 3: Update Frontend Configuration

1. Update `web/src/lib/config.ts` with your deployed Application IDs:

```typescript
export const CONFIG = {
  // ... other config
  EMOTION_FACTORY_ID: YOUR_EMOTION_FACTORY_ID,
  SWAP_POOL_IDS: {
    "Happy": YOUR_HAPPY_SWAP_POOL_ID,
    "Sad": YOUR_SAD_SWAP_POOL_ID,
    // ... other emotions
  },
  LIQUIDITY_POOL_IDS: {
    "Happy": YOUR_HAPPY_LIQUIDITY_POOL_ID,
    // ... other emotions
  },
  STAKING_REWARDS_ID: YOUR_STAKING_REWARDS_ID,
  GOVERNANCE_ID: YOUR_GOVERNANCE_ID,
  MOOD_TOKEN_ID: YOUR_MOOD_TOKEN_ID,
};
```

2. Create frontend environment file:
```bash
cd web
cp ../.env .env.local
```

## Step 4: Update README.md

Update the README.md with your deployed Application IDs:

```markdown
## Algorand Testnet Contracts

**Main Application ID**: YOUR_EMOTION_FACTORY_ID
**AlgoExplorer Testnet**: [https://explorer.perawallet.app/](https://explorer.perawallet.app/)

### Contract Links
- EmotionFactory: [https://explorer.perawallet.app/application/YOUR_EMOTION_FACTORY_ID](https://explorer.perawallet.app/application/YOUR_EMOTION_FACTORY_ID)
- Governance: [https://explorer.perawallet.app/application/YOUR_GOVERNANCE_ID](https://explorer.perawallet.app/application/YOUR_GOVERNANCE_ID)
- $MOOD Token: [https://explorer.perawallet.app/asset/YOUR_MOOD_TOKEN_ID](https://explorer.perawallet.app/asset/YOUR_MOOD_TOKEN_ID)
```

## Step 5: Test the Application

1. Start the frontend:
```bash
cd web
npm run dev
```

2. Open [http://localhost:3000](http://localhost:3000)

3. Connect your Pera Wallet

4. Test the features:
   - Mint daily emotions
   - Swap between ALGO and emotion tokens
   - Add/remove liquidity
   - Stake LP tokens for rewards

## Step 6: Run Tests

```bash
# Test smart contracts
python -m unittest tests/test_compile_contracts.py

# Test frontend
cd web
npm test
```

## Troubleshooting

### Common Issues

1. **"Insufficient balance"**: Make sure you have enough Testnet ALGOs
2. **"Application not found"**: Check that Application IDs are correct
3. **"Transaction failed"**: Check that all required parameters are set

### Getting Help

- Check the [Algorand Developer Portal](https://developer.algorand.org/)
- Join the [Algorand Discord](https://discord.gg/algorand)
- Review the [PyTeal Documentation](https://pyteal.readthedocs.io/)

## Next Steps

After successful deployment:

1. **Update README.md** with your Application IDs
2. **Commit and push** to GitHub
3. **Share your project** with the community
4. **Consider adding features** like:
   - More emotion types
   - Advanced trading features
   - Mobile app integration
   - Analytics dashboard
