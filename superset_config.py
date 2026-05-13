# superset_config.py
import os

# -------------------------
# Database (SQLAlchemy)
# -------------------------
# Preferir a URI explícita definida no ambiente (SUPERSET_DATABASE_URI).
# Caso não exista, montar a partir das variáveis individuais.
POSTGRES_USER = os.environ.get("SUPERSET_DATABASE_USER", os.environ.get("POSTGRES_USER", "bankpy_superset"))
POSTGRES_PASSWORD = os.environ.get("SUPERSET_DATABASE_PASSWORD", os.environ.get("POSTGRES_PASSWORD", "Engenharia10"))
POSTGRES_DB = os.environ.get("SUPERSET_DATABASE_DB", os.environ.get("POSTGRES_DB", "superset"))
POSTGRES_HOST = os.environ.get("SUPERSET_DATABASE_HOST", os.environ.get("POSTGRES_HOST", "bankpy_db"))
POSTGRES_PORT = os.environ.get("SUPERSET_DATABASE_PORT", "5432")

SQLALCHEMY_DATABASE_URI = os.environ.get(
    "SUPERSET_DATABASE_URI",
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# -------------------------
# Security / Secret key
# -------------------------
SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY", "Qv8s9z2Kf4R7mN6yT1uX0bWqZpL3aVhGd9Jr5cYtF2oPq8H")

# -------------------------
# Localization / Timezone
# -------------------------
LANGUAGES = {
    'en': {'flag': 'us', 'name': 'English'},
    'pt': {'flag': 'br', 'name': 'Português'},
}
DEFAULT_TIMEZONE = os.environ.get("TZ", "America/Sao_Paulo")

# -------------------------
# Cache (opcional)
# -------------------------
# SimpleCache funciona sem dependências externas; para produção prefira Redis.
CACHE_CONFIG = {
    'CACHE_TYPE': os.environ.get("SUPERSET_CACHE_TYPE", "SimpleCache"),
    'CACHE_DEFAULT_TIMEOUT': int(os.environ.get("SUPERSET_CACHE_TIMEOUT", 300)),
}

# -------------------------
# Uploads
# -------------------------
# Diretório dentro do container onde uploads serão gravados.
UPLOAD_FOLDER = os.environ.get("SUPERSET_UPLOAD_FOLDER", "/app/superset_home/uploads")
ALLOWED_EXTENSIONS = set(os.environ.get("SUPERSET_ALLOWED_EXTENSIONS", "csv,xls,xlsx").split(","))

# -------------------------
# Optional extras
# -------------------------
# Mapbox key se necessário para mapas
MAPBOX_API_KEY = os.environ.get("MAPBOX_API_KEY", "")

# Proxy fix (se estiver atrás de proxy/reverse-proxy)
ENABLE_PROXY_FIX = os.environ.get("SUPERSET_ENABLE_PROXY_FIX", "False").lower() in ("1", "true", "yes")

# Feature flags (adicionar conforme necessidade)
FEATURE_FLAGS = {
    # 'ALERT_REPORTS': True,
}

# -------------------------
# Logging (opcional)
# -------------------------
LOG_LEVEL = os.environ.get("SUPERSET_LOG_LEVEL", "INFO")

# -------------------------
# Final notes
# -------------------------
# Evite deixar segredos em texto no repositório. Prefira definir:
# SUPERSET_DATABASE_URI, SUPERSET_SECRET_KEY, SUPERSET_DATABASE_PASSWORD no arquivo .env.
