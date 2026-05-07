# Django Helm Chart

A generic Django (plus Celery) Helm chart demonstration. Do not use directly in production.

Contributions may be accepted as merge requests. Be respectful of my time. I will not review if I do not have time. Fork the project instead. Please only open issues that you'd like to implement yourself or fund. Do not open support or feature requests. This chart is **not** intended to cover every use case with Django and Helm. It's a personal project that you are welcome to view and fork. Breaking changes to your workflow may happen at any time and without warning.

# Preparing your Django app

This chart supports a web plus optional celery and beat deployments. Be prepared to extend it as necessary.

Django settings will be managed by environment variables. `django-environ` works well for this and can parse the DATABASE_URL connection string. This chart expects SECRET_KEY and DATABASE_URL variables.

Kubernetes works best when it is able to determine application health. Your Django app should have a `/_health/` view such as

```
def health(request):
    return HttpResponse("ok", content_type="text/plain")

urlpatterns = [
    path("_health/", health),
...
```

Set the value web.livenessProbe.path and web.readinessProbe.path to change the URL.

## Run commands

This helm chart will set a "role" environment variable to web, worker, or beat. Your Docker image could read this variable and run the correct command.

Alternatively, set the service.args. For example:

```
web:
  args:
    - run_it
```

Remember that Kubernetes "args" are Docker's CMD (or command). Pretty confusing!

# Usage

Use only for demonstration purposes. Fork the repo for production.

1. Add our Helm chart repo `helm repo add django https://gitlab.com/api/v4/projects/26807467/packages/helm/stable`
2. Review our values.yaml. At a minimum you'll need to set env.secret.SECRET_KEY and env.secret.DATABASE_URL.
3. Install the chart `helm install your-app django/django -f your-values.yml`

# Tips

- Use [helm diff](https://github.com/databus23/helm-diff). One typo will wipe your app without warning otherwise.
- Stateful services like PostgreSQL in kubernetes are only partially supported. There is no clean way to run major upgrades. I don't recommend using them.
- Fork instead of using this directly.

## Managing environment variables and secrets

I suggest either

- Keep them in a values.yml file in a private repo
- Make use of --reuse-values and --set
- Keep them in a non helm chart managed service
- Use the opentofu helm provider, with a secure state backend or encrypted state.

## Deploying in CI

I use `alpine/helm` with Gitlab CI. [Example](https://gitlab.com/glitchtip/glitchtip-frontend/-/blob/master/.gitlab-ci.yml).

# Support development

Maintaining this chart takes time. Considering supporting it by

- [Donating on liberapay](https://liberapay.com/burke-software/)
- Check out [GlitchTip](https://glitchtip.com) error tracking, which is where this project started

Commercial support is available - email info@burkesoftware.com

If you want the scope of this project to include more, such as better merge request review or stable releases. You should consider forking it, talk to me about being a maintainer, or fund it.
