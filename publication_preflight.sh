#!/usr/bin/env bash

echo "== Publication preflight — AuditorSecSuite_PRE =="

STOP=0

echo
echo "== 1) Comprobar repositorio Git =="
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "OK: dentro de repositorio Git"
else
  echo "ERROR: no se está dentro de un repositorio Git"
  STOP=1
fi

echo
echo "== 2) Comprobar working tree versionable =="
if [ "$STOP" = "0" ]; then
  PENDING="$(git status --short | grep -v "^!! .env" || true)"
  if [ -n "$PENDING" ]; then
    echo "ERROR: hay cambios pendientes versionables:"
    echo "$PENDING"
    STOP=1
  else
    echo "OK: sin cambios versionables pendientes"
  fi
fi

echo
echo "== 3) Comprobar ficheros sensibles básicos =="
if [ "$STOP" = "0" ]; then
  SENSITIVE_VERSIONED="$(git ls-files | grep -Ei "(^|/)(\.env|.*\.pem|.*\.key|id_rsa|id_ed25519|.*secret.*|.*password.*)$" || true)"
  if [ -n "$SENSITIVE_VERSIONED" ]; then
    echo "ERROR: posibles ficheros sensibles versionados:"
    echo "$SENSITIVE_VERSIONED"
    STOP=1
  else
    echo "OK: sin ficheros sensibles básicos versionados"
  fi
fi

echo
echo "== 4) Ejecutar security audit =="
if [ "$STOP" = "0" ]; then
  if [ -x "./Documentacio/scripts/security_audit.sh" ]; then
    ./Documentacio/scripts/security_audit.sh
    SECURITY_STATUS=$?
  else
    echo "ERROR: no existe ./Documentacio/scripts/security_audit.sh"
    SECURITY_STATUS=1
  fi

  if [ "$SECURITY_STATUS" != "0" ]; then
    STOP=1
  fi
fi

echo
echo "== 5) Ejecutar validadores de alineación =="
if [ "$STOP" = "0" ]; then
  if [ -x "./Documentacio/scripts/verify_documentation_alignment.sh" ]; then
    ./Documentacio/scripts/verify_documentation_alignment.sh
    DOC_STATUS=$?
  else
    echo "ERROR: no existe ./Documentacio/scripts/verify_documentation_alignment.sh"
    DOC_STATUS=1
  fi

  if [ -x "./Documentacio/scripts/verify_project_alignment.sh" ]; then
    ./Documentacio/scripts/verify_project_alignment.sh
    PROJECT_STATUS=$?
  else
    echo "ERROR: no existe ./Documentacio/scripts/verify_project_alignment.sh"
    PROJECT_STATUS=1
  fi

  if [ "$DOC_STATUS" != "0" ] || [ "$PROJECT_STATUS" != "0" ]; then
    STOP=1
  fi
fi

echo
echo "== 6) Comprobar diff whitespace =="
if [ "$STOP" = "0" ]; then
  git diff --check
  DIFF_STATUS=$?

  git diff --cached --check
  CACHED_DIFF_STATUS=$?

  if [ "$DIFF_STATUS" != "0" ] || [ "$CACHED_DIFF_STATUS" != "0" ]; then
    STOP=1
  fi
fi

echo
echo "== 7) Resultado =="
if [ "$STOP" = "0" ]; then
  echo "OK_PUBLICATION_PREFLIGHT=1"
else
  echo "STOP_PUBLICATION_PREFLIGHT=1"
fi

exit "$STOP"
