"""
LiquidityPool.py
Manages liquidity provision for emotion ASA <-> ALGO pairs
"""

from pyteal import *
from beaker import *

# Import decorators
external = Application.external
create = Application.create

class LiquidityPoolState:
    asset_id = GlobalStateValue(
        stack_type=TealType.uint64,
        descr="Asset ID of the emotion token"
    )
    
    lp_token_id = GlobalStateValue(
        stack_type=TealType.uint64,
        descr="Asset ID of the LP token"
    )
    
    total_supply = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Total supply of LP tokens"
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
    
    min_liquidity = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(1000),  # Minimum LP tokens to mint
        descr="Minimum liquidity required"
    )

class LiquidityPool(Application):
    def __init__(self):
        super().__init__()
        self.state = LiquidityPoolState()
    
    @create
    def create(self):
        return self.initialize_application_state()
    
    @external
    def bootstrap(self, asset_id: abi.Uint64):
        """Initialize pool with an asset and create LP token"""
        return Seq(
            Assert(self.state.lp_token_id == Int(0)),  # Not already initialized
            self.state.asset_id.set(asset_id.get()),
            
            # Create LP token
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetConfig,
                TxnField.config_asset_name: Concat(
                    Bytes("LP-"),
                    Itob(asset_id.get())
                ),
                TxnField.config_asset_unit_name: Bytes("LP"),
                TxnField.config_asset_total: Int(2**64 - 1),  # Max supply
                TxnField.config_asset_decimals: Int(6),
                TxnField.config_asset_manager: Global.current_application_address(),
                TxnField.config_asset_reserve: Global.current_application_address(),
                TxnField.config_asset_freeze: Global.current_application_address(),
                TxnField.config_asset_clawback: Global.current_application_address(),
            }),
            InnerTxnBuilder.Submit(),
            
            self.state.lp_token_id.set(InnerTxn.created_asset_id()),
        )
    
    @external
    def add_liquidity(
        self,
        algo_amount: abi.Uint64,
        asset_amount: abi.Uint64,
        min_lp: abi.Uint64,
    ):
        """Add liquidity to pool"""
        return Seq(
            Assert(self.state.lp_token_id != Int(0)),  # Pool initialized
            
            # Calculate LP tokens to mint
            (lp_to_mint := abi.Uint64()).set(
                If(
                    self.state.total_supply == Int(0),
                    # Initial liquidity - mint minimum
                    self.state.min_liquidity,
                    # Subsequent liquidity - mint proportional
                    If(
                        algo_amount.get() * self.state.total_supply / self.state.algo_reserve < 
                        asset_amount.get() * self.state.total_supply / self.state.asset_reserve,
                        algo_amount.get() * self.state.total_supply / self.state.algo_reserve,
                        asset_amount.get() * self.state.total_supply / self.state.asset_reserve
                    )
                )
            ),
            
            # Verify minimum LP
            Assert(lp_to_mint.get() >= min_lp.get()),
            
            # Receive payments
            Assert(Gtxn[0].type_enum() == TxnType.Payment),
            Assert(Gtxn[0].sender() == Txn.sender()),
            Assert(Gtxn[0].receiver() == Global.current_application_address()),
            Assert(Gtxn[0].amount() == algo_amount.get()),
            
            Assert(Gtxn[1].type_enum() == TxnType.AssetTransfer),
            Assert(Gtxn[1].sender() == Txn.sender()),
            Assert(Gtxn[1].asset_receiver() == Global.current_application_address()),
            Assert(Gtxn[1].xfer_asset() == self.state.asset_id),
            Assert(Gtxn[1].asset_amount() == asset_amount.get()),
            
            # Mint LP tokens
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: self.state.lp_token_id,
                TxnField.asset_amount: lp_to_mint.get(),
                TxnField.asset_receiver: Txn.sender(),
            }),
            InnerTxnBuilder.Submit(),
            
            # Update state
            self.state.algo_reserve.set(self.state.algo_reserve + algo_amount.get()),
            self.state.asset_reserve.set(self.state.asset_reserve + asset_amount.get()),
            self.state.total_supply.set(self.state.total_supply + lp_to_mint.get()),
        )
    
    @external
    def remove_liquidity(self, lp_amount: abi.Uint64, min_algo: abi.Uint64, min_asset: abi.Uint64):
        """Remove liquidity from pool"""
        return Seq(
            Assert(self.state.lp_token_id != Int(0)),  # Pool initialized
            
            # Calculate amounts to return
            (algo_amount := abi.Uint64()).set(
                lp_amount.get() * self.state.algo_reserve / self.state.total_supply
            ),
            (asset_amount := abi.Uint64()).set(
                lp_amount.get() * self.state.asset_reserve / self.state.total_supply
            ),
            
            # Verify minimums
            Assert(algo_amount.get() >= min_algo.get()),
            Assert(asset_amount.get() >= min_asset.get()),
            
            # Receive LP tokens
            Assert(Gtxn[0].type_enum() == TxnType.AssetTransfer),
            Assert(Gtxn[0].sender() == Txn.sender()),
            Assert(Gtxn[0].asset_receiver() == Global.current_application_address()),
            Assert(Gtxn[0].xfer_asset() == self.state.lp_token_id),
            Assert(Gtxn[0].asset_amount() == lp_amount.get()),
            
            # Return ALGO and asset
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.amount: algo_amount.get(),
                TxnField.receiver: Txn.sender(),
            }),
            InnerTxnBuilder.Submit(),
            
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: self.state.asset_id,
                TxnField.asset_amount: asset_amount.get(),
                TxnField.asset_receiver: Txn.sender(),
            }),
            InnerTxnBuilder.Submit(),
            
            # Burn LP tokens (send to reserve address)
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: self.state.lp_token_id,
                TxnField.asset_amount: lp_amount.get(),
                TxnField.asset_receiver: Global.current_application_address(),
            }),
            InnerTxnBuilder.Submit(),
            
            # Update state
            self.state.algo_reserve.set(self.state.algo_reserve - algo_amount.get()),
            self.state.asset_reserve.set(self.state.asset_reserve - asset_amount.get()),
            self.state.total_supply.set(self.state.total_supply - lp_amount.get()),
        )
    
    @external(read_only=True)
    def get_pool_info(self, *, output: abi.Uint64):
        """Get pool info (asset ID, LP token ID, reserves, total supply)"""
        return output.set(Concat(
            Itob(self.state.asset_id),
            Itob(self.state.lp_token_id),
            Itob(self.state.algo_reserve),
            Itob(self.state.asset_reserve),
            Itob(self.state.total_supply)
        ))

if __name__ == "__main__":
    app = LiquidityPool()
    print(app.build())
