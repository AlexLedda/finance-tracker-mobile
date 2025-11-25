# 📱 Guida alla Pubblicazione - Finance Tracker

## ✅ Configurazione Completata

L'app è stata configurata con:
- **Nome**: Finance Tracker
- **Bundle ID iOS**: com.financetracker.app
- **Package Android**: com.financetracker.app
- **Versione**: 1.0.0
- **Descrizione**: L'app che ti permette di tenere sotto controllo le finanze e di avere suggerimenti su come risparmiare tramite AI

---

## 📋 Prossimi Passi

### 1️⃣ Crea gli Account Developer

#### **Google Play Console** (Android)
1. Vai su: https://play.google.com/console/signup
2. Paga la quota una tantum: **$25**
3. Completa la verifica dell'identità
4. Tempo di attivazione: ~24-48 ore

#### **Apple Developer Program** (iOS)
1. Vai su: https://developer.apple.com/programs/
2. Iscriviti al programma: **$99/anno**
3. Completa la verifica (serve ID e carta)
4. Tempo di attivazione: ~24-48 ore

---

### 2️⃣ Installa EAS CLI (Expo Application Services)

Una volta creati gli account, installa EAS CLI sul tuo computer:

```bash
npm install -g eas-cli
```

Oppure se usi Yarn:
```bash
yarn global add eas-cli
```

---

### 3️⃣ Configura EAS nel Progetto

Naviga nella cartella del progetto frontend e configura EAS:

```bash
cd /app/frontend
eas login
```

Inserisci le credenziali del tuo account Expo.

Poi configura il progetto:
```bash
eas build:configure
```

Questo creerà un file `eas.json` con la configurazione delle build.

---

### 4️⃣ Crea le Build

#### **Build per Android (APK/AAB)**

Per creare una build Android:
```bash
eas build --platform android
```

Scegli:
- Build type: **production**
- Format: **AAB** (Android App Bundle - consigliato per Play Store)

EAS creerà la build sui loro server cloud e ti darà un link per scaricarla.

#### **Build per iOS (IPA)**

Per creare una build iOS:
```bash
eas build --platform ios
```

Scegli:
- Build type: **production**

**Nota**: Per iOS dovrai configurare i certificati. EAS può gestirli automaticamente per te.

#### **Build per entrambi**
```bash
eas build --platform all
```

---

### 5️⃣ Test delle Build

Prima di pubblicare, testa le build standalone:

**Android:**
- Scarica l'APK da EAS
- Installa sul tuo telefono Android
- Testa tutte le funzionalità

**iOS:**
- Usa TestFlight per distribuire ai tester
- Oppure installa direttamente su dispositivo registrato

---

### 6️⃣ Prepara i Materiali per gli Store

#### **Screenshot Richiesti**

**iOS (App Store):**
- iPhone 6.7" (iPhone 15 Pro Max): 1290 x 2796 px
- iPhone 6.5" (iPhone 14 Pro Max): 1284 x 2778 px
- iPhone 5.5" (iPhone 8 Plus): 1242 x 2208 px
- iPad Pro 12.9": 2048 x 2732 px

**Android (Play Store):**
- Phone: 1080 x 1920 px (minimo)
- 7" Tablet: 1024 x 1768 px
- 10" Tablet: 1536 x 2048 px

**Quanti screenshot:**
- Minimo: 2 screenshot
- Massimo: 8 screenshot
- Consigliato: 4-6 screenshot delle funzionalità principali

#### **Icone**

- **iOS**: 1024 x 1024 px (senza trasparenza, formato PNG)
- **Android**: 512 x 512 px (può avere trasparenza)

#### **Descrizioni**

**Descrizione Breve** (max 80 caratteri):
```
Gestisci le tue finanze con AI - Budget, Obiettivi e Consigli
```

**Descrizione Completa** (esempio):
```
Finance Tracker è l'app definitiva per gestire le tue finanze personali con l'aiuto dell'intelligenza artificiale.

🎯 FUNZIONALITÀ PRINCIPALI:
• 💰 Tracciamento Transazioni - Registra entrate e uscite con facilità
• 📊 Dashboard Visuale - Grafici intuitivi per capire le tue spese
• 💼 Gestione Budget - Imposta limiti di spesa per categoria
• 🏆 Obiettivi di Risparmio - Definisci e raggiungi i tuoi traguardi
• 🤖 Consigli AI Personalizzati - Suggerimenti intelligenti per risparmiare
• 📈 Statistiche Dettagliate - Analisi complete delle tue finanze
• 🔒 Sicuro e Privato - I tuoi dati sono protetti

💡 CONSIGLI AI
L'intelligenza artificiale analizza le tue abitudini di spesa e ti fornisce consigli personalizzati per ottimizzare il tuo budget e raggiungere i tuoi obiettivi finanziari.

📱 SINCRONIZZAZIONE
Accedi da web e mobile - i tuoi dati sono sempre sincronizzati.

Inizia oggi a prendere il controllo delle tue finanze!
```

#### **Categorie**

**App Store (iOS):**
- Categoria primaria: Finance
- Categoria secondaria: Productivity

**Play Store (Android):**
- Categoria: Finance
- Tag: finanza personale, budget, risparmio, AI, contabilità

#### **Parole Chiave** (iOS, max 100 caratteri):
```
finanze,budget,risparmio,AI,transazioni,contabilità,spese,obiettivi,soldi
```

---

### 7️⃣ Privacy Policy (OBBLIGATORIA)

Devi creare una Privacy Policy. Ecco un template base:

**URL Privacy Policy**: Puoi crearla con:
- https://www.privacypolicygenerator.info/
- https://www.freeprivacypolicy.com/
- Oppure ospitarla sul tuo sito

**Punti da includere:**
- Quali dati raccogli (email, transazioni finanziarie)
- Come usi i dati (statistiche, consigli AI)
- Dove vengono salvati (MongoDB, server sicuri)
- Se condividi dati con terze parti (OpenAI per AI)
- Come gli utenti possono eliminare i dati
- Contatti per domande sulla privacy

---

### 8️⃣ Carica sugli Store

#### **Google Play Store**

1. Vai su: https://play.google.com/console
2. Clicca "Crea app"
3. Inserisci:
   - Nome: Finance Tracker
   - Lingua predefinita: Italiano
   - Tipo: App
   - Gratuita/a pagamento: Gratuita
4. Compila le sezioni:
   - **Scheda dello store** (descrizioni, screenshot, icona)
   - **Classificazione contenuti** (compila questionario)
   - **Prezzi e distribuzione** (seleziona paesi)
   - **Sicurezza dei dati** (dichiara dati raccolti)
   - **Privacy Policy** (inserisci URL)
5. Nella sezione **Produzione**:
   - Carica l'AAB scaricato da EAS
   - Compila le note di rilascio
6. Clicca **Invia per revisione**
7. Tempo di revisione: 1-3 giorni

#### **Apple App Store**

1. Vai su: https://appstoreconnect.apple.com
2. Clicca "My Apps" → "+" → "New App"
3. Inserisci:
   - Platform: iOS
   - Name: Finance Tracker
   - Primary Language: Italian
   - Bundle ID: com.financetracker.app
   - SKU: financetracker (identificativo unico)
4. Configura l'app:
   - **Pricing**: Gratuita
   - **Privacy Policy URL**: (il tuo URL)
   - **Category**: Finance
5. Nella sezione **1.0 Prepare for Submission**:
   - Carica screenshot per tutte le dimensioni
   - Inserisci descrizione e parole chiave
   - Carica icona 1024x1024
6. **Build**: Seleziona la build caricata da EAS
7. **Age Rating**: Compila questionario
8. **Review Information**: Inserisci email e note per i reviewer
9. Clicca **Submit for Review**
10. Tempo di revisione: 1-7 giorni (media 24-48 ore)

---

### 9️⃣ Aggiornamenti Futuri

Per pubblicare aggiornamenti:

1. Aggiorna il version number in `app.json`:
```json
{
  "version": "1.0.1",
  "ios": {
    "buildNumber": "2"
  },
  "android": {
    "versionCode": 2
  }
}
```

2. Crea nuova build:
```bash
eas build --platform all
```

3. Carica la nuova build sugli store con le note di rilascio

---

## 🎯 Checklist Completa

### Prima della Pubblicazione
- [ ] Account Google Play Console attivo
- [ ] Account Apple Developer attivo
- [ ] Privacy Policy creata e pubblicata online
- [ ] Screenshot preparati (4-6 per piattaforma)
- [ ] Icone app preparate (1024x1024 iOS, 512x512 Android)
- [ ] Descrizioni scritte (breve e completa)
- [ ] EAS CLI installato
- [ ] Build Android (AAB) creata e testata
- [ ] Build iOS (IPA) creata e testata
- [ ] Tutti i link e email di contatto verificati

### Durante la Pubblicazione
- [ ] Store listing completato su Google Play
- [ ] Store listing completato su App Store Connect
- [ ] Build caricate
- [ ] Classificazione contenuti completata
- [ ] Informazioni di sicurezza completate
- [ ] Submitted for review

### Dopo la Pubblicazione
- [ ] Monitora recensioni e feedback
- [ ] Rispondi alle recensioni degli utenti
- [ ] Prepara aggiornamenti basati sui feedback
- [ ] Monitora analytics e crash reports

---

## 💡 Suggerimenti

1. **Inizia con Android** - È più veloce da approvare (1-3 giorni vs 1-7 di iOS)
2. **Usa TestFlight** (iOS) per beta testing prima della release pubblica
3. **Prepara screenshot professionali** - Usa tool come Figma o Canva
4. **Scrivi descrizioni chiare** - Evidenzia i benefici, non solo le funzionalità
5. **Monitora le metriche** - Usa Google Play Console e App Store Connect analytics
6. **Rispondi alle recensioni** - Dimostra che ascolti gli utenti
7. **Aggiorna regolarmente** - Bug fix e nuove funzionalità ogni 2-4 settimane

---

## 🆘 Problemi Comuni

**Build fallita su EAS:**
- Verifica che tutte le dipendenze siano compatibili
- Controlla i log di build per errori specifici

**App rifiutata da Apple:**
- Motivo comune: Privacy Policy mancante o poco chiara
- Motivo comune: Screenshot non aggiornati
- Motivo comune: Descrizione ingannevole

**App rifiutata da Google:**
- Motivo comune: Classificazione contenuti errata
- Motivo comune: Privacy Policy non conforme al GDPR
- Motivo comune: Icona o screenshot di bassa qualità

---

## 📞 Link Utili

- **EAS Build**: https://docs.expo.dev/build/introduction/
- **App Store Guidelines**: https://developer.apple.com/app-store/review/guidelines/
- **Play Store Guidelines**: https://play.google.com/console/about/guides/
- **Privacy Policy Generator**: https://www.privacypolicygenerator.info/
- **Screenshot Generator**: https://www.screely.com/

---

## 🎉 Sei Pronto!

L'app è configurata e pronta per la pubblicazione. Una volta creati gli account developer:

1. Esegui `eas build --platform all` 
2. Scarica le build
3. Carica sugli store
4. Attendi l'approvazione
5. Congratulazioni, la tua app è live! 🚀

---

**Ultimo aggiornamento**: 25 Novembre 2025
**App Version**: 1.0.0
**Bundle ID**: com.financetracker.app
