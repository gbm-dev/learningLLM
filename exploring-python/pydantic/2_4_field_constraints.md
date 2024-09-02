# 2.4. Field Constraints

Pydantic allows you to add constraints to fields, ensuring that the data not only matches the correct type but also adheres to specific rules. This section covers how to use built-in constraints and create custom ones.

## Using Built-in Constraints

Pydantic provides several built-in constraints that you can use with the `Field` function:

### Length Constraints

For strings, lists, and other sequences:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    tags: List[str] = Field(default_factory=list, max_length=5)

user = User(username="alice", tags=["staff", "admin"])
print(user)

# These will raise validation errors:
# User(username="a")  # Too short
# User(username="a" * 51)  # Too long
# User(username="alice", tags=["a", "b", "c", "d", "e", "f"])  # Too many tags
```

### Numeric Constraints

For integers and floats:

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: int = Field(..., ge=1)  # greater than or equal to 1
    price: float = Field(..., gt=0, le=1000)  # greater than 0 and less than or equal to 1000
    quantity: int = Field(..., multiple_of=5)  # must be a multiple of 5

product = Product(id=1, price=99.99, quantity=15)
print(product)

# These will raise validation errors:
# Product(id=0, price=99.99, quantity=15)  # id too low
# Product(id=1, price=1001, quantity=15)  # price too high
# Product(id=1, price=99.99, quantity=17)  # quantity not a multiple of 5
```

### Regex Constraints

For string patterns:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    username: str = Field(..., regex="^[a-zA-Z0-9_]+$")
    phone: str = Field(..., regex=r"^\+?1?\d{9,15}$")

user = User(username="john_doe", phone="+1234567890")
print(user)

# These will raise validation errors:
# User(username="john@doe", phone="+1234567890")  # Invalid username
# User(username="john_doe", phone="123")  # Invalid phone number
```

## Creating Custom Constraints

For more complex validation rules, you can create custom validators:

```python
from pydantic import BaseModel, Field, validator

class Order(BaseModel):
    items: List[str] = Field(..., min_length=1)
    total: float = Field(..., gt=0)

    @validator('total')
    def validate_total(cls, v, values):
        if 'items' in values and len(values['items']) > 5 and v < 100:
            raise ValueError("Orders with more than 5 items must have a total greater than 100")
        return v

order1 = Order(items=["item1", "item2"], total=50)
print(order1)

# This will raise a validation error:
# Order(items=["item1", "item2", "item3", "item4", "item5", "item6"], total=50)
```

In this example, we've created a custom validator that checks if an order with more than 5 items has a total greater than 100.

By using these field constraints, you can ensure that your data not only has the correct types but also meets specific business rules and requirements.