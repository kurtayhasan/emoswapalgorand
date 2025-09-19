#!/usr/bin/env python3
"""
Create a new testnet wallet for deployment
"""

from algosdk import account, mnemonic
import json

def create_testnet_wallet():
    """Create a new testnet wallet"""
    # Generate a new test account
    private_key, address = account.generate_account()
    test_mnemonic = mnemonic.from_private_key(private_key)
    
    print("=" * 60)
    print("🔑 YENİ TESTNET CÜZDANI OLUŞTURULDU")
    print("=" * 60)
    print(f"📧 Cüzdan Adresi: {address}")
    print(f"🔐 Mnemonic: {test_mnemonic}")
    print("=" * 60)
    print("💰 TEST ALGO ALMAK İÇİN:")
    print("1. https://bank.testnet.algorand.network/ adresine git")
    print("2. Yukarıdaki cüzdan adresini yapıştır")
    print("3. 'Request funds' butonuna tıkla")
    print("4. Birkaç dakika bekle (ALGO gelecek)")
    print("=" * 60)
    
    # Save to .env file
    with open('.env', 'w') as f:
        f.write(f'DEPLOYER_MNEMONIC="{test_mnemonic}"\n')
        f.write('NEXT_PUBLIC_ALGOD_SERVER="https://testnet-api.algonode.cloud"\n')
        f.write('NEXT_PUBLIC_ALGOD_PORT=""\n')
        f.write('NEXT_PUBLIC_ALGOD_TOKEN=""\n')
        f.write('NEXT_PUBLIC_EMOTION_FACTORY_ID=0\n')
        f.write('NEXT_PUBLIC_SWAP_POOL_IDS="{}"\n')
        f.write('NEXT_PUBLIC_LIQUIDITY_POOL_IDS="{}"\n')
        f.write('NEXT_PUBLIC_STAKING_REWARDS_ID=0\n')
        f.write('NEXT_PUBLIC_GOVERNANCE_ID=0\n')
        f.write('NEXT_PUBLIC_MOOD_TOKEN_ID=0\n')
    
    print("✅ .env dosyası güncellendi")
    print("✅ Cüzdan bilgileri kaydedildi")
    
    return address, test_mnemonic

if __name__ == "__main__":
    create_testnet_wallet()
