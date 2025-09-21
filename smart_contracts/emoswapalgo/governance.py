from algopy import ARC4Contract, UInt64, GlobalState, Global, Txn, TealType
from algopy.arc4 import abimethod


class Governance(ARC4Contract):
    # Global state variables
    admin = GlobalState(TealType.bytes, default=Global.creator_address())
    min_proposal_amount = GlobalState(TealType.uint64, default=UInt64(1000))
    voting_period = GlobalState(TealType.uint64, default=UInt64(604800))  # 7 days
    proposal_count = GlobalState(TealType.uint64, default=UInt64(0))
    mood_token_id = GlobalState(TealType.uint64, default=UInt64(746157034))

    @abimethod()
    def set_min_proposal_amount(self, amount: UInt64) -> None:
        """Set minimum proposal amount (admin only)"""
        assert Txn.sender == self.admin.get()
        self.min_proposal_amount.set(amount)

    @abimethod()
    def set_voting_period(self, period: UInt64) -> None:
        """Set voting period in seconds (admin only)"""
        assert Txn.sender == self.admin.get()
        self.voting_period.set(period)

    @abimethod()
    def get_min_proposal_amount(self) -> UInt64:
        """Get minimum proposal amount"""
        return self.min_proposal_amount.get()

    @abimethod()
    def get_voting_period(self) -> UInt64:
        """Get voting period"""
        return self.voting_period.get()

    @abimethod()
    def get_proposal_count(self) -> UInt64:
        """Get total proposal count"""
        return self.proposal_count.get()

    @abimethod()
    def get_mood_token_id(self) -> UInt64:
        """Get MOOD token ID"""
        return self.mood_token_id.get()

    @abimethod()
    def create_proposal(self, proposal_id: UInt64) -> UInt64:
        """Create a new governance proposal (admin only)"""
        assert Txn.sender == self.admin.get()
        
        # Increment proposal count
        current_count = self.proposal_count.get()
        self.proposal_count.set(current_count + UInt64(1))
        
        return current_count + UInt64(1)