"""
Tests for Dependency Injection Examples
========================================

This file demonstrates how easy it is to test code
that uses dependency injection.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import the examples
sys.path.insert(0, str(Path(__file__).parent.parent))


# ============================================================================
# FAKE IMPLEMENTATIONS FOR TESTING
# ============================================================================

class FakeDatabase:
    """Fake database that stores data in memory."""
    
    def __init__(self):
        self.users = {}
        self.save_count = 0
    
    def save_user(self, user: dict) -> None:
        self.users[user["id"]] = user
        self.save_count += 1
    
    def get_user(self, user_id: int) -> dict:
        return self.users.get(user_id, {})


class FakeEmailService:
    """Fake email service that tracks sent emails."""
    
    def __init__(self):
        self.sent_emails = []
    
    def send_email(self, to: str, subject: str, body: str) -> None:
        self.sent_emails.append({
            "to": to,
            "subject": subject,
            "body": body
        })


# ============================================================================
# SERVICE TO TEST (Using Dependency Injection)
# ============================================================================

class UserService:
    """User service that depends on database and email."""
    
    def __init__(self, db, email):
        self.db = db
        self.email = email
    
    def register_user(self, user_id: int, name: str, email: str) -> dict:
        """Register a new user."""
        user = {
            "id": user_id,
            "name": name,
            "email": email
        }
        
        self.db.save_user(user)
        self.email.send_email(
            to=email,
            subject="Welcome!",
            body=f"Welcome {name}!"
        )
        
        return user
    
    def get_user(self, user_id: int) -> dict:
        """Get a user by ID."""
        return self.db.get_user(user_id)


# ============================================================================
# TESTS
# ============================================================================

def test_register_user_saves_to_database():
    """Test that registering a user saves to the database."""
    # Arrange
    fake_db = FakeDatabase()
    fake_email = FakeEmailService()
    service = UserService(fake_db, fake_email)
    
    # Act
    user = service.register_user(1, "Alice", "alice@example.com")
    
    # Assert
    assert user["name"] == "Alice"
    assert user["email"] == "alice@example.com"
    assert fake_db.save_count == 1
    assert len(fake_db.users) == 1
    
    print("✅ test_register_user_saves_to_database passed")


def test_register_user_sends_email():
    """Test that registering a user sends a welcome email."""
    # Arrange
    fake_db = FakeDatabase()
    fake_email = FakeEmailService()
    service = UserService(fake_db, fake_email)
    
    # Act
    service.register_user(1, "Bob", "bob@example.com")
    
    # Assert
    assert len(fake_email.sent_emails) == 1
    email = fake_email.sent_emails[0]
    assert email["to"] == "bob@example.com"
    assert email["subject"] == "Welcome!"
    assert "Bob" in email["body"]
    
    print("✅ test_register_user_sends_email passed")


def test_register_multiple_users():
    """Test that multiple users can be registered."""
    # Arrange
    fake_db = FakeDatabase()
    fake_email = FakeEmailService()
    service = UserService(fake_db, fake_email)
    
    # Act
    service.register_user(1, "Alice", "alice@example.com")
    service.register_user(2, "Bob", "bob@example.com")
    service.register_user(3, "Charlie", "charlie@example.com")
    
    # Assert
    assert fake_db.save_count == 3
    assert len(fake_db.users) == 3
    assert len(fake_email.sent_emails) == 3
    
    print("✅ test_register_multiple_users passed")


def test_get_user_returns_saved_user():
    """Test that we can retrieve a saved user."""
    # Arrange
    fake_db = FakeDatabase()
    fake_email = FakeEmailService()
    service = UserService(fake_db, fake_email)
    
    # Act
    service.register_user(1, "Alice", "alice@example.com")
    retrieved_user = service.get_user(1)
    
    # Assert
    assert retrieved_user["name"] == "Alice"
    assert retrieved_user["email"] == "alice@example.com"
    
    print("✅ test_get_user_returns_saved_user passed")


def test_get_nonexistent_user_returns_empty():
    """Test that getting a non-existent user returns empty dict."""
    # Arrange
    fake_db = FakeDatabase()
    fake_email = FakeEmailService()
    service = UserService(fake_db, fake_email)
    
    # Act
    user = service.get_user(999)
    
    # Assert
    assert user == {}
    
    print("✅ test_get_nonexistent_user_returns_empty passed")


# ============================================================================
# TEST RUNNER
# ============================================================================

def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("RUNNING TESTS")
    print("=" * 70)
    print()
    
    tests = [
        test_register_user_saves_to_database,
        test_register_user_sends_email,
        test_register_multiple_users,
        test_get_user_returns_saved_user,
        test_get_nonexistent_user_returns_empty,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} error: {e}")
            failed += 1
    
    print()
    print("=" * 70)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)
    print()
    
    if failed == 0:
        print("🎉 All tests passed!")
    else:
        print(f"❌ {failed} test(s) failed")
    
    return failed == 0


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_testing_benefits():
    """Show why DI makes testing easy."""
    print("\n" + "=" * 70)
    print("WHY DEPENDENCY INJECTION MAKES TESTING EASY")
    print("=" * 70)
    print()
    
    print("Benefits:")
    print("  ✅ No need for real database")
    print("  ✅ No need for real email server")
    print("  ✅ Tests run instantly (no network calls)")
    print("  ✅ Tests are reliable (no external dependencies)")
    print("  ✅ Easy to verify behavior (inspect fake objects)")
    print("  ✅ Each test is isolated (new fakes each time)")
    print()
    
    print("Example:")
    print("  # Arrange")
    print("  fake_db = FakeDatabase()")
    print("  fake_email = FakeEmailService()")
    print("  service = UserService(fake_db, fake_email)")
    print()
    print("  # Act")
    print("  service.register_user(1, 'Alice', 'alice@example.com')")
    print()
    print("  # Assert")
    print("  assert len(fake_db.users) == 1")
    print("  assert len(fake_email.sent_emails) == 1")
    print()


if __name__ == "__main__":
    demonstrate_testing_benefits()
    success = run_all_tests()
    
    if not success:
        sys.exit(1)

