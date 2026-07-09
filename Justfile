set dotenv-load

# List available commands
[private]
default:
  just help

# List available commands
help:
  just --justfile {{justfile()}} --list

# Prep module from https://github.com/hotosm/justfiles
prep *args:
    @curl -sS https://raw.githubusercontent.com/hotosm/justfiles/main/prep.just \
      -o {{justfile_directory()}}/tasks/prep.just;
    @just --justfile {{justfile_directory()}}/tasks/prep.just {{args}}

# Chart module from https://github.com/hotosm/justfiles
chart *args:
    @curl -sS https://raw.githubusercontent.com/hotosm/justfiles/main/chart.just \
      -o {{justfile_directory()}}/tasks/chart.just;
    @just --justfile {{justfile_directory()}}/tasks/chart.just --set chart_name "hot-website" {{args}}

# Refresh staging DB from prod CNPG (destroys and repopulates staging data, idempotent)
db-refresh-staging:
    #!/usr/bin/env bash
    set -euo pipefail

    # --- Confirm destructive action ---
    just _echo-red "WARNING: this will DROP the staging 'hotosm' database and replace it with a fresh dump from prod."
    read -r -p "Proceed? [y/N] " reply
    [[ "$reply" =~ ^(y|Y|yes|YES)$ ]] || { just _echo-yellow "Aborted."; exit 1; }

    # --- Locate prod primary pod ---
    prod_pod=$(kubectl get pod -n postgres \
      -l cnpg.io/cluster=hot-website-db,cnpg.io/instanceRole=primary \
      -o jsonpath='{.items[0].metadata.name}')

    # --- Drop & recreate staging DB (forces off any open connections) ---
    just _echo-yellow "==> Dropping and recreating staging DB..."
    kubectl exec -n staging-website hot-website-postgres-0 -- sh -c '
      PGPASSWORD="$POSTGRES_PASSWORD" psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d postgres \
        -c "DROP DATABASE IF EXISTS \"$POSTGRES_DB\" WITH (FORCE);" \
        -c "CREATE DATABASE \"$POSTGRES_DB\" OWNER \"$POSTGRES_USER\";"'

    # --- Stream pg_dump: prod -> staging ---
    just _echo-yellow "==> Streaming pg_dump postgres/${prod_pod} -> staging..."
    kubectl exec -n postgres "$prod_pod" -c postgres -- \
      pg_dump -U postgres --no-owner --no-privileges hotosm \
    | kubectl exec -i -n staging-website hot-website-postgres-0 -- \
      sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"'

    # --- Rewrite prod URLs in redirect table so staging testers don't hit prod ---
    just _echo-yellow "==> Rewriting wagtailredirects_redirect prod URLs -> staging..."
    kubectl exec -i -n staging-website hot-website-postgres-0 -- \
      sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"' <<'SQL'
    UPDATE wagtailredirects_redirect
    SET redirect_link = REPLACE(redirect_link, 'https://www.hotosm.org/', 'https://staging.website.hotosm.org/')
    WHERE redirect_link LIKE 'https://www.hotosm.org/%';
    SQL

    just _echo-blue "==> Staging DB refreshed from prod."

# Echo to terminal with blue colour
[no-cd]
_echo-blue text:
  #!/usr/bin/env sh
  printf "\033[0;34m%s\033[0m\n" "{{ text }}"

# Echo to terminal with yellow colour
[no-cd]
_echo-yellow text:
  #!/usr/bin/env sh
  printf "\033[0;33m%s\033[0m\n" "{{ text }}"

# Echo to terminal with red colour
[no-cd]
_echo-red text:
  #!/usr/bin/env sh
  printf "\033[0;41m%s\033[0m\n" "{{ text }}"
