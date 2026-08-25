"""
NETRIX configuration — robust SQLite (and optional MySQL) database setup.
"""
import os
import sys
import tempfile
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).resolve().parent
load_dotenv(basedir / '.env')

_instance = basedir / 'instance'


def _ensure_dir(path: Path) -> bool:
    """Create directory and verify it is writable. Returns True on success."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / '.write_test'
        probe.write_text('ok', encoding='utf-8')
        probe.unlink()
        return True
    except Exception as exc:
        print(f'[NETRIX] Cannot write to {path}: {exc}', file=sys.stderr)
        return False


def _sqlite_uri(db_path: Path) -> str:
    """
    Build a correct absolute SQLite URI for any OS.
    SQLAlchemy expects: sqlite:///C:/path/to.db  (Windows)
                        sqlite:////absolute/path  (Unix – 4 slashes)
    Using Path.as_uri() is the most reliable approach.
    """
    # as_uri() -> file:///C:/... or file:///home/...
    # SQLAlchemy wants sqlite: + absolute path with forward slashes
    absolute = db_path.resolve()
    # Three slashes after sqlite: plus absolute path starting with /
    # On Windows absolute is like C:\foo → need sqlite:///C:/foo
    posix = absolute.as_posix()
    if absolute.drive:
        # Windows: sqlite:///C:/Users/...
        return f'sqlite:///{posix}'
    # Unix: sqlite:////home/...  (four slashes total)
    return f'sqlite:///{posix}'


def resolve_database_uri():
    """
    Priority:
      1. DATABASE_URL environment variable (MySQL, Postgres, or absolute SQLite)
      2. instance/netrix.db next to the app (if writable)
      3. System temp directory fallback
    """
    env_url = (os.environ.get('DATABASE_URL') or '').strip()
    if env_url:
        # Fix common relative SQLite mistake: sqlite:///instance/netrix.db
        if env_url.startswith('sqlite:///') and not env_url.startswith('sqlite:////'):
            rest = env_url[len('sqlite:///'):]
            # Relative path → make absolute under basedir
            if not rest.startswith('/') and not (len(rest) > 1 and rest[1] == ':'):
                abs_path = (basedir / rest).resolve()
                fixed = _sqlite_uri(abs_path)
                print(f'[NETRIX] Expanded relative DATABASE_URL → {fixed}')
                return fixed
        return env_url

    # Prefer instance/ next to the application
    if _ensure_dir(_instance):
        db_path = _instance / 'netrix.db'
        return _sqlite_uri(db_path)

    # Fallback: OS temp dir
    tmp_dir = Path(tempfile.gettempdir())
    _ensure_dir(tmp_dir)
    db_path = tmp_dir / 'netrix.db'
    print(f'[NETRIX] Using temp database: {db_path}', file=sys.stderr)
    return _sqlite_uri(db_path)


def sqlite_connect_args(uri: str) -> dict:
    """Extra connect args only for SQLite."""
    if not uri.startswith('sqlite'):
        return {}
    return {
        'timeout': 30,
        'check_same_thread': False,  # required for Flask threaded/dev server
    }


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-netrix-2024'
    SQLALCHEMY_DATABASE_URI = resolve_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'connect_args': sqlite_connect_args(SQLALCHEMY_DATABASE_URI),
    }
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = 3600 * 24
    UPLOAD_FOLDER = str(_instance / 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_HTTPONLY = True


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
