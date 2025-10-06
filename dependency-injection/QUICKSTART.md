# 🚀 Quick Start Guide

## Run All Examples in Order

```bash
cd /Users/cinziamalangone/personal/python-foundation-playbook/dependency-injection

# 1. See the problem
python 01_without_di.py

# 2. See the solution
python 02_with_di_basic.py

# 3. See testing benefits
python 03_with_di_testing.py

# 4. See singleton pattern
python 05_singleton_pattern.py

# 5. See complete real-world example
python 06_real_world_example.py

# 6. Run tests
python tests/test_di_examples.py
```

## Optional: FastAPI Example

```bash
# Install dependencies
pip install fastapi uvicorn

# Run FastAPI server
python 04_fastapi_di.py

# Visit http://localhost:8000/docs
```

## What to Learn from Each File

| File | What You'll Learn |
|------|------------------|
| `01_without_di.py` | Why NOT using DI is bad |
| `02_with_di_basic.py` | How to use DI (basic) |
| `03_with_di_testing.py` | How DI makes testing easy |
| `04_fastapi_di.py` | FastAPI automatic DI |
| `05_singleton_pattern.py` | The @once() decorator |
| `06_real_world_example.py` | Complete application |

## Next Steps

1. ✅ Run all examples in order
2. ✅ Read the code comments carefully
3. ✅ Modify examples to experiment
4. ✅ Try creating your own DI example
5. ✅ Read the full README.md

Happy learning! 🎉
