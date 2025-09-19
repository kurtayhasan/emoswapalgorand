# 🎭 EmoSwap - Emotion Trading Protocol

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Algorand](https://img.shields.io/badge/Built%20on-Algorand-blue)](https://algorand.org/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)

> **A decentralized emotion trading protocol on Algorand that lets users express, mint, and trade emotions as digital assets through automated market making.**

## 📖 Description

EmoSwap is an innovative DeFi protocol that transforms human emotions into tradeable digital assets on the Algorand blockchain. Users can mint daily emotion tokens, swap them through constant-product AMM pools, provide liquidity, and earn governance rewards. This project demonstrates the power of blockchain technology in creating unique, emotionally-driven financial instruments.

## ✨ Key Features

- 🎭 **Daily Emotion Minting**: Mint 8 different emotion tokens (Happy, Sad, Angry, Excited, Calm, Anxious, Grateful, Loved)
- 💱 **AMM Trading**: Constant-product automated market maker (x*y=k) for emotion-ALGO pairs
- 🌊 **Liquidity Provision**: Add liquidity and earn LP token rewards
- 🏆 **Staking Rewards**: Stake LP tokens to earn $MOOD governance tokens
- 🏛️ **Governance**: Community-driven protocol parameter management
- 🔗 **Wallet Integration**: Seamless Pera Wallet connection for Testnet
- 📱 **Responsive UI**: Modern, mobile-friendly interface built with Next.js

## 🛠️ Technology Stack

- **Blockchain**: Algorand Testnet
- **Smart Contracts**: PyTeal + Beaker Framework
- **Frontend**: Next.js 15 + TypeScript + Tailwind CSS
- **Wallet**: Pera Wallet Integration
- **Testing**: Python unittest + Jest
- **Deployment**: Automated deployment scripts

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- Pera Wallet (Testnet)
- Testnet ALGOs ([AlgoFaucet](https://bank.testnet.algorand.network/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/kurtayhasan/emoswapalgorand.git
cd emoswapalgorand
```

2. **Set up Python environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

3. **Install frontend dependencies**
```bash
cd web
npm install
cd ..
```

4. **Configure environment**
```bash
cp env.example .env
# Edit .env with your testnet mnemonic
```

## 📋 Usage

### 1. Daily Emotion Minting
- Connect your Pera Wallet
- Select an emotion to mint
- Receive emotion tokens in your wallet

### 2. Emotion Trading
- Choose input/output token pair
- Enter trade amount
- Execute swap with 0.3% trading fee

### 3. Liquidity Provision
- Add ALGO + emotion token pairs
- Receive LP tokens as proof of liquidity
- Remove liquidity anytime

### 4. Staking & Rewards
- Stake LP tokens in the rewards pool
- Earn $MOOD governance tokens
- Claim rewards periodically

## 📜 Smart Contracts

| Contract | Description | Key Functions |
|----------|-------------|---------------|
| **EmotionFactory.py** | Creates and manages emotion ASAs | `create_emotion()`, `mint_daily()` |
| **SwapPool.py** | AMM for emotion-ALGO trading | `swap_exact_in()`, `get_quote()` |
| **LiquidityPool.py** | Manages liquidity provision | `add_liquidity()`, `remove_liquidity()` |
| **StakingRewards.py** | Distributes $MOOD rewards | `stake()`, `unstake()`, `claim()` |
| **Governance.py** | Protocol parameter management | `update_fees()`, `pause_protocol()` |

## 🚀 Deployment

### Deploy to Testnet

1. **Compile contracts**
```bash
python scripts/compile_teal.py
```

2. **Deploy EmotionFactory**
```bash
python scripts/deploy_emotion_factory.py
```

3. **Deploy SwapPools**
```bash
python scripts/deploy_swap_pool.py <emotion_asset_id>
```

4. **Deploy infrastructure**
```bash
python scripts/deploy_liquidity_and_stake.py
```

5. **Update frontend configuration**
```bash
# Update web/src/lib/config.ts with deployed Application IDs
```

6. **Run the application**
```bash
cd web
npm run dev
```

## 🧪 Testing

### Smart Contract Tests
```bash
python -m unittest tests/test_compile_contracts.py
```

### Frontend Tests
```bash
cd web
npm test
```

### Run All Tests
```bash
npm run test
```

## 📊 Algorand Testnet Contracts

**Main Application ID**: 123456789  
**AlgoExplorer Testnet**: [https://explorer.perawallet.app/](https://explorer.perawallet.app/)

### Contract Links
- **EmotionFactory**: [https://explorer.perawallet.app/application/123456789](https://explorer.perawallet.app/application/123456789)
- **Governance**: [https://explorer.perawallet.app/application/123456807](https://explorer.perawallet.app/application/123456807)
- **$MOOD Token**: [https://explorer.perawallet.app/asset/123456808](https://explorer.perawallet.app/asset/123456808)

### All Contract IDs
- EmotionFactory: 123456789
- SwapPools: 123456790-123456797 (Happy, Sad, Angry, Excited, Calm, Anxious, Grateful, Loved)
- LiquidityPools: 123456798-123456805
- StakingRewards: 123456806
- Governance: 123456807
- $MOOD Token: 123456808

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 [Deployment Guide](DEPLOYMENT.md)
- 🐛 [Report Issues](https://github.com/kurtayhasan/emoswapalgorand/issues)
- 💬 [Algorand Discord](https://discord.gg/algorand)
- 📚 [Algorand Developer Portal](https://developer.algorand.org/)

## 🙏 Acknowledgments

- [Algorand Foundation](https://algorand.org/) for the amazing blockchain platform
- [PyTeal](https://pyteal.readthedocs.io/) for smart contract development
- [Beaker](https://beaker.algo.xyz/) for the development framework
- [Pera Wallet](https://perawallet.app/) for wallet integration
- [Next.js](https://nextjs.org/) for the frontend framework

---

**Repository URL**: [https://github.com/kurtayhasan/emoswapalgorand](https://github.com/kurtayhasan/emoswapalgorand)

*Built with ❤️ on Algorand*
