"""
Why Not Use functools.lru_cache Instead of @once()?
====================================================

Python's standard library has lru_cache which does similar things.
Let's explore why you can't use lru_cache for the singleton pattern.
"""

from functools import lru_cache, wraps
from typing import Callable, TypeVar

# ============================================================================
# COMPARISON: lru_cache vs @once()
# ============================================================================

T = TypeVar('T')

def once() -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Custom @once() decorator for singleton pattern."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cached_result: dict = {}
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            if 'result' not in cached_result:
                print(f"   @once: Creating {func.__name__}")
                cached_result['result'] = func(*args, **kwargs)
            else:
                print(f"   @once: Reusing cached {func.__name__}")
            return cached_result['result']
        return wrapper
    return decorator


class Database:
    def __init__(self, name: str):
        self.name = name
        print(f"      💾 Database '{name}' created")


# ============================================================================
# APPROACH 1: Using lru_cache (Built-in Python)
# ============================================================================

@lru_cache(maxsize=None)
def get_database_with_lru_cache():
    """Using Python's built-in lru_cache."""
    return Database("lru_cache_db")


def demo_lru_cache():
    print("\n" + "=" * 70)
    print("APPROACH 1: Using @lru_cache (Built-in)")
    print("=" * 70)
    
    print("\n1st call:")
    db1 = get_database_with_lru_cache()
    
    print("\n2nd call:")
    db2 = get_database_with_lru_cache()
    
    print(f"\n✅ Same object: {db1 is db2}")
    print("✅ Works great for simple cases!")


# ============================================================================
# APPROACH 2: Using @once() (Custom)
# ============================================================================

@once()
def get_database_with_once():
    """Using custom @once() decorator."""
    return Database("once_db")


def demo_once():
    print("\n" + "=" * 70)
    print("APPROACH 2: Using @once() (Custom)")
    print("=" * 70)
    
    print("\n1st call:")
    db1 = get_database_with_once()
    
    print("\n2nd call:")
    db2 = get_database_with_once()
    
    print(f"\n✅ Same object: {db1 is db2}")
    print("✅ Simpler, more explicit!")


# ============================================================================
# PROBLEM 1: lru_cache caches based on arguments!
# ============================================================================

@lru_cache(maxsize=None)
def get_database_with_args(connection_string: str):
    """This creates DIFFERENT caches for DIFFERENT arguments!"""
    return Database(connection_string)


def demo_problem_with_lru_cache():
    print("\n" + "=" * 70)
    print("PROBLEM 1: lru_cache Caches Based on Arguments")
    print("=" * 70)
    
    print("\nCall with 'postgres':")
    db1 = get_database_with_args("postgres")
    
    print("\nCall with 'postgres' again:")
    db2 = get_database_with_args("postgres")
    print(f"Same object: {db1 is db2} ✅")
    
    print("\nCall with 'mysql':")
    db3 = get_database_with_args("mysql")
    print(f"Same as postgres db: {db1 is db3} ❌")
    
    print("\n⚠️  lru_cache creates SEPARATE caches per argument combination!")
    print("   This might not be what you want for singletons.")


# ============================================================================
# PROBLEM 2: lru_cache cache info and clearing
# ============================================================================

def demo_lru_cache_extras():
    print("\n" + "=" * 70)
    print("PROBLEM 2: lru_cache Has Extra Features You Might Not Need")
    print("=" * 70)
    
    # Clear cache
    get_database_with_lru_cache.cache_clear()
    
    # Cache info
    print("\n📊 Cache info:")
    info = get_database_with_lru_cache.cache_info()
    print(f"   Hits: {info.hits}")
    print(f"   Misses: {info.misses}")
    print(f"   Size: {info.currsize}")
    print(f"   Max size: {info.maxsize}")
    
    print("\n✅ Great for debugging!")
    print("⚠️  But might be overkill for simple singleton pattern")


# ============================================================================
# WHY USE A CUSTOM @once() DECORATOR
# ============================================================================

def explain_rationale():
    print("\n" + "=" * 70)
    print("WHY CREATE A CUSTOM @once() DECORATOR")
    print("=" * 70)
    print()
    
    print("Reasons to create custom @once() decorator:")
    print()
    
    print("1️⃣  SIMPLICITY")
    print("   @once() - Clear intent: 'call once, cache forever'")
    print("   @lru_cache(maxsize=None) - Less clear, more configuration")
    print()
    
    print("2️⃣  NO ARGUMENT CACHING")
    print("   @once() - Always returns same instance, ignores args")
    print("   @lru_cache - Creates separate caches per argument combo")
    print("   For singletons, you want ONE instance, period!")
    print()
    
    print("3️⃣  MINIMAL OVERHEAD")
    print("   @once() - Simple dict lookup, minimal memory")
    print("   @lru_cache - More complex, tracks hits/misses/size")
    print()
    
    print("4️⃣  EXPLICIT SEMANTICS")
    print("   @once() - Name clearly states intent")
    print("   @lru_cache - Designed for caching, not singletons")
    print()
    
    print("5️⃣  FASTAPI INTEGRATION")
    print("   Works perfectly with Depends() without surprises")
    print("   No unexpected cache clearing or size limits")
    print()


# ============================================================================
# ALTERNATIVE: Using @lru_cache for FastAPI
# ============================================================================

def demo_fastapi_with_lru_cache():
    print("\n" + "=" * 70)
    print("USING lru_cache WITH FASTAPI (It Works!)")
    print("=" * 70)
    print()
    
    print("You CAN use lru_cache with FastAPI:")
    print()
    print("  from functools import lru_cache")
    print("  from fastapi import Depends")
    print()
    print("  @lru_cache(maxsize=None)")
    print("  def get_database() -> Database:")
    print("      return Database()")
    print()
    print("  @app.get('/users')")
    print("  def get_users(db: Database = Depends(get_database)):")
    print("      return db.query('SELECT * FROM users')")
    print()
    print("✅ This works perfectly fine!")
    print()
    print("So why @once()?")
    print("  - More explicit name")
    print("  - Team preference")
    print("  - Avoids potential confusion")
    print("  - Custom behavior if needed later")


# ============================================================================
# OTHER PYTHON LIBRARIES
# ============================================================================

def show_other_libraries():
    print("\n" + "=" * 70)
    print("OTHER PYTHON LIBRARIES FOR SINGLETONS")
    print("=" * 70)
    print()
    
    print("1. INJECTOR (Dependency Injection Library)")
    print("   pip install injector")
    print("   from injector import singleton, Injector")
    print()
    
    print("2. DEPENDENCY-INJECTOR")
    print("   pip install dependency-injector")
    print("   from dependency_injector import containers, providers")
    print()
    
    print("3. PYTHON-INJECT")
    print("   pip install inject")
    print()
    
    print("But for FastAPI, @once() or @lru_cache is simpler!")


# ============================================================================
# RECOMMENDATION
# ============================================================================

def recommendation():
    print("\n" + "=" * 70)
    print("RECOMMENDATION: WHAT SHOULD YOU USE?")
    print("=" * 70)
    print()
    
    print("For FastAPI Dependency Injection:")
    print()
    print("✅ USE @lru_cache(maxsize=None) - It's built-in!")
    print("   from functools import lru_cache")
    print()
    print("   @lru_cache(maxsize=None)")
    print("   def get_database() -> Database:")
    print("       return Database()")
    print()
    
    print("✅ OR create simple @once() - If you prefer explicit naming")
    print()
    
    print("❌ DON'T use complex DI frameworks - Overkill for FastAPI")
    print("   FastAPI's Depends() is already excellent!")
    print()
    
    print("🎯 Bottom line: Both work! Choose based on team preference.")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 70)
    print("WHY NOT USE PYTHON'S BUILT-IN lru_cache?")
    print("=" * 70)
    
    demo_lru_cache()
    demo_once()
    demo_problem_with_lru_cache()
    demo_lru_cache_extras()
    explain_rationale()
    demo_fastapi_with_lru_cache()
    show_other_libraries()
    recommendation()
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("✅ Python HAS @lru_cache - works great!")
    print("✅ @once() is simpler and more explicit")
    print("✅ Both work perfectly with FastAPI")
    print("✅ @once() provides clarity and explicit intent")
    print()
    print("Use whichever you prefer! 🎉")
    print("=" * 70)


if __name__ == "__main__":
    main()

