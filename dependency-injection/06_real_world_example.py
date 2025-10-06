"""
06 - Real-World Complete Example
=================================

This example brings together all the concepts:
- Dependency Injection
- Testing with fakes
- FastAPI integration
- @once() singleton pattern
- Multi-layer architecture

A complete mini application similar to App architecture.
"""

from typing import Optional, Annotated
from dataclasses import dataclass
from functools import wraps
from typing import Callable, TypeVar

# ============================================================================
# SINGLETON DECORATOR
# ============================================================================

T = TypeVar('T')

def once() -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Ensure function is called only once."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cached_result: dict = {}
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            if 'result' not in cached_result:
                cached_result['result'] = func(*args, **kwargs)
            return cached_result['result']
        return wrapper
    return decorator


# ============================================================================
# DOMAIN MODELS
# ============================================================================

@dataclass
class User:
    """Domain model for a user."""
    id: int
    name: str
    email: str
    active: bool = True


@dataclass
class Dataset:
    """Domain model for a dataset (like in App)."""
    id: str
    name: str
    owner_id: int
    file_count: int


# ============================================================================
# INFRASTRUCTURE LAYER (External Services)
# ============================================================================

class PostgresDatabase:
    """PostgreSQL database connection."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        print(f"💾 Connected to PostgreSQL: {connection_string}")
        # Simulate in-memory storage
        self._users = {
            1: User(1, "Alice", "alice@example.com"),
            2: User(2, "Bob", "bob@example.com"),
        }
        self._datasets = {
            "ds-001": Dataset("ds-001", "RNA-Seq Data", 1, 42),
            "ds-002": Dataset("ds-002", "Microscopy Images", 2, 156),
        }
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)
    
    def save_user(self, user: User) -> None:
        self._users[user.id] = user
        print(f"💾 Saved user: {user.name}")
    
    def get_dataset(self, dataset_id: str) -> Optional[Dataset]:
        return self._datasets.get(dataset_id)
    
    def save_dataset(self, dataset: Dataset) -> None:
        self._datasets[dataset.id] = dataset
        print(f"💾 Saved dataset: {dataset.name}")


class OpenSearchClient:
    """OpenSearch for full-text search (like in App)."""
    
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        print(f"🔍 Connected to OpenSearch: {endpoint}")
    
    def index_dataset(self, dataset: Dataset) -> None:
        print(f"🔍 Indexed dataset '{dataset.name}' in OpenSearch")
    
    def search_datasets(self, query: str) -> list[str]:
        print(f"🔍 Searching datasets for: {query}")
        return ["ds-001", "ds-002"]  # Simplified


class S3Client:
    """S3 client for file storage."""
    
    def __init__(self, region: str = "us-west-2"):
        self.region = region
        print(f"📦 Connected to S3 in region: {region}")
    
    def upload_file(self, bucket: str, key: str, data: bytes) -> str:
        url = f"s3://{bucket}/{key}"
        print(f"📦 Uploaded to {url}")
        return url
    
    def download_file(self, bucket: str, key: str) -> bytes:
        print(f"📦 Downloaded from s3://{bucket}/{key}")
        return b"file contents"


class EmailService:
    """Email service for notifications."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        print(f"📧 Email service initialized")
    
    def send_notification(self, to: str, subject: str, body: str) -> None:
        print(f"📧 Sent email to {to}: {subject}")


# ============================================================================
# APPLICATION LAYER (Business Logic)
# ============================================================================

class DatasetService:
    """
    Business logic for datasets.
    This is like DatasetProvider in App.
    """
    
    def __init__(
        self,
        db: PostgresDatabase,
        search: OpenSearchClient,
        s3: S3Client,
        email: EmailService
    ):
        self.db = db
        self.search = search
        self.s3 = s3
        self.email = email
    
    def create_dataset(
        self,
        dataset_id: str,
        name: str,
        owner_id: int,
        file_count: int
    ) -> Dataset:
        """Create a new dataset."""
        # 1. Create dataset object
        dataset = Dataset(dataset_id, name, owner_id, file_count)
        
        # 2. Save to database
        self.db.save_dataset(dataset)
        
        # 3. Index in search engine
        self.search.index_dataset(dataset)
        
        # 4. Notify owner
        user = self.db.get_user(owner_id)
        if user:
            self.email.send_notification(
                to=user.email,
                subject="Dataset Created",
                body=f"Your dataset '{name}' has been created!"
            )
        
        return dataset
    
    def get_dataset(self, dataset_id: str) -> Optional[Dataset]:
        """Retrieve a dataset."""
        return self.db.get_dataset(dataset_id)
    
    def search_datasets(self, query: str) -> list[Dataset]:
        """Search for datasets."""
        dataset_ids = self.search.search_datasets(query)
        datasets = []
        for dataset_id in dataset_ids:
            dataset = self.db.get_dataset(dataset_id)
            if dataset:
                datasets.append(dataset)
        return datasets


class UserService:
    """Business logic for users."""
    
    def __init__(self, db: PostgresDatabase, email: EmailService):
        self.db = db
        self.email = email
    
    def register_user(self, user_id: int, name: str, email: str) -> User:
        """Register a new user."""
        user = User(user_id, name, email)
        self.db.save_user(user)
        
        self.email.send_notification(
            to=email,
            subject="Welcome!",
            body=f"Welcome {name}!"
        )
        
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        return self.db.get_user(user_id)


# ============================================================================
# DEPENDENCY INJECTION CONFIGURATION
# ============================================================================

@once()
def get_database() -> PostgresDatabase:
    """Singleton database connection."""
    return PostgresDatabase("postgresql://localhost:5432/app")


@once()
def get_search_client() -> OpenSearchClient:
    """Singleton OpenSearch client."""
    return OpenSearchClient("https://search.example.com")


@once()
def get_s3_client() -> S3Client:
    """Singleton S3 client."""
    return S3Client("us-west-2")


@once()
def get_email_service() -> EmailService:
    """Singleton email service."""
    return EmailService("secret-api-key")


@once()
def get_dataset_service() -> DatasetService:
    """Dataset service with all dependencies injected."""
    return DatasetService(
        db=get_database(),
        search=get_search_client(),
        s3=get_s3_client(),
        email=get_email_service()
    )


@once()
def get_user_service() -> UserService:
    """User service with dependencies injected."""
    return UserService(
        db=get_database(),
        email=get_email_service()
    )


# ============================================================================
# API LAYER (FastAPI Routes - Simplified)
# ============================================================================

def demonstrate_api_usage():
    """Simulates FastAPI route handlers."""
    print("\n" + "=" * 70)
    print("API LAYER - Route Handlers")
    print("=" * 70)
    
    # Simulate: POST /datasets
    print("\n📝 POST /datasets")
    dataset_service = get_dataset_service()
    new_dataset = dataset_service.create_dataset(
        dataset_id="ds-003",
        name="New RNA-Seq Experiment",
        owner_id=1,
        file_count=78
    )
    print(f"✅ Created: {new_dataset}")
    
    # Simulate: GET /datasets/ds-001
    print("\n📝 GET /datasets/ds-001")
    dataset_service = get_dataset_service()  # Same instance!
    dataset = dataset_service.get_dataset("ds-001")
    print(f"✅ Retrieved: {dataset}")
    
    # Simulate: GET /datasets/search?q=RNA
    print("\n📝 GET /datasets/search?q=RNA")
    dataset_service = get_dataset_service()  # Still same instance!
    results = dataset_service.search_datasets("RNA")
    print(f"✅ Found {len(results)} datasets")


# ============================================================================
# TESTING WITH FAKES
# ============================================================================

class FakeDatabase:
    """Fake database for testing."""
    
    def __init__(self):
        self._users = {}
        self._datasets = {}
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)
    
    def save_user(self, user: User) -> None:
        self._users[user.id] = user
    
    def get_dataset(self, dataset_id: str) -> Optional[Dataset]:
        return self._datasets.get(dataset_id)
    
    def save_dataset(self, dataset: Dataset) -> None:
        self._datasets[dataset.id] = dataset


class FakeEmailService:
    """Fake email service for testing."""
    
    def __init__(self):
        self.sent_emails = []
    
    def send_notification(self, to: str, subject: str, body: str) -> None:
        self.sent_emails.append({"to": to, "subject": subject, "body": body})


def test_user_registration():
    """Test user registration with fake dependencies."""
    print("\n" + "=" * 70)
    print("TESTING - User Registration")
    print("=" * 70)
    
    # Arrange: Create fake dependencies
    fake_db = FakeDatabase()
    fake_email = FakeEmailService()
    service = UserService(fake_db, fake_email)
    
    # Act: Register a user
    user = service.register_user(100, "Test User", "test@example.com")
    
    # Assert
    assert user.name == "Test User"
    assert len(fake_email.sent_emails) == 1
    assert fake_email.sent_emails[0]["to"] == "test@example.com"
    
    print("✅ Test passed!")
    print(f"   User registered: {user}")
    print(f"   Email sent: {fake_email.sent_emails[0]}")


# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

def main():
    print("=" * 70)
    print("REAL-WORLD COMPLETE EXAMPLE")
    print("=" * 70)
    print()
    print("Architecture layers:")
    print("  1. Infrastructure (Database, Search, S3, Email)")
    print("  2. Application (Services with business logic)")
    print("  3. API (Route handlers)")
    print()
    print("Key patterns:")
    print("  ✅ Dependency Injection")
    print("  ✅ Singleton pattern (@once)")
    print("  ✅ Separation of concerns")
    print("  ✅ Testability with fakes")
    
    # Show infrastructure creation
    print("\n" + "=" * 70)
    print("INFRASTRUCTURE - Creating singletons")
    print("=" * 70)
    db = get_database()
    search = get_search_client()
    s3 = get_s3_client()
    email = get_email_service()
    print("✅ All infrastructure created once")
    
    # Show API usage
    demonstrate_api_usage()
    
    # Show testing
    test_user_registration()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("This example demonstrates:")
    print("  ✅ Multi-layer architecture (Infrastructure → Application → API)")
    print("  ✅ Dependency injection throughout")
    print("  ✅ Singleton pattern for expensive resources")
    print("  ✅ Easy testing with fake implementations")
    print("  ✅ Clear separation of concerns")
    print()
    print("This is exactly how the App codebase is structured! 🎉")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()

