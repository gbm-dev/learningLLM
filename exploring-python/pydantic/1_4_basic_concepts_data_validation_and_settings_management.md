# 1.4. Basic Concepts: Data Validation and Settings Management

This section introduces the fundamental concepts of data validation and settings management using Pydantic. We'll explore how Pydantic models work and how they can be used for both data validation and managing application settings.

## Understanding Data Models

In Pydantic, data models are at the core of data validation. They are defined as Python classes that inherit from `pydantic.BaseModel`.

### Basic Data Model

Here's a simple example of a Pydantic data model:

```python
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool = True
    tags: List[str] = []
    age: Optional[int] = None

# Create a user instance
user = User(id=1, name="John Doe", email="john@example.com", tags=["customer", "premium"])
print(user)
# Output: id=1 name='John Doe' email='john@example.com' is_active=True tags=['customer', 'premium'] age=None

# Access fields
print(user.name)  # Output: John Doe

# Convert to dictionary
user_dict = user.dict()
print(user_dict)
# Output: {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'is_active': True, 'tags': ['customer', 'premium'], 'age': None}
```

In this example:
- Fields are defined using type annotations.
- Default values can be specified (e.g., `is_active: bool = True`).
- Complex types like `List[str]` and `Optional[int]` are supported.
- Pydantic provides special types like `EmailStr` for additional validation.

### Data Validation

Pydantic automatically validates data when creating model instances:

```python
from pydantic import ValidationError

try:
    invalid_user = User(id="not an int", name=123, email="invalid-email")
except ValidationError as e:
    print(e)
    """
    3 validation errors for User
    id
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='not an int', input_type=str]
    name
      Input should be a valid string [type=string_type, input_value=123, input_type=int]
    email
      The email address is not valid. It must have exactly one @-sign. [type=value_error.email]
    """
```

## Settings Management

Pydantic is not just for data validation; it's also excellent for managing application settings. The `BaseSettings` class is specifically designed for this purpose.

### Creating a Settings Model

Here's an example of how to use Pydantic for settings management:

```python
from pydantic import BaseSettings, EmailStr, Field
from typing import List

class AppSettings(BaseSettings):
    app_name: str = "My App"
    admin_email: EmailStr
    debug_mode: bool = False
    allowed_hosts: List[str] = ["localhost", "127.0.0.1"]
    database_url: str = Field(..., env="DATABASE_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Usage
settings = AppSettings()
print(f"App Name: {settings.app_name}")
print(f"Admin Email: {settings.admin_email}")
print(f"Debug Mode: {settings.debug_mode}")
print(f"Database URL: {settings.database_url}")
```

In this example:
- `BaseSettings` is used instead of `BaseModel`.
- Default values can be set directly in the model.
- The `Config` class is used to specify an environment file.
- `Field(...)` is used to mark `database_url` as required and specify its environment variable name.

### Loading Settings

Pydantic's `BaseSettings` will automatically load values from:
1. Environment variables
2. `.env` file (if specified)
3. Default values in the model

This allows for flexible configuration management across different environments.

## Combining Data Validation and Settings Management

Pydantic's power comes from its ability to handle both data validation and settings management seamlessly. Here's an example that combines both concepts:

```python
from pydantic import BaseSettings, BaseModel, EmailStr, Field, ValidationError
from typing import List, Optional

class UserProfile(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class AppSettings(BaseSettings):
    app_name: str = "User Management System"
    debug_mode: bool = False
    max_users: int = Field(100, ge=1, le=1000)
    admin_emails: List[EmailStr]

    class Config:
        env_file = ".env"

def create_user(settings: AppSettings, user_data: dict) -> UserProfile:
    try:
        user = UserProfile(**user_data)
        # Here you might add the user to a database
        print(f"User created: {user}")
        return user
    except ValidationError as e:
        if settings.debug_mode:
            print(f"Validation error: {e}")
        raise

# Usage
settings = AppSettings()
try:
    new_user = create_user(settings, {"name": "Alice", "email": "alice@example.com", "age": 30})
except ValidationError:
    print("Failed to create user due to invalid data")
```

This example demonstrates:
- How to use `BaseModel` for data validation (`UserProfile`)
- How to use `BaseSettings` for application configuration (`AppSettings`)
- How to combine both in a practical scenario (user creation function)
- The use of Pydantic's built-in types like `EmailStr`
- Field constraints with `Field(100, ge=1, le=1000)`
- Error handling with `ValidationError`

By leveraging these concepts, you can create robust, type-safe applications with clear configuration management and reliable data validation.