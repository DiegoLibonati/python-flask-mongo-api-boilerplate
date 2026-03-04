# Template Flask Mongo API

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
4. Execute: `pip install -r requirements.txt`
5. Execute: `pip install -r requirements.test.txt`
6. Execute all the commands you want

## Description

Personal template for developing an API with Flask and MongoDB.

## Technologies used

1. Python -> Flask
2. Docker
3. MongoDB -> PyMongo
4. Gunicorn

## Libraries used

#### Requirements.txt

```
flask==3.1.2
pymongo==4.16.0
pydantic==2.11.9
werkzeug==3.1.3
gunicorn==23.0.0
pre-commit==4.3.0
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

[`https://www.diegolibonati.com.ar/#/project/Template-Flask-Mongo-API`](https://www.diegolibonati.com.ar/#/project/Template-Flask-Mongo-API)

## Testing

1. Join to the correct path of the clone
2. Execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute: `pip install -r requirements.txt`
5. Execute: `pip install -r requirements.test.txt`
6. Execute: `pytest --log-cli-level=INFO`

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

```ts
TZ=America/Argentina/Buenos_Aires

MONGO_HOST=template-db
MONGO_PORT=27017
MONGO_USER=admin
MONGO_PASS=secret123
MONGO_DB_NAME=template_db
MONGO_AUTH_SOURCE=admin

HOST=0.0.0.0
PORT=5050
```

## Project Structure
```
Template-Flask-Mongo-API/
├── src/
│   ├── blueprints/
│   │   ├── routes.py
│   │   └── v1/
│   │       └── template_bp.py
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
│   │   └── template_controller.py
│   ├── services/
│   │   └── template_service.py
│   ├── data_access/
│   │   └── template_dao.py
│   ├── models/
│   │   └── template_model.py
│   ├── constants/
│   │   ├── codes.py
│   │   ├── messages.py
│   │   └── defaults.py
│   ├── startup/
│   │   └── init_templates.py
│   └── utils/
│       ├── exceptions.py
│       ├── error_handler.py
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
19. `pyproject.toml` -> **Unified project configuration** for pytest, ruff, and project metadata.

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
Controller (template_controller.py)  →  Handles request/response
    │
    ▼
Service (template_service.py)  →  Applies business rules
    │
    ▼
DAO (template_dao.py)          →  Executes database query
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
    add_default_templates()

    return app


# Usage
app = create_app("development")  # Development environment
app = create_app("testing")      # Testing environment
app = create_app("production")   # Production environment
```

#### 2. Repository Pattern (DAO)

**Purpose**: Abstracts data access logic, providing a clean API for data operations. The business layer doesn't know how data is stored.

**Location**: `src/data_access/template_dao.py`

```python
class TemplateDAO:
    @staticmethod
    def insert_one(template: dict) -> InsertOneResult:
        return mongo.db.templates.insert_one(template)

    @staticmethod
    def find() -> list[dict[str, Any]]:
        return TemplateDAO.parse_templates(list(mongo.db.templates.find()))

    @staticmethod
    def find_one_by_id(_id: ObjectId) -> dict[str, Any] | None:
        return TemplateDAO.parse_template(mongo.db.templates.find_one({"_id": ObjectId(_id)}))

    @staticmethod
    def find_one_by_name(name: str) -> dict[str, Any] | None:
        return TemplateDAO.parse_template(
            mongo.db.templates.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
        )

    @staticmethod
    def delete_one_by_id(_id: ObjectId) -> DeleteResult:
        return mongo.db.templates.delete_one({"_id": ObjectId(_id)})
```

**Benefit**: If you switch from MongoDB to PostgreSQL, only the DAO layer needs to change.

#### 3. Service Layer Pattern

**Purpose**: Encapsulates business logic in a dedicated layer. Controllers stay thin, and business rules are centralized.

**Location**: `src/services/template_service.py`

```python
class TemplateService:
    @staticmethod
    def add_template(template: TemplateModel) -> InsertOneResult:
        # Business rule: Check for duplicates
        existing = TemplateDAO.find_one_by_name(template.name)
        if existing:
            raise ConflictAPIError(
                code=CODE_ERROR_TEMPLATE_ALREADY_EXISTS,
                message=MESSAGE_ERROR_TEMPLATE_ALREADY_EXISTS,
            )
        return TemplateDAO.insert_one(template.model_dump())

    @staticmethod
    def get_all_templates() -> list[dict[str, Any]]:
        return TemplateDAO.find()

    @staticmethod
    def delete_template_by_id(_id: ObjectId) -> DeleteResult:
        # Business rule: Verify existence before deletion
        existing = TemplateDAO.find_one_by_id(_id)
        if not existing:
            raise NotFoundAPIError(
                code=CODE_NOT_FOUND_TEMPLATE, 
                message=MESSAGE_NOT_FOUND_TEMPLATE
            )
        return TemplateDAO.delete_one_by_id(_id)
```

**Benefit**: Business rules are in one place, not scattered across controllers.

#### 4. Decorator Pattern

**Purpose**: Adds behavior to functions without modifying them. Wraps functions to extend functionality.

**Location**: `src/utils/error_handler.py`

```python
def handle_exceptions(fn: Callable[P, R]) -> Callable[P, R]:
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
def create_template() -> Response:
    # If ValidationError or PyMongoError occurs,
    # it's automatically caught and converted to an API error
    data = request.get_json()
    template = TemplateModel(**data)
    TemplateService.add_template(template)
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
mongo.db.templates.find()
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
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "templates_db")
    
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