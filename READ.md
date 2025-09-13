project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── core/               # Core configurations
│   │   ├── __init__.py
│   │   ├── config.py       # Configuration settings
│   │   ├── security.py     # Authentication & authorization
│   │   └── database.py     # Database connection
│   ├── api/               # API endpoints
│   │   ├── __init__.py
│   │   ├── v1/            # API versioning
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/ # Route handlers
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   └── items.py
│   │   │   └── routers.py # API routers
│   ├── models/            # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/           # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── services/          # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   ├── repositories/      # Data access layer
│   │   ├── __init__.py
│   │   ├── user_repo.py
│   │   └── item_repo.py
│   ├── utils/             # Utilities & helpers
│   │   ├── __init__.py
│   │   ├── email.py
│   │   └── validation.py
│   └── tests/             # Test suite
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_api/
│       └── test_services/
├── alembic/               # Database migrations
│   ├── versions/
│   ├── env.py
│   └── alembic.ini
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md