# Python Foundation Playbook

A collection of hands-on examples and explanations for fundamental Python concepts, focusing on practical patterns and best practices.

## 📚 Topics Covered

### 🔌 Dependency Injection
Learn dependency injection patterns in Python, from basics to real-world FastAPI applications.

**Directory**: `dependency-injection/`

Topics include:
- What is dependency injection and why use it?
- Basic DI patterns in Python
- Testing with DI
- FastAPI dependency injection
- Singleton patterns (`@once()` vs `@lru_cache`)
- Real-world examples

**Start here**: [dependency-injection/QUICKSTART.md](dependency-injection/QUICKSTART.md)

### 🔐 Closures
Understand how Python closures work and why they matter.

**Directory**: `closures/`

Topics include:
- How closures capture and remember variables
- Step-by-step examples from simple to complex
- Alternative approaches to achieve closure-like behavior
- How decorators use closures internally

**Start here**: [closures/README.md](closures/README.md)

## 🚀 Quick Start

Each directory is self-contained with its own README and examples:

```bash
# Explore dependency injection
cd dependency-injection
python 01_without_di.py
python 02_with_di_basic.py

# Learn about closures
cd closures
python closure_explained.py
python closure_alternatives.py
```

## 📖 Learning Path

Recommended order for beginners:

1. **Start with Closures** (`closures/`) - Understand the foundation
2. **Move to Dependency Injection** (`dependency-injection/`) - Apply the concepts
3. **Explore FastAPI DI** - See real-world applications

## 🎯 Who Is This For?

- Python developers wanting to understand advanced patterns
- Developers transitioning from other languages
- Anyone building testable, maintainable Python applications
- FastAPI users wanting to master dependency injection

## 💡 Philosophy

This playbook focuses on:
- **Practical examples** over theory
- **Runnable code** that you can experiment with
- **Progressive complexity** from simple to advanced
- **Real-world patterns** used in production applications

## 🛠️ Requirements

```bash
# For dependency injection examples with FastAPI
cd dependency-injection
pip install -r requirements.txt
```

For closure examples, only Python 3.7+ standard library is needed.

## 📝 Contributing

This is a personal learning playbook, but suggestions and improvements are welcome!

## 📄 License

Feel free to use these examples for learning and reference.
