from algopy import ARC4Contract, UInt64, GlobalState, Global, Txn, TealType
from algopy.arc4 import abimethod


class StakingRewards(ARC4Contract):
    # Global state variables
    admin = GlobalState(TealType.bytes, default=Global.creator_address())
    reward_token = GlobalState(TealType.uint64, default=UInt64(746157034))  # MOOD token
    reward_rate = GlobalState(TealType.uint64, default=UInt64(10))  # 10% per year
    total_staked = GlobalState(TealType.uint64, default=UInt64(0))
    last_update_time = GlobalState(TealType.uint64, default=UInt64(0))

    @abimethod()
    def set_reward_token(self, token_id: UInt64) -> None:
        """Set reward token (admin only)"""
        assert Txn.sender == self.admin.get()
        self.reward_token.set(token_id)

    @abimethod()
    def set_reward_rate(self, rate: UInt64) -> None:
        """Set reward rate (percentage per year) (admin only)"""
        assert Txn.sender == self.admin.get()
        self.reward_rate.set(rate)

    @abimethod()
    def get_reward_rate(self) -> UInt64:
        """Get reward rate"""
        return self.reward_rate.get()

    @abimethod()
    def get_total_staked(self) -> UInt64:
        """Get total staked amount"""
        return self.total_staked.get()

    @abimethod()
    def get_reward_token(self) -> UInt64:
        """Get reward token ID"""
        return self.reward_token.get()

    @abimethod()
    def stake(self, amount: UInt64) -> UInt64:
        """Stake LP tokens (admin only for now)"""
        assert Txn.sender == self.admin.get()
        
        current_staked = self.total_staked.get()
        self.total_staked.set(current_staked + amount)
        
        return current_staked + amount

    @abimethod()
    def unstake(self, amount: UInt64) -> UInt64:
        """Unstake LP tokens (admin only for now)"""
        assert Txn.sender == self.admin.get()
        
        current_staked = self.total_staked.get()
        assert current_staked >= amount  # Check sufficient balance
        
        self.total_staked.set(current_staked - amount)
        
        return current_staked - amount