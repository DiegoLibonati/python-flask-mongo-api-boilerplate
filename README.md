# Python Flask Mongo Api Boilerplate

## Educational Purpose

This project was created primarily for **educational and learning purposes**.  
While it is well-structured and could technically be used in production, it is **not intended for commercialization**.  
The main goal is to explore and demonstrate best practices, patterns, and technologies in software development.

## Getting Started for Development

1. Clone the repository
2. Go to the repository folder and execute: `docker-compose -f dev.docker-compose.yml build --no-cache` in the terminal
3. Once built, you must execute the command: `docker-compose -f dev.docker-compose.yml up --force-recreate` in the terminal

NOTE: You have to be standing in the folder containing the: `dev.docker-compose.yml` and you need to install `Docker Desktop` if you are in Windows.

### Pre-Commit for Development

NOTE: Install **pre-commit** inside repository folder.

1. Once you're inside the virtual environment, let's install the hooks specified in the pre-commit. Execute: `pre-commit install`
2. Now every time you try to commit, the pre-commit lint will run. If you want to do it manually, you can run the command: `pre-commit run --all-files`

### Create a Virtual Env for Pre-Commit and Tests (And other things)

1. Join to the correct path of the clone
2. Execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute in Linux/Mac: `source venv/bin/activate`
5. Execute: `pip install -r requirements.txt`
6. Execute: `pip install -r requirements.dev.txt`
7. Execute: `pip install -r requirements.test.txt`
8. Execute all the commands you want

## Getting Started for Production

1. Clone the repository
2. Set your production environment variables in `.env` (see **Env Keys** section)
3. Go to the repository folder and execute: `docker-compose -f prod.docker-compose.yml build --no-cache` in the terminal
4. Once built, execute: `docker-compose -f prod.docker-compose.yml up -d` in the terminal

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

### Gunicorn

The production server is configured in `src/configs/gunicorn_config.py`:

- **Workers**: `cpu_count * 2 + 1` (auto-scaled to the host machine)
- **Threads**: `2` per worker
- **Timeout**: `120s` (request), `30s` (graceful shutdown)
- **Logs**: stdout/stderr (compatible with Docker log drivers)

### Security considerations before deploying

- Run `pip-audit -r requirements.txt` to check for known vulnerabilities in production dependencies
- Replace the default MongoDB credentials in `.env` with strong, unique values
- The production Dockerfile runs the app as a non-root user (`appuser`) — do not override this

## Description

**Python Flask Mongo Api Boilerplate** is a production-ready boilerplate for building REST APIs with **Flask** and **MongoDB**, designed to eliminate the repetitive setup and architectural decisions that come with every new backend project.

**What it is:** A starting point — not a framework — for developers who want to spin up a Flask + MongoDB API without rebuilding the same infrastructure from scratch each time. Every layer, pattern, and tooling choice is already wired together and working.

**The problem it solves:** Starting a Flask API from zero means making the same decisions repeatedly: how to structure layers, how to handle errors globally, how to validate input, how to configure environments, how to connect to MongoDB cleanly, how to set up Docker, linting, tests, and security audits. This boilerplate makes all those decisions once, so you can focus on building the actual product.

**What it includes:**
- **Layered architecture** enforced by convention: Blueprint → Controller → Service → DAO → MongoDB. Each layer has a single responsibility and only talks to the one directly below it.
- **Pydantic v2** for request validation and data serialization, with a custom `exceptions_handler` decorator that automatically converts `ValidationError` and `PyMongoError` into structured JSON API responses — no try/catch boilerplate in controllers.
- **Custom exception hierarchy** (`ValidationAPIError`, `NotFoundAPIError`, `ConflictAPIError`, `InternalAPIError`) that produces consistent error responses across the entire API.
- **MongoDB Singleton** via `mongo_config.py` — a single shared connection instance across all modules, initialized through Flask's app context.
- **Environment-based configuration** using a `DefaultConfig` base class extended by `DevelopmentConfig`, `TestingConfig`, and `ProductionConfig`, loaded dynamically by the app factory.
- **Docker** setup for development and production, with a separate `docker-compose.test.yml` that spins up a real MongoDB container for integration tests.
- **Gunicorn** as the production WSGI server, configured via `gunicorn_config.py`.
- **Ruff** for fast linting and formatting, enforced automatically via **pre-commit** hooks on every commit.
- **pip-audit** integration for scanning production dependencies against known vulnerability databases.
- **pytest** configured with real database connections (no mocks), organized to mirror the `src/` structure — tests run against an actual MongoDB instance in Docker.
- **Startup initialization** layer (`src/startup/`) for seeding default data when the app boots.

**How to use it:** Clone the repository, bring up the Docker environment, and replace the `note` resource (blueprint, controller, service, DAO, model, constants) with your own domain logic. The architecture, tooling, error handling, and test setup are already in place — you only write what's unique to your application.

## Technologies used

1. Python -> Flask
2. Docker
3. MongoDB -> PyMongo
4. Gunicorn

## Libraries used

#### Requirements.txt

```
flask==3.1.3
pymongo==4.16.0
pydantic==2.11.9
gunicorn==23.0.0
```

#### Requirements.dev.txt

```
pre-commit==4.3.0
pip-audit==2.7.3
ruff==0.11.12
```

#### Requirements.test.txt

```
pytest==8.4.2
pytest-env==1.1.5
pytest-cov==4.1.0
pytest-timeout==2.3.1
pytest-xdist==3.5.0
```

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/python-flask-mongo-api-boilerplate`](https://www.diegolibonati.com.ar/#/project/python-flask-mongo-api-boilerplate)

## Testing

1. Join to the correct path of the clone
2. Execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute: `pip install -r requirements.txt`
5. Execute: `pip install -r requirements.test.txt`
6. Execute: `pytest --log-cli-level=INFO`

## Security Audit

You can check your dependencies for known vulnerabilities using **pip-audit**.

1. Go to the repository folder
2. Activate your virtual environment
3. Execute: `pip install -r requirements.dev.txt`
4. Execute: `pip-audit -r requirements.txt`

## Env Keys

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

```ts
TZ=America/Argentina/Buenos_Aires

MONGO_HOST=boilerplate-db
MONGO_PORT=27017
MONGO_USER=admin
MONGO_PASS=secret123
MONGO_DB_NAME=boilerplate_db
MONGO_AUTH_SOURCE=admin

HOST=0.0.0.0
PORT=5050

ME_BASICAUTH_USERNAME=admin
ME_BASICAUTH_PASSWORD=admin123
```

## Project Structure

```
python-flask-mongo-api-boilerplate/
├── src/
│   ├── blueprints/
│   │   ├── routes.py
│   │   └── v1/
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
│       ├── exceptions_handler.py
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
├── docker-compose.test.yml
├── requirements.txt
├── requirements.test.txt
├── requirements.dev.txt
├── pyproject.toml
├── .env
├── .env.example
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
10. `utils` -> Contains **shared utilities** including custom exceptions, error handling decorators, and helper functions.
11. `test` -> Contains **integration tests** organized to mirror the `src/` structure. Uses real database connections via Docker.
12. `conftest.py` -> Defines **pytest fixtures** for database setup, app initialization, and test data.
13. `app.py` -> The **application factory**. Creates and configures the Flask app instance using the Factory pattern.
14. `wsgi.py` -> The **production entry point** for WSGI servers like Gunicorn.
15. `Dockerfile.*` -> Docker configurations for **development and production** environments.
16. `docker-compose.test.yml` -> Defines the **test environment** with MongoDB container for integration testing.
17. `requirements.txt` -> Lists **production dependencies**.
18. `requirements.test.txt` -> Lists **testing dependencies** (pytest, pytest-env, etc.).
19. `requirements.test.txt` -> Lists **development dependencies** (pre-commit, pip-audit, etc.).
20. `pyproject.toml` -> **Unified project configuration** for pytest, ruff, and project metadata.

## Architecture & Design Patterns

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

**Location**: `src/utils/exceptions_handler.py`

```python
def exceptions_handler(fn: Callable[P, R]) -> Callable[P, R]:
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
@handle_exceptions
def alive() -> Response:
    response = {
        "message": "I am Alive!",
        "version_bp": "2.0.0",
    }
    return jsonify(response), 200


@handle_exceptions
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

## Known Issues

None at the moment.
