# HOT Website Helm Chart

## Secrets

By default, the chart loads environment variables from an existing Kubernetes
Secret named `hot-website-secret-env`.

You can override the name with:

```yaml
existingSecret: my-secret-name
```

The Secret is referenced with `envFrom`, so each Secret key becomes an
environment variable in the web Deployment and chart Jobs.

### Required keys

These keys should be present for a production deployment:

| Key | Purpose |
| --- | --- |
| `SECRET_KEY` | Django secret key. |
| `DATABASE_URL` | Database connection URL used by Django. |
| `AWS_STORAGE_BUCKET_NAME` | S3 bucket for uploaded media. |
| `AWS_ACCESS_KEY_ID` | AWS access key for S3 media storage. |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key for S3 media storage. |
| `MAPBOX_ACCESS_TOKEN` | Mapbox token used by map widgets. |

### Optional keys

| Key | Purpose |
| --- | --- |
| `AWS_S3_REGION_NAME` | S3 region. Defaults to `us-west-1` if omitted. |
| `SENTRY_DSN` | Enables Sentry error reporting. |
| `DEEPL_KEY` | Enables DeepL translation integration. |
| `DJANGO_SUPERUSER_USERNAME` | Required only when `superuserJob.enabled=true`. |
| `DJANGO_SUPERUSER_PASSWORD` | Required only when `superuserJob.enabled=true`. |
| `DJANGO_SUPERUSER_EMAIL` | Optional email for the bootstrap superuser. |

### Sealed Secret Example

Create a Secret with the runtime values the website needs, then seal it for the
target cluster and namespace:

```bash
kubectl create secret generic hot-website-secret-env \
    --namespace='website' \
    --from-literal=SECRET_KEY='replace-with-a-long-random-django-secret-key' \
    --from-literal=DATABASE_URL='postgres://hotosm:password@hot-website-db-rw.postgres.svc.cluster.local:5432/hotosm' \
    --from-literal=AWS_STORAGE_BUCKET_NAME='hot-website-media' \
    --from-literal=AWS_ACCESS_KEY_ID='replace-with-aws-access-key-id' \
    --from-literal=AWS_SECRET_ACCESS_KEY='replace-with-aws-secret-access-key' \
    --from-literal=AWS_S3_REGION_NAME='us-west-1' \
    --from-literal=MAPBOX_ACCESS_TOKEN='replace-with-mapbox-token' \
    --from-literal=SENTRY_DSN='https://examplePublicKey@o0.ingest.sentry.io/0' \
    --from-literal=DEEPL_KEY='replace-with-deepl-key' \
    --dry-run=client \
    -o yaml > secret.yaml

kubeseal -f secret.yaml -w sealed-secret.yaml
```

## Non-Secret Environment Variables

Non-secret runtime values should be set through `values.yaml` under `env`, not
in the Kubernetes Secret.

Common values:

| Key | Purpose |
| --- | --- |
| `DJANGO_SETTINGS_MODULE` | Django settings module. Defaults to `hot_osm.settings.production` in this chart. |
| `ALLOWED_HOSTS` | Comma-separated Django allowed hosts. |
| `GUNICORN_TIMEOUT` | Overrides Gunicorn timeout. Defaults to `30`. |
| `GUNICORN_WORKERS` | Overrides Gunicorn worker count. Defaults to `5`. |
| `GUNICORN_WORKER_CLASS` | Overrides Gunicorn worker class. Defaults to `sync`. |

`GUNICORN_BIND` is set by the chart from `web.port`.
