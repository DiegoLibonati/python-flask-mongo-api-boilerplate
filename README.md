# Python Flask Mongo Api Boilerplate

## Educational Purpose

This project was created primarily for **educational and learning purposes**.  
While it is well-structured and could technically be used in production, it is **not intended for commercialization**.  
The main goal is to explore and demonstrate best practices, patterns, and technologies in software development.

## Description

**Python Flask Mongo Api Boilerplate** is a production-ready boilerplate for building REST APIs with **Flask** and **MongoDB**, designed to eliminate the repetitive setup and architectural decisions that come with every new backend project.

**What it is:** A starting point — not a framework — for developers who want to spin up a Flask + MongoDB API without rebuilding the same infrastructure from scratch each time. Every layer, pattern, and tooling choice is already wired together and working.

**The problem it solves:** Starting a Flask API from zero means making the same decisions repeatedly: how to structure layers, how to handle errors globally, how to validate input, how to configure environments, how to connect to MongoDB cleanly, how to set up Docker, linting, tests, and security audits. This boilerplate makes all those decisions once, so you can focus on building the actual product.

**What it includes:**
- **Layered architecture** enforced by convention: Blueprint → Controller → Service → DAO → MongoDB. Each layer has a single responsibility and only talks to the one directly below it.
- **Pydantic v2** for request validation and data serialization, with a custom `exceptions_decorator` decorator that automatically converts `ValidationError` and `PyMongoError` into structured JSON API responses — no try/catch boilerplate in controllers.
- **Custom exception hierarchy** (`ValidationAPIError`, `NotFoundAPIError`, `ConflictAPIError`, `InternalAPIError`) that produces consistent error responses across the entire API.
- **MongoDB Singleton** via `mongo_config.py` — a single shared connection instance across all modules, initialized through Flask's app context.
- **Environment-based configuration** using a `DefaultConfig` base class extended by `DevelopmentConfig`, `TestingConfig`, and `ProductionConfig`, loaded dynamically by the app factory.
- **Docker** setup for development and production, with a separate `test.docker-compose.yml` that spins up a real MongoDB container for integration tests.
- **Gunicorn** as the production WSGI server, configured via `gunicorn_config.py`.
- **Ruff** for fast linting and formatting, enforced automatically via **pre-commit** hooks on every commit.
- **pip-audit** integration for scanning production dependencies against known vulnerability databases.
- **pytest** configured with real database connections (no mocks), organized to mirror the `src/` structure — tests run against an actual MongoDB instance in Docker.
- **GitHub Actions CI/CD** pipeline (`.github/workflows/ci.yml`) that runs linting, type checking with mypy, security audit, tests, and Docker builds on every push and pull request to `main`.
- **Health endpoint** (`GET /api/v1/health`) for liveness checks, with a matching `HEALTHCHECK` directive in the production Dockerfile.
- **Global error handlers** for 404 (unknown routes) and 500 (unhandled exceptions) that return the same structured JSON format as the rest of the API.
- **Startup initialization** layer (`src/startup/`) for seeding default data when the app boots, controlled by the `SEED_DEFAULT_DATA` env var.

**How to use it:** Clone the repository, bring up the Docker environment, and replace the `note` resource (blueprint, controller, service, DAO, model, constants) with your own domain logic. The architecture, tooling, error handling, and test setup are already in place — you only write what's unique to your application.

## Technologies used

1. Python 3.11 -> Flask
2. Docker
3. MongoDB -> PyMongo
4. Gunicorn

## Libraries used

#### Runtime (`[project.dependencies]`)

```
flask==3.1.3
pymongo==4.16.0
pydantic==2.11.9
gunicorn==23.0.0
```

#### Dev (`[project.optional-dependencies]` dev)

```
pre-commit==4.3.0
pip-audit==2.7.3
ruff==0.11.12
mypy==1.13.0
```

#### Test (`[project.optional-dependencies]` test)

```
pytest==9.0.3
pytest-env==1.1.5
pytest-cov==4.1.0
pytest-timeout==2.3.1
pytest-xdist==3.5.0
```

## Getting Started

With the dependencies catalogued above, the next step is bringing the stack up locally. These steps wire up a fully working development environment with Flask + MongoDB running inside Docker. For production deployment instructions, jump to [Production](#production).

1. Clone the repository
2. Copy `.env.example` to `.env` and adjust values if needed (see [Env Keys](#env-keys) for what each variable means)
3. Go to the repository folder and execute: `docker-compose -f dev.docker-compose.yml build --no-cache` in the terminal
4. Once built, you must execute the command: `docker-compose -f dev.docker-compose.yml up --force-recreate` in the terminal

NOTE: You have to be standing in the folder containing the: `dev.docker-compose.yml` and you need to install `Docker Desktop` if you are in Windows.

### Create a Virtual Env for Local Tooling

The Docker environment runs the app, but to use the local tooling (pre-commit hooks, tests, security audit) you need a Python virtual environment on the host. This venv is the one referenced later by [Testing](#testing) and [Security Audit](#security-audit), so create it once here:

1. Join to the correct path of the clone
2. Execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute in Linux/Mac: `source venv/bin/activate`
5. Execute: `pip install -r requirements.txt`
6. Execute: `pip install -r requirements.dev.txt`
7. Execute: `pip install -r requirements.test.txt`
8. Execute all the commands you want

### Pre-Commit for Development

NOTE: Install **pre-commit** inside repository folder.

1. Once you're inside the virtual environment, let's install the hooks specified in the pre-commit. Execute: `pre-commit install`
2. Now every time you try to commit, the pre-commit lint will run. If you want to do it manually, you can run the command: `pre-commit run --all-files`

## Env Keys

Step 2 of [Getting Started](#getting-started) had you copy `.env.example` to `.env`. This section documents what every variable in that file controls so you can adjust them confidently per environment.

1. `TZ`: Refers to the timezone setting for the container.
2. `MONGO_HOST`: Specifies the hostname or address where the MongoDB server is located. In this case, `host.docker.internal` allows a Docker container to connect to the host machine.
3. `MONGO_PORT`: Defines the port on which the MongoDB server is listening for connections. The default MongoDB port is `27017`.
4. `MONGO_USER`: Indicates the username for authenticating with the MongoDB database.
5. `MONGO_PASS`: Contains the password associated with the user specified in `MONGO_USER` for authentication.
6. `MONGO_DB_NAME`: Specifies the name of the database to which the application will connect within the MongoDB server.
7. `MONGO_AUTH_SOURCE`: Defines the database where the user credentials will be verified. Typically set to `admin` when the credentials were created in that database.
8. `HOST`: Refers to the network interface where the backend API listens (e.g., 0.0.0.0 to allow external connections).
9. `PORT`: Refers to the port on which the backend API is exposed.
10. `ME_BASICAUTH_USERNAME`: Username for the Mongo Express web UI basic authentication.
11. `ME_BASICAUTH_PASSWORD`: Password for the Mongo Express web UI basic authentication.
12. `MAX_CONTENT_LENGTH`: Maximum allowed request body size in bytes (default: 1048576 = 1 MB). Prevents oversized payloads from exhausting memory.
13. `SEED_DEFAULT_DATA`: Set to `true` to seed default data on startup. Only enabled in development by default.

```bash
TZ=America/Argentina/Buenos_Aires

MONGO_HOST=boilerplate-db
MONGO_PORT=27017
MONGO_USER=admin
MONGO_PASS=secret123
MONGO_DB_NAME=boilerplate_db
MONGO_AUTH_SOURCE=admin

HOST=0.0.0.0
PORT=5050
SEED_DEFAULT_DATA=false

MAX_CONTENT_LENGTH=1048576

ME_BASICAUTH_USERNAME=admin
ME_BASICAUTH_PASSWORD=admin123
```

## Project Structure

With the environment running and configured, the following layout is what you'll be working in:

```
python-flask-mongo-api-boilerplate/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── blueprints/
│   │   ├── routes.py
│   │   └── v1/
│   │       ├── health_bp.py
│   │       └── note_bp.py
│   ├── configs/
│   │   ├── __init__.py
│   │   ├── default_config.py
│   │   ├── development_config.py
│   │   ├── production_config.py
│   │   ├── testing_config.py
│   │   ├── gunicorn_config.py
│   │   ├── logger_config.py
│   │   └── mongo_config.py
│   ├── controllers/
│   │   ├── health_controller.py
│   │   └── note_controller.py
│   ├── services/
│   │   └── note_service.py
│   ├── data_access/
│   │   └── note_dao.py
│   ├── models/
│   │   └── note_model.py
│   ├── constants/
│   │   ├── codes.py
│   │   ├── messages.py
│   │   └── defaults.py
│   ├── startup/
│   │   └── init_notes.py
│   └── utils/
│       ├── exceptions.py
│       ├── exceptions_decorator.py
│       └── helpers.py
├── test/
│   ├── conftest.py
│   ├── test_blueprints/
│   ├── test_controllers/
│   ├── test_services/
│   ├── test_data_access/
│   ├── test_models/
│   ├── test_startup/
│   └── test_utils/
├── app.py
├── wsgi.py
├── Dockerfile.development
├── Dockerfile.production
├── dev.docker-compose.yml
├── prod.docker-compose.yml
├── test.docker-compose.yml
├── requirements.txt
├── requirements.test.txt
├── requirements.dev.txt
├── pyproject.toml
├── .editorconfig
├── .env
├── .env.example
├── .python-version
├── .gitignore
├── .pre-commit-config.yaml
└── README.md
```

1. `src` -> Root directory of the source code. Contains the full application logic following a **layered architecture** pattern.
2. `configs` -> Contains all **configuration classes** organized by environment (development, production, testing). Includes database connection, logging setup, and server settings.
3. `blueprints` -> Defines **API routes and endpoints**. Organized by API version (`v1/`) to support versioning.
4. `controllers` -> Handles **HTTP request/response logic**. Receives requests from blueprints and delegates business logic to services.
5. `services` -> Contains **business logic and rules**. Validates data, enforces constraints, and orchestrates operations between controllers and data access layer.
6. `data_access` -> Implements the **Repository/DAO pattern**. Abstracts all database operations, making it easy to switch databases without affecting other layers.
7. `models` -> Defines **Pydantic models** for data validation and serialization.
8. `constants` -> Holds **static values** like error codes, user messages, and default configurations.
9. `startup` -> Contains **initialization logic** executed when the application starts, such as seeding default data.
10. `utils` -> Contains **shared utilities** including custom exceptions, the `exceptions_decorator` error-handling decorator, and helper functions.
11. `test` -> Contains **integration tests** organized to mirror the `src/` structure. Uses real database connections via Docker.
12. `conftest.py` -> Defines **pytest fixtures** for database setup, app initialization, and test data.
13. `app.py` -> The **application factory**. Creates and configures the Flask app instance using the Factory pattern.
14. `wsgi.py` -> The **production entry point** for WSGI servers like Gunicorn.
15. `Dockerfile.*` -> Docker configurations for **development and production** environments.
16. `test.docker-compose.yml` -> Defines the **test environment** with MongoDB container for integration testing.
17. `requirements.txt` -> Installs the package in editable mode (`-e .`), pulling dependencies from `pyproject.toml`.
18. `requirements.test.txt` -> Installs test extras (`-e .[test]`): pytest and related plugins.
19. `requirements.dev.txt` -> Installs dev extras (`-e .[dev]`): pre-commit, ruff, mypy, pip-audit.
20. `pyproject.toml` -> **Single source of truth** for project metadata, all dependency groups, and tool configuration (pytest, ruff, mypy).
21. `.editorconfig` -> Enforces **consistent editor settings** (indentation, line endings, charset) across editors and IDEs.
22. `.github/workflows/ci.yml` -> **GitHub Actions CI/CD pipeline** that runs lint, type check, security audit, tests, and Docker builds on every push and pull request to `main`.
23. `.python-version` -> Pins the **Python version** (3.11) for tools that read this file (e.g., pyenv).

## Architecture & Design Patterns

The folder structure above is a direct reflection of the architectural decisions described in this section.

### Layered Architecture

This project follows a **Layered Architecture** pattern, organizing code into distinct levels with clear responsibilities. Each layer only communicates with the layer directly below it.

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│                  (Blueprints & Controllers)                 │
│            Handles HTTP requests and responses              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      BUSINESS LAYER                         │
│                        (Services)                           │
│          Contains business logic and validations            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATA ACCESS LAYER                       │
│                         (DAO)                               │
│            Abstracts database operations                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        DATABASE                             │
│                        (MongoDB)                            │
└─────────────────────────────────────────────────────────────┘
```

#### Benefits

- **Separation of Concerns**: Each layer has a single responsibility
- **Testability**: Layers can be tested independently
- **Maintainability**: Changes in one layer don't affect others
- **Flexibility**: Easy to swap implementations (e.g., change database)

#### Request Flow Example

```
HTTP Request
    │
    ▼
Blueprint (routes.py)          →  Defines endpoint URL
    │
    ▼
Controller (note_controller.py)  →  Handles request/response
    │
    ▼
Service (note_service.py)  →  Applies business rules
    │
    ▼
DAO (note_dao.py)          →  Executes database query
    │
    ▼
MongoDB                        →  Stores/retrieves data
```

### Design Patterns

#### 1. Factory Pattern

**Purpose**: Creates objects without specifying the exact class to create. Useful for creating instances with different configurations.

**Location**: `app.py`

```python
def create_app(config_name="development") -> Flask:
    app = Flask(__name__)

    config_module = importlib.import_module(f"src.configs.{config_name}_config")
    app.config.from_object(config_module.__dict__[f"{config_name.capitalize()}Config"])

    init_mongo(app)
    register_routes(app)
    add_default_notes()

    return app


# Usage
app = create_app("development")  # Development environment
app = create_app("testing")      # Testing environment
app = create_app("production")   # Production environment
```

#### 2. Repository Pattern (DAO)

**Purpose**: Abstracts data access logic, providing a clean API for data operations. The business layer doesn't know how data is stored.

**Location**: `src/data_access/note_dao.py`

```python
class NoteDAO:
    @staticmethod
    def insert_one(note: dict[str, Any]) -> InsertOneResult:
        return mongo.db.notes.insert_one(note)

    @staticmethod
    def find() -> list[dict[str, Any]]:
        return NoteDAO.parse_notes(list(mongo.db.notes.find()))

    @staticmethod
    def find_one_by_id(_id: ObjectId) -> dict[str, Any] | None:
        return NoteDAO.parse_note(mongo.db.notes.find_one({"_id": ObjectId(_id)}))

    @staticmethod
    def find_one_by_name(name: str) -> dict[str, Any] | None:
        return NoteDAO.parse_note(
            mongo.db.notes.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
        )

    @staticmethod
    def delete_one_by_id(_id: ObjectId) -> DeleteResult:
        return mongo.db.notes.delete_one({"_id": ObjectId(_id)})
```

**Benefit**: If you switch from MongoDB to PostgreSQL, only the DAO layer needs to change.

#### 3. Service Layer Pattern

**Purpose**: Encapsulates business logic in a dedicated layer. Controllers stay thin, and business rules are centralized.

**Location**: `src/services/note_service.py`

```python
class NoteService:
    @staticmethod
    def add_note(note: NoteModel) -> InsertOneResult:
        # Business rule: Check for duplicates
        existing = NoteDAO.find_one_by_name(note.name)
        if existing:
            raise ConflictAPIError(
                code=CODE_ALREADY_EXISTS_NOTE,
                message=MESSAGE_ALREADY_EXISTS_NOTE,
            )
        return NoteDAO.insert_one(note.model_dump())

    @staticmethod
    def get_all_notes() -> list[dict[str, Any]]:
        return NoteDAO.find()

    @staticmethod
    def delete_note_by_id(_id: ObjectId) -> DeleteResult:
        # Business rule: Verify existence before deletion
        existing = NoteDAO.find_one_by_id(_id)
        if not existing:
            raise NotFoundAPIError(
                code=CODE_NOT_FOUND_NOTE,
                message=MESSAGE_NOT_FOUND_NOTE
            )
        return NoteDAO.delete_one_by_id(_id)
```

**Benefit**: Business rules are in one place, not scattered across controllers.

#### 4. Decorator Pattern

**Purpose**: Adds behavior to functions without modifying them. Wraps functions to extend functionality.

**Location**: `src/utils/exceptions_decorator.py`

```python
def exceptions_decorator(fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return fn(*args, **kwargs)

        except ValidationError as e:
            raise ValidationAPIError(
                code=CODE_ERROR_PYDANTIC,
                message=MESSAGE_ERROR_PYDANTIC,
                payload={"details": e.errors()},
            )

        except PyMongoError as e:
            raise InternalAPIError(
                code=CODE_ERROR_DATABASE,
                message=MESSAGE_ERROR_DATABASE,
            )

    return wrapper
```

**Usage in Controller**:

```python
@exceptions_decorator
def alive() -> Response:
    response = {
        "message": "I am Alive!",
        "version_bp": "2.0.0",
    }
    return jsonify(response), 200


@exceptions_decorator
def create_note() -> Response:
    # If ValidationError or PyMongoError occurs,
    # it's automatically caught and converted to an API error
    data = request.get_json()
    note = NoteModel(**data)
    NoteService.add_note(note)
    return jsonify({"message": "Created"}), 201
```

**Benefit**: No need to repeat try/catch blocks in every controller.

#### 5. Singleton Pattern

**Purpose**: Ensures only one instance of a class exists throughout the application.

**Location**: `src/configs/mongo_config.py`

```python
class Mongo:
    def __init__(self):
        self.client: MongoClient | None = None
        self.db: Database | None = None

    def init_app(self, app: Flask) -> None:
        mongo_uri = app.config["MONGO_URI"]
        db_name = app.config["MONGO_DB_NAME"]

        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]


# Single instance used across the entire application
mongo = Mongo()


def init_mongo(app: Flask) -> None:
    mongo.init_app(app)
```

**Usage**:

```python
from src.configs.mongo_config import mongo

# Always the same instance
mongo.db.notes.find()
```

**Benefit**: One database connection shared across all modules, avoiding connection overhead.

#### 6. Template Method Pattern

**Purpose**: Defines a base structure that subclasses can customize by overriding specific parts.

**Location**: `src/configs/`

```python
# src/configs/default_config.py - Base template
class DefaultConfig:
    TZ = os.getenv("TZ", "America/Argentina/Buenos_Aires")

    MONGO_HOST = os.getenv("MONGO_HOST", "host.docker.internal")
    MONGO_PORT = os.getenv("MONGO_PORT", 27017)
    MONGO_USER = os.getenv("MONGO_USER", "admin")
    MONGO_PASS = os.getenv("MONGO_PASS", "secret123")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "boilerplate_db")

    DEBUG = False
    TESTING = False


# src/configs/development_config.py - Customizes for development
class DevelopmentConfig(DefaultConfig):
    DEBUG = True


# src/configs/testing_config.py - Customizes for testing
class TestingConfig(DefaultConfig):
    TESTING = True
    DEBUG = True
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "test_db")


# src/configs/production_config.py - Customizes for production
class ProductionConfig(DefaultConfig):
    DEBUG = False
    TESTING = False
```

**Benefit**: Common configuration in one place; environments only override what's different.

## Testing

Once the architecture is clear, the test suite mirrors the same `src/` layout and runs against a real MongoDB instance (no mocks). It reuses the virtual environment created in [Getting Started](#create-a-virtual-env-for-local-tooling) — no extra setup is needed:

1. Activate the virtual environment (Windows: `venv\Scripts\activate`, Linux/Mac: `source venv/bin/activate`)
2. Execute: `pytest --log-cli-level=INFO`

NOTE: `pytest` boots the MongoDB container defined in `test.docker-compose.yml` automatically — make sure Docker Desktop is running.

## Security Audit

Before shipping any build, scan production dependencies for known vulnerabilities using **pip-audit**. This also runs from the virtual environment created in [Getting Started](#create-a-virtual-env-for-local-tooling) — `pip-audit` is already installed via `requirements.dev.txt`:

1. Activate the virtual environment (Windows: `venv\Scripts\activate`, Linux/Mac: `source venv/bin/activate`)
2. Execute: `pip-audit -r requirements.txt`

## Build

With tests passing and no flagged vulnerabilities, build the production Docker image. The production build uses a multi-stage slim image and runs the app as a non-root `appuser`:

1. Go to the repository folder
2. Execute: `docker-compose -f prod.docker-compose.yml build --no-cache`

The resulting image bakes in Gunicorn as the WSGI server, configured in `src/configs/gunicorn_config.py`:

- **Workers**: `cpu_count * 2 + 1` (auto-scaled to the host machine)
- **Threads**: `2` per worker
- **Timeout**: `120s` (request), `30s` (graceful shutdown)
- **Logs**: stdout/stderr (compatible with Docker log drivers)

## Production

Production deployment is the result of completing the previous sections — it does not introduce a new flow, only the steps that are specific to running the built image on a real host.

**Pre-flight checklist** (do these in order before deploying):

1. Run the suite — see [Testing](#testing)
2. Audit production dependencies — see [Security Audit](#security-audit)
3. Build the production image — see [Build](#build)

**Production-specific steps:**

1. On the production host, set strong, unique values for every variable listed in [Env Keys](#env-keys) inside `.env` — **do not** reuse the development credentials
2. Start the stack: `docker-compose -f prod.docker-compose.yml up -d`

NOTE: The API server will only start after MongoDB passes its health check. The `restart: always` policy ensures both containers come back up automatically after a crash or reboot.

### What's different from development

| | Development | Production |
|---|---|---|
| Server | Flask dev server | Gunicorn (`wsgi.py`) |
| Debug mode | `True` | `False` |
| Docker image | Full build | Multi-stage slim image |
| Container user | root | `appuser` (non-root) |
| MongoDB data | Ephemeral | Persistent volume (`db-data`) |
| MongoDB port | Exposed to host | Internal network only |

### Production hardening notes

- The production Dockerfile runs the app as a non-root user (`appuser`) — do not override this
- MongoDB is not exposed to the host network in production; access it through the application or an authenticated tunnel
- Re-run [Security Audit](#security-audit) on every dependency bump before rebuilding the image

## Known Issues

None at the moment.

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/python-flask-mongo-api-boilerplate`](https://www.diegolibonati.com.ar/#/project/python-flask-mongo-api-boilerplate)
