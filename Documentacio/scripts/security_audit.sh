#!/usr/bin/env bash
echo "== Security audit — AuditorSecSuite_PRE =="
STOP=0

echo
echo "== 1) Ficheros sensibles versionados/staged =="
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  BAD="$(
    {
      git ls-files 2>/dev/null
      git diff --cached --name-only 2>/dev/null
    } | sort -u \
      | grep -E '(^|/)(\.env|.*\.pem|.*\.key|.*\.p12|.*\.pfx|.*\.dump|.*\.sql|.*\.sqlite3|storage/|logs/|_doc_offline/|scripts/backups/)' \
      | grep -vE '(^|/)\.env\.example$' || true
  )"

  if [ -n "$BAD" ]; then
    echo "ERROR: ficheros sensibles detectados:"
    echo "$BAD"
    STOP=1
  else
    echo "OK: sin ficheros sensibles detectados"
  fi
else
  echo "OK: repo Git todavía no inicializado"
fi

echo
echo "== 2) .env ignorado =="
if [ -f ".env" ]; then
  if grep -q '^\.env$' .gitignore; then
    echo "OK: .env está en .gitignore"
  else
    echo "ERROR: .env existe pero no está ignorado"
    STOP=1
  fi
fi

echo
echo "== 3) .env.example permitido como plantilla =="
if [ -f ".env.example" ]; then
  if grep -Eq 'change-me|localhost|127\.0\.0\.1' .env.example; then
    echo "OK: .env.example parece plantilla"
  else
    echo "ERROR: .env.example no contiene placeholders esperados"
    STOP=1
  fi
else
  echo "AVISO: no existe .env.example"
fi

echo
echo "== 4) Resultado =="
if [ "$STOP" = "0" ]; then
  echo "OK_SECURITY_AUDIT=1"
else
  echo "STOP_SECURITY_AUDIT=1"
fi
