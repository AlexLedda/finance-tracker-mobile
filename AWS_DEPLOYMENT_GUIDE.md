# Guida al Deployment su AWS

Questa guida ti accompagna nei passaggi necessari per configurare l'infrastruttura AWS per `finance-tracker-mobile`.

## 1. Database (Amazon DocumentDB)
Poiché l'app usa MongoDB, su AWS il servizio gestito compatibile è **Amazon DocumentDB**.

1.  Vai sulla **Console AWS** > **Amazon DocumentDB**.
2.  Clicca su **Create cluster**.
3.  **Configurazione**:
    *   **Cluster identifier**: es. `finance-tracker-db`.
    *   **Engine version**: Scegli l'ultima stabile (es. 5.0.0).
    *   **Instance class**: Per test/sviluppo, `db.t3.medium` è la più economica.
    *   **Number of instances**: 1 (per risparmiare) o 2 (per alta disponibilità).
4.  **Autenticazione**: Imposta username e password (es. `financeadmin` / `...password...`).
5.  **Advanced settings** (Importante):
    *   **Network**: Assicurati che sia nella stessa VPC dove metterai il backend.
    *   **Security Group**: Crea un nuovo Security Group (es. `docdb-sg`) che permetta traffico sulla porta `27017` dai server del backend.
6.  Una volta creato, annota l'**Endpoint** (es. `finance-tracker-db.cluster-xyz.eu-south-1.docdb.amazonaws.com`).

## 2. Backend (AWS App Runner o EC2)
Per semplicità, consigliamo **AWS App Runner** (gestito) o **EC2** con Docker.

### Opzione A: AWS App Runner (Più semplice)
1.  Collega il tuo repository GitHub ad App Runner.
2.  Configura il deployment:
    *   **Runtime**: Python 3.
    *   **Build command**: `pip install -r backend/requirements.txt`.
    *   **Start command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port 8000`.
3.  **Environment Variables**: Aggiungi qui le variabili definite in `backend/AWS_CONFIG.md`:
    *   `MONGO_URL`: La stringa di connessione a DocumentDB.
    *   `JWT_SECRET`: La tua chiave segreta.
4.  **Networking**: App Runner deve avere accesso alla VPC di DocumentDB (VPC Connector) per connettersi al database privato.

### Opzione B: EC2 (Manuale/Docker)
1.  Lancia un'istanza **EC2** (es. `t3.micro` con Ubuntu).
2.  Assicurati che il **Security Group** dell'EC2 permetta traffico HTTP (80) e SSH (22).
3.  Connettiti in SSH e installa Docker:
    ```bash
    sudo apt update && sudo apt install docker.io docker-compose -y
    ```
4.  Clona il repository:
    ```bash
    git clone https://github.com/AlexLedda/finance-tracker-mobile.git
    cd finance-tracker-mobile
    ```
5.  Configura il file `.env` nel backend come spiegato in `backend/AWS_CONFIG.md`.
6.  Avvia con Docker Compose:
    ```bash
    docker-compose up -d --build
    ```

## 3. Sicurezza (Security Groups)
È fondamentale configurare le regole di rete:

*   **SG Backend (EC2/App Runner)**:
    *   Inbound: Porta 80/443 (HTTP/HTTPS) da `0.0.0.0/0` (Internet).
    *   Outbound: Tutto (per scaricare pacchetti e connettersi al DB).
*   **SG Database (DocumentDB)**:
    *   Inbound: Porta 27017 **SOLO** dal Security Group del Backend (`sg-backend`). **NON aprire 0.0.0.0/0**.

## 4. Verifica
Controlla i log del backend. Se vedi "Connection Successful", il deploy è andato a buon fine!
