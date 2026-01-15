#!/bin/bash
# Kjører IC_SMR3 og IC_SMR6 simuleringer

cd "/Users/siva/projects/Kjernekraft Prosjekt/NordicNuclearAnalysis"
export PYTHONPATH="$PWD"
export PATH="/Library/Frameworks/Python.framework/Versions/3.12/bin:$PATH"

# Slett ufullstendige filer først
rm -f "CASE_2050_IC/scenario_SMR3/powergama_SMR3_v1_1991_2020.sqlite"
rm -f "CASE_2050_IC/scenario_SMR6/powergama_SMR6_v1_1991_2020.sqlite"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starter IC_SMR3 og IC_SMR6..."

# Kjør begge i bakgrunnen
python3 CASE_2050_IC/scenario_SMR3/SMR3.py > logs/IC_SMR3_log.txt 2>&1 &
PID1=$!
python3 CASE_2050_IC/scenario_SMR6/SMR6.py > logs/IC_SMR6_log.txt 2>&1 &
PID2=$!

echo "[$(date '+%Y-%m-%d %H:%M:%S')] PIDs: IC_SMR3=$PID1, IC_SMR6=$PID2"
echo "Venter på at begge skal fullføre..."

# Vent på begge
wait $PID1
EC1=$?
echo "[$(date '+%Y-%m-%d %H:%M:%S')] IC_SMR3 ferdig (exit code: $EC1)"

wait $PID2
EC2=$?
echo "[$(date '+%Y-%m-%d %H:%M:%S')] IC_SMR6 ferdig (exit code: $EC2)"

# Kjør analyser
if [ $EC1 -eq 0 ] && [ $EC2 -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starter analyser..."
    python3 CASE_2050_IC/scenario_SMR3/SMR3_db_simple.py > logs/IC_SMR3_analysis.txt 2>&1
    python3 CASE_2050_IC/scenario_SMR6/SMR6_db_simple.py > logs/IC_SMR6_analysis.txt 2>&1
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Analyser ferdige!"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Alt ferdig!"
