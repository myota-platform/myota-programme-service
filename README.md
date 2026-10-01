# MyOTA programme service

MyOTA is a programme-agnostic platform for outdoor activation programmes. MPOTA is represented as a configured programme, not as the platform itself. No rules or charter text are copied from POTA or any other programme: every programme supplies its own configuration, policy, eligibility, awards and public charter.

This repository owns programme configuration and shared entity-category master
data. It publishes programme-owned policy inputs, themes, content, locales,
jurisdictions, assignments, and optional OIDC mappings for the other services
to consume. Awards and activity execution belong to myota-activity-service;
entities and imports belong to myota-geodata-service.

## What works now

- Identity, geodata, activity, and public/admin web capabilities are separate
  repositories; this service exposes their programme policy inputs.
- Programme configuration: shared entity category assignments, programme-owned rules, minimum QSOs, awards, theme and optional OIDC settings.
- Shared category master data with stable codes, geometry kinds, descriptions, active/inactive lifecycle, reusable across programmes, and explicit assignment APIs for administration.
- Geodata lifecycle: imported candidate → community proposal → approver review → approved entity.
- Provenance-aware imports with adapter metadata for ParkServe, OSM, government GIS and manual proposals.
- The current slice provides category master data and assignments, programme
  rules/themes/content/OIDC fields, and configuration-gap tracking.

Phase 1 adds `PATCH /v1/programmes/{slug}`, idempotent `PUT`/`DELETE` category
membership resources, and `PATCH` resources for programme content and policy
draft lifecycle transitions. Legacy action routes remain available as
deprecated aliases; see the [Phase 1 API resource update record](https://github.com/myota-platform/myota-docs/blob/main/docs/api-phase1-resource-updates.md).

## Configuration gap baseline

The service currently exposes the vertical-slice primitives, but programme
configuration is not yet a complete governance and policy control plane. In
particular, the editor still needs programme lifecycle/version publication,
owner and legal metadata, locale/default/fallback management, jurisdiction and
approver-scope configuration, schema-driven activation/QSO/geodata/privacy
policy forms, OIDC administration, notification/public-output defaults, and a
policy simulator with historical snapshots.

The authoritative list, ownership boundaries, priorities, and non-goals are
maintained in
[`myota-docs/docs/programme-configuration-gap-analysis.md`](https://github.com/myota-platform/myota-docs/blob/main/docs/programme-configuration-gap-analysis.md).
The `oidc` and `locales` fields already exist in the bootstrap data model, but
their complete administration workflow is still pending. Generic policy JSON
drafts are compatibility scaffolding until the programme-owned schemas are
implemented.

The default test/runtime adapter is in-memory so the slice can be exercised without third-party Python packages. PostgreSQL/PostGIS is the production storage target and is defined in `db/migrations/`.

The durable runtime exposes programme, catalogue and category-assignment
aggregates at `/metrics`; collection and distributed request telemetry are
provided through the OpenTelemetry deployment boundary.

## Run the vertical slice

```bash
python3 -m unittest discover -s tests -v
python3 services/dev_server.py
```

Open <http://127.0.0.1:8080>. The dev server starts the four services on ports 8001–8004 and proxies the browser API calls. It is intentionally dependency-free.

For a containerized PostGIS environment, use `docker compose up --build` after starting Colima. The image uses the same service code with `SERVICE=identity|programmes|geodata|activity`.

## Architecture

Read the [project charter](https://github.com/myota-platform/myota-docs/blob/main/docs/project-charter.md)
and [repository map](https://github.com/myota-platform/myota-docs/blob/main/docs/repository-map.md).
The [programme configuration gap analysis](https://github.com/myota-platform/myota-docs/blob/main/docs/programme-configuration-gap-analysis.md)
is the authoritative backlog for this service and its admin UI.

## Source project

The original `ea7klk/mpota` repository remains untouched. Its charter and planned flows are treated as the migration source; see [`docs/migration-from-mpota.md`](docs/migration-from-mpota.md).
