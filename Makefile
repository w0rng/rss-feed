run_full:
	docker compose up -d

run_only_core:
	docker compose up -d web scheduler db
