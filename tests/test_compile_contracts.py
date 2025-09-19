"""
Test contract compilation and basic functionality
"""

import unittest
import sys
from pathlib import Path

# Add contracts directory to path
sys.path.append(str(Path(__file__).parent.parent / "contracts"))

from EmotionFactory import EmotionFactory
from SwapPool import SwapPool
from LiquidityPool import LiquidityPool
from StakingRewards import StakingRewards
from Governance import Governance

class TestContractCompilation(unittest.TestCase):
    def test_emotion_factory_compilation(self):
        """Test EmotionFactory contract compiles"""
        app = EmotionFactory()
        approval, clear = app.build()
        self.assertIsNotNone(approval)
        self.assertIsNotNone(clear)
    
    def test_swap_pool_compilation(self):
        """Test SwapPool contract compiles"""
        app = SwapPool()
        approval, clear = app.build()
        self.assertIsNotNone(approval)
        self.assertIsNotNone(clear)
    
    def test_liquidity_pool_compilation(self):
        """Test LiquidityPool contract compiles"""
        app = LiquidityPool()
        approval, clear = app.build()
        self.assertIsNotNone(approval)
        self.assertIsNotNone(clear)
    
    def test_staking_rewards_compilation(self):
        """Test StakingRewards contract compiles"""
        app = StakingRewards()
        approval, clear = app.build()
        self.assertIsNotNone(approval)
        self.assertIsNotNone(clear)
    
    def test_governance_compilation(self):
        """Test Governance contract compiles"""
        app = Governance()
        approval, clear = app.build()
        self.assertIsNotNone(approval)
        self.assertIsNotNone(clear)

if __name__ == "__main__":
    unittest.main()
