# EmoSwap - Algorand Emotion Trading Platform

EmoSwap, Algorand blockchain üzerinde duyguları tokenize eden ve ticaretini yapan yenilikçi bir DeFi platformudur.

## 🎯 Proje Özeti

EmoSwap, kullanıcıların günlük duygularını tokenize edebileceği, bu tokenları takas edebileceği ve likidite sağlayarak ödül kazanabileceği bir platformdur.

## 🏗️ Mimari

### Smart Contracts (TEAL v2)
- **emotion_factory.teal**: Duygu tokenlarını oluşturur ve günlük mint işlemlerini yönetir
- **governance.teal**: Protokol parametrelerini ve gelecekteki DAO yönetimini yönetir
- **liquidity_pool.teal**: Duygu ASA <-> ALGO çiftleri için likidite sağlama
- **staking_rewards.teal**: LP token stake ederek $MOOD governance token kazanma
- **swap_pool.teal**: Duygu ASA <-> ALGO çiftleri için sabit çarpım AMM (x*y=k)
- **clear.teal**: Tüm kontratlar için ortak clear program

### Frontend
- **Next.js 15** ile modern React uygulaması
- **Algorand Wallet** entegrasyonu
- **Responsive** ve kullanıcı dostu arayüz

## 🚀 Kurulum

### Gereksinimler
- Node.js 18+
- npm veya yarn
- Algorand Wallet (Pera, MyAlgo, vs.)

### Kurulum Adımları

1. **Repository'yi klonlayın**
```bash
git clone https://github.com/yourusername/emoswapalgo.git
cd emoswapalgo
```

2. **Bağımlılıkları yükleyin**
```bash
npm install
cd web
npm install
```

3. **Web uygulamasını başlatın**
```bash
cd web
npm run dev
```

4. **Tarayıcıda açın**
```
http://localhost:3000
```

## 📋 Deployment

### Algo Studio ile Deployment (Önerilen)

1. **Algo Studio'ya gidin**: https://studio.algorand.org/
2. **Yeni proje oluşturun**
3. **TEAL dosyalarını kopyalayın**:
   - `contracts/emotion_factory.teal`
   - `contracts/governance.teal`
   - `contracts/liquidity_pool.teal`
   - `contracts/staking_rewards.teal`
   - `contracts/swap_pool.teal`
   - `contracts/clear.teal`
4. **TestNet'e deploy edin**
5. **App ID'leri alın**
6. **Konfigürasyonları güncelleyin**

### Otomatik Deployment

```bash
node scripts/deploy.js
```

## 🔧 Konfigürasyon

### Environment Variables
```env
NEXT_PUBLIC_ALGOD_SERVER=https://testnet-api.algonode.cloud
NEXT_PUBLIC_ALGOD_PORT=
NEXT_PUBLIC_ALGOD_TOKEN=
```

### Contract IDs
```typescript
// web/src/lib/config.ts
export const CONFIG = {
  EMOTION_FACTORY_ID: 746159123, // Deploy edildi
  GOVERNANCE_ID: 0,              // Beklemede
  STAKING_REWARDS_ID: 0,         // Beklemede
  LIQUIDITY_POOL_ID: 0,          // Beklemede
  SWAP_POOL_ID: 0,               // Beklemede
  MOOD_TOKEN_ID: 746157034,      // Deploy edildi
};
```

## 📊 Mevcut Durum

| Bileşen | Durum | Açıklama |
|---------|-------|----------|
| **$MOOD Token** | ✅ Deploy Edildi | ID: 746157034 |
| **Web Arayüzü** | ✅ Çalışıyor | http://localhost:3000 |
| **EmoSwap Ana Kontrat** | ✅ Deploy Edildi | ID: 746159123 |
| **AlgoKit Yapısı** | ✅ Uygulandı | Modern Python kontratları |
| **Konfigürasyonlar** | ✅ Güncellendi | App ID'ler eklendi |

## 🎨 Özellikler

### Desteklenen Duygular
- 😊 Happy (Mutlu)
- 😢 Sad (Üzgün)
- 😠 Angry (Kızgın)
- 🤩 Excited (Heyecanlı)
- 😌 Calm (Sakin)
- 😟 Anxious (Endişeli)
- 🙏 Grateful (Minnettar)
- ❤️ Loved (Sevilen)

### Trading Özellikleri
- **Minimum Swap**: 0.001 ALGO
- **Maksimum Slippage**: %5
- **Swap Fee**: %0.3

### Staking Özellikleri
- **Minimum Stake**: 1.0 LP Token
- **Reward Rate**: %10

## 🔗 Bağlantılar

- **TestNet Explorer**: https://testnet.algoexplorer.io/
- **$MOOD Token**: https://testnet.algoexplorer.io/asset/746157034
- **EmoSwap Ana Kontrat**: https://testnet.algoexplorer.io/application/746159123
- **Algo Studio**: https://studio.algorand.org/

## 📝 Lisans

MIT License

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📞 İletişim

- **GitHub**: [@yourusername](https://github.com/yourusername)
- **Twitter**: [@emoswapalgo](https://twitter.com/emoswapalgo)

---

**Not**: Bu proje Algorand TestNet üzerinde çalışmaktadır. MainNet deployment için ek güvenlik testleri gereklidir.