#!/usr/bin/env bash

echo "== Publication preflight — AuditorSecSuite_PRE =="
STOP=0

echo
echo "== 1) Working tree limpio =="
PENDING="$(git status --short)"
if [ -n "$PENDING" ]; then
  echo "ERROR: working tree no está limpio:"
  echo "$PENDING"
  STOP=1
else
  echo "OK: working tree limpio"
fi

echo
echo "== 2) Ficheros sensibles versionados =="
BAD="$(
  git ls-files \
    | grep -E '(^|/)(\.env|.*\.pem|.*\.key|.*\.p12|.*\.pfx|.*\.dump|.*\.sql|.*\.sqlite3|storage/|logs/|_doc_offline/|scripts/backups/)' \
    | grep -vE '(^|/)\.env\.example$' || true
)"
if [ -n "$BAD" ]; then
  echo "ERROR: ficheros sensibles versionados:"
  echo "$BAD"
  STOP=1
else
  echo "OK: sin ficheros sensibles versionados"
fi

echo
echo "== 3) Referencias internas reales en ficheros versionados =="
INTERNAL_HITS="$(
  git grep -n -E '192\.168\.1\.253|/SERVER/VM/AuditorSecSuite_PRE' -- . \
    ':!.git' ':!Documentacio/scripts/publication_preflight.sh' 2>/dev/null || true
)"
if [ -n "$INTERNAL_HITS" ]; then
  echo "ERROR: referencias internas reales detectadas:"
  echo "$INTERNAL_HITS"
  STOP=1
else
  echo "OK: sin IP/ruta interna real en ficheros versionados"
fi

echo
echo "== 4) gitleaks =="
if [ "$STOP" = "0" ]; then
  if command -v gitleaks >/dev/null 2>&1; then
    gitleaks detect --source . --redact --verbose
    GL_STATUS=$?
  else
    echo "gitleaks no instalado; usando Docker image zricethezav/gitleaks:latest"
    docker run --rm -v "$PWD:/repo:ro" zricethezav/gitleaks:latest detect --source=/repo --redact --verbose
    GL_STATUS=$?
  fi

  if [ "$GL_STATUS" = "0" ]; then
    echo "OK: gitleaks"
  else
    echo "ERROR: gitleaks detectó hallazgos o falló"
    STOP=1
  fi
fi

echo
echo "== 5) trufflehog =="
if [ "$STOP" = "0" ]; then
  if command -v trufflehog >/dev/null 2>&1; then
    trufflehog git "file://$PWD" --no-update --fail --only-verified
    TH_STATUS=$?
  else
    echo "trufflehog no instalado; usando Docker image trufflesecurity/trufflehog:latest"
    docker run --rm -v "$PWD:/repo:ro" trufflesecurity/trufflehog:latest git file:///repo --no-update --fail --only-verified
    TH_STATUS=$?
  fi

  if [ "$TH_STATUS" = "0" ]; then
    echo "OK: trufflehog"
  else
    echo "ERROR: trufflehog detectó hallazgos o falló"
    STOP=1
  fi
fi

echo
echo "== 6) Resultado =="
if [ "$STOP" = "0" ]; then
  echo "OK_PUBLICATION_PREFLIGHT=1"
else
  echo "STOP_PUBLICATION_PREFLIGHT=1"
fi
