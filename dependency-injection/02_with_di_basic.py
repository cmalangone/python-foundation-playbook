"""
02 - With Dependency Injection (The Solution)
==============================================

This example shows how dependency injection solves the problems
from the previous example.
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
    ✅ SOLUTION: This class receives its dependencies!
    
    Benefits:
    - Easy to test (inject fake dependencies)
    - Reuses existing connections
    - Loosely coupled
    - Easy to swap implementations
    """
    
    def __init__(self, db: Database, email: EmailService):
        """
        Dependencies are INJECTED through the constructor.
        
        Args:
            db: The database to use (someone else creates it)
            email: The email service to use (someone else creates it)
        """
        # ✅ Receiving dependencies from outside
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
# DEMONSTRATION
# ============================================================================

def main():
    print("=" * 70)
    print("WITH DEPENDENCY INJECTION - Problems Solved!")
    print("=" * 70)
    print()
    
    print("Solution 1: Share connections across multiple services")
    print("-" * 70)
    # Create dependencies ONCE
    db = Database()
    email = EmailService()
    print()
    
    # Inject the same dependencies into multiple services
    service1 = UserService(db, email)
    service2 = UserService(db, email)
    print("✅ Both services share the same DB and email connections!")
    print("   Only 1 database connection, 1 email connection.\n")
    
    print("\nSolution 2: Easy to test with fake dependencies")
    print("-" * 70)
    print("✅ We can inject fake/mock dependencies for testing")
    print("   (See 03_with_di_testing.py for examples)\n")
    
    print("\nSolution 3: Using the service")
    print("-" * 70)
    user = service1.register_user("Alice", "alice@example.com")
    print(f"✅ Registered: {user['name']}")
    print()
    
    print("Solution 4: Easy to change implementations")
    print("-" * 70)
    # Want a different database? Just create a different one!
    mysql_db = Database("mysql://localhost:3306/mydb")
    service_with_mysql = UserService(mysql_db, email)
    print("✅ Now using MySQL instead of PostgreSQL!")
    print("   No need to change UserService code!\n")
    
    print("\n" + "=" * 70)
    print("Key Principle: 'Don't create what you need, ask for it!'")
    print("=" * 70)
    print()
    print("Next: See 03_with_di_testing.py for testing examples ➡️")
    print("=" * 70)


if __name__ == "__main__":
    main()

