"""
04 - FastAPI Dependency Injection
==================================

FastAPI has built-in dependency injection that automatically
resolves and injects dependencies into your route handlers.

To run this example:
    pip install fastapi uvicorn
    python 04_fastapi_di.py
    # Then visit http://localhost:8000/docs
"""

from typing import Annotated
from fastapi import FastAPI, Depends

# ============================================================================
# DEPENDENCIES (Services)
# ============================================================================

class Database:
    """Simulates a database."""
    
    def __init__(self):
        print("💾 Creating database connection")
        self.users = {
            1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
            2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
        }
    
    def get_user(self, user_id: int) -> dict:
        return self.users.get(user_id, {})


class Logger:
    """Simulates a logging service."""
    
    def __init__(self):
        print("📝 Creating logger")
    
    def log(self, message: str) -> None:
        print(f"📝 LOG: {message}")


class UserService:
    """Business logic for users."""
    
    def __init__(self, db: Database, logger: Logger):
        """
        UserService needs both a database and a logger.
        FastAPI will automatically provide these!
        """
        self.db = db
        self.logger = logger
        print("👤 Creating UserService")
    
    def get_user_info(self, user_id: int) -> dict:
        self.logger.log(f"Fetching user {user_id}")
        user = self.db.get_user(user_id)
        if user:
            self.logger.log(f"Found user: {user['name']}")
        else:
            self.logger.log(f"User {user_id} not found")
        return user


# ============================================================================
# DEPENDENCY PROVIDER FUNCTIONS
# ============================================================================

def get_database() -> Database:
    """
    FastAPI will call this function when a route needs a Database.
    
    This is called a "dependency provider" or "factory function".
    """
    return Database()


def get_logger() -> Logger:
    """FastAPI will call this function when a route needs a Logger."""
    return Logger()


def get_user_service(
    db: Database = Depends(get_database),
    logger: Logger = Depends(get_logger)
) -> UserService:
    """
    FastAPI will:
    1. Call get_database() to get a Database
    2. Call get_logger() to get a Logger
    3. Call this function with both dependencies
    4. Return the UserService
    
    This is called a "dependency chain" - dependencies can have dependencies!
    """
    return UserService(db, logger)


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(title="Dependency Injection Example")


@app.get("/")
def root():
    """Simple endpoint with no dependencies."""
    return {"message": "Visit /docs to see the API documentation"}


@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """
    FastAPI automatically:
    1. Sees that we need a UserService
    2. Calls get_user_service()
    3. Which needs Database and Logger
    4. Calls get_database() and get_logger()
    5. Creates UserService with those dependencies
    6. Passes it to our route handler
    
    We don't have to do ANY of that manually!
    """
    user = service.get_user_info(user_id)
    if user:
        return user
    return {"error": "User not found"}, 404


# Using Annotated for cleaner syntax (Python 3.9+)
@app.get("/users/{user_id}/simple")
def get_user_simple(
    user_id: int,
    service: Annotated[UserService, Depends(get_user_service)]
):
    """
    Alternative syntax using Annotated.
    This is the preferred way in modern FastAPI.
    """
    user = service.get_user_info(user_id)
    if user:
        return user
    return {"error": "User not found"}, 404


@app.get("/users/{user_id}/direct-deps")
def get_user_direct(
    user_id: int,
    db: Database = Depends(get_database),
    logger: Logger = Depends(get_logger)
):
    """
    You can also inject dependencies directly without a service class.
    """
    logger.log(f"Direct fetch of user {user_id}")
    user = db.get_user(user_id)
    return user if user else {"error": "User not found"}


# ============================================================================
# DEMONSTRATION
# ============================================================================

def main():
    """Run the FastAPI application."""
    print("=" * 70)
    print("FASTAPI DEPENDENCY INJECTION")
    print("=" * 70)
    print()
    print("Starting server...")
    print()
    print("🌐 Visit these URLs:")
    print("   http://localhost:8000/docs         - Interactive API docs")
    print("   http://localhost:8000/users/1      - Get user 1")
    print("   http://localhost:8000/users/2      - Get user 2")
    print()
    print("Watch the console to see when dependencies are created!")
    print()
    print("=" * 70)
    print()
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# ============================================================================
# EXPLANATION
# ============================================================================

"""
HOW FASTAPI DEPENDENCY INJECTION WORKS:
=========================================

When a request comes in to /users/1:

1. FastAPI looks at the route handler parameters
2. Sees: service: UserService = Depends(get_user_service)
3. Calls get_user_service()
4. get_user_service needs Database and Logger
5. Calls get_database() → returns Database instance
6. Calls get_logger() → returns Logger instance
7. Passes both to get_user_service()
8. get_user_service returns UserService instance
9. Passes UserService to the route handler
10. Route handler executes with the UserService

The dependency tree looks like:

    get_user()
        ↓ needs
    UserService
        ↓ needs
    ┌─────────┬──────────┐
    ↓         ↓          ↓
Database   Logger   (more deps...)

FastAPI resolves this tree automatically!


KEY BENEFITS:
=============

✅ Automatic resolution of dependency chains
✅ Type-safe (FastAPI validates types)
✅ Works with async dependencies
✅ Can override dependencies in tests
✅ Automatic API documentation
✅ No global state needed
✅ Easy to understand and maintain


COMPARISON TO MANUAL DI:
=========================

# Manual (what we did in previous examples):
db = Database()
logger = Logger()
service = UserService(db, logger)
user = service.get_user_info(1)

# FastAPI (automatic):
# Just declare what you need, FastAPI does the rest!
def get_user(service: UserService = Depends(get_user_service)):
    return service.get_user_info(1)
"""


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("❌ FastAPI not installed!")
        print("Install with: pip install fastapi uvicorn")
        print()
        print("Or just read the code to understand the concepts!")

