"""
05 - Singleton Pattern with @once() Decorator
==============================================

This example shows how to implement and use the @once() decorator
pattern from the App codebase. This ensures expensive
resources (like database connections) are created only once.
"""

from functools import wraps
from typing import Callable, TypeVar, Any

# ============================================================================
# THE @once() DECORATOR IMPLEMENTATION
# ============================================================================

T = TypeVar('T')


def once() -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator that ensures a function is called only once.
    Subsequent calls return the cached result.
    
    This is useful for expensive operations like:
    - Creating database connections
    - Loading configuration
    - Initializing external service clients
    
    Usage:
        @once()
        def get_database():
            return Database()  # Only created once!
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        # Storage for the cached result
        cached_result: dict[str, Any] = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            # Use a key to check if we've already called this function
            cache_key = 'result'
            
            if cache_key not in cached_result:
                # First call - execute the function and cache the result
                print(f"🔧 [FIRST CALL] Creating {func.__name__}")
                cached_result[cache_key] = func(*args, **kwargs)
            else:
                # Subsequent calls - return cached result
                print(f"♻️  [CACHED] Reusing {func.__name__}")
            
            return cached_result[cache_key]
        
        return wrapper
    return decorator


# ============================================================================
# EXPENSIVE RESOURCES
# ============================================================================

class Database:
    """Simulates an expensive database connection."""
    
    def __init__(self, connection_string: str = "postgresql://localhost:5432/mydb"):
        # Simulate expensive connection
        print(f"    💾 Opening database connection to {connection_string}")
        print(f"    💾 This is EXPENSIVE and SLOW!")
        self.connection_string = connection_string
        self.query_count = 0
    
    def query(self, sql: str) -> str:
        self.query_count += 1
        return f"Result from query #{self.query_count}"


class CacheService:
    """Simulates a cache service like Redis."""
    
    def __init__(self, host: str = "localhost"):
        print(f"    🔴 Connecting to Redis at {host}")
        print(f"    🔴 This is EXPENSIVE!")
        self.host = host


class EmailService:
    """Simulates an email service connection."""
    
    def __init__(self, api_key: str = "secret-key"):
        print(f"    📧 Initializing email service")
        print(f"    📧 This is EXPENSIVE!")
        self.api_key = api_key


# ============================================================================
# WITHOUT @once() - THE PROBLEM
# ============================================================================

def get_database_without_once() -> Database:
    """Without @once(), this creates a new database every time!"""
    return Database()


def demonstrate_without_once():
    print("\n" + "=" * 70)
    print("WITHOUT @once() - Creating Multiple Connections")
    print("=" * 70)
    
    print("\n1st call:")
    db1 = get_database_without_once()
    
    print("\n2nd call:")
    db2 = get_database_without_once()
    
    print("\n3rd call:")
    db3 = get_database_without_once()
    
    print(f"\n❌ Problem: Created {3} separate database connections!")
    print(f"   db1 is db2: {db1 is db2}")  # False - different objects
    print(f"   db2 is db3: {db2 is db3}")  # False - different objects


# ============================================================================
# WITH @once() - THE SOLUTION
# ============================================================================

@once()
def get_database() -> Database:
    """With @once(), this creates the database only on the first call!"""
    return Database()


@once()
def get_cache() -> CacheService:
    """Cache service - also created only once."""
    return CacheService()


@once()
def get_email() -> EmailService:
    """Email service - also created only once."""
    return EmailService()


def demonstrate_with_once():
    print("\n" + "=" * 70)
    print("WITH @once() - Reusing Single Connection")
    print("=" * 70)
    
    print("\n1st call:")
    db1 = get_database()
    
    print("\n2nd call:")
    db2 = get_database()
    
    print("\n3rd call:")
    db3 = get_database()
    
    print(f"\n✅ Solution: Only created 1 database connection, reused 3 times!")
    print(f"   db1 is db2: {db1 is db2}")  # True - same object!
    print(f"   db2 is db3: {db2 is db3}")  # True - same object!


# ============================================================================
# REAL-WORLD USAGE WITH FASTAPI
# ============================================================================

def demonstrate_fastapi_pattern():
    """
    This is how it's used in the App codebase with FastAPI.
    """
    print("\n" + "=" * 70)
    print("REAL-WORLD PATTERN (FastAPI + @once())")
    print("=" * 70)
    print()
    print("In FastAPI, you combine @once() with Depends():")
    print()
    print("  from fastapi import Depends")
    print()
    print("  @once()")
    print("  def get_database() -> Database:")
    print("      return Database()  # Created only once!")
    print()
    print("  @app.get('/users/{user_id}')")
    print("  def get_user(")
    print("      user_id: int,")
    print("      db: Database = Depends(get_database)")
    print("  ):")
    print("      return db.query(f'SELECT * FROM users WHERE id={user_id}')")
    print()
    print("Benefits:")
    print("  ✅ Database created only once (efficiency)")
    print("  ✅ Shared across all requests (resource reuse)")
    print("  ✅ FastAPI handles the injection (convenience)")
    print("  ✅ Easy to override in tests (testability)")


# ============================================================================
# MULTIPLE DEPENDENCIES EXAMPLE
# ============================================================================

class UserService:
    """Service that depends on multiple singletons."""
    
    def __init__(self, db: Database, cache: CacheService, email: EmailService):
        self.db = db
        self.cache = cache
        self.email = email


@once()
def get_user_service() -> UserService:
    """
    UserService depends on other singletons.
    All dependencies are created only once!
    """
    return UserService(
        db=get_database(),      # ♻️ Reuses existing database
        cache=get_cache(),      # ♻️ Reuses existing cache
        email=get_email()       # ♻️ Reuses existing email
    )


def demonstrate_dependency_chain():
    print("\n" + "=" * 70)
    print("DEPENDENCY CHAIN WITH @once()")
    print("=" * 70)
    
    print("\n1st UserService creation:")
    service1 = get_user_service()
    
    print("\n2nd UserService creation:")
    service2 = get_user_service()
    
    print("\n✅ Both services share the same underlying resources!")
    print(f"   Same database: {service1.db is service2.db}")
    print(f"   Same cache: {service1.cache is service2.cache}")
    print(f"   Same email: {service1.email is service2.email}")


# ============================================================================
# DEMONSTRATION
# ============================================================================

def main():
    print("=" * 70)
    print("SINGLETON PATTERN WITH @once() DECORATOR")
    print("=" * 70)
    print()
    print("Problem: Creating database connections is expensive!")
    print("Solution: Create once, reuse everywhere")
    
    # Show the problem
    demonstrate_without_once()
    
    # Show the solution
    demonstrate_with_once()
    
    # Show real-world pattern
    demonstrate_fastapi_pattern()
    
    # Show dependency chains
    demonstrate_dependency_chain()
    
    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)
    print()
    print("✅ Use @once() for expensive resources")
    print("   - Database connections")
    print("   - API clients")
    print("   - Configuration loading")
    print()
    print("✅ Combine with dependency injection")
    print("   - FastAPI's Depends() + @once() = Perfect combo")
    print()
    print("✅ Memory efficient")
    print("   - One instance instead of many")
    print()
    print("✅ Thread-safe in practice")
    print("   - FastAPI handles concurrency correctly")
    print()
    print("Next: See 06_real_world_example.py for a complete application ➡️")
    print("=" * 70)


if __name__ == "__main__":
    main()

