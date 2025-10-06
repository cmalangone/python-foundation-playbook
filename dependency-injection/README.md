# 🎯 Dependency Injection Tutorial

A comprehensive, hands-on guide to understanding **Dependency Injection** in Python

## 📚 What is Dependency Injection?

**Simple Definition**: Don't create what you need inside a class—ask for it from outside.

```python
# ❌ BAD: Class creates its own dependencies
class PizzaShop:
    def __init__(self):
        self.db = Database()  # Hard-coded!

# ✅ GOOD: Dependencies are provided (injected)
class PizzaShop:
    def __init__(self, db: Database):
        self.db = db  # Injected!
```

## 🎓 Learning Path

Work through the examples in order:

### 1️⃣ **01_without_di.py** - The Problem
- Shows why creating dependencies inside classes is problematic
- Demonstrates tight coupling issues
- Highlights testing difficulties

**Run it:**
```bash
python 01_without_di.py
```

### 2️⃣ **02_with_di_basic.py** - The Solution
- Introduces dependency injection pattern
- Shows how to inject dependencies through constructors
- Demonstrates loose coupling benefits

**Run it:**
```bash
python 02_with_di_basic.py
```

### 3️⃣ **03_with_di_testing.py** - Testing Benefits
- Shows how DI makes testing easy
- Demonstrates fake/mock dependencies
- Compares testing with and without DI

**Run it:**
```bash
python 03_with_di_testing.py
```

### 4️⃣ **04_fastapi_di.py** - FastAPI Integration
- Shows FastAPI's automatic dependency injection
- Demonstrates `Depends()` function
- Shows dependency chains

**Run it:**
```bash
pip install fastapi uvicorn
python 04_fastapi_di.py
# Visit http://localhost:8000/docs
```

### 5️⃣ **05_singleton_pattern.py** - The @once() Decorator
- Implements singleton pattern for expensive resources
- Shows how to create resources only once
- Demonstrates resource reuse

**Run it:**
```bash
python 05_singleton_pattern.py
```

### 6️⃣ **06_real_world_example.py** - Complete Application
- Brings all concepts together
- Multi-layer architecture (Infrastructure → Application → API)

**Run it:**
```bash
python 06_real_world_example.py
```

## 🔑 Key Concepts

### Constructor Injection
```python
class UserService:
    def __init__(self, db: Database, email: EmailService):
        self.db = db        # Injected
        self.email = email  # Injected
```

### Dependency Provider Functions
```python
def get_database() -> Database:
    return Database()

def get_user_service(
    db: Database = Depends(get_database)
) -> UserService:
    return UserService(db)
```

### Singleton Pattern
```python
@once()
def get_database() -> Database:
    return Database()  # Created only once!

db1 = get_database()  # Creates database
db2 = get_database()  # Reuses existing database
assert db1 is db2     # True!
```

## 🎨 Visual Architecture

```
┌─────────────────────────────────────────┐
│         Application Layer               │
│    (Business Logic / Services)          │
│                                          │
│  UserService    DatasetService           │
│      ↓               ↓                   │
└──────┼───────────────┼───────────────────┘
       │               │
┌──────┼───────────────┼───────────────────┐
│      ↓               ↓                   │
│  Infrastructure Layer                    │
│  (External Services)                     │
│                                          │
│  Database  OpenSearch  S3  Email         │
└──────────────────────────────────────────┘

Dependencies flow: Infrastructure → Application → API
```

## ✅ Benefits of Dependency Injection

### 1. **Testability**
```python
# Production: Use real database
service = UserService(RealDatabase())

# Testing: Use fake database
service = UserService(FakeDatabase())
```

### 2. **Flexibility**
```python
# Easy to swap implementations
service = UserService(PostgresDatabase())  # Use PostgreSQL
service = UserService(MySQLDatabase())     # Or MySQL
```

### 3. **Reusability**
```python
# Share expensive resources
db = Database()
service1 = UserService(db)  # Share same DB
service2 = AdminService(db) # connection
```

### 4. **Loose Coupling**
```python
# UserService doesn't know or care
# what specific database is used
class UserService:
    def __init__(self, db: DatabaseInterface):
        self.db = db  # Any database that implements the interface!
```

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.10+
python --version

# Optional: For FastAPI example
pip install fastapi uvicorn
```

### Run All Examples
```bash
cd /Users/cinziamalangone/personal/python-foundation-playbook/dependency-injection

# Basic examples
python 01_without_di.py
python 02_with_di_basic.py
python 03_with_di_testing.py
python 05_singleton_pattern.py
python 06_real_world_example.py

# FastAPI example (requires installation)
python 04_fastapi_di.py
```

### Run Tests
```bash
python tests/test_di_examples.py
```

## 📖 Real-World Usage

### Example 

```python
# commons/api/dependencies.py

from commons.utils.once import once
from fastapi import Depends

@once()
def get_database() -> Database:
    """Singleton database connection"""
    return Database("postgresql://...")

@once()
def get_search_client() -> OpenSearch:
    """Singleton search client"""
    return OpenSearch("https://...")

@once()
def get_dataset_provider(
    db: Database = Depends(get_database),
    search: OpenSearch = Depends(get_search_client)
) -> DatasetProvider:
    """Dataset service with injected dependencies"""
    return DatasetProvider(db, search)

# In route handler:
@app.post("/datasets")
def create_dataset(
    dataset: dict,
    provider: DatasetProvider = Depends(get_dataset_provider)
):
    return provider.create_dataset(dataset)
```

## 🎯 Common Patterns

### Pattern 1: Constructor Injection (Most Common)
```python
class Service:
    def __init__(self, dependency: Dependency):
        self.dependency = dependency
```

### Pattern 2: Factory Functions
```python
def create_service(dependency: Dependency) -> Service:
    return Service(dependency)
```

### Pattern 3: Singleton with @once()
```python
@once()
def get_service() -> Service:
    return Service()  # Created once, reused forever
```

### Pattern 4: Dependency Chains
```python
def get_service_a() -> ServiceA:
    return ServiceA()

def get_service_b(a: ServiceA = Depends(get_service_a)) -> ServiceB:
    return ServiceB(a)  # ServiceB depends on ServiceA
```

## 📝 Summary

| Without DI | With DI |
|------------|---------|
| ❌ Hard to test | ✅ Easy to test |
| ❌ Tight coupling | ✅ Loose coupling |
| ❌ Hard to reuse | ✅ Easy to reuse |
| ❌ Hard to change | ✅ Easy to change |
| ❌ Multiple instances | ✅ Shared instances |

## 🎓 Additional Resources

- **FastAPI Dependency Injection**: https://fastapi.tiangolo.com/tutorial/dependencies/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html
- **SOLID Principles**: Especially the "D" (Dependency Inversion Principle)

## 💡 Tips

1. **Always inject expensive resources** (databases, API clients, file handles)
2. **Use type hints** for better IDE support and documentation
3. **Combine @once() with FastAPI Depends()** for optimal resource usage
4. **Create fake implementations** for testing
5. **Keep constructors simple** - just store dependencies, don't do work

## 🤔 When to Use DI?

**Use DI when:**
- ✅ Working with external services (databases, APIs)
- ✅ You need to test your code
- ✅ Multiple classes need the same resource
- ✅ You want to swap implementations

**Don't need DI for:**
- ❌ Simple data classes
- ❌ Pure functions with no dependencies
- ❌ Temporary/throwaway scripts

## 🎉 Congratulations!

You now understand dependency injection—one of the most important design patterns in modern software development!

**Next Steps:**
1. Practice by refactoring your own code to use DI
2. Try creating your own FastAPI service with DI

---

**Questions?** Review the examples again, they build on each other progressively!

