#!/bin/bash
# Automatisk batch-kjøring av alle simuleringer
# Kjører 2 parallelle om gangen for å unngå GLPK-konflikter

cd "/Users/siva/projects/Kjernekraft Prosjekt/NordicNuclearAnalysis"
export PYTHONPATH="$PWD"

log() {
    echo "[$(date '+%H:%M:%S')] $1"
}

wait_for_completion() {
    local pids=("$@")
    for pid in "${pids[@]}"; do
        wait $pid
    done
}

# === BATCH 1: MD_BL + MD_SMR1 ===
log "BATCH 1: MD_BL + MD_SMR1 kjører allerede..."
# Vent på eksisterende prosesser
while pgrep -f "CASE_2050_MD/scenario_BL/BL.py" > /dev/null || pgrep -f "CASE_2050_MD/scenario_SMR1/SMR1.py" > /dev/null; do
    sleep 60
done
log "BATCH 1 FERDIG!"

# === BATCH 2: MD_SMR3 + MD_SMR6 ===
log "Starter BATCH 2: MD_SMR3 + MD_SMR6"
python3 CASE_2050_MD/scenario_SMR3/SMR3.py > logs/SMR3_log.txt 2>&1 &
pid1=$!
python3 CASE_2050_MD/scenario_SMR6/SMR6.py > logs/SMR6_log.txt 2>&1 &
pid2=$!
log "PIDs: $pid1, $pid2"
wait_for_completion $pid1 $pid2
log "BATCH 2 FERDIG!"

# === BATCH 3: IC_BL + IC_SMR1 ===
log "Starter BATCH 3: IC_BL + IC_SMR1"
python3 CASE_2050_IC/scenario_BL/BL.py > logs/IC_BL_log.txt 2>&1 &
pid1=$!
python3 CASE_2050_IC/scenario_SMR1/SMR1.py > logs/IC_SMR1_log.txt 2>&1 &
pid2=$!
log "PIDs: $pid1, $pid2"
wait_for_completion $pid1 $pid2
log "BATCH 3 FERDIG!"

# === BATCH 4: IC_SMR3 + IC_SMR6 ===
log "Starter BATCH 4: IC_SMR3 + IC_SMR6"
python3 CASE_2050_IC/scenario_SMR3/SMR3.py > logs/IC_SMR3_log.txt 2>&1 &
pid1=$!
python3 CASE_2050_IC/scenario_SMR6/SMR6.py > logs/IC_SMR6_log.txt 2>&1 &
pid2=$!
log "PIDs: $pid1, $pid2"
wait_for_completion $pid1 $pid2
log "BATCH 4 FERDIG!"

# === KJØR ANALYSER ===
log "Starter analyser..."
for case in MD IC; do
    for scenario in BL SMR1 SMR3 SMR6; do
        log "Analyse: CASE_2050_${case}/scenario_${scenario}"
        python3 CASE_2050_${case}/scenario_${scenario}/${scenario}_db_simple.py > logs/${case}_${scenario}_analysis.txt 2>&1
    done
done

log "=== ALLE SIMULERINGER OG ANALYSER FERDIGE! ==="
