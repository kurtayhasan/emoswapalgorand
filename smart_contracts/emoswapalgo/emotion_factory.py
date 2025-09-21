from algopy import ARC4Contract, UInt64, GlobalState, Global, Txn, TealType
from algopy.arc4 import abimethod


class EmotionFactory(ARC4Contract):
    # Global state variables
    admin = GlobalState(TealType.bytes, default=Global.creator_address())
    mint_amount = GlobalState(TealType.uint64, default=UInt64(10))
    paused = GlobalState(TealType.uint64, default=UInt64(0))
    emotion_count = GlobalState(TealType.uint64, default=UInt64(0))
    mood_token_id = GlobalState(TealType.uint64, default=UInt64(746157034))

    @abimethod()
    def set_mint_amount(self, amount: UInt64) -> None:
        """Set daily mint amount per emotion (admin only)"""
        assert Txn.sender == self.admin.get()
        self.mint_amount.set(amount)

    @abimethod()
    def set_paused(self, paused_state: UInt64) -> None:
        """Set pause state (0=active, 1=paused) (admin only)"""
        assert Txn.sender == self.admin.get()
        self.paused.set(paused_state)

    @abimethod()
    def get_mint_amount(self) -> UInt64:
        """Get daily mint amount"""
        return self.mint_amount.get()

    @abimethod()
    def get_paused_state(self) -> UInt64:
        """Get pause state"""
        return self.paused.get()

    @abimethod()
    def get_emotion_count(self) -> UInt64:
        """Get total emotion count"""
        return self.emotion_count.get()

    @abimethod()
    def get_mood_token_id(self) -> UInt64:
        """Get MOOD token ID"""
        return self.mood_token_id.get()

    @abimethod()
    def create_emotion(self, emotion_name: String) -> UInt64:
        """Create a new emotion token (admin only)"""
        assert Txn.sender == self.admin.get()
        assert self.paused.get() == UInt64(0)  # Not paused
        
        # Increment emotion count
        current_count = self.emotion_count.get()
        self.emotion_count.set(current_count + UInt64(1))
        
        return current_count + UInt64(1)