"""
Quick Comparison: @lru_cache vs @once()
========================================

Both work! Choose based on preference.
"""

from functools import lru_cache, wraps
from typing import Callable, TypeVar

# ============================================================================
# OPTION 1: USE PYTHON'S BUILT-IN lru_cache
# ============================================================================

@lru_cache(maxsize=None)
def get_database_builtin():
    """Using Python's standard library - NO custom code needed!"""
    print("Creating database with lru_cache...")
    return {"connection": "postgres://localhost:5432"}


# ============================================================================
# OPTION 2: SIMPLE CUSTOM @once()
# ============================================================================

T = TypeVar('T')

def once() -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Dead simple singleton decorator - 10 lines of code."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cached = {}
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            if 'result' not in cached:
                cached['result'] = func(*args, **kwargs)
            return cached['result']
        return wrapper
    return decorator


@once()
def get_database_custom():
    """Using custom @once() - clear and explicit."""
    print("Creating database with @once()...")
    return {"connection": "postgres://localhost:5432"}


# ============================================================================
# BOTH WORK THE SAME WAY
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("COMPARISON: Both approaches work identically!")
    print("=" * 70)
    
    # Test lru_cache
    print("\n📦 Using @lru_cache (built-in):")
    db1 = get_database_builtin()
    db2 = get_database_builtin()  # Cached!
    print(f"   Same object: {db1 is db2}")
    
    # Test @once()
    print("\n🔧 Using @once() (custom):")
    db3 = get_database_custom()
    db4 = get_database_custom()  # Cached!
    print(f"   Same object: {db3 is db4}")
    
    print("\n" + "=" * 70)
    print("VERDICT: Use whichever you prefer!")
    print("=" * 70)
    print()
    print("✅ @lru_cache - Already in Python, no code to write")
    print("✅ @once() - More explicit name, simpler implementation")
    print()
    print("Both are perfectly valid choices! 🎉")

