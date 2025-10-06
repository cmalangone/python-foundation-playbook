"""
Understanding Closures: Why the 'cached' Variable Persists
===========================================================

This explains how @once() and @lru_cache work under the hood.
The key concept is CLOSURES.
"""

from functools import wraps
from typing import Callable, TypeVar

# ============================================================================
# STEP 1: Understanding Closures (Simple Example)
# ============================================================================

def create_counter():
    """This function creates a counter that remembers its count."""
    count = 0  # This variable is created in this function's scope
    
    def increment():
        nonlocal count  # Access the outer function's variable
        count += 1
        return count
    
    return increment  # Return the INNER function


def demo_simple_closure():
    print("=" * 70)
    print("STEP 1: Understanding Closures")
    print("=" * 70)
    print()
    print("What is a closure?")
    print("A closure is when an inner function 'remembers' variables")
    print("from its outer function, even after the outer function returns.")
    print()
    
    # Create a counter
    counter = create_counter()
    
    print("🔍 What just happened:")
    print("   1. create_counter() was called")
    print("   2. count = 0 was created")
    print("   3. increment() function was created")
    print("   4. create_counter() FINISHED and returned increment()")
    print()
    print("❓ Question: Is 'count' lost?")
    print("   NO! increment() 'closes over' count - it remembers it!")
    print()
    
    # Use the counter
    print("Calling counter():")
    print(f"   1st call: {counter()}")  # 1
    print(f"   2nd call: {counter()}")  # 2
    print(f"   3rd call: {counter()}")  # 3
    print()
    print("✅ The 'count' variable is still alive!")
    print("   It's stored in the closure of increment()")


# ============================================================================
# STEP 2: Looking at @once() Internals
# ============================================================================

T = TypeVar('T')

def once() -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Let's trace exactly what happens."""
    print("\n🔧 once() decorator factory is being CALLED")
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        print(f"🔧 decorator() is wrapping {func.__name__}")
        
        # ⭐ THIS IS THE KEY! This variable is created ONCE
        cached_result: dict = {}
        print(f"   📦 Created cached_result dict: {id(cached_result)}")
        
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            print(f"   🎯 wrapper() called, checking cached_result {id(cached_result)}")
            
            if 'result' not in cached_result:
                print(f"      ➡️  Cache MISS - calling {func.__name__}")
                cached_result['result'] = func(*args, **kwargs)
            else:
                print(f"      ➡️  Cache HIT - returning cached value")
            
            return cached_result['result']
        
        print(f"   ✅ Returning wrapper function")
        print(f"   🔒 wrapper 'closes over' cached_result")
        return wrapper
    
    return decorator


def demo_once_internals():
    print("\n" + "=" * 70)
    print("STEP 2: How @once() Works with Closures")
    print("=" * 70)
    
    @once()
    def get_database():
        print("         💾 Creating database...")
        return {"connection": "postgres"}
    
    print("\n📍 Decoration complete! Function is ready to use.")
    print()
    print("Now let's call get_database() multiple times:")
    print()
    
    print("1st call:")
    db1 = get_database()
    
    print("\n2nd call:")
    db2 = get_database()
    
    print("\n3rd call:")
    db3 = get_database()
    
    print(f"\n✅ All three calls returned the same object:")
    print(f"   db1 is db2: {db1 is db2}")
    print(f"   db2 is db3: {db2 is db3}")


# ============================================================================
# STEP 3: Visualizing the Closure
# ============================================================================

def visualize_closure():
    print("\n" + "=" * 70)
    print("STEP 3: Visualizing the Closure")
    print("=" * 70)
    print()
    print("Here's what's in memory:")
    print()
    print("┌─────────────────────────────────────────────────────────┐")
    print("│  OUTER SCOPE (decorator function)                       │")
    print("│                                                          │")
    print("│  cached_result = {}  ← Created once when decorating     │")
    print("│                                                          │")
    print("│  ┌───────────────────────────────────────────────────┐  │")
    print("│  │  INNER SCOPE (wrapper function)                   │  │")
    print("│  │                                                    │  │")
    print("│  │  def wrapper(*args, **kwargs):                    │  │")
    print("│  │      if 'result' not in cached_result:  ← Access!│  │")
    print("│  │          cached_result['result'] = ...            │  │")
    print("│  │      return cached_result['result']               │  │")
    print("│  │                                                    │  │")
    print("│  └───────────────────────────────────────────────────┘  │")
    print("│           ↑                                              │")
    print("│           └── This function 'closes over' cached_result │")
    print("└─────────────────────────────────────────────────────────┘")
    print()
    print("Key points:")
    print("  ✅ cached_result is created ONCE (when decorator runs)")
    print("  ✅ wrapper 'remembers' cached_result via closure")
    print("  ✅ cached_result stays alive as long as wrapper exists")
    print("  ✅ Every call to wrapper sees the SAME cached_result")


# ============================================================================
# STEP 4: What if we DON'T use closure? (Wrong way)
# ============================================================================

def once_wrong():
    """WRONG: Creating cache inside wrapper - won't work!"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # ❌ BAD: Creating new dict every time!
            cached_result = {}
            
            if 'result' not in cached_result:
                print("      Creating (every time!)")
                cached_result['result'] = func(*args, **kwargs)
            return cached_result['result']
        return wrapper
    return decorator


def demo_wrong_approach():
    print("\n" + "=" * 70)
    print("STEP 4: What if we DON'T use closure? (WRONG)")
    print("=" * 70)
    print()
    
    @once_wrong()
    def get_database():
        return {"connection": "postgres"}
    
    print("Calling get_database() three times:")
    db1 = get_database()
    db2 = get_database()
    db3 = get_database()
    
    print(f"\n❌ Problem: Different objects every time!")
    print(f"   db1 is db2: {db1 is db2}")
    print(f"   db2 is db3: {db2 is db3}")
    print()
    print("Why? Because cached_result is created INSIDE wrapper,")
    print("so it's recreated on every call!")


# ============================================================================
# STEP 5: Inspecting the Closure
# ============================================================================

def inspect_closure():
    print("\n" + "=" * 70)
    print("STEP 5: Python's Closure Internals")
    print("=" * 70)
    print()
    
    def once_simple():
        def decorator(func):
            cached_result = {}  # Closure variable
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                if 'result' not in cached_result:
                    cached_result['result'] = func(*args, **kwargs)
                return cached_result['result']
            return wrapper
        return decorator
    
    @once_simple()
    def get_database():
        return {"connection": "postgres"}
    
    # Python stores closure variables in __closure__
    print("🔍 Inspecting get_database.__closure__:")
    print(f"   Closure: {get_database.__closure__}")
    print()
    
    if get_database.__closure__:
        print(f"   Number of closed-over variables: {len(get_database.__closure__)}")
        print()
        print("   Closed-over variables:")
        for i, cell in enumerate(get_database.__closure__):
            print(f"      {i}: {cell.cell_contents}")
            print(f"         Type: {type(cell.cell_contents)}")
            if isinstance(cell.cell_contents, dict):
                print(f"         Contents: {cell.cell_contents}")
    
    print()
    print("✅ Python stores the closure variables in the function object!")


# ============================================================================
# STEP 6: Comparing to Global Variables (Alternative)
# ============================================================================

# Global cache (alternative approach - not recommended)
_global_cache = {}

def get_database_global():
    """Using global variable instead of closure."""
    if 'result' not in _global_cache:
        print("Creating with global cache...")
        _global_cache['result'] = {"connection": "postgres"}
    return _global_cache['result']


def demo_global_alternative():
    print("\n" + "=" * 70)
    print("STEP 6: Alternative - Global Variables")
    print("=" * 70)
    print()
    print("You COULD use a global variable instead of closure:")
    print()
    print("  _global_cache = {}  # Module-level variable")
    print()
    print("  def get_database():")
    print("      if 'result' not in _global_cache:")
    print("          _global_cache['result'] = Database()")
    print("      return _global_cache['result']")
    print()
    print("This works, but:")
    print("  ❌ Pollutes global namespace")
    print("  ❌ Can be accessed/modified from anywhere")
    print("  ❌ Harder to have multiple caches")
    print("  ✅ Closures are better - encapsulation!")


# ============================================================================
# MAIN DEMO
# ============================================================================

def main():
    print("=" * 70)
    print("UNDERSTANDING CLOSURES: Why 'cached' Persists")
    print("=" * 70)
    print()
    print("Your question: Why isn't the cached variable lost?")
    print("Answer: CLOSURES! Let's see how they work...")
    
    # Run all demos
    demo_simple_closure()
    demo_once_internals()
    visualize_closure()
    demo_wrong_approach()
    inspect_closure()
    demo_global_alternative()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: The Magic of Closures")
    print("=" * 70)
    print()
    print("When you write:")
    print()
    print("  def decorator(func):")
    print("      cached_result = {}  ← Created ONCE")
    print()
    print("      def wrapper():")
    print("          cached_result['x'] = ...  ← Remembers it!")
    print()
    print("      return wrapper")
    print()
    print("What happens:")
    print("  1️⃣  decorator() runs ONCE (during @decoration)")
    print("  2️⃣  cached_result is created ONCE")
    print("  3️⃣  wrapper() is created and 'closes over' cached_result")
    print("  4️⃣  decorator() returns wrapper")
    print("  5️⃣  decorator() scope ends BUT...")
    print("  6️⃣  cached_result stays alive! (closure keeps it)")
    print("  7️⃣  Every call to wrapper() sees the SAME cached_result")
    print()
    print("✅ This is why caching works!")
    print("✅ This is the power of closures!")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()

