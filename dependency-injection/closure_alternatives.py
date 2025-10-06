"""
Alternative Ways to Achieve Closure-like Behavior
==================================================

Closures are one way to keep state. Here are 6 different approaches!
"""

from functools import wraps
from typing import Callable, TypeVar

T = TypeVar('T')


# ============================================================================
# METHOD 1: CLOSURE (What we've been using)
# ============================================================================

def once_with_closure():
    """Standard closure approach."""
    def decorator(func):
        cached_result = {}  # Closure variable
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'result' not in cached_result:
                print(f"   [CLOSURE] Creating {func.__name__}")
                cached_result['result'] = func(*args, **kwargs)
            return cached_result['result']
        return wrapper
    return decorator


@once_with_closure()
def get_db_closure():
    return {"connection": "postgres", "method": "closure"}


# ============================================================================
# METHOD 2: CLASS WITH __call__ (Callable Object)
# ============================================================================

class OnceCallable:
    """A class that acts like a decorator using __call__."""
    
    def __init__(self, func):
        self.func = func
        self.cached_result = None  # Instance variable
        self.called = False
        wraps(func)(self)  # Preserve function metadata
    
    def __call__(self, *args, **kwargs):
        """This makes the instance callable like a function."""
        if not self.called:
            print(f"   [CLASS] Creating {self.func.__name__}")
            self.cached_result = self.func(*args, **kwargs)
            self.called = True
        return self.cached_result


@OnceCallable
def get_db_class():
    return {"connection": "postgres", "method": "class"}


# ============================================================================
# METHOD 3: FUNCTION ATTRIBUTES (Store on function itself!)
# ============================================================================

def once_with_function_attribute():
    """Use the function object itself to store state."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Store cache directly on the wrapper function!
            if not hasattr(wrapper, '_cached_result'):
                print(f"   [FUNC ATTR] Creating {func.__name__}")
                wrapper._cached_result = func(*args, **kwargs)
            return wrapper._cached_result
        return wrapper
    return decorator


@once_with_function_attribute()
def get_db_function_attr():
    return {"connection": "postgres", "method": "function_attribute"}


# ============================================================================
# METHOD 4: CLASS AS DECORATOR (More Explicit)
# ============================================================================

class OnceDecorator:
    """A decorator class with explicit __init__ and __call__."""
    
    def __init__(self, func):
        """Called when decorating the function."""
        self.func = func
        self.cache = {}
        wraps(func)(self)
    
    def __call__(self, *args, **kwargs):
        """Called when the decorated function is called."""
        if 'result' not in self.cache:
            print(f"   [DECORATOR CLASS] Creating {self.func.__name__}")
            self.cache['result'] = self.func(*args, **kwargs)
        return self.cache['result']


@OnceDecorator
def get_db_decorator_class():
    return {"connection": "postgres", "method": "decorator_class"}


# ============================================================================
# METHOD 5: GLOBAL DICTIONARY (Not recommended, but works)
# ============================================================================

_global_cache = {}

def once_with_global(func):
    """Using a global dictionary."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = func.__name__
        if key not in _global_cache:
            print(f"   [GLOBAL] Creating {func.__name__}")
            _global_cache[key] = func(*args, **kwargs)
        return _global_cache[key]
    return wrapper


@once_with_global
def get_db_global():
    return {"connection": "postgres", "method": "global"}


# ============================================================================
# METHOD 6: USING MUTABLE DEFAULT ARGUMENT (Hacky but interesting!)
# ============================================================================

def once_with_default_arg():
    """Using mutable default argument (Python quirk)."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, _cache={}):  # Default arg created once!
            if 'result' not in _cache:
                print(f"   [DEFAULT ARG] Creating {func.__name__}")
                _cache['result'] = func(*args)
            return _cache['result']
        return wrapper
    return decorator


@once_with_default_arg()
def get_db_default_arg():
    return {"connection": "postgres", "method": "default_arg"}


# ============================================================================
# METHOD 7: PROPERTY-LIKE PATTERN (Descriptor Protocol)
# ============================================================================

class CachedProperty:
    """Like @property but caches the result."""
    
    def __init__(self, func):
        self.func = func
        self.cache_name = f'_cached_{func.__name__}'
    
    def __get__(self, obj, objtype=None):
        """Called when accessing the attribute."""
        if obj is None:
            return self
        
        # Check if cached on the object
        if not hasattr(obj, self.cache_name):
            print(f"   [DESCRIPTOR] Creating {self.func.__name__}")
            result = self.func(obj)
            setattr(obj, self.cache_name, result)
        
        return getattr(obj, self.cache_name)


class DatabaseManager:
    """Example class using CachedProperty."""
    
    @CachedProperty
    def connection(self):
        return {"connection": "postgres", "method": "descriptor"}


# ============================================================================
# DEMONSTRATION AND COMPARISON
# ============================================================================

def demo_all_methods():
    print("=" * 70)
    print("7 WAYS TO ACHIEVE CLOSURE-LIKE BEHAVIOR")
    print("=" * 70)
    
    # Method 1: Closure
    print("\n1️⃣  METHOD 1: CLOSURE (Standard approach)")
    print("-" * 70)
    db1a = get_db_closure()
    db1b = get_db_closure()  # Should not print "Creating"
    print(f"   Same object: {db1a is db1b}")
    print(f"   Result: {db1a}")
    
    # Method 2: Callable Class
    print("\n2️⃣  METHOD 2: CLASS WITH __call__")
    print("-" * 70)
    db2a = get_db_class()
    db2b = get_db_class()
    print(f"   Same object: {db2a is db2b}")
    print(f"   Result: {db2a}")
    print(f"   Type of decorator: {type(get_db_class)}")  # It's a class instance!
    
    # Method 3: Function Attributes
    print("\n3️⃣  METHOD 3: FUNCTION ATTRIBUTES")
    print("-" * 70)
    db3a = get_db_function_attr()
    db3b = get_db_function_attr()
    print(f"   Same object: {db3a is db3b}")
    print(f"   Result: {db3a}")
    print(f"   Cached on function: {hasattr(get_db_function_attr, '_cached_result')}")
    
    # Method 4: Decorator Class
    print("\n4️⃣  METHOD 4: DECORATOR CLASS")
    print("-" * 70)
    db4a = get_db_decorator_class()
    db4b = get_db_decorator_class()
    print(f"   Same object: {db4a is db4b}")
    print(f"   Result: {db4a}")
    
    # Method 5: Global Dictionary
    print("\n5️⃣  METHOD 5: GLOBAL DICTIONARY")
    print("-" * 70)
    db5a = get_db_global()
    db5b = get_db_global()
    print(f"   Same object: {db5a is db5b}")
    print(f"   Result: {db5a}")
    print(f"   Global cache: {_global_cache}")
    
    # Method 6: Default Argument
    print("\n6️⃣  METHOD 6: MUTABLE DEFAULT ARGUMENT")
    print("-" * 70)
    db6a = get_db_default_arg()
    db6b = get_db_default_arg()
    print(f"   Same object: {db6a is db6b}")
    print(f"   Result: {db6a}")
    
    # Method 7: Descriptor
    print("\n7️⃣  METHOD 7: DESCRIPTOR PROTOCOL")
    print("-" * 70)
    manager = DatabaseManager()
    db7a = manager.connection
    db7b = manager.connection
    print(f"   Same object: {db7a is db7b}")
    print(f"   Result: {db7a}")


# ============================================================================
# COMPARISON TABLE
# ============================================================================

def show_comparison():
    print("\n" + "=" * 70)
    print("COMPARISON OF METHODS")
    print("=" * 70)
    print()
    
    print("┌─────────────────────┬──────────┬──────────┬──────────────────┐")
    print("│ Method              │ Clean?   │ Popular? │ Use Case         │")
    print("├─────────────────────┼──────────┼──────────┼──────────────────┤")
    print("│ 1. Closure          │ ✅ Yes   │ ⭐⭐⭐   │ General purpose  │")
    print("│ 2. Callable Class   │ ✅ Yes   │ ⭐⭐⭐   │ Need state       │")
    print("│ 3. Function Attr    │ ⚠️  Okay  │ ⭐       │ Quick & dirty    │")
    print("│ 4. Decorator Class  │ ✅ Yes   │ ⭐⭐     │ Complex logic    │")
    print("│ 5. Global Dict      │ ❌ No    │ ⭐       │ Simple scripts   │")
    print("│ 6. Default Arg      │ ⚠️  Hacky │ ⭐       │ Python quirk     │")
    print("│ 7. Descriptor       │ ✅ Yes   │ ⭐⭐     │ Class properties │")
    print("└─────────────────────┴──────────┴──────────┴──────────────────┘")


# ============================================================================
# DETAILED PROS/CONS
# ============================================================================

def show_pros_cons():
    print("\n" + "=" * 70)
    print("PROS & CONS OF EACH METHOD")
    print("=" * 70)
    
    methods = [
        {
            "name": "1. CLOSURE",
            "pros": ["Standard Python pattern", "Clean syntax", "Good encapsulation"],
            "cons": ["Can be confusing for beginners"],
            "when": "Default choice for most cases"
        },
        {
            "name": "2. CALLABLE CLASS (__call__)",
            "pros": ["Explicit state management", "Easy to understand", "Can add more methods"],
            "cons": ["More verbose", "Slightly more memory"],
            "when": "When you need complex state or multiple methods"
        },
        {
            "name": "3. FUNCTION ATTRIBUTES",
            "pros": ["Simple", "No closure needed", "Can inspect cache"],
            "cons": ["Feels hacky", "Not common pattern"],
            "when": "Quick prototyping"
        },
        {
            "name": "4. DECORATOR CLASS",
            "pros": ["Very explicit", "Object-oriented", "Easy to extend"],
            "cons": ["More code", "Overkill for simple cases"],
            "when": "Complex decorator logic"
        },
        {
            "name": "5. GLOBAL DICTIONARY",
            "pros": ["Simple to understand", "Easy to debug"],
            "cons": ["Pollutes namespace", "Not thread-safe", "Hard to test"],
            "when": "Simple scripts only"
        },
        {
            "name": "6. DEFAULT ARGUMENT",
            "pros": ["Clever Python trick", "No closure"],
            "cons": ["Confusing", "Easy to misuse", "Not recommended"],
            "when": "Don't use this! Just for learning"
        },
        {
            "name": "7. DESCRIPTOR PROTOCOL",
            "pros": ["Powerful", "Property-like", "Django uses this"],
            "cons": ["Complex", "Only works in classes"],
            "when": "Class attributes that need lazy initialization"
        }
    ]
    
    for method in methods:
        print(f"\n{method['name']}")
        print("─" * 70)
        print("✅ Pros:")
        for pro in method['pros']:
            print(f"   • {pro}")
        print("❌ Cons:")
        for con in method['cons']:
            print(f"   • {con}")
        print(f"💡 When to use: {method['when']}")


# ============================================================================
# RECOMMENDATION
# ============================================================================

def show_recommendation():
    print("\n" + "=" * 70)
    print("RECOMMENDATION")
    print("=" * 70)
    print()
    print("For most cases, choose between:")
    print()
    print("🥇 CLOSURE (Method 1)")
    print("   @once()")
    print("   def get_database():")
    print("       return Database()")
    print()
    print("   ✅ Standard Python pattern")
    print("   ✅ Clean and concise")
    print("   ✅ What most developers expect")
    print()
    print("🥈 CALLABLE CLASS (Method 2)")
    print("   @OnceCallable")
    print("   def get_database():")
    print("       return Database()")
    print()
    print("   ✅ More explicit")
    print("   ✅ Easier to understand for OOP developers")
    print("   ✅ Can add more functionality easily")
    print()
    print("🎯 Bottom line: Use CLOSURE for simplicity,")
    print("   use CALLABLE CLASS for clarity and extensibility.")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 70)
    print("ALTERNATIVE WAYS TO ACHIEVE CLOSURE BEHAVIOR")
    print("=" * 70)
    print()
    print("Question: Are there other ways to do closures?")
    print("Answer: Yes! Here are 7 different approaches:")
    
    demo_all_methods()
    show_comparison()
    show_pros_cons()
    show_recommendation()
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("All 7 methods work! They all achieve the same result:")
    print("  ✅ Call function once")
    print("  ✅ Cache the result")
    print("  ✅ Return cached result on subsequent calls")
    print()
    print("The difference is HOW they store the cached result:")
    print("  1. Closure variable (most common)")
    print("  2. Class instance variable")
    print("  3. Function attribute")
    print("  4. Class with __call__")
    print("  5. Global dictionary")
    print("  6. Default argument (mutable)")
    print("  7. Descriptor protocol")
    print()
    print("Choose based on your needs and coding style! 🎉")
    print("=" * 70)


if __name__ == "__main__":
    main()

