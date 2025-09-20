"""
Governance.py
Manages protocol parameters and future DAO governance
"""

from pyteal import (
    Txn, Global, Int, Bytes, Concat, Itob, Assert, Seq, If, TxnField, TxnType,
    InnerTxn, InnerTxnBuilder, TealType, Gtxn, Reject
)
from beaker import *

# Import decorators
external = Application.external
create = Application.create

class GovernanceState:
    admin = GlobalStateValue(
        stack_type=TealType.bytes,
        default=Global.creator_address(),
        descr="Admin address"
    )
    
    mood_token_id = GlobalStateValue(
        stack_type=TealType.uint64,
        descr="Asset ID of the $MOOD governance token"
    )
    
    # Protocol parameters stored in global state
    swap_fee_bps = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(30),  # 0.3% fee
        descr="Swap fee in basis points"
    )
    
    emission_rate = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(100_000),  # 0.1 $MOOD per block per LP token
        descr="Staking emission rate"
    )
    
    min_liquidity = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(1000),  # Minimum LP tokens
        descr="Minimum liquidity required"
    )

class Governance(Application):
    def __init__(self):
        super().__init__()
        self.state = GovernanceState()
    
    @create
    def create(self):
        return self.initialize_application_state()
    
    @external
    def bootstrap(self, mood_token_id: abi.Uint64):
        """Initialize governance with $MOOD token"""
        return Seq(
            Assert(self.state.mood_token_id == Int(0)),  # Not initialized
            self.state.mood_token_id.set(mood_token_id.get()),
        )
    
    @external(authorize=Authorize.only(Global.creator_address()))
    def set_param(self, key: abi.String, value: abi.Uint64):
        """Set protocol parameter (admin only for MVP)"""
        return Seq(
            # Switch on parameter key
            If(key.get() == Bytes("swap_fee_bps"),
               self.state.swap_fee_bps.set(value.get()),
               If(key.get() == Bytes("emission_rate"),
                  self.state.emission_rate.set(value.get()),
                  If(key.get() == Bytes("min_liquidity"),
                     self.state.min_liquidity.set(value.get()),
                     Reject()))),  # Invalid parameter
        )
    
    @external(read_only=True)
    def get_param(self, key: abi.String, *, output: abi.Uint64):
        """Get protocol parameter value"""
        return If(key.get() == Bytes("swap_fee_bps"),
                 output.set(self.state.swap_fee_bps),
                 If(key.get() == Bytes("emission_rate"),
                    output.set(self.state.emission_rate),
                    If(key.get() == Bytes("min_liquidity"),
                       output.set(self.state.min_liquidity),
                       output.set(Int(0)))))  # Invalid parameter

if __name__ == "__main__":
    app = Governance()
    print(app.build())
