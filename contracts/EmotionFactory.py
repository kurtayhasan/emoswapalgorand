"""
EmotionFactory.py
Manages emotion tokens (ASA) and daily minting functionality.
"""

from pyteal import *
from beaker import *

# Global state keys
ADMIN_KEY = Bytes("admin")
MINT_AMOUNT_KEY = Bytes("mint_amt")
PAUSED_KEY = Bytes("paused")
EMOTION_COUNT_KEY = Bytes("emotion_count")

# Box storage for emotion mappings
emotion_to_asset = BoxMapping(abi.String, abi.Uint64)

class EmotionFactoryState:
    admin = GlobalStateValue(
        stack_type=TealType.bytes,
        default=Global.creator_address(),
        descr="Admin address"
    )
    mint_amount = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(10),
        descr="Daily mint amount per emotion"
    )
    paused = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Pause state (0=active, 1=paused)"
    )
    emotion_count = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Total number of emotions created"
    )

class EmotionFactory(Application):
    def __init__(self):
        super().__init__()
        self.state = EmotionFactoryState()
        self.emotion_to_asset = emotion_to_asset

    @external
    def create_emotion(self, name: abi.String, *, output: abi.Uint64):
        """Create a new emotion ASA if it doesn't exist"""
        return Seq(
            # Check if not paused
            Assert(self.state.paused == Int(0)),
            
            # Check if emotion already exists
            (emotion_exists := abi.Bool()).set(
                self.emotion_to_asset[name.get()].exists()
            ),
            Assert(emotion_exists.get() == Int(0)),
            
            # Create ASA
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetConfig,
                TxnField.config_asset_name: name.get(),
                TxnField.config_asset_unit_name: name.get()[:4],  # First 4 chars
                TxnField.config_asset_total: Int(1000000),  # 1M total supply
                TxnField.config_asset_decimals: Int(0),
                TxnField.config_asset_manager: Global.current_application_address(),
                TxnField.config_asset_reserve: Global.current_application_address(),
                TxnField.config_asset_freeze: Global.current_application_address(),
                TxnField.config_asset_clawback: Global.current_application_address(),
            }),
            InnerTxnBuilder.Submit(),
            
            # Store mapping
            self.emotion_to_asset[name.get()].set(InnerTxn.created_asset_id()),
            
            # Update count
            self.state.emotion_count.set(self.state.emotion_count + Int(1)),
            
            # Return asset ID
            output.set(InnerTxn.created_asset_id()),
        )

    @external
    def mint_daily(self, name: abi.String, receiver: abi.Account):
        """Mint daily allowance of emotion token to receiver"""
        return Seq(
            # Check if not paused
            Assert(self.state.paused == Int(0)),
            
            # Check if emotion exists
            (emotion_exists := abi.Bool()).set(
                self.emotion_to_asset[name.get()].exists()
            ),
            Assert(emotion_exists.get() == Int(1)),
            
            # Get current day (simplified - using block timestamp)
            current_day := Global.latest_timestamp() / Int(86400),  # 86400 seconds per day
            
            # Check local state for last mint day
            (last_mint_day := abi.Uint64()).set(
                App.localGet(receiver.address(), Bytes("last_mint_day"))
            ),
            
            # If no previous mint or different day, allow minting
            If(
                last_mint_day.get() == Int(0),
                # First time minting
                Seq(
                    # Mint tokens
                    InnerTxnBuilder.Begin(),
                    InnerTxnBuilder.SetFields({
                        TxnField.type_enum: TxnType.AssetTransfer,
                        TxnField.xfer_asset: self.emotion_to_asset[name.get()],
                        TxnField.asset_receiver: receiver.address(),
                        TxnField.asset_amount: self.state.mint_amount,
                    }),
                    InnerTxnBuilder.Submit(),
                    
                    # Update local state
                    App.localPut(receiver.address(), Bytes("last_mint_day"), current_day),
                ),
                # Check if different day
                If(
                    last_mint_day.get() != current_day,
                    Seq(
                        # Mint tokens
                        InnerTxnBuilder.Begin(),
                        InnerTxnBuilder.SetFields({
                            TxnField.type_enum: TxnType.AssetTransfer,
                            TxnField.xfer_asset: self.emotion_to_asset[name.get()],
                            TxnField.asset_receiver: receiver.address(),
                            TxnField.asset_amount: self.state.mint_amount,
                        }),
                        InnerTxnBuilder.Submit(),
                        
                        # Update local state
                        App.localPut(receiver.address(), Bytes("last_mint_day"), current_day),
                    ),
                    # Same day, reject
                    Reject()
                )
            ),
        )

    @external
    def get_emotion_asset(self, name: abi.String, *, output: abi.Uint64):
        """Get asset ID for emotion name"""
        return Seq(
            (emotion_exists := abi.Bool()).set(
                self.emotion_to_asset[name.get()].exists()
            ),
            Assert(emotion_exists.get() == Int(1)),
            output.set(self.emotion_to_asset[name.get()]),
        )

    @external(authorize=Authorize.only(Global.creator_address()))
    def set_mint_amount(self, amount: abi.Uint64):
        """Set daily mint amount (admin only)"""
        return self.state.mint_amount.set(amount.get())

    @external(authorize=Authorize.only(Global.creator_address()))
    def pause(self):
        """Pause the contract (admin only)"""
        return self.state.paused.set(Int(1))

    @external(authorize=Authorize.only(Global.creator_address()))
    def unpause(self):
        """Unpause the contract (admin only)"""
        return self.state.paused.set(Int(0))

    @external(authorize=Authorize.only(Global.creator_address()))
    def update_admin(self, new_admin: abi.Account):
        """Update admin address (admin only)"""
        return self.state.admin.set(new_admin.address())

    @external(read_only=True)
    def get_emotion_count(self, *, output: abi.Uint64):
        """Get total number of emotions created"""
        return output.set(self.state.emotion_count)

    @external(read_only=True)
    def is_paused(self, *, output: abi.Bool):
        """Check if contract is paused"""
        return output.set(self.state.paused == Int(1))

if __name__ == "__main__":
    app = EmotionFactory()
    print(app.build())
