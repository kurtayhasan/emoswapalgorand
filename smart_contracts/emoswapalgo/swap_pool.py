from algopy import ARC4Contract, UInt64, GlobalState, Global, Txn, TealType
from algopy.arc4 import abimethod


class SwapPool(ARC4Contract):
    # Global state variables
    admin = GlobalState(TealType.bytes, default=Global.creator_address())
    asset_a = GlobalState(TealType.uint64, default=UInt64(0))
    asset_b = GlobalState(TealType.uint64, default=UInt64(0))
    reserve_a = GlobalState(TealType.uint64, default=UInt64(0))
    reserve_b = GlobalState(TealType.uint64, default=UInt64(0))
    fee_rate = GlobalState(TealType.uint64, default=UInt64(3))  # 0.3%

    @abimethod()
    def set_assets(self, asset_a: UInt64, asset_b: UInt64) -> None:
        """Set asset pair for the pool (admin only)"""
        assert Txn.sender == self.admin.get()
        self.asset_a.set(asset_a)
        self.asset_b.set(asset_b)

    @abimethod()
    def set_fee_rate(self, rate: UInt64) -> None:
        """Set swap fee rate (in basis points) (admin only)"""
        assert Txn.sender == self.admin.get()
        self.fee_rate.set(rate)

    @abimethod()
    def get_reserves(self) -> tuple[UInt64, UInt64]:
        """Get current reserves"""
        return (self.reserve_a.get(), self.reserve_b.get())

    @abimethod()
    def get_fee_rate(self) -> UInt64:
        """Get swap fee rate"""
        return self.fee_rate.get()

    @abimethod()
    def swap_a_for_b(self, amount_a: UInt64) -> UInt64:
        """Swap asset A for asset B (admin only for now)"""
        assert Txn.sender == self.admin.get()
        
        current_reserve_a = self.reserve_a.get()
        current_reserve_b = self.reserve_b.get()
        
        # Simple constant product formula: x * y = k
        # amount_b = (reserve_b * amount_a) / (reserve_a + amount_a)
        if current_reserve_a > UInt64(0) and current_reserve_b > UInt64(0):
            amount_b = (current_reserve_b * amount_a) / (current_reserve_a + amount_a)
            
            # Update reserves
            self.reserve_a.set(current_reserve_a + amount_a)
            self.reserve_b.set(current_reserve_b - amount_b)
            
            return amount_b
        else:
            return UInt64(0)

    @abimethod()
    def swap_b_for_a(self, amount_b: UInt64) -> UInt64:
        """Swap asset B for asset A (admin only for now)"""
        assert Txn.sender == self.admin.get()
        
        current_reserve_a = self.reserve_a.get()
        current_reserve_b = self.reserve_b.get()
        
        # Simple constant product formula: x * y = k
        # amount_a = (reserve_a * amount_b) / (reserve_b + amount_b)
        if current_reserve_a > UInt64(0) and current_reserve_b > UInt64(0):
            amount_a = (current_reserve_a * amount_b) / (current_reserve_b + amount_b)
            
            # Update reserves
            self.reserve_a.set(current_reserve_a - amount_a)
            self.reserve_b.set(current_reserve_b + amount_b)
            
            return amount_a
        else:
            return UInt64(0)