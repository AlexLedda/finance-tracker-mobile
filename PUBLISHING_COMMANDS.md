# 🚀 Comandi Pronti per la Pubblicazione

## ✅ L'app è stata configurata!

**Configurazione Completata:**
- Nome: **Finance Tracker**
- Bundle ID iOS: **com.financetracker.app**
- Package Android: **com.financetracker.app**
- Versione: **1.0.0**

---

## 📝 Cosa Fare SUBITO

### 1️⃣ Crea gli Account Developer

Prima di procedere, devi creare questi account:

**🤖 Google Play Console** (per Android)
- URL: https://play.google.com/console/signup
- Costo: $25 (pagamento unico)
- Tempo attivazione: 24-48 ore

**🍎 Apple Developer Program** (per iOS)
- URL: https://developer.apple.com/programs/
- Costo: $99/anno
- Tempo attivazione: 24-48 ore

---

## 💻 Comandi da Eseguire (DOPO aver creato gli account)

### 2️⃣ Installa EAS CLI

Apri il terminale sul tuo computer ed esegui:

```bash
npm install -g eas-cli
```

Oppure se usi Yarn:
```bash
yarn global add eas-cli
```

---

### 3️⃣ Entra nella cartella del progetto

**IMPORTANTE**: Devi eseguire questi comandi dal tuo computer locale, NON nella piattaforma Emergent.

Prima scarica il progetto da Emergent (usando GitHub o download diretto), poi:

```bash
cd percorso/al/tuo/progetto/frontend
```

---

### 4️⃣ Login a Expo

```bash
eas login
```

Inserisci le credenziali del tuo account Expo (quello che hai creato).

---

### 5️⃣ Configura EAS

```bash
eas build:configure
```

Questo creerà un file `eas.json`. Rispondi alle domande:
- Generate a new Android Keystore? → **Yes**
- Generate a new iOS Distribution Certificate? → **Yes**

---

### 6️⃣ Crea le Build

#### **Opzione A: Build per Android (consigliato per iniziare)**

```bash
eas build --platform android
```

Scegli:
- Select build profile: **production**

Tempo: ~10-15 minuti
Output: Riceverai un link per scaricare l'AAB (Android App Bundle)

#### **Opzione B: Build per iOS**

```bash
eas build --platform ios
```

Scegli:
- Select build profile: **production**

Tempo: ~15-20 minuti
Output: Riceverai un link per scaricare l'IPA

**Nota per iOS**: Ti verrà chiesto di configurare i certificati Apple. EAS può gestirli automaticamente se hai l'account Apple Developer attivo.

#### **Opzione C: Build per entrambi**

```bash
eas build --platform all
```

Questo creerà sia la build Android che iOS contemporaneamente.

---

## 📱 Dopo le Build

### 7️⃣ Scarica le Build

Una volta completata la build, EAS ti darà un link simile a:
```
✔ Build successful!
https://expo.dev/accounts/tuoaccount/projects/finance-tracker/builds/...
```

1. Clicca sul link
2. Scarica il file (AAB per Android, IPA per iOS)
3. Salva in una cartella sicura

---

### 8️⃣ Testa le Build

**Android:**
```bash
# Installa sul tuo dispositivo Android via USB
adb install percorso/al/file.apk
```

Oppure carica l'AAB su Play Store in "Internal Testing" per testarlo.

**iOS:**
- Usa TestFlight per distribuire ai tester
- Segui la guida: https://docs.expo.dev/submit/ios/

---

### 9️⃣ Carica sugli Store

#### **Google Play Store**

1. Vai su: https://play.google.com/console
2. Crea una nuova app
3. Segui la guida in `PUBLISHING_GUIDE.md` sezione 8️⃣

Oppure usa EAS Submit:
```bash
eas submit --platform android
```

#### **Apple App Store**

1. Vai su: https://appstoreconnect.apple.com
2. Crea una nuova app
3. Segui la guida in `PUBLISHING_GUIDE.md` sezione 8️⃣

Oppure usa EAS Submit:
```bash
eas submit --platform ios
```

---

## 🔄 Aggiornamenti Futuri

Quando vuoi pubblicare un aggiornamento:

1. **Aggiorna il codice** dell'app
2. **Incrementa la versione** in `/app/frontend/app.json`:
   ```json
   {
     "version": "1.0.1",
     "ios": { "buildNumber": "2" },
     "android": { "versionCode": 2 }
   }
   ```
3. **Crea nuova build**:
   ```bash
   eas build --platform all
   ```
4. **Carica sugli store**

---

## 🎨 Materiali che ti Servono

Prima di pubblicare, prepara:

### Screenshot (4-6 immagini)
- Schermata login
- Dashboard con grafici
- Lista transazioni
- Gestione budget
- Obiettivi
- Consigli AI

Dimensioni consigliate:
- iOS: 1290 x 2796 px
- Android: 1080 x 1920 px

### Icona App
- 1024 x 1024 px (PNG, senza trasparenza)

### Privacy Policy
Crea un documento che spiega:
- Quali dati raccogli
- Come li usi
- Dove li salvi
- Come gli utenti possono eliminarli

Genera gratis su: https://www.privacypolicygenerator.info/

### Descrizioni
Vedi esempi in `PUBLISHING_GUIDE.md` sezione 6️⃣

---

## 📞 Supporto

**Problemi con i comandi?**
- Documentazione EAS: https://docs.expo.dev/build/introduction/
- Community Expo: https://forums.expo.dev/

**Problemi con gli store?**
- App Store: https://developer.apple.com/support/
- Play Store: https://support.google.com/googleplay/android-developer/

---

## ✅ Checklist Veloce

Prima di pubblicare, assicurati di aver fatto:

- [ ] Creato account Google Play Console
- [ ] Creato account Apple Developer
- [ ] Installato EAS CLI
- [ ] Fatto login a Expo
- [ ] Configurato EAS nel progetto
- [ ] Creato build Android e iOS
- [ ] Testato le build su dispositivi reali
- [ ] Preparato screenshot
- [ ] Creato Privacy Policy
- [ ] Scritto descrizioni
- [ ] Caricato sugli store
- [ ] Inviato per revisione

---

## 🎉 Prossimi Passi

1. **Oggi**: Crea gli account developer
2. **Domani**: Installa EAS e crea le build
3. **Dopodomani**: Prepara i materiali (screenshot, descrizioni)
4. **Tra 3 giorni**: Carica sugli store
5. **Tra 1 settimana**: La tua app è live! 🚀

---

**Note Importanti:**
- ⏰ Google Play: approvazione in 1-3 giorni
- ⏰ App Store: approvazione in 1-7 giorni (media 24-48 ore)
- 💰 Totale costi: $124 (Google $25 + Apple $99)
- 🔄 Apple Developer si rinnova ogni anno, Google è pagamento unico

**Hai bisogno di aiuto?** Torna qui e chiedi! Sono pronto ad assisterti in ogni fase del processo. 🤝
