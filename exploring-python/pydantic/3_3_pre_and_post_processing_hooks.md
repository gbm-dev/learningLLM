# 3.3. Pre and Post-Processing Hooks

Pydantic provides mechanisms to modify data before and after validation. These hooks allow you to transform input data, perform complex validations, or modify the final model state. This section covers how to use pre and post-processing hooks and explores use cases for each.

## Modifying Data Before Validation

### Root Validators

Root validators allow you to access and modify the entire input data before it's parsed into individual fields. They're defined using the `@root_validator(pre=True)` decorator.

```python
from pydantic import BaseModel, root_validator

class User(BaseModel):
    username: str
    password: str

    @root_validator(pre=True)
    def check_credentials(cls, values):
        username = values.get('username', '')
        password = values.get('password', '')
        if username == 'admin' and not password.startswith('secret_'):
            raise ValueError('Invalid admin password')
        return values
```

### Field Aliases

Field aliases allow you to accept input data with different key names:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    user_id: int = Field(..., alias='id')
    full_name: str = Field(..., alias='name')
```

## Modifying Data After Validation

### Post-Validation Root Validators

You can use root validators to modify the final model state after all fields have been validated:

```python
from pydantic import BaseModel, root_validator

class Order(BaseModel):
    items: List[str]
    total: float

    @root_validator
    def calculate_total(cls, values):
        items = values.get('items', [])
        values['total'] = sum(len(item) for item in items) * 1.5
        return values
```

### Custom Setter Methods

You can define custom setter methods for fields to modify their values after validation:

```python
from pydantic import BaseModel, validator

class User(BaseModel):
    name: str
    email: str

    @validator('email')
    def lowercase_email(cls, v):
        return v.lower()
```

## Use Cases for Preprocessing and Postprocessing

### Preprocessing Use Cases

1. **Data Normalization**: Standardize input data before validation.

```python
from pydantic import BaseModel, root_validator

class Address(BaseModel):
    street: str
    city: str
    country: str

    @root_validator(pre=True)
    def normalize_country(cls, values):
        if 'country' in values:
            values['country'] = values['country'].upper()
        return values
```

2. **Default Value Injection**: Add default values for missing fields.

```python
from pydantic import BaseModel, root_validator
from datetime import datetime

class Event(BaseModel):
    name: str
    date: datetime

    @root_validator(pre=True)
    def set_default_date(cls, values):
        if 'date' not in values:
            values['date'] = datetime.now()
        return values
```

3. **Input Format Conversion**: Convert input from one format to another.

```python
from pydantic import BaseModel, root_validator
import json

class Config(BaseModel):
    settings: dict

    @root_validator(pre=True)
    def parse_json(cls, values):
        if isinstance(values.get('settings'), str):
            try:
                values['settings'] = json.loads(values['settings'])
            except json.JSONDecodeError:
                raise ValueError('Invalid JSON in settings')
        return values
```

### Postprocessing Use Cases

1. **Derived Field Calculation**: Compute values based on other fields.

```python
from pydantic import BaseModel, root_validator

class Rectangle(BaseModel):
    width: float
    height: float
    area: float = 0

    @root_validator
    def calculate_area(cls, values):
        values['area'] = values.get('width', 0) * values.get('height', 0)
        return values
```

2. **Data Enrichment**: Add additional information to the model.

```python
from pydantic import BaseModel, root_validator
import httpx

class User(BaseModel):
    username: str
    avatar_url: str = ''

    @root_validator
    def fetch_avatar(cls, values):
        username = values.get('username')
        if username and not values.get('avatar_url'):
            response = httpx.get(f'https://api.github.com/users/{username}')
            if response.status_code == 200:
                values['avatar_url'] = response.json().get('avatar_url', '')
        return values
```

3. **Consistency Checks**: Ensure logical consistency across fields.

```python
from pydantic import BaseModel, root_validator
from datetime import date

class Reservation(BaseModel):
    check_in: date
    check_out: date
    nights: int

    @root_validator
    def check_dates_and_nights(cls, values):
        check_in = values.get('check_in')
        check_out = values.get('check_out')
        if check_in and check_out:
            nights = (check_out - check_in).days
            if nights != values.get('nights'):
                values['nights'] = nights
        return values
```

## Best Practices for Pre and Post-Processing Hooks

1. **Keep It Simple**: Try to perform one clear task per hook.
2. **Handle Exceptions**: Always handle potential exceptions in your hooks to provide clear error messages.
3. **Document Behavior**: Clearly document any modifications made by hooks, especially if they change input data.
4. **Consider Performance**: Be mindful of performance implications, especially for hooks that perform external operations.
5. **Maintain Immutability**: When possible, create new objects instead of modifying existing ones to maintain immutability.

By effectively using pre and post-processing hooks, you can create more flexible and powerful Pydantic models that can handle complex data transformations and validations while maintaining clean and understandable code.