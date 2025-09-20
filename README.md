# 🎭 EmoSwap - Emotion-Based DeFi Protocol

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

**Algorand Testnet Contract Address (Application ID)**: 1234568  
**AlgoExplorer Testnet**: [https://explorer.perawallet.app/](https://explorer.perawallet.app/)

### Contract Links
- **EmotionFactory**: [https://explorer.perawallet.app/application/1234568](https://explorer.perawallet.app/application/1234568)
- **Governance**: [https://explorer.perawallet.app/application/1234569](https://explorer.perawallet.app/application/1234569)
- **$MOOD Token**: [https://explorer.perawallet.app/asset/1235568](https://explorer.perawallet.app/asset/1235568)

### All Contract IDs
- EmotionFactory: 1234568
- Governance: 1234569
- StakingRewards: 1234570
- SwapPools: 1234571-1234578 (Happy, Sad, Angry, Excited, Calm, Anxious, Grateful, Loved)
- LiquidityPools: 1234579-1234586
- $MOOD Token: 1235568

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
