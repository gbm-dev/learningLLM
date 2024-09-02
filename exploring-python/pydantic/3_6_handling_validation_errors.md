# 3.6. Handling Validation Errors

Proper handling of validation errors is crucial for creating user-friendly applications. This section covers understanding Pydantic's `ValidationError`, creating custom error messages, implementing custom error classes, and strategies for error localization.

## Understanding ValidationError

When Pydantic encounters invalid data during model instantiation or validation, it raises a `ValidationError`. This error contains detailed information about what went wrong.

Basic example:

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    username: str
    age: int

try:
    User(username='john', age='not an integer')
except ValidationError as e:
    print(e)
    """
    1 validation error for User
    age
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='not an integer', input_type=str]
    """
```

### Accessing Error Details

You can access detailed error information programmatically:

```python
try:
    User(username='john', age='not an integer')
except ValidationError as e:
    print(e.errors())
    """
    [
        {
            'loc': ('age',),
            'msg': 'Input should be a valid integer, unable to parse string as an integer',
            'type': 'int_parsing',
            'input': 'not an integer',
            'ctx': {...}
        }
    ]
    """
```

## Custom Error Messages

You can provide custom error messages in your validators to make errors more user-friendly and context-specific.

### Field-level Custom Messages

```python
from pydantic import BaseModel, validator

class User(BaseModel):
    username: str
    age: int

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

    @validator('age')
    def age_valid(cls, v):
        if v < 18:
            raise ValueError('User must be 18 or older')
        return v
```

### Model-level Custom Messages

For root validators:

```python
from pydantic import BaseModel, root_validator

class Order(BaseModel):
    items: int
    price_per_item: float

    @root_validator
    def check_total(cls, values):
        items = values.get('items')
        price = values.get('price_per_item')
        if items and price and items * price > 1000:
            raise ValueError('Total order value cannot exceed 1000')
        return values
```

## Creating Custom Error Classes

For more complex error handling, you can create custom error classes:

```python
from pydantic import BaseModel, validator

class AgeError(ValueError):
    def __init__(self, age: int, limit: int):
        self.age = age
        self.limit = limit
        super().__init__(f"Age {age} is below the limit of {limit}")

class User(BaseModel):
    username: str
    age: int

    @validator('age')
    def age_valid(cls, v):
        if v < 18:
            raise AgeError(v, 18)
        return v

try:
    User(username='john', age=16)
except ValidationError as e:
    for error in e.errors():
        if isinstance(error['exc'], AgeError):
            print(f"Custom error: {error['exc']}")
        else:
            print(f"Standard error: {error['msg']}")
```

## Error Localization Strategies

Localizing error messages is important for international applications. Here are some strategies:

### 1. Using gettext

You can use Python's `gettext` module for internationalization:

```python
import gettext
from pydantic import BaseModel, validator

# Set up gettext
_ = gettext.gettext

class User(BaseModel):
    username: str
    age: int

    @validator('age')
    def age_valid(cls, v):
        if v < 18:
            raise ValueError(_('User must be 18 or older'))
        return v
```

### 2. Error Message Mapping

Create a dictionary of error messages for different languages:

```python
from pydantic import BaseModel, validator

ERROR_MESSAGES = {
    'en': {
        'age_limit': 'User must be 18 or older',
    },
    'es': {
        'age_limit': 'El usuario debe tener 18 años o más',
    }
}

class User(BaseModel):
    username: str
    age: int

    @validator('age')
    def age_valid(cls, v):
        if v < 18:
            raise ValueError('age_limit')
        return v

    class Config:
        error_msg_templates = ERROR_MESSAGES['en']  # Set default language
```

### 3. Custom Error Handler

Implement a custom error handler that translates error messages:

```python
from pydantic import BaseModel, ValidationError

def translate_error(error_type, lang='en'):
    translations = {
        'en': {
            'int_parsing': 'Must be a valid integer',
            'age_limit': 'Must be 18 or older',
        },
        'es': {
            'int_parsing': 'Debe ser un número entero válido',
            'age_limit': 'Debe tener 18 años o más',
        }
    }
    return translations.get(lang, {}).get(error_type, error_type)

class User(BaseModel):
    age: int

try:
    User(age='not an integer')
except ValidationError as e:
    for error in e.errors():
        print(translate_error(error['type'], 'es'))
```

## Best Practices for Handling Validation Errors

1. **Be Specific**: Provide clear, specific error messages that help users understand what went wrong.

2. **Localize Errors**: Implement a localization strategy for error messages in multi-language applications.

3. **Consistent Error Format**: Maintain a consistent format for error messages across your application.

4. **Separate Presentation from Logic**: Keep error generation separate from error presentation to maintain flexibility.

5. **Log Validation Errors**: Consider logging validation errors for debugging and monitoring purposes.

6. **Graceful Degradation**: In web applications, ensure that validation errors are handled gracefully on both client and server sides.

7. **Security Considerations**: Be cautious about exposing sensitive information in error messages, especially in production environments.