"""
StakingRewards.py
Manages staking of LP tokens to earn $MOOD governance token
"""

from typing import Final

from beaker import *

# Import decorators
external = Application.external
create = Application.create
from pyteal import (
    And, Assert, Bytes, Concat, Global, Gtxn, If, Int, Itob,
    Seq, Txn, TxnField, TxnType, InnerTxnBuilder, TealType
)

class StakingRewardsState:
    mood_token_id = GlobalStateValue(
        stack_type=TealType.uint64,
        descr="Asset ID of the $MOOD governance token"
    )
    
    lp_token_id = GlobalStateValue(
        stack_type=TealType.uint64,
        descr="Asset ID of the LP token being staked"
    )
    
    total_staked = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Total LP tokens staked"
    )
    
    emission_rate = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(100_000),  # 0.1 $MOOD per block per LP token staked
        descr="Emission rate (microMOOD per block per LP token)"
    )
    
    last_update_block = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Last block rewards were updated"
    )

class StakingRewards(Application):
    # Constants
    MIN_STAKE: Final = Int(1_000_000)  # 1.0 LP tokens minimum
    
    def __init__(self):
        super().__init__()
        self.state = StakingRewardsState()
        # Per-user stake tracking
        self.user_stakes = Mapping(abi.Address, abi.Uint64)
    
    @create
    def create(self):
        return self.initialize_application_state()
    
    @external
    def bootstrap(self, mood_token_id: abi.Uint64, lp_token_id: abi.Uint64):
        """Initialize staking contract with token IDs"""
        return Seq(
            Assert(self.state.mood_token_id == Int(0)),  # Not already initialized
            self.state.mood_token_id.set(mood_token_id.get()),
            self.state.lp_token_id.set(lp_token_id.get()),
            self.state.last_update_block.set(Global.round()),
        )
    
    @external
    def stake(self, amount: abi.Uint64):
        """Stake LP tokens"""
        return Seq(
            # Update rewards first
            self._update_rewards(),
            
            # Verify minimum stake amount
            Assert(amount.get() >= self.MIN_STAKE),
            
            # Verify LP token transfer
            Assert(Gtxn[0].type_enum() == TxnType.AssetTransfer),
            Assert(Gtxn[0].sender() == Txn.sender()),
            Assert(Gtxn[0].asset_receiver() == Global.current_application_address()),
            Assert(Gtxn[0].xfer_asset() == self.state.lp_token_id),
            Assert(Gtxn[0].asset_amount() == amount.get()),
            
            # Update total staked and user stake
            self.state.total_staked.set(
                self.state.total_staked + amount.get()
            ),
            # Update user's stake
            (current_stake := abi.Uint64()).set(self.user_stakes[Txn.sender()]),
            self.user_stakes[Txn.sender()].set(
                current_stake.get() + amount.get()
            ),
        )
    
    @external
    def unstake(self, amount: abi.Uint64):
        """Unstake LP tokens"""
        return Seq(
            # Update rewards first
            self._update_rewards(),
            
            # Verify caller's stake balance
            # Verify user has enough staked
            (user_stake := abi.Uint64()).set(self.user_stakes[Txn.sender()]),
            Assert(amount.get() <= user_stake.get()),
            
            # Return LP tokens
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: self.state.lp_token_id,
                TxnField.asset_amount: amount.get(),
                TxnField.asset_receiver: Txn.sender(),
            }),
            InnerTxnBuilder.Submit(),
            
            # Update total staked and user stake
            self.state.total_staked.set(
                self.state.total_staked - amount.get()
            ),
            # Update user's stake
            (current_stake := abi.Uint64()).set(self.user_stakes[Txn.sender()]),
            self.user_stakes[Txn.sender()].set(
                current_stake.get() - amount.get()
            ),
        )
    
    @external
    def claim(self):
        """Claim accumulated $MOOD rewards"""
        return Seq(
            # Update rewards first
            self._update_rewards(),
            
            # Calculate rewards
            (blocks_elapsed := abi.Uint64()).set(
                Global.round() - self.state.last_update_block
            ),
            # Calculate rewards with overflow protection
            (reward_amount := abi.Uint64()).set(
                (blocks_elapsed.get() * self.state.emission_rate * self.state.total_staked) / Int(1_000_000)
            ),
            
            # Send rewards if any
            If(reward_amount.get() > Int(0),
               Seq(
                   InnerTxnBuilder.Begin(),
                   InnerTxnBuilder.SetFields({
                       TxnField.type_enum: TxnType.AssetTransfer,
                       TxnField.xfer_asset: self.state.mood_token_id,
                       TxnField.asset_amount: reward_amount.get(),
                       TxnField.asset_receiver: Txn.sender(),
                   }),
                   InnerTxnBuilder.Submit(),
               )
            ),
            
            # Update last update block
            self.state.last_update_block.set(Global.round()),
        )
    
    def _update_rewards(self):
        """Internal: Update reward state"""
        return Seq(
            # Calculate elapsed blocks
            (blocks_elapsed := abi.Uint64()).set(
                Global.round() - self.state.last_update_block
            ),
            
            # If any blocks elapsed and tokens staked, distribute rewards
            If(
                And(
                    blocks_elapsed.get() > Int(0),
                    self.state.total_staked > Int(0)
                ),
                Seq(
                    # Calculate rewards with overflow protection
                    (reward_amount := abi.Uint64()).set(
                        (blocks_elapsed.get() * self.state.emission_rate * self.state.total_staked) / Int(1_000_000)
                    ),
                    
                    # Distribute rewards if any
                    If(reward_amount.get() > Int(0),
                       Seq(
                           InnerTxnBuilder.Begin(),
                           InnerTxnBuilder.SetFields({
                               TxnField.type_enum: TxnType.AssetTransfer,
                               TxnField.xfer_asset: self.state.mood_token_id,
                               TxnField.asset_amount: reward_amount.get(),
                               TxnField.asset_receiver: Txn.sender(),
                           }),
                           InnerTxnBuilder.Submit(),
                       )
                    ),
                )
            ),
            
            # Update last update block
            self.state.last_update_block.set(Global.round()),
        )

if __name__ == "__main__":
    app = StakingRewards()
    print(app.build())

