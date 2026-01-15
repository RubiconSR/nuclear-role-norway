#!/bin/bash
# Overvåker IC_SMR3 og IC_SMR6 og kjører analyser når de er ferdige

cd "/Users/siva/projects/Kjernekraft Prosjekt/NordicNuclearAnalysis"
export PYTHONPATH="$PWD"
export PATH="/Library/Frameworks/Python.framework/Versions/3.12/bin:$PATH"

LOG="/Users/siva/projects/Kjernekraft Prosjekt/NordicNuclearAnalysis/logs/monitor.txt"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG"
}

log "Starter overvåkning av IC_SMR3 og IC_SMR6..."

# Vent til begge simuleringer er ferdige (sjekk om prosesser kjører)
while true; do
    SMR3_RUNNING=$(pgrep -f "CASE_2050_IC/scenario_SMR3/SMR3.py" 2>/dev/null)
    SMR6_RUNNING=$(pgrep -f "CASE_2050_IC/scenario_SMR6/SMR6.py" 2>/dev/null)

    if [ -z "$SMR3_RUNNING" ] && [ -z "$SMR6_RUNNING" ]; then
        log "Begge simuleringer er ferdige!"
        break
    fi

    # Vis framdrift
    SMR3_PROG=$(tail -1 logs/IC_SMR3_log.txt 2>/dev/null | grep -o '[0-9]*/262992' | tail -1)
    SMR6_PROG=$(tail -1 logs/IC_SMR6_log.txt 2>/dev/null | grep -o '[0-9]*/262992' | tail -1)
    log "Framdrift - IC_SMR3: $SMR3_PROG, IC_SMR6: $SMR6_PROG"

    sleep 300  # Sjekk hvert 5. minutt
done

# Sjekk at databasene er fullstendige
SMR3_COUNT=$(sqlite3 "CASE_2050_IC/scenario_SMR3/powergama_SMR3_v1_1991_2020.sqlite" "SELECT COUNT(*) FROM Res_ObjFunc;" 2>/dev/null)
SMR6_COUNT=$(sqlite3 "CASE_2050_IC/scenario_SMR6/powergama_SMR6_v1_1991_2020.sqlite" "SELECT COUNT(*) FROM Res_ObjFunc;" 2>/dev/null)

log "Database rader - IC_SMR3: $SMR3_COUNT, IC_SMR6: $SMR6_COUNT (forventet: 262992)"

# Kjør analyser hvis databasene er (nesten) fullstendige
if [ "$SMR3_COUNT" -ge 260000 ] 2>/dev/null; then
    log "Kjører analyse for IC_SMR3..."
    python3 CASE_2050_IC/scenario_SMR3/SMR3_db_simple.py > logs/IC_SMR3_analysis.txt 2>&1
    log "IC_SMR3 analyse ferdig!"
fi

if [ "$SMR6_COUNT" -ge 260000 ] 2>/dev/null; then
    log "Kjører analyse for IC_SMR6..."
    python3 CASE_2050_IC/scenario_SMR6/SMR6_db_simple.py > logs/IC_SMR6_analysis.txt 2>&1
    log "IC_SMR6 analyse ferdig!"
fi

log "=== Overvåkning og analyser ferdige! ==="
