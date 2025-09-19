"""
Simple PyTeal contract for testing
"""

from pyteal import *

def approval_program():
    """Approval program"""
    return Int(1)

def clear_state_program():
    """Clear state program"""
    return Int(1)

if __name__ == "__main__":
    print("Approval program:", compileTeal(approval_program(), mode=Mode.Application, version=8))
    print("Clear state program:", compileTeal(clear_state_program(), mode=Mode.Application, version=8))
