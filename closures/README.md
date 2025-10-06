# Python Closures

Understanding closures in Python - how functions can capture and remember variables from their enclosing scope.

## What's a Closure?

A closure is a function that remembers values from its enclosing scope, even after that scope has finished executing. This is a fundamental concept in Python that powers decorators, callbacks, and many design patterns.

## Files in This Directory

### `closure_explained.py`
Comprehensive explanation of how closures work in Python:
- Step-by-step examples from simple to complex
- Understanding variable scoping and persistence
- How `@once()` and `@lru_cache` use closures internally
- Visual explanations of memory and scope

**Run it**: `python closure_explained.py`

### `closure_alternatives.py`
Different approaches to achieve closure-like behavior:
- Method 1: Closures (standard approach)
- Method 2: Class-based state
- Method 3: Function attributes
- Method 4: Global variables (not recommended)
- Method 5: Mutable default arguments (dangerous!)
- Method 6: `functools.partial`

**Run it**: `python closure_alternatives.py`

## Quick Example

```python
def create_counter():
    count = 0  # This variable is "captured" by the closure
    
    def increment():
        nonlocal count  # Access the captured variable
        count += 1
        return count
    
    return increment

# The counter remembers its state!
counter = create_counter()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
```

## Why Learn Closures?

Closures are essential for understanding:
- **Decorators** - How `@decorator` syntax works
- **Callbacks** - Functions that remember context
- **Functional programming** - Higher-order functions
- **State management** - Encapsulating private state
- **Dependency injection** - Singleton patterns like `@once()`

## Related Topics

See the `dependency-injection/` directory for practical applications of closures in:
- Singleton patterns with `@once()` decorator
- Comparing `@lru_cache` vs custom decorators
- FastAPI dependency injection

## Resources

- [Python Closures Documentation](https://docs.python.org/3/reference/datamodel.html#function-objects)
- [PEP 227 - Statically Nested Scopes](https://www.python.org/dev/peps/pep-0227/)

