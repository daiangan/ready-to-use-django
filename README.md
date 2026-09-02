# Ready-to-use Django

A compact Django starter for API-backed projects. It provides secure defaults,
environment-specific settings, a modern Unfold admin, OpenAPI documentation, optional
S3 media storage, and automated quality checks while keeping models and admin code in
their conventional app modules.

## Highlights

- Python 3.13+ and Django 6.1
- Django REST Framework with token authentication
- [Django Unfold](https://unfoldadmin.com/) admin interface
- OpenAPI 3 schema and locally hosted Swagger UI through drf-spectacular
- SQLite for zero-configuration local development
- PostgreSQL through `DATABASE_URL` in production
- WhiteNoise static files and optional S3 media storage
- Ruff, branch-aware coverage, Django deployment checks, and GitHub Actions
- Dependabot updates for Python packages and GitHub Actions

## Project layout

```text
.
├── api/                 API routes, views, models, and tests
├── django_project/      Root URL configuration and WSGI/ASGI entry points
├── settings/
│   ├── base.py          Settings shared by all environments
│   ├── dev.py           Local development settings
│   └── prod.py          Validated production settings
├── utils/               Shared models and built-in admin customization
├── .env.example         Documented environment variables
├── requirements.txt     Direct runtime dependencies
├── requirements-dev.txt Runtime plus development tools
└── requirements-lock.txt Fully resolved environment used by CI
```

## Quick start

Python dependencies belong in the project-local virtual environment. The `.venv`
directory is ignored by Git.

```bash
git clone https://github.com/daiangan/ready-to-use-django.git
cd ready-to-use-django
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-lock.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Development uses SQLite at `db.sqlite3`; no database service or `.env` file is
required. Copy `.env.example` to `.env` when you want to change the local defaults.

## Local URLs

| Feature | URL |
| --- | --- |
| Unfold admin | <http://127.0.0.1:8000/backadmin/> |
| API liveness check | <http://127.0.0.1:8000/api/v1/health/> |
| OpenAPI schema | <http://127.0.0.1:8000/api/v1/openapi/> |
| Swagger UI | <http://127.0.0.1:8000/api/v1/doc/> |

The API version is controlled by `API_VERSION` in `settings/base.py`.

## Configuration

`manage.py` defaults to `settings.dev`. The WSGI and ASGI entry points default to
`settings.prod`. Override either behavior by exporting `DJANGO_SETTINGS_MODULE` before
starting Django; it cannot be selected from `.env` because Django needs the module name
before loading a settings file.

### Common variables

| Variable | Development default | Purpose |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Insecure local-only value | Cryptographic signing key; required in production |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,[::1]` | Comma-separated accepted hostnames |
| `DATABASE_URL` | Local SQLite | Database connection URL; required in production |
| `DJANGO_CORS_ALLOWED_ORIGINS` | Empty | Comma-separated browser origins |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Empty | Comma-separated trusted CSRF origins |
| `DJANGO_API_PAGE_SIZE` | `20` | Default limit/offset page size |
| `DJANGO_LANGUAGE_CODE` | `en-us` | Default language |
| `DJANGO_TIME_ZONE` | `UTC` | Application time zone |
| `DJANGO_LOG_LEVEL` | `INFO` | Root console log level |

See `.env.example` for development, HTTPS, proxy, and optional AWS settings.

### API authentication

Token authentication and `IsAuthenticated` are global defaults. Public endpoints must
opt in explicitly with a permission class; the liveness endpoint is the included
example.

Create missing tokens for all existing users with:

```bash
python manage.py api_tests
```

Clients authenticate with this header:

```http
Authorization: Token your-token-value
```

## Models and admin conventions

Domain models stay in each app's `models.py`, and their admin configuration stays in
the matching `admin.py`. `utils.models.TimeStampedModel` provides the existing
`created` and `modified` convention for models that need timestamps.

Unfold requires project admin classes to inherit from its `ModelAdmin`:

```python
from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Example


@admin.register(Example)
class ExampleAdmin(ModelAdmin):
    list_display = (
        "name",
        "created",
        "modified",
    )
    search_fields = (
        "name",
    )
```

The built-in User, Group, and REST Framework Token admin screens are already
re-registered with Unfold-compatible classes in `utils/admin.py`.

## Production

Production refuses to start without these variables:

```text
DJANGO_SECRET_KEY
DJANGO_ALLOWED_HOSTS
DATABASE_URL
```

A PostgreSQL URL looks like:

```text
postgresql://user:password@database-host:5432/database-name
```

Prepare and start a conventional WSGI deployment with:

```bash
DJANGO_SETTINGS_MODULE=settings.prod python manage.py migrate
DJANGO_SETTINGS_MODULE=settings.prod python manage.py collectstatic --noinput
gunicorn django_project.wsgi:application
```

Static assets use WhiteNoise. When `AWS_STORAGE_BUCKET_NAME` is present, uploaded
media uses S3. Prefer your hosting platform's IAM role over long-lived AWS keys.

Set `DJANGO_TRUST_X_FORWARDED_PROTO=true` only when Django is behind a trusted reverse
proxy that strips client-supplied forwarding headers and writes
`X-Forwarded-Proto` itself.

Before launch, review HSTS values for the domain. Start with a short duration, verify
HTTPS everywhere, then increase `DJANGO_SECURE_HSTS_SECONDS`; enable preload only when
the domain and all subdomains satisfy preload requirements.

## Tests and quality checks

Run the local equivalent of CI:

```bash
ruff check .
python manage.py makemigrations --check --dry-run
coverage run manage.py test
coverage report
python manage.py spectacular --file schema.yml --validate
```

Validate production settings separately:

```bash
DJANGO_SETTINGS_MODULE=settings.prod \
DJANGO_SECRET_KEY=deployment-check-only-long-random-placeholder-1234567890 \
DJANGO_ALLOWED_HOSTS=example.com \
DATABASE_URL=sqlite:///deployment-check.sqlite3 \
DJANGO_SECURE_HSTS_PRELOAD=true \
python manage.py check --deploy
```

CI runs linting, migration checks, tests, coverage, OpenAPI validation, and deployment
checks on Python 3.13 and 3.14.

## Updating dependencies

Edit the direct pins in `requirements.txt` or development tools in
`requirements-dev.txt`, recreate `.venv`, run the complete check suite, and regenerate
`requirements-lock.txt` from the tested environment. Commit all related dependency
files together.

## Maintainer

Created and maintained by [Daian Gan](https://github.com/daiangan).
