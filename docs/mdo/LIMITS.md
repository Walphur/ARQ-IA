# MDO E02-F01 — Límites

## Incluido (por fases)

Ver ADR-006. Solo estructura de datos core.

## Excluido

Perception/`motor_ia`, geometry, materials, costs, IA chat, marketplace, ChangeSet/Branch/Merge, Scenario, outbox E04, flag `MDO_V1`, reescribir Identity, usar Process como SoT.

## Independencia (decisión 7)

Ningún módulo en `backend/mdo/` puede importar:

- `motor_ia`, `presupuesto_pdf`, `billing_mp`, `email_service`
- paquetes de frontend
- adapters de vendor de otros dominios salvo SQLAlchemy/Pydantic/Alembic/stdlib

`main.py` puede importar MDO (composition root). MDO **no** importa `main`.

## ParameterSet

Solo `data.params` y `data.metadata`.

## Element

`discipline_code` + `element_type` dotted — no enum monolítico.

## Discipline ≠ System instalaciones

Grafo System+Connection (RFC) diferido.
