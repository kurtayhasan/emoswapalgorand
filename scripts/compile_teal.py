#!/usr/bin/env python3
"""
Compile PyTeal contracts to TEAL files
"""

from pathlib import Path
import importlib.util
import sys

def import_contract(file_path):
    spec = importlib.util.spec_from_file_location("contract", file_path)
    contract = importlib.util.module_from_spec(spec)
    sys.modules["contract"] = contract
    spec.loader.exec_module(contract)
    return contract

def compile_contract(contract_file):
    contract_path = Path(__file__).parent.parent / "contracts" / contract_file
    build_path = Path(__file__).parent.parent / "contracts" / "build"
    build_path.mkdir(exist_ok=True)
    
    # Import and compile
    contract = import_contract(contract_path)
    app = contract.app
    
    # Save approval and clear programs
    approval_path = build_path / f"{contract_file.replace('.py', '_approval.teal')}"
    clear_path = build_path / f"{contract_file.replace('.py', '_clear.teal')}"
    
    with open(approval_path, "w") as f:
        f.write(app.approval_program())
    with open(clear_path, "w") as f:
        f.write(app.clear_program())
        
    print(f"✓ Compiled {contract_file}")
    print(f"  Approval: {approval_path}")
    print(f"  Clear: {clear_path}")

def main():
    contracts = [
        "EmotionFactory.py",
        "SwapPool.py", 
        "LiquidityPool.py",
        "StakingRewards.py",
        "Governance.py"
    ]
    
    print("Compiling contracts...")
    for contract in contracts:
        try:
            compile_contract(contract)
        except Exception as e:
            print(f"Error compiling {contract}: {e}")
            continue

if __name__ == "__main__":
    main()
