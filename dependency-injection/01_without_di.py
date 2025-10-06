"""
01 - Without Dependency Injection (The Problem)
================================================

This example shows the problems that arise when classes
create their own dependencies instead of receiving them.
"""


class Database:
    """Simulates a database connection."""
    
    def __init__(self, connection_string: str = "postgresql://localhost:5432/mydb"):
        self.connection_string = connection_string
        print(f"💾 Connecting to database: {connection_string}")
    
    def get_user(self, user_id: int) -> dict:
        """Simulate fetching a user from the database."""
        return {
            "id": user_id,
            "name": f"User {user_id}",
            "email": f"user{user_id}@example.com"
        }
    
    def save_user(self, user: dict) -> None:
        """Simulate saving a user to the database."""
        print(f"💾 Saving user: {user['name']}")


class EmailService:
    """Simulates sending emails."""
    
    def __init__(self, smtp_server: str = "smtp.example.com"):
        self.smtp_server = smtp_server
        print(f"📧 Connecting to email server: {smtp_server}")
    
    def send_email(self, to: str, subject: str, body: str) -> None:
        """Simulate sending an email."""
        print(f"📧 Sending email to {to}: {subject}")


class UserService:
    """
    ❌ PROBLEM: This class creates its own dependencies!
    
    Issues:
    - Hard to test (requires real database and email server)
    - Can't reuse existing connections
    - Tightly coupled to specific implementations
    - Can't easily swap implementations
    """
    
    def __init__(self):
        # ❌ Creating dependencies inside the class
        self.db = Database()  # Creates its own database connection!
        self.email = EmailService()  # Creates its own email service!
    
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
# DEMONSTRATION
# ============================================================================

def main():
    print("=" * 70)
    print("WITHOUT DEPENDENCY INJECTION - Problems Demonstrated")
    print("=" * 70)
    print()
    
    print("Problem 1: Multiple instances create multiple connections")
    print("-" * 70)
    service1 = UserService()  # Creates new DB and email connections
    print()
    service2 = UserService()  # Creates ANOTHER set of connections!
    print()
    print("👎 We now have 2 database connections and 2 email connections!")
    print("   This wastes resources and is inefficient.\n")
    
    print("\nProblem 2: Can't test without real external services")
    print("-" * 70)
    service = UserService()
    print("👎 To test UserService, we need:")
    print("   - A real database running")
    print("   - A real email server")
    print("   - This makes tests slow, flaky, and complex!\n")
    
    print("\nProblem 3: Using the service")
    print("-" * 70)
    user = service.register_user("Alice", "alice@example.com")
    print(f"✅ Registered: {user['name']}")
    print()
    
    print("Problem 4: Can't change implementations")
    print("-" * 70)
    print("👎 What if we want to:")
    print("   - Use a different database (MySQL instead of PostgreSQL)?")
    print("   - Use a different email provider (SendGrid)?")
    print("   - Use a mock database for testing?")
    print("   We can't! We'd have to modify UserService code.\n")
    
    print("\n" + "=" * 70)
    print("See 02_with_di_basic.py for the solution! ➡️")
    print("=" * 70)


if __name__ == "__main__":
    main()

