# Configurazione Backend per AWS

Per connettere il backend a un database AWS (DocumentDB o Atlas), segui questi passaggi:

1. **Certificati SSL**: 
   Il file `rds-combined-ca-bundle.pem` è stato scaricato nella cartella `backend/`. Questo è necessario per le connessioni sicure a DocumentDB.

2. **Variabili d'Ambiente**:
   Crea un file `.env` nel backend con i seguenti valori, sostituendo i placeholder con i tuoi dati:

   ```bash
   # Connection String
   # Per Amazon DocumentDB:
   MONGO_URL=mongodb://<username>:<password>@<endpoint>:<port>/?tls=true&tlsCAFile=rds-combined-ca-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false
   
   # Per MongoDB Atlas:
   # MONGO_URL=mongodb+srv://<user>:<pass>@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority

   DB_NAME=financetracker
   ENVIRONMENT=production
   JWT_SECRET=<la_tua_chiave_segreta_sicura>
   ```

3. **Deploy**:
   Quando avvii il container Docker, assicurati che il file `.env` sia caricato o che queste variabili siano passate al container.
