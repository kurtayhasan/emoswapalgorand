"""
SwapPool.py
Constant-product AMM (x*y=k) for emotion ASA <-> ALGO pairs
"""

from pyteal import *
from beaker import *

class SwapPoolState:
    asset_id = GlobalStateValue(
        stack_type=TealType.uint64,
        descr="Asset ID of the emotion token"
    )
    
    algo_reserve = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="ALGO reserve in the pool"
    )
    
    asset_reserve = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Asset reserve in the pool"
    )
    
    fee_sink = GlobalStateValue(
        stack_type=TealType.bytes,
        default=Global.creator_address(),
        descr="Address to receive fees"
    )
    
    fee_bps = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(30),  # 0.3% fee = 30 bps
        descr="Fee in basis points"
    )
    
    is_bootstrapped = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Whether pool has been bootstrapped"
    )

class SwapPool(Application):
    def __init__(self):
        super().__init__()
        self.state = SwapPoolState()
    
    @create
    def create(self):
        return self.initialize_application_state()
    
    @external
    def bootstrap(self, asset_id: abi.Uint64):
        """Initialize pool with an asset"""
        return Seq(
            Assert(self.state.is_bootstrapped == Int(0)),
            self.state.asset_id.set(asset_id.get()),
            self.state.is_bootstrapped.set(Int(1)),
        )
    
    @external
    def swap_exact_in(self, asset_in: abi.Asset, amount_in: abi.Uint64, min_out: abi.Uint64):
        """Swap an exact amount of input tokens"""
        return Seq(
            # Verify pool is bootstrapped
            Assert(self.state.is_bootstrapped == Int(1)),
            
            # Get current reserves
            (reserve_in := abi.Uint64()).set(
                If(
                    asset_in.asset_id() == Int(0),  # ALGO
                    self.state.algo_reserve,
                    self.state.asset_reserve
                )
            ),
            (reserve_out := abi.Uint64()).set(
                If(
                    asset_in.asset_id() == Int(0),  # ALGO
                    self.state.asset_reserve,
                    self.state.algo_reserve
                )
            ),
            
            # Calculate amount out with fee
            (amount_in_with_fee := abi.Uint64()).set(
                amount_in.get() * (Int(10000) - self.state.fee_bps)
            ),
            (numerator := abi.Uint64()).set(
                amount_in_with_fee.get() * reserve_out.get()
            ),
            (denominator := abi.Uint64()).set(
                (reserve_in.get() * Int(10000)) + amount_in_with_fee.get()
            ),
            (amount_out := abi.Uint64()).set(numerator.get() / denominator.get()),
            
            # Verify minimum output
            Assert(amount_out.get() >= min_out.get()),
            
            # Handle transfers
            If(asset_in.asset_id() == Int(0),
               # ALGO in, ASA out
               Seq(
                   # Verify payment
                   Assert(Gtxn[0].type_enum() == TxnType.Payment),
                   Assert(Gtxn[0].sender() == Txn.sender()),
                   Assert(Gtxn[0].receiver() == Global.current_application_address()),
                   Assert(Gtxn[0].amount() == amount_in.get()),
                   
                   # Send ASA
                   InnerTxnBuilder.Begin(),
                   InnerTxnBuilder.SetFields({
                       TxnField.type_enum: TxnType.AssetTransfer,
                       TxnField.xfer_asset: self.state.asset_id,
                       TxnField.asset_amount: amount_out.get(),
                       TxnField.asset_receiver: Txn.sender(),
                   }),
                   InnerTxnBuilder.Submit(),
                   
                   # Update reserves
                   self.state.algo_reserve.set(self.state.algo_reserve + amount_in.get()),
                   self.state.asset_reserve.set(self.state.asset_reserve - amount_out.get()),
               ),
               # ASA in, ALGO out
               Seq(
                   # Verify asset transfer
                   Assert(Gtxn[0].type_enum() == TxnType.AssetTransfer),
                   Assert(Gtxn[0].sender() == Txn.sender()),
                   Assert(Gtxn[0].asset_receiver() == Global.current_application_address()),
                   Assert(Gtxn[0].xfer_asset() == self.state.asset_id),
                   Assert(Gtxn[0].asset_amount() == amount_in.get()),
                   
                   # Send ALGO
                   InnerTxnBuilder.Begin(),
                   InnerTxnBuilder.SetFields({
                       TxnField.type_enum: TxnType.Payment,
                       TxnField.amount: amount_out.get(),
                       TxnField.receiver: Txn.sender(),
                   }),
                   InnerTxnBuilder.Submit(),
                   
                   # Update reserves
                   self.state.asset_reserve.set(self.state.asset_reserve + amount_in.get()),
                   self.state.algo_reserve.set(self.state.algo_reserve - amount_out.get()),
               )
            )
        )
    
    @external(read_only=True)
    def get_quote(self, asset_in: abi.Asset, amount_in: abi.Uint64, *, output: abi.Uint64):
        """Get expected output amount for a swap"""
        return Seq(
            Assert(self.state.is_bootstrapped == Int(1)),
            
            # Get reserves based on input asset
            (reserve_in := abi.Uint64()).set(
                If(
                    asset_in.asset_id() == Int(0),
                    self.state.algo_reserve,
                    self.state.asset_reserve
                )
            ),
            (reserve_out := abi.Uint64()).set(
                If(
                    asset_in.asset_id() == Int(0),
                    self.state.asset_reserve,
                    self.state.algo_reserve
                )
            ),
            
            # Calculate output with fee
            (amount_in_with_fee := abi.Uint64()).set(
                amount_in.get() * (Int(10000) - self.state.fee_bps)
            ),
            (numerator := abi.Uint64()).set(
                amount_in_with_fee.get() * reserve_out.get()
            ),
            (denominator := abi.Uint64()).set(
                (reserve_in.get() * Int(10000)) + amount_in_with_fee.get()
            ),
            
            output.set(numerator.get() / denominator.get()),
        )
    
    @external(read_only=True)
    def get_reserves(self, *, output: abi.Tuple2[abi.Uint64, abi.Uint64]):
        """Get pool reserves"""
        return output.set((self.state.algo_reserve, self.state.asset_reserve))

if __name__ == "__main__":
    app = SwapPool()
    print(app.build())
