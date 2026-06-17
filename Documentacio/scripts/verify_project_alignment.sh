#!/usr/bin/env bash
echo "== Verify project alignment — AuditorSecSuite_PRE =="
STOP=0
for F in compose.yaml Dockerfile requirements.txt app/manage.py app/core/version.py .gitignore .env.example; do
  if [ -f "$F" ]; then
    echo "OK: $F"
  else
    echo "ERROR: falta $F"
    STOP=1
  fi
done
grep -q "name: auditorsecsuite_pre" compose.yaml && echo "OK: compose project" || { echo "ERROR: compose project"; STOP=1; }
grep -q "APPLICATION_VERSION" app/core/version.py && echo "OK: versión explícita" || { echo "ERROR: versión explícita"; STOP=1; }
if [ "$STOP" = "0" ]; then
  echo "OK_PROJECT_ALIGNMENT=1"
else
  echo "STOP_PROJECT_ALIGNMENT=1"
fi
