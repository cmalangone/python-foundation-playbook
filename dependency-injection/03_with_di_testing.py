"""
03 - Testing with Dependency Injection
=======================================

This example shows how dependency injection makes testing
incredibly easy by allowing us to inject fake/mock dependencies.
"""


# ============================================================================
# REAL IMPLEMENTATIONS (Production Code)
# ============================================================================

class Database:
    """Real database - would connect to actual database."""
    
    def __init__(self, connection_string: str = "postgresql://localhost:5432/mydb"):
        self.connection_string = connection_string
    
    def save_user(self, user: dict) -> None:
        """Would actually save to database."""
        print(f"💾 [REAL DB] Saving user: {user['name']}")


class EmailService:
    """Real email service - would send actual emails."""
    
    def __init__(self, smtp_server: str = "smtp.example.com"):
        self.smtp_server = smtp_server
    
    def send_email(self, to: str, subject: str, body: str) -> None:
        """Would actually send email via SMTP."""
        print(f"📧 [REAL EMAIL] Sending to {to}: {subject}")


class UserService:
    """Our service that uses database and email."""
    
    def __init__(self, db: Database, email: EmailService):
        self.db = db
        self.email = email
    
    def register_user(self, name: str, email: str) -> dict:
        """Register a new user and send welcome email."""
        user = {
            "id": 123,
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


# ============================================================================
# FAKE IMPLEMENTATIONS (Test Code)
# ============================================================================

class FakeDatabase:
    """Fake database for testing - no real database needed!"""
    
    def __init__(self):
        self.saved_users = []  # Store in memory instead of real DB
    
    def save_user(self, user: dict) -> None:
        """Fake save - just append to list."""
        self.saved_users.append(user)
        print(f"🧪 [FAKE DB] Saved user to memory: {user['name']}")


class FakeEmailService:
    """Fake email service for testing - no real emails sent!"""
    
    def __init__(self):
        self.sent_emails = []  # Track sent emails
    
    def send_email(self, to: str, subject: str, body: str) -> None:
        """Fake email - just append to list."""
        email = {"to": to, "subject": subject, "body": body}
        self.sent_emails.append(email)
        print(f"🧪 [FAKE EMAIL] Recorded email to {to}: {subject}")


# ============================================================================
# TESTING
# ============================================================================

def test_user_registration():
    """Test that user registration works correctly."""
    print("\n" + "=" * 70)
    print("TEST: User Registration")
    print("=" * 70)
    
    # Arrange: Create fake dependencies
    fake_db = FakeDatabase()
    fake_email = FakeEmailService()
    service = UserService(fake_db, fake_email)
    
    # Act: Register a user
    user = service.register_user("Alice", "alice@example.com")
    
    # Assert: Check that everything worked
    assert user["name"] == "Alice"
    assert user["email"] == "alice@example.com"
    assert len(fake_db.saved_users) == 1
    assert fake_db.saved_users[0]["name"] == "Alice"
    assert len(fake_email.sent_emails) == 1
    assert fake_email.sent_emails[0]["to"] == "alice@example.com"
    
    print("\n✅ Test passed! User was saved and email was sent.")
    print(f"   User saved: {fake_db.saved_users[0]}")
    print(f"   Email sent: {fake_email.sent_emails[0]}")


def test_multiple_registrations():
    """Test that we can register multiple users."""
    print("\n" + "=" * 70)
    print("TEST: Multiple Registrations")
    print("=" * 70)
    
    # Arrange
    fake_db = FakeDatabase()
    fake_email = FakeEmailService()
    service = UserService(fake_db, fake_email)
    
    # Act: Register multiple users
    service.register_user("Alice", "alice@example.com")
    service.register_user("Bob", "bob@example.com")
    service.register_user("Charlie", "charlie@example.com")
    
    # Assert
    assert len(fake_db.saved_users) == 3
    assert len(fake_email.sent_emails) == 3
    
    print("\n✅ Test passed! All users were registered.")
    print(f"   Total users saved: {len(fake_db.saved_users)}")
    print(f"   Total emails sent: {len(fake_email.sent_emails)}")


def demonstrate_production_usage():
    """Show how the same code works in production with real dependencies."""
    print("\n" + "=" * 70)
    print("PRODUCTION: Using Real Dependencies")
    print("=" * 70)
    
    # In production, inject real dependencies
    real_db = Database()
    real_email = EmailService()
    service = UserService(real_db, real_email)
    
    # Same code, different dependencies!
    user = service.register_user("Production User", "prod@example.com")
    
    print("\n✅ Production registration complete!")


# ============================================================================
# DEMONSTRATION
# ============================================================================

def main():
    print("=" * 70)
    print("DEPENDENCY INJECTION FOR TESTING")
    print("=" * 70)
    print()
    print("Key Insight: Same code, different dependencies!")
    print("- In tests: Use fake dependencies (fast, no external services)")
    print("- In production: Use real dependencies (actual DB, email, etc.)")
    
    # Run tests with fake dependencies
    test_user_registration()
    test_multiple_registrations()
    
    # Show production usage with real dependencies
    demonstrate_production_usage()
    
    print("\n" + "=" * 70)
    print("Benefits of DI for Testing:")
    print("=" * 70)
    print("✅ No need for real database")
    print("✅ No need for real email server")
    print("✅ Tests are FAST (no network calls)")
    print("✅ Tests are RELIABLE (no external dependencies)")
    print("✅ Tests are ISOLATED (each test has its own fake dependencies)")
    print()
    print("Next: See 04_fastapi_di.py for FastAPI's automatic DI ➡️")
    print("=" * 70)


if __name__ == "__main__":
    main()

