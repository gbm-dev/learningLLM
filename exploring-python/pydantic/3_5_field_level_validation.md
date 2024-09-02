# 3.5. Field-Level Validation

Field-level validation in Pydantic allows you to apply specific validation rules to individual fields. This section covers how to implement field-specific validators and how to combine them with model-level validation for comprehensive data integrity checks.

## Specific Validation for Individual Fields

Field-level validators are defined using the `@validator` decorator and are applied to specific fields in your model.

Basic syntax:

```python
from pydantic import BaseModel, validator

class User(BaseModel):
    username: str
    email: str
    age: int

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'Must be alphanumeric'
        return v

    @validator('email')
    def email_valid(cls, v):
        assert '@' in v, 'Must be a valid email'
        return v

    @validator('age')
    def age_valid(cls, v):
        assert 18 <= v <= 120, 'Must be between 18 and 120'
        return v
```

In this example, each field has its own specific validation rule.

## Advanced Field-Level Validation Techniques

### 1. Validating Multiple Fields

You can apply a single validator to multiple fields:

```python
from pydantic import BaseModel, validator

class Rectangle(BaseModel):
    width: float
    height: float

    @validator('width', 'height')
    def check_positive(cls, v):
        assert v > 0, 'Must be positive'
        return v
```

### 2. Accessing Other Field Values

Validators can access the values of other fields:

```python
from pydantic import BaseModel, validator

class Payment(BaseModel):
    amount: float
    currency: str
    exchange_rate: float = 1.0

    @validator('exchange_rate', always=True)
    def check_exchange_rate(cls, v, values):
        currency = values.get('currency')
        if currency == 'USD':
            return 1.0
        assert v != 1.0, f'Exchange rate must be specified for {currency}'
        return v
```

### 3. Pre and Post Field Validation

You can specify whether a validator should run before or after the default validation:

```python
from pydantic import BaseModel, validator

class User(BaseModel):
    name: str

    @validator('name', pre=True)
    def remove_whitespace(cls, v):
        return v.strip() if isinstance(v, str) else v

    @validator('name')
    def check_name_length(cls, v):
        assert len(v) >= 2, 'Name must be at least 2 characters'
        return v
```

## Combining Field and Model-Level Validation

To create a comprehensive validation strategy, you can combine field-level validators with root validators:

```python
from pydantic import BaseModel, validator, root_validator

class Order(BaseModel):
    item_count: int
    price_per_item: float
    total_price: float

    @validator('item_count')
    def check_item_count(cls, v):
        assert v > 0, 'Must order at least one item'
        return v

    @validator('price_per_item')
    def check_price(cls, v):
        assert v > 0, 'Price must be positive'
        return v

    @root_validator
    def check_total_price(cls, values):
        item_count = values.get('item_count')
        price_per_item = values.get('price_per_item')
        total_price = values.get('total_price')
        
        if all(v is not None for v in (item_count, price_per_item, total_price)):
            assert total_price == item_count * price_per_item, 'Total price does not match item count and price'
        
        return values
```

In this example:
- Field-level validators ensure that `item_count` and `price_per_item` are positive.
- The root validator checks if the `total_price` matches the calculation from `item_count` and `price_per_item`.

## Best Practices for Field-Level Validation

1. **Keep Validators Simple**: Each validator should ideally check one thing, making them easier to understand and maintain.

2. **Use Clear Error Messages**: Provide informative error messages that guide the user on how to correct the input.

3. **Handle Type Errors**: Remember that validators might receive data of unexpected types, especially when `pre=True`.

4. **Use `always=True` for Optional Fields**: If you want a validator to run even when the field is not provided, use `always=True`.

5. **Prefer Field-Level Validation**: Use field-level validators when possible, and reserve root validators for cross-field validations.

6. **Combine with Pydantic's Built-in Validators**: Use Pydantic's `Field` constraints along with custom validators for comprehensive validation.

```python
from pydantic import BaseModel, Field, validator

class Product(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    price: float = Field(..., gt=0)

    @validator('name')
    def name_must_be_titlecase(cls, v):
        return v.title()
```

By effectively using field-level validation and combining it with model-level validation, you can create robust Pydantic models that ensure data integrity at both the individual field level and across the entire model.