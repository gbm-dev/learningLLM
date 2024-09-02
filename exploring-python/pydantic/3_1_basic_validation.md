# 3.1. Basic Validation

Pydantic provides robust data validation capabilities out of the box. This section explores how Pydantic validates data and how to handle invalid data.

## How Pydantic Validates Data

Pydantic performs validation automatically when you create an instance of a model or when you assign values to model fields. The validation process includes:

1. **Type Checking**: Ensures that the data matches the specified type.
2. **Coercion**: Attempts to convert data to the correct type when possible.
3. **Constraint Checking**: Applies any constraints defined for the fields.

Here's a basic example:

```python
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=0, lt=120)

# Valid data
valid_user = User(username="john_doe", email="john@example.com", age=30)
print(valid_user)
# Output: username='john_doe' email='john@example.com' age=30

# Pydantic will coerce the age to an integer
coerced_user = User(username="jane_doe", email="jane@example.com", age="25")
print(coerced_user)
# Output: username='jane_doe' email='jane@example.com' age=25
```

## Handling Invalid Data

When Pydantic encounters invalid data, it raises a `ValidationError`. This error contains detailed information about what went wrong during validation.

```python
from pydantic import BaseModel, EmailStr, Field, ValidationError

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=0, lt=120)

try:
    invalid_user = User(username="a", email="not_an_email", age=150)
except ValidationError as e:
    print(e)
    """
    3 validation errors for User
    username
      String should have at least 3 characters [type=string_too_short, input_value='a', input_type=str]
    email
      The email address is not valid. It must have exactly one @-sign. [type=value_error.email]
    age
      Input should be less than 120 [type=less_than, input_value=150, input_type=int]
    """
```

### Accessing Validation Errors

You can access the validation errors programmatically:

```python
try:
    invalid_user = User(username="a", email="not_an_email", age=150)
except ValidationError as e:
    for error in e.errors():
        print(f"Field: {error['loc'][0]}, Error: {error['msg']}")
    """
    Field: username, Error: String should have at least 3 characters
    Field: email, Error: The email address is not valid. It must have exactly one @-sign.
    Field: age, Error: Input should be less than 120
    """
```

## Best Practices for Basic Validation

1. **Use Appropriate Field Types**: Choose the most specific field type that fits your data (e.g., `EmailStr` for email addresses).

2. **Set Constraints**: Use `Field()` to set constraints like `min_length`, `max_length`, `ge` (greater than or equal), `le` (less than or equal), etc.

3. **Handle ValidationError**: Always handle `ValidationError` exceptions in your code to gracefully manage invalid data.

4. **Use Optional Fields**: For fields that aren't required, use `Optional[Type]` and provide a default value or `None`.

```python
from typing import Optional
from pydantic import BaseModel

class Profile(BaseModel):
    name: str
    bio: Optional[str] = None
    age: Optional[int] = None
```

5. **Leverage Union Types**: When a field can be one of several types, use `Union`.

```python
from typing import Union
from pydantic import BaseModel

class Item(BaseModel):
    id: Union[int, str]
    quantity: Union[int, float]
```

By understanding and effectively using Pydantic's basic validation features, you can ensure that your data adheres to the expected structure and constraints, catching errors early and improving the overall reliability of your application.