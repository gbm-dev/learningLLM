# 3.2. Custom Validators

While Pydantic's built-in validation is powerful, there are often cases where you need to implement custom validation logic. This section covers how to write custom validator functions and use decorator syntax for validators.

## Writing Validator Functions

Custom validators in Pydantic are methods that are decorated with the `@validator` decorator. These methods can perform additional checks or transformations on field values.

Basic syntax for a validator:

```python
from pydantic import BaseModel, validator

class User(BaseModel):
    name: str
    password: str

    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('must be at least 8 characters')
        if not any(char.isdigit() for char in v):
            raise ValueError('must contain at least one digit')
        return v
```

In this example:
- `name_must_contain_space` checks if the name contains a space and capitalizes it.
- `password_strength` checks if the password meets certain criteria.

## Decorator Syntax for Validators

The `@validator` decorator has several options to customize its behavior:

### Pre and Post Validators

- **Pre-validators**: Run before Pydantic's default validation.
- **Post-validators**: Run after Pydantic's default validation (default behavior).

```python
from pydantic import BaseModel, validator

class Order(BaseModel):
    items: List[str]
    total: float

    @validator('items', pre=True)
    def split_items(cls, v):
        if isinstance(v, str):
            return v.split(',')
        return v

    @validator('total')
    def check_total(cls, v, values):
        if 'items' in values and len(values['items']) > 5 and v < 100:
            raise ValueError('orders with more than 5 items must have a total greater than 100')
        return v
```

### Validating Multiple Fields

You can apply a single validator to multiple fields:

```python
from pydantic import BaseModel, validator

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int

    @validator('first_name', 'last_name')
    def check_name(cls, v):
        if not v.isalpha():
            raise ValueError('must contain only alphabetic characters')
        return v.capitalize()
```

### Whole Model Validation

Use `'*'` to create a validator that runs after all other validation:

```python
from pydantic import BaseModel, validator

class Triangle(BaseModel):
    side1: float
    side2: float
    side3: float

    @validator('*')
    def check_triangle_inequality(cls, v, values):
        if len(values) == 3:
            a, b, c = values['side1'], values['side2'], v
            if not (a + b > c and b + c > a and c + a > b):
                raise ValueError('triangle inequality not satisfied')
        return v
```

### Accessing Other Field Values

Validators can access the values of other fields:

```python
from pydantic import BaseModel, validator
from datetime import date

class Event(BaseModel):
    name: str
    start_date: date
    end_date: date

    @validator('end_date')
    def check_dates(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end date must be after start date')
        return v
```

## Best Practices for Custom Validators

1. **Keep Validators Simple**: Each validator should ideally check one thing. This makes them easier to understand and maintain.

2. **Use Clear Error Messages**: Provide informative error messages that guide the user on how to correct the input.

3. **Handle Edge Cases**: Consider all possible input scenarios, including None values if the field is optional.

4. **Use Type Annotations**: Annotate the return type of your validators to maintain type consistency.

5. **Avoid Side Effects**: Validators should not modify external state or have side effects.

6. **Use always=True for Optional Fields**: If you want a validator to run even when the field is not provided, use `always=True`:

```python
from pydantic import BaseModel, validator
from typing import Optional

class User(BaseModel):
    username: Optional[str] = None

    @validator('username', always=True)
    def set_default_username(cls, v):
        return v or 'anonymous'
```

By leveraging custom validators, you can implement complex validation logic that goes beyond simple type checking, ensuring that your data not only has the correct structure but also meets specific business rules and requirements.