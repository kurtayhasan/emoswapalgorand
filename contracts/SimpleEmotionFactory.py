"""
Simple EmotionFactory for testing
"""

from pyteal import *
from beaker import *

class SimpleEmotionFactory(Application):
    def __init__(self):
        super().__init__()
        
        # Global state
        self.admin = GlobalStateValue(
            stack_type=TealType.bytes,
            default=Global.creator_address(),
            descr="Admin address"
        )
        
        self.emotion_count = GlobalStateValue(
            stack_type=TealType.uint64,
            default=Int(0),
            descr="Total number of emotions created"
        )
    
    @Application.create
    def create(self):
        return self.initialize_global_state()
    
    @Application.external
    def create_emotion(self, name: abi.String, *, output: abi.Uint64):
        """Create a new emotion ASA"""
        return Seq(
            # Increment emotion count
            self.emotion_count.set(self.emotion_count + Int(1)),
            
            # Create ASA
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetField(TxnField.type_enum, TxnType.AssetConfig),
            InnerTxnBuilder.SetField(TxnField.config_asset_name, name.get()),
            InnerTxnBuilder.SetField(TxnField.config_asset_unit_name, name.get()[:4]),
            InnerTxnBuilder.SetField(TxnField.config_asset_total, Int(1000000)),
            InnerTxnBuilder.SetField(TxnField.config_asset_decimals, Int(6)),
            InnerTxnBuilder.SetField(TxnField.config_asset_manager, Global.creator_address()),
            InnerTxnBuilder.SetField(TxnField.config_asset_reserve, Global.creator_address()),
            InnerTxnBuilder.SetField(TxnField.config_asset_freeze, Global.creator_address()),
            InnerTxnBuilder.SetField(TxnField.config_asset_clawback, Global.creator_address()),
            InnerTxnBuilder.Submit(),
            
            # Return asset ID
            output.set(InnerTxn.created_asset_id()),
        )
    
    @Application.external
    def mint_daily(self, emotion_name: abi.String):
        """Mint daily emotion tokens"""
        return Seq(
            # Simple implementation - just return success
            Int(1)
        )

if __name__ == "__main__":
    app = SimpleEmotionFactory()
    print(app.build())
