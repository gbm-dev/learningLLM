# 2.1. Creating Basic Models

Pydantic models are the foundation of working with Pydantic. They provide a way to define the structure and types of your data, enabling automatic validation and serialization.

## Defining Your First Pydantic Model

To create a Pydantic model, you need to:
1. Import `BaseModel` from Pydantic
2. Create a class that inherits from `BaseModel`
3. Define fields using type annotations

Here's a simple example:

```python
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
    is_active: bool = True

# Create an instance of the model
user = User(id=1, name="John Doe", email="john@example.com", age=30)
print(user)
# Output: id=1 name='John Doe' email='john@example.com' age=30 is_active=True
```

In this example:
- `User` is a Pydantic model that inherits from `BaseModel`.
- Fields are defined using type annotations (e.g., `id: int`).
- `Optional[int]` is used for `age` to indicate it's not required.
- Default values can be set (e.g., `is_active: bool = True`).

## Understanding Model Behavior

Pydantic models come with several built-in behaviors:

### 1. Automatic Validation

When you create an instance of a model, Pydantic automatically validates the input data:

```python
try:
    invalid_user = User(id="not an int", name=123, email="invalid-email")
except ValueError as e:
    print(f"Validation error: {e}")
```

### 2. Type Coercion

Pydantic tries to coerce values to the correct type when possible:

```python
user = User(id="1", name="Alice", email="alice@example.com")
print(user.id)  # Output: 1 (converted to int)
```

### 3. Attribute Access

You can access model fields as attributes:

```python
print(user.name)  # Output: Alice
user.age = 25
print(user.age)  # Output: 25
```

### 4. Dictionary Conversion

Models can be easily converted to dictionaries:

```python
user_dict = user.dict()
print(user_dict)
# Output: {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'age': 25, 'is_active': True}
```

### 5. JSON Serialization

Models can be serialized to JSON:

```python
json_data = user.json()
print(json_data)
# Output: {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 25, "is_active": true}
```

### 6. Copy and Update

You can create a copy of a model with updated fields:

```python
updated_user = user.copy(update={"age": 26, "is_active": False})
print(updated_user)
# Output: id=1 name='Alice' email='alice@example.com' age=26 is_active=False
```

By understanding these behaviors, you can leverage Pydantic models to create robust, type-safe data structures in your Python applications.