# EmoSwap Architecture

## Overview

EmoSwap is an emotion-based DeFi protocol built on Algorand. Users can mint daily emotion tokens, trade them through AMM pools, provide liquidity, and stake LP tokens to earn $MOOD governance tokens.

## Core Components

### EmotionFactory
- Creates new emotion ASAs
- Manages daily minting (fixed amount per user per day)
- Whitelist control for new emotions
- Global state: admin, mint_amt, paused
- Box storage: emotion name → assetId mapping
- Local state: last_day_minted per emotion

### SwapPool
- Constant-product AMM (x*y=k) for emotion/ALGO pairs
- Single pool per emotion token
- 0.3% swap fee to protocol
- Global state: reserves, asset IDs
- Methods: bootstrap, swap_exact_in

### LiquidityPool
- Issues LP tokens for emotion/ALGO pairs
- Proportional share of pool reserves
- Global state: LP token ID, reserves, total supply
- Methods: add_liquidity, remove_liquidity

### StakingRewards
- Stake LP tokens to earn $MOOD
- Linear reward emission per block
- Global state: staked amounts, emissions, last update
- Methods: stake, unstake, claim

### Governance
- Protocol parameter management
- Future DAO voting (MVP: admin-only)
- Global state: parameters, admin
- Parameters: fees, emission rates, etc.

## Flow Diagrams

### Daily Mint Flow
```
User ─── mint_daily(emotion) ───> EmotionFactory
  │                                     │
  │                                     v
  │             <─── Check last mint date
  │                                     │
  └─── Receive emotion tokens <──── Mint if eligible
```

### Swap Flow (x*y=k)
```
User ─── swap_exact_in ───> SwapPool
  │         │                  │
  │   (amount_in)        Check reserves
  │         │                  │
  │         v            Calculate out
  │     Send asset   <────    │
  │         │                 │
  └─── Receive out    Update reserves
```

### LP Flow
```
User ─── add_liquidity ───> LiquidityPool
  │    (ALGO + ASA)           │
  │                           v
  │                    Calculate shares
  │                           │
  └─── Receive LP <──── Mint LP tokens
```

### Staking Flow
```
User ─── stake(LP) ───> StakingRewards
  │                          │
  │                    Track stake
  │                          │
  └─── $MOOD rewards <── Emit per block
```

## Data Model

### Global State
- EmotionFactory
  - admin: address
  - mint_amt: uint64
  - paused: uint64
  - Box: emotion → assetId

- SwapPool
  - asset_id: uint64
  - reserves: uint64[2]
  - fee_bps: uint64

- LiquidityPool
  - lp_token_id: uint64
  - total_supply: uint64
  - reserves: uint64[2]

- StakingRewards
  - mood_token_id: uint64
  - emission_rate: uint64
  - total_staked: uint64

### Local State
- EmotionFactory
  - last_day_minted: uint64 (per emotion)

### ASAs
- Emotion tokens: Daily mintable tokens
- LP tokens: Pool share certificates 
- $MOOD: Governance token
