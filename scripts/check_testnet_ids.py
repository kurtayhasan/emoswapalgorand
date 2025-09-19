#!/usr/bin/env python3
"""
Check Application IDs on testnet
"""

import requests
import json

def check_application_ids():
    """Check if Application IDs exist on testnet"""
    app_ids = [1000000001, 1000000002, 1000000003, 1000000004, 1000000005]
    
    print('TESTNET APPLICATION ID KONTROLU')
    print('=' * 50)
    
    for app_id in app_ids:
        try:
            url = f'https://testnet-api.algonode.cloud/v2/applications/{app_id}'
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                print(f'Application {app_id}: ACTIVE')
                print(f'   Creator: {data.get("params", {}).get("creator", "N/A")}')
                print(f'   Explorer: https://testnet.algoexplorer.io/application/{app_id}')
            else:
                print(f'Application {app_id}: NOT FOUND')
                
        except Exception as e:
            print(f'Application {app_id}: ERROR - {e}')
        
        print()
    
    print('NOT: Bu ID\'ler mock ID\'lerdir. Gerçek deploy için contract\'ları deploy etmeniz gerekir.')

if __name__ == "__main__":
    check_application_ids()
