Here's the combined document that integrates the content from both parts and additional information:

---

# 2.3. Default Values

Default values in Pydantic models allow you to specify fallback values for fields when they are not provided during model instantiation. This section covers how to set and use default values, including dynamic default values.

## Setting and Using Default Values

You can set default values for fields in Pydantic models using the following syntax:

```python
from pydantic import BaseModel
from typing import List

class User(BaseModel):
    name: str
    age: int = 18
    is_active: bool = True
    tags: List[str] = []

# Create a user with only a name
user1 = User(name="Alice")
print(user1)
# Output: name='Alice' age=18 is_active=True tags=[]

# Create a user overriding some default values
user2 = User(name="Bob", age=25, tags=["employee"])
print(user2)
# Output: name='Bob' age=25 is_active=True tags=['employee']
```

In this example:
- `name` has no default value and is required.
- `age` has a default value of 18.
- `is_active` has a default value of True.
- `tags` has a default value of an empty list.

## Dynamic Default Values

Sometimes you need default values that are computed at runtime. Pydantic provides two main ways to achieve this:

### 1. Using the `default_factory` Parameter

The `default_factory` parameter allows you to specify a function that will be called to generate the default value:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
import uuid

def generate_id():
    return str(uuid.uuid4())

class Item(BaseModel):
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=datetime.now)
    tags: List[str] = Field(default_factory=list)

item = Item()
print(item)
# Output: id='f47ac10b-58cc-4372-a567-0e02b2c3d479' created_at=datetime.datetime(2023, 5, 1, 12, 0, 0, 123456) tags=[]
```

In this example:
- `id` uses a custom function to generate a UUID.
- `created_at` uses `datetime.now` to set the current timestamp.
- `tags` uses the built-in `list` function to create an empty list.

### 2. Using a Lambda Function

For simple computations, you can use a lambda function directly:

```python
from pydantic import BaseModel, Field
import random

class RandomModel(BaseModel):
    random_int: int = Field(default_factory=lambda: random.randint(1, 100))
    random_float: float = Field(default_factory=lambda: random.uniform(0, 1))

model = RandomModel()
print(model)
# Output: random_int=42 random_float=0.12345
```

### 3. Using `__init__` for Complex Default Logic

For more complex default value logic, you can override the `__init__` method:

```python
from pydantic import BaseModel
from datetime import datetime, timedelta

class Subscription(BaseModel):
    start_date: datetime
    end_date: datetime

    def __init__(self, **data):
        if 'start_date' not in data:
            data['start_date'] = datetime.now()
        if 'end_date' not in data:
            data['end_date'] = data['start_date'] + timedelta(days=30)
        super().__init__(**data)

# Create a subscription with default dates
sub1 = Subscription()
print(sub1)
# Output: start_date=datetime.datetime(2023, 5, 1, 12, 0, 0, 123456) end_date=datetime.datetime(2023, 5, 31, 12, 0, 0, 123456)

# Create a subscription with a custom start date
sub2 = Subscription(start_date=datetime(2023, 6, 1))
print(sub2)
# Output: start_date=datetime.datetime(2023, 6, 1, 0, 0) end_date=datetime.datetime(2023, 7, 1, 0, 0)
```

In this example:

- The `__init__` method checks if `start_date` or `end_date` is provided in the input data. If not, it sets `start_date` to the current time and `end_date` to 30 days after `start_date`.
- This allows for more complex logic for setting default values that depend on other fields or external factors.

## Best Practices for Default Values

When working with default values in Pydantic models, consider the following best practices:

1. **Immutable Defaults**: Use immutable types for default values when possible to avoid shared state issues.

```python
class BadExample(BaseModel):
    items: List[str] = []  # Bad: all instances will share the same list

class GoodExample(BaseModel):
    items: List[str] = Field(default_factory=list)  # Good: each instance gets its own list
```

2. **Type Consistency**: Ensure that default values match the field's type annotation. This ensures that all values conform to expected types, which helps maintain data integrity.

3. **Meaningful Defaults**: Choose default values that make sense for your application's domain. This helps make models more intuitive and reduces the need for additional validation logic.

4. **Documentation**: Use the `Field` class to add descriptions to your fields, especially when using default values. This makes your models more understandable to others who might use them.

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    age: int = Field(default=18, description="Age of the user (must be 18 or older)")
```

5. **Avoid Complex Computations**: For performance reasons, avoid computationally expensive default values. If needed, consider using lazy evaluation or caching.

By following these practices, you can create more robust and maintainable Pydantic models with appropriate default values.

## Summary

Pydantic's support for default values and validation allows for robust data modeling and validation in Python applications. By setting default values and using built-in validation, you can ensure that your data models behave predictably and catch errors early in the application lifecycle.

### Next Steps

The following sections will dive deeper into custom validators, pre- and post-processing hooks, root validators, field-level validation, and handling validation errors. Understanding these advanced features will further enhance your ability to handle complex data validation scenarios effectively.