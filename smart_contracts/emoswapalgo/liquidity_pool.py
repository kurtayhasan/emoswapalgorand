from algopy import ARC4Contract, UInt64, GlobalState, Global, Txn, TealType
from algopy.arc4 import abimethod


class LiquidityPool(ARC4Contract):
    # Global state variables
    admin = GlobalState(TealType.bytes, default=Global.creator_address())
    asset_a = GlobalState(TealType.uint64, default=UInt64(0))
    asset_b = GlobalState(TealType.uint64, default=UInt64(0))
    reserve_a = GlobalState(TealType.uint64, default=UInt64(0))
    reserve_b = GlobalState(TealType.uint64, default=UInt64(0))
    total_supply = GlobalState(TealType.uint64, default=UInt64(0))
    fee_rate = GlobalState(TealType.uint64, default=UInt64(3))  # 0.3%

    @abimethod()
    def set_assets(self, asset_a: UInt64, asset_b: UInt64) -> None:
        """Set asset pair for the pool (admin only)"""
        assert Txn.sender == self.admin.get()
        self.asset_a.set(asset_a)
        self.asset_b.set(asset_b)

    @abimethod()
    def set_fee_rate(self, rate: UInt64) -> None:
        """Set fee rate in basis points (admin only)"""
        assert Txn.sender == self.admin.get()
        self.fee_rate.set(rate)

    @abimethod()
    def get_reserves(self) -> tuple[UInt64, UInt64]:
        """Get current reserves"""
        return (self.reserve_a.get(), self.reserve_b.get())

    @abimethod()
    def get_total_supply(self) -> UInt64:
        """Get total LP token supply"""
        return self.total_supply.get()

    @abimethod()
    def get_fee_rate(self) -> UInt64:
        """Get fee rate"""
        return self.fee_rate.get()

    @abimethod()
    def add_liquidity(self, amount_a: UInt64, amount_b: UInt64) -> UInt64:
        """Add liquidity to the pool (admin only)"""
        assert Txn.sender == self.admin.get()
        
        # Update reserves
        current_reserve_a = self.reserve_a.get()
        current_reserve_b = self.reserve_b.get()
        
        self.reserve_a.set(current_reserve_a + amount_a)
        self.reserve_b.set(current_reserve_b + amount_b)
        
        # Update total supply (simplified)
        current_supply = self.total_supply.get()
        self.total_supply.set(current_supply + UInt64(1))
        
        return current_supply + UInt64(1)