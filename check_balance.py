#!/usr/bin/env python3
"""
Check testnet account balance
"""

from algosdk.v2client import algod

def check_balance():
    """Check account balance"""
    # Get algod client
    client = algod.AlgodClient('', 'https://testnet-api.algonode.cloud')
    
    # Check account balance
    account_address = 'KVFAMVUX4CTVDUEFFGKD6GMRWPIYQKGVC5CFIQJGWKXNGG66PGRMBKTAPM'
    
    try:
        account_info = client.account_info(account_address)
        balance = account_info.get('amount', 0) / 1000000
        print(f'Account balance: {balance} ALGO')
        
        if balance == 0:
            print('❌ Hesapta ALGO yok!')
            print('📝 Lütfen https://bank.testnet.algorand.network/ adresine gidin')
            print(f'📧 Cüzdan adresini yapıştırın: {account_address}')
            print('💰 Test ALGO isteyin')
        else:
            print('✅ Hesapta yeterli ALGO var!')
            print('🚀 Deploy işlemi başlatılabilir')
            
    except Exception as e:
        print(f'❌ Hesap kontrolü hatası: {e}')
        print('📝 Lütfen https://bank.testnet.algorand.network/ adresine gidin')
        print(f'📧 Cüzdan adresini yapıştırın: {account_address}')

if __name__ == "__main__":
    check_balance()
