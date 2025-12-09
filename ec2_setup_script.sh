#!/bin/bash

# Script di Setup Automatico per Finance Tracker su EC2
# IP Istanza: 54.163.221.234
# Database: finance-tracker-db.cluster-cs5iqekgmbdh.us-east-1.docdb.amazonaws.com

echo "🚀 Inizio configurazione server..."

# 1. Aggiornamento sistema e installazione Docker
echo "📦 Installazione Docker..."
sudo apt-get update
sudo apt-get install -y docker.io docker-compose git

# Avvia Docker e abilita all'avvio
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# 2. Configurazione SWAP (2GB) per evitare OOM su t2.micro durante build
if [ ! -f /swapfile ]; then
    echo "📦 Configurazione Swap (2GB)..."
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "✅ Swap configurato."
else
    echo "ℹ️ Swap già presente."
fi

# 3. Clone/Update Repository
echo "📥 Clonazione repository..."
if [ -d "finance-tracker-mobile" ]; then
    echo "Cartella esistente, aggiorno..."
    cd finance-tracker-mobile
    git pull origin main
else
    git clone https://github.com/AlexLedda/finance-tracker-mobile.git
    cd finance-tracker-mobile
fi

# 3. Configurazione Certificato AWS
echo "🔒 Configurazione SSL..."
cd backend
# Scarica il certificato se non esiste
if [ ! -f "rds-combined-ca-bundle.pem" ]; then
    curl -o rds-combined-ca-bundle.pem https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem
fi

# 4. Configurazione Variabili d'Ambiente (.env)
echo "📝 Creazione file .env..."

# Chiedi le credenziali del DB (non hardcoded per sicurezza)
read -p "Inserisci Username DocumentDB: " DB_USER
read -s -p "Inserisci Password DocumentDB: " DB_PASS
echo ""
read -s -p "Inserisci JWT Secret (o premi invio per generarlo): " JWT_SECRET
echo ""

if [ -z "$JWT_SECRET" ]; then
    JWT_SECRET=$(openssl rand -hex 32)
    echo "Chiave generata: $JWT_SECRET"
fi

# Scrivi il file .env nella root (dove c'è docker-compose.yaml)
cd ..
cat > .env <<EOL
MONGO_URL=mongodb://$DB_USER:$DB_PASS@$DOCDB_ENDPOINT:27017/?tls=true&tlsCAFile=rds-combined-ca-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false
DB_NAME=financetracker
ENVIRONMENT=production
AWS_CA_BUNDLE_PATH=rds-combined-ca-bundle.pem
JWT_SECRET=$JWT_SECRET
EOL

# 5. Avvio con Docker Compose
echo "🚀 Avvio Backend..."
# Siamo già nella root
# Modifica docker-compose per usare il Dockerfile corretto se necessario o build
sudo docker-compose up -d --build

echo "✅ Deployment completato!"
echo "Il backend dovrebbe essere attivo su http://54.163.221.234:8000"
