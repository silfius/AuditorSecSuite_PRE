#!/usr/bin/env bash
echo "== Verify documentation alignment — AuditorSecSuite_PRE =="
STOP=0
for F in ESTADO_ACTUAL ROADMAP ARQUITECTURA TESTING INSTRUCCIONES_PROYECTO MANUAL_USUARIO_VIVO OPERACION CHECKLIST_CIERRE DECISIONES_Y_ERRORES CHANGELOG SECURITY SOLICITUDES_USUARIO INDICE_TECNICO PLANTEJAMENT_FUNCIONAL_BASE CONSUMO_TOKENS; do
  if [ -f "Documentacio/docs/$F.md" ]; then
    echo "OK: $F.md"
  else
    echo "ERROR: falta $F.md"
    STOP=1
  fi
done
if [ -f "Documentacio/specs/SPEC_000_BASE_PROYECTO.md" ]; then
  echo "OK: SPEC_000_BASE_PROYECTO.md"
else
  echo "ERROR: falta SPEC_000_BASE_PROYECTO.md"
  STOP=1
fi
if [ "$STOP" = "0" ]; then
  echo "OK_DOCUMENTATION_ALIGNMENT=1"
else
  echo "STOP_DOCUMENTATION_ALIGNMENT=1"
fi
