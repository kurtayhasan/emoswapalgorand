from algopy import ARC4Contract, String, UInt64, GlobalState, Global, Txn, TealType
from algopy.arc4 import abimethod


class Emoswapalgo(ARC4Contract):
    # Global state variables
    admin = GlobalState(TealType.bytes, default=Global.creator_address())
    mood_token_id = GlobalState(TealType.uint64, default=UInt64(746157034))
    emotion_factory_id = GlobalState(TealType.uint64, default=UInt64(746159123))
    governance_id = GlobalState(TealType.uint64, default=UInt64(0))
    liquidity_pool_id = GlobalState(TealType.uint64, default=UInt64(0))
    staking_rewards_id = GlobalState(TealType.uint64, default=UInt64(0))
    swap_pool_id = GlobalState(TealType.uint64, default=UInt64(0))
    
    @abimethod()
    def hello(self, name: String) -> String:
        """Welcome message"""
        return "Hello, " + name + "! Welcome to EmoSwap - The Future of Emotion Trading!"
    
    @abimethod()
    def get_mood_token_id(self) -> UInt64:
        """Get MOOD token ID"""
        return self.mood_token_id.get()
    
    @abimethod()
    def get_emotion_factory_id(self) -> UInt64:
        """Get EmotionFactory App ID"""
        return self.emotion_factory_id.get()
    
    @abimethod()
    def get_governance_id(self) -> UInt64:
        """Get Governance App ID"""
        return self.governance_id.get()
    
    @abimethod()
    def get_liquidity_pool_id(self) -> UInt64:
        """Get LiquidityPool App ID"""
        return self.liquidity_pool_id.get()
    
    @abimethod()
    def get_staking_rewards_id(self) -> UInt64:
        """Get StakingRewards App ID"""
        return self.staking_rewards_id.get()
    
    @abimethod()
    def get_swap_pool_id(self) -> UInt64:
        """Get SwapPool App ID"""
        return self.swap_pool_id.get()
    
    @abimethod()
    def set_governance_id(self, app_id: UInt64) -> None:
        """Set Governance App ID (admin only)"""
        assert Txn.sender == self.admin.get()
        self.governance_id.set(app_id)
    
    @abimethod()
    def set_liquidity_pool_id(self, app_id: UInt64) -> None:
        """Set LiquidityPool App ID (admin only)"""
        assert Txn.sender == self.admin.get()
        self.liquidity_pool_id.set(app_id)
    
    @abimethod()
    def set_staking_rewards_id(self, app_id: UInt64) -> None:
        """Set StakingRewards App ID (admin only)"""
        assert Txn.sender == self.admin.get()
        self.staking_rewards_id.set(app_id)
    
    @abimethod()
    def set_swap_pool_id(self, app_id: UInt64) -> None:
        """Set SwapPool App ID (admin only)"""
        assert Txn.sender == self.admin.get()
        self.swap_pool_id.set(app_id)
    
    @abimethod()
    def get_all_contract_ids(self) -> tuple[UInt64, UInt64, UInt64, UInt64, UInt64, UInt64]:
        """Get all contract IDs"""
        return (
            self.mood_token_id.get(),
            self.emotion_factory_id.get(),
            self.governance_id.get(),
            self.liquidity_pool_id.get(),
            self.staking_rewards_id.get(),
            self.swap_pool_id.get()
        )
