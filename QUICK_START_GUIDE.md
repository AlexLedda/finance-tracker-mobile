# 🚀 Guida Rapida - Collegamento finance-tracker-1316

## ✅ Cosa hai già

- ✅ **Backend completo** funzionante e testato (25/25 test passati)
- ✅ **App mobile** Expo già configurata e funzionante
- ✅ **Database MongoDB** condiviso
- ✅ **Consigli AI** con OpenAI GPT-4 già integrato

## 🔗 URL Backend Condiviso

```
https://fintrack-mobile-8.preview.emergentagent.com/api
```

## 📋 Checklist Rapida per finance-tracker-1316

### 1️⃣ **Modifica 1 File: Configurazione API**

Nel tuo progetto `finance-tracker-1316`, trova il file dove configuri l'API (probabilmente `api.js`, `config.js`, o simile) e cambia:

```javascript
// PRIMA
const API_URL = 'http://localhost:8001/api';

// DOPO
const API_URL = 'https://fintrack-mobile-8.preview.emergentagent.com/api';
```

### 2️⃣ **Verifica Autenticazione con Token**

Assicurati che il tuo codice includa il token JWT in ogni richiesta:

```javascript
headers: {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}
```

### 3️⃣ **Testa**

1. Fai logout e login nella web app
2. Crea una transazione sulla web app
3. Apri l'app mobile → dovresti vedere la stessa transazione! 🎉

---

## 📚 Documentazione Completa

Ho creato 2 file completi per te:

### 1. **API_DOCUMENTATION.md** 
- Documentazione completa di tutti gli endpoint
- Esempi di request/response per ogni API
- Gestione errori
- Formato dei dati

### 2. **INTEGRATION_EXAMPLES.js**
- Codice React pronto all'uso
- Servizi per autenticazione, transazioni, budget, obiettivi, statistiche, consigli AI
- Componenti esempio completi
- Protected routes

---

## 🎯 Endpoint Principali (Sintesi)

### Autenticazione
```bash
POST /api/auth/register  # Registrazione
POST /api/auth/login     # Login
```

### Transazioni
```bash
GET    /api/transactions     # Lista
POST   /api/transactions     # Crea
DELETE /api/transactions/:id # Elimina
```

### Budget
```bash
GET    /api/budgets     # Lista
POST   /api/budgets     # Crea
PUT    /api/budgets/:id # Aggiorna
DELETE /api/budgets/:id # Elimina
```

### Obiettivi
```bash
GET    /api/goals                          # Lista
POST   /api/goals                          # Crea
PUT    /api/goals/:id/contribute?amount=X  # Contributo
DELETE /api/goals/:id                      # Elimina
```

### Altro
```bash
GET  /api/stats  # Statistiche complete
POST /api/advice # Consigli AI personalizzati
```

---

## 💡 Esempio Rapido

### Login
```javascript
const response = await fetch('https://fintrack-mobile-8.preview.emergentagent.com/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'test@example.com',
    password: 'password123'
  })
});

const { token, id, email, name } = await response.json();
localStorage.setItem('token', token);
```

### Ottieni Transazioni
```javascript
const response = await fetch('https://fintrack-mobile-8.preview.emergentagent.com/api/transactions', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});

const transactions = await response.json();
console.log(transactions); // Array di transazioni
```

### Crea Transazione
```javascript
const response = await fetch('https://fintrack-mobile-8.preview.emergentagent.com/api/transactions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    type: 'expense',
    amount: 50.00,
    category: 'Alimentari',
    description: 'Spesa settimanale',
    date: new Date().toISOString()
  })
});

const newTransaction = await response.json();
```

---

## 🎉 Risultato Finale

Dopo aver collegato la web app:

✅ **Utenti Condivisi**
- Registrazione su web → accesso da mobile
- Registrazione su mobile → accesso da web

✅ **Dati Sincronizzati**
- Transazioni create su mobile appaiono su web
- Budget creati su web appaiono su mobile
- Obiettivi aggiornati ovunque in tempo reale

✅ **Funzionalità Complete**
- Dashboard con statistiche in tempo reale
- Consigli AI personalizzati su entrambe le piattaforme
- Gestione completa di transazioni, budget e obiettivi

---

## 🔧 Troubleshooting

### Errore 401 (Unauthorized)
- Verifica che il token sia salvato correttamente
- Controlla che l'header `Authorization: Bearer {token}` sia incluso
- Il token potrebbe essere scaduto → rifai login

### Errore 404 (Not Found)
- Verifica l'URL: deve essere `https://fintrack-mobile-8.preview.emergentagent.com/api`
- Controlla che l'endpoint sia corretto (es: `/api/transactions` non `/transactions`)

### Errore CORS
- Il backend ha già CORS abilitato per tutte le origini
- Se persiste, controlla configurazione browser/firewall

### Dati non sincronizzati
- Assicurati di usare lo stesso account (email) su entrambe le app
- Controlla che le richieste vadano allo stesso backend URL
- Verifica che il token JWT sia valido

---

## 📞 Link Utili

- **Backend API**: https://fintrack-mobile-8.preview.emergentagent.com/api
- **Test Backend**: https://fintrack-mobile-8.preview.emergentagent.com/api/ → Dovrebbe ritornare `{"message":"FinanceTracker API is running"}`
- **Documentazione Completa**: Vedi `API_DOCUMENTATION.md`
- **Esempi di Codice**: Vedi `INTEGRATION_EXAMPLES.js`

---

## 🎯 Prossimi Passi

1. **Ora**: Modifica l'URL API in finance-tracker-1316
2. **Poi**: Testa login e sincronizzazione dati
3. **Infine**: Verifica tutte le funzionalità (transazioni, budget, obiettivi, statistiche, consigli AI)

**Tempo stimato per integrazione**: 15-30 minuti 🚀

---

**Creato**: 22 Maggio 2025
**Backend Status**: ✅ Operativo e Testato
**Database**: ✅ MongoDB Condiviso
**AI**: ✅ OpenAI GPT-4 Integrato
