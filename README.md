# EmoSwap - Algorand Emotion Trading Platform

EmoSwap is an innovative DeFi platform that tokenizes emotions and enables their trading on the Algorand blockchain.

## 🎯 Project Overview

EmoSwap is a platform where users can tokenize their daily emotions, trade these tokens, and earn rewards by providing liquidity.

## 🏗️ Architecture

### Smart Contracts (AlgoPy)
- **contract.py**: Main EmoSwap contract with global state management
- **emotion_factory.py**: Creates emotion tokens and manages daily minting
- **governance.py**: Manages protocol parameters and future DAO governance
- **liquidity_pool.py**: Provides liquidity for emotion ASA <-> ALGO pairs
- **staking_rewards.py**: Earn $MOOD governance tokens by staking LP tokens
- **swap_pool.py**: Constant product AMM (x*y=k) for emotion ASA <-> ALGO pairs

### Frontend
- **Next.js 15** modern React application
- **Algorand Wallet** integration
- **Responsive** and user-friendly interface

## 🚀 Installation

### Requirements
- Node.js 18+
- npm or yarn
- Algorand Wallet (Pera, MyAlgo, etc.)

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/kurtayhasan/emoswapalgorand.git
cd emoswapalgorand
```

2. **Install dependencies**
```bash
npm install
cd web
npm install
```

3. **Start the web application**
```bash
cd web
npm run dev
```

4. **Open in browser**
```
http://localhost:3000
```

## 📋 Deployment

### AlgoKit Deployment (Recommended)

1. **Install AlgoKit**: `pipx install algokit`
2. **Deploy to TestNet**:
```bash
python -m smart_contracts deploy
```
3. **Get App IDs** from deployment logs
4. **Update configurations** in `web/src/lib/config.ts`

### Manual Deployment

```bash
algokit project deploy
```

## 🔧 Configuration

### Environment Variables
```env
NEXT_PUBLIC_ALGOD_SERVER=https://testnet-api.algonode.cloud
NEXT_PUBLIC_ALGOD_PORT=
NEXT_PUBLIC_ALGOD_TOKEN=
```

### Contract IDs
```typescript
// web/src/lib/config.ts
export const CONFIG = {
  EMOTION_FACTORY_ID: 746159123, // Deployed
  GOVERNANCE_ID: 0,              // Pending
  STAKING_REWARDS_ID: 0,         // Pending
  LIQUIDITY_POOL_ID: 0,          // Pending
  SWAP_POOL_ID: 0,               // Pending
  MOOD_TOKEN_ID: 746157034,      // Deployed
};
```

## 📊 Current Status

| Component | Status | Description |
|-----------|--------|-------------|
| **$MOOD Token** | ✅ Deployed | ID: 746157034 |
| **Web Interface** | ✅ Running | http://localhost:3000 |
| **EmoSwap Main Contract** | ✅ Deployed | ID: 746159123 |
| **AlgoKit Structure** | ✅ Applied | Modern Python contracts |
| **Configurations** | ✅ Updated | App IDs added |

## 🎨 Features

### Supported Emotions
- 😊 Happy
- 😢 Sad
- 😠 Angry
- 🤩 Excited
- 😌 Calm
- 😟 Anxious
- 🙏 Grateful
- ❤️ Loved

### Trading Features
- **Minimum Swap**: 0.001 ALGO
- **Maximum Slippage**: 5%
- **Swap Fee**: 0.3%

### Staking Features
- **Minimum Stake**: 1.0 LP Token
- **Reward Rate**: 10%

## 🔗 Links

- **TestNet Explorer**: https://testnet.algoexplorer.io/
- **$MOOD Token**: https://testnet.algoexplorer.io/asset/746157034
- **EmoSwap Main Contract**: https://testnet.algoexplorer.io/application/746159123
- **Algo Studio**: https://studio.algorand.org/

## 📝 License

MIT License

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Contact

- **GitHub**: [@kurtayhasan](https://github.com/kurtayhasan)
- **Twitter**: [@emoswapalgo](https://twitter.com/emoswapalgo)

---

**Note**: This project runs on Algorand TestNet. Additional security tests are required for MainNet deployment.