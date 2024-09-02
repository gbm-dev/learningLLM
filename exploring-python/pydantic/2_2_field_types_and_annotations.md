# 2.2. Field Types and Annotations

Pydantic uses Python's type annotations to define the structure and types of data in models. This section covers the various field types you can use in Pydantic models, including built-in Python types and Pydantic's custom types.

## Built-in Python Types

Pydantic supports all common Python types out of the box:

```python
from typing import List, Dict, Tuple, Set, Optional, Union
from datetime import datetime, date
from pydantic import BaseModel

class ExampleModel(BaseModel):
    string_field: str
    integer_field: int
    float_field: float
    boolean_field: bool
    list_field: List[str]
    dict_field: Dict[str, int]
    tuple_field: Tuple[int, str, float]
    set_field: Set[int]
    optional_field: Optional[str]
    union_field: Union[int, str]
    date_field: date
    datetime_field: datetime

example = ExampleModel(
    string_field="hello",
    integer_field=123,
    float_field=3.14,
    boolean_field=True,
    list_field=["a", "b", "c"],
    dict_field={"key": 42},
    tuple_field=(1, "two", 3.0),
    set_field={1, 2, 3},
    optional_field=None,
    union_field="42",
    date_field="2023-05-01",
    datetime_field="2023-05-01T12:00:00"
)
print(example)
```

## Pydantic's Custom Types

Pydantic provides several custom types for common use cases:

### EmailStr

For validating email addresses:

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr

user = User(email="user@example.com")
print(user.email)  # Output: user@example.com

# This will raise a validation error
# User(email="invalid-email")
```

### HttpUrl

For validating HTTP/HTTPS URLs:

```python
from pydantic import BaseModel, HttpUrl

class Website(BaseModel):
    url: HttpUrl

site = Website(url="https://www.example.com")
print(site.url)  # Output: https://www.example.com

# This will raise a validation error
# Website(url="not-a-url")
```

### SecretStr

For handling sensitive data:

```python
from pydantic import BaseModel, SecretStr

class Credentials(BaseModel):
    password: SecretStr

creds = Credentials(password="mysecretpassword")
print(creds.password)  # Output: SecretStr('**********')
print(creds.password.get_secret_value())  # Output: mysecretpassword
```

### conint, confloat, constr

For constrained numeric and string types:

```python
from pydantic import BaseModel, conint, confloat, constr

class ConstrainedModel(BaseModel):
    age: conint(ge=0, lt=120)  # greater than or equal to 0, less than 120
    score: confloat(ge=0, le=1)  # between 0 and 1 inclusive
    name: constr(min_length=2, max_length=50)  # length between 2 and 50

model = ConstrainedModel(age=30, score=0.75, name="Alice")
print(model)

# These will raise validation errors:
# ConstrainedModel(age=150, score=2, name="A")
```

### UUID

For handling UUID fields:

```python
from pydantic import BaseModel
from uuid import UUID

class Item(BaseModel):
    id: UUID

item = Item(id="123e4567-e89b-12d3-a456-426614174000")
print(item.id)  # Output: 123e4567-e89b-12d3-a456-426614174000
```

### Custom Types

You can also create custom types for specific use cases:

```python
from pydantic import BaseModel, constr

# Custom type for a US zip code
USZipCode = constr(regex=r'^\d{5}(-\d{4})?$')

class Address(BaseModel):
    zip_code: USZipCode

address = Address(zip_code="12345")
print(address.zip_code)  # Output: 12345

# This will raise a validation error
# Address(zip_code="invalid-zip")
```

By leveraging these field types and annotations, you can create precise and type-safe Pydantic models that accurately represent your data structures and enforce validation rules.