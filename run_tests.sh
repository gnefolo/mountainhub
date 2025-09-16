#!/bin/bash

# Script per eseguire i test di MountainHub

# Colori per output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== MountainHub Test Runner ===${NC}"
echo "Esecuzione dei test automatizzati..."

# Crea directory tests se non esiste
mkdir -p tests

# Attiva l'ambiente virtuale
source venv/bin/activate

# Installa dipendenze di test se non presenti
pip install flask-testing pytest pytest-cov

# Esegui i test unitari
echo -e "\n${YELLOW}=== Esecuzione test unitari ===${NC}"
python -m pytest tests/test_api.py -v

# Esegui i test con coverage
echo -e "\n${YELLOW}=== Esecuzione test con coverage ===${NC}"
python -m pytest --cov=src tests/

# Esegui test di integrazione API
echo -e "\n${YELLOW}=== Test di integrazione API ===${NC}"
echo "Avvio del server Flask in background..."
python src/main.py > /dev/null 2>&1 &
SERVER_PID=$!

# Attendi che il server sia pronto
sleep 3

# Esegui test API con curl
echo "Test API GET /api/trails"
curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/trails
if [ $? -eq 0 ]; then
    echo -e " ${GREEN}OK${NC}"
else
    echo -e " ${RED}FALLITO${NC}"
fi

echo "Test API GET /api/equipment/categories"
curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/equipment/categories
if [ $? -eq 0 ]; then
    echo -e " ${GREEN}OK${NC}"
else
    echo -e " ${RED}FALLITO${NC}"
fi

echo "Test API POST /api/equipment/configure"
curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"activity_type":"hiking","season":"summer","skill_level":"beginner"}' http://localhost:5000/api/equipment/configure
if [ $? -eq 0 ]; then
    echo -e " ${GREEN}OK${NC}"
else
    echo -e " ${RED}FALLITO${NC}"
fi

# Termina il server Flask
echo "Terminazione del server Flask..."
kill $SERVER_PID

echo -e "\n${YELLOW}=== Test completati ===${NC}"

