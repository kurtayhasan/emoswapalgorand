#!/bin/bash

echo "========================================"
echo "EmoSwap GitHub Deployment Script"
echo "========================================"
echo

echo "[1/6] Initializing Git repository..."
git init

echo
echo "[2/6] Adding all files to Git..."
git add .

echo
echo "[3/6] Creating initial commit..."
git commit -m "Initial commit: EmoSwap emotion-based DeFi protocol on Algorand

- Complete emotion trading protocol
- PyTeal smart contracts (EmotionFactory, SwapPool, LiquidityPool, StakingRewards, Governance)
- Next.js frontend with Pera Wallet integration
- Comprehensive testing suite
- Deployment automation scripts
- Professional documentation

Ready for Algorand Testnet deployment!"

echo
echo "[4/6] Adding remote origin..."
git remote add origin https://github.com/kurtayhasan/emoswapalgorand.git

echo
echo "[5/6] Setting main branch..."
git branch -M main

echo
echo "[6/6] Pushing to GitHub..."
git push -u origin main

echo
echo "========================================"
echo "✅ Deployment Complete!"
echo "========================================"
echo
echo "Your EmoSwap project is now live at:"
echo "https://github.com/kurtayhasan/emoswapalgorand"
echo
echo "Next steps:"
echo "1. Deploy contracts to Algorand Testnet"
echo "2. Update Application IDs in config files"
echo "3. Test all features"
echo "4. Share your project!"
echo
