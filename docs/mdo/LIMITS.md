# MDO E02-F01 — Límites

## Incluido (por fases)

Ver ADR-006 (core) y ADR-007 (Perception→MDO).

E03-F01 agrega dual-write Perception → Building/Level/Space/Element vía MdoService.
Process.items permanece la salida legacy.

## Excluido

Perception/`motor_ia` rewrite, geometry engine, materials, costs, IA chat, marketplace, ChangeSet/Branch/Merge, Scenario, outbox E04, flag `MDO_V1`, reescribir Identity, usar Process como SoT definitivo.

## Independencia (decisión 7)

Ningún módulo en `backend/mdo/` puede importar:

- `motor_ia`, `presupuesto_pdf`, `billing_mp`, `email_service`
- paquetes de frontend
- adapters de vendor de otros dominios salvo SQLAlchemy/Pydantic/Alembic/stdlib

`main.py` puede importar MDO (composition root). MDO **no** importa `main` ni `motor_ia`.

## ParameterSet

Solo `data.params` y `data.metadata`.

## Element

`discipline_code` + `element_type` dotted — no enum monolítico.

## Discipline ≠ System instalaciones

Grafo System+Connection (RFC) diferido.
