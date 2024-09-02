# 2.5. Custom Field Types

While Pydantic provides a wide range of built-in types, there may be cases where you need to create custom field types to handle specific data structures or validation requirements. This section covers how to define and use custom field types in Pydantic models.

## Defining Custom Types

To create a custom type in Pydantic, you typically need to:

1. Define a new class that inherits from an existing type or `pydantic.BaseModel`.
2. Implement the `__get_validators__` method to yield validator functions.
3. Implement the validation logic in the validator functions.

Here's an example of a custom type for a hexadecimal color code:

```python
from pydantic import BaseModel, ValidationError
from typing import Any

class HexColor:
    def __init__(self, value: str):
        self.value = value

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if not v.startswith('#'):
            raise ValueError('must start with a "#"')
        if len(v) != 7:
            raise ValueError('must be 7 characters long')
        try:
            int(v[1:], 16)
        except ValueError:
            raise ValueError('invalid hexadecimal color code')
        return cls(v)

    def __repr__(self):
        return f'HexColor({self.value!r})'

class ColorModel(BaseModel):
    color: HexColor

# Valid usage
color_model = ColorModel(color='#0000FF')
print(color_model.color)  # Output: HexColor('#0000FF')

# These will raise validation errors:
# ColorModel(color='0000FF')  # Missing '#'
# ColorModel(color='#00FF')  # Too short
# ColorModel(color='#GGGGGG')  # Invalid hexadecimal
```

## When and How to Use Custom Types

Custom types are useful in several scenarios:

1. **Complex validation**: When you need to perform complex validation that goes beyond simple type checking or built-in constraints.

2. **Domain-specific types**: For representing domain-specific concepts that aren't covered by built-in types.

3. **Data normalization**: When you want to normalize data as part of the validation process.

4. **Custom serialization/deserialization**: For types that need special handling when converting to/from JSON or other formats.

Here's an example of a custom type that normalizes and validates ISBN numbers:

```python
from pydantic import BaseModel, ValidationError
import re

class ISBN:
    def __init__(self, value: str):
        self.value = value

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        
        # Remove hyphens and spaces
        v = re.sub(r'[\s-]', '', v)
        
        if len(v) not in (10, 13):
            raise ValueError('ISBN must be 10 or 13 characters long')
        
        if len(v) == 10:
            if not v[:9].isdigit() or not (v[9].isdigit() or v[9].lower() == 'x'):
                raise ValueError('Invalid ISBN-10 format')
        else:
            if not v.isdigit():
                raise ValueError('Invalid ISBN-13 format')
        
        return cls(v)

    def __repr__(self):
        return f'ISBN({self.value!r})'

class Book(BaseModel):
    title: str
    isbn: ISBN

# Valid usage
book = Book(title="Python Programming", isbn="978-1-4919-1903-4")
print(book.isbn)  # Output: ISBN('9781491919034')

# These will raise validation errors:
# Book(title="Invalid Book", isbn="123")  # Too short
# Book(title="Invalid Book", isbn="978-1-4919-1903-A")  # Invalid character
```

In this example, the `ISBN` custom type normalizes the input by removing hyphens and spaces, and then validates the format for both ISBN-10 and ISBN-13.

## Best Practices for Custom Types

When creating custom types:

1. **Keep it simple**: Try to use built-in types and constraints when possible. Only create custom types when necessary.

2. **Thorough validation**: Ensure your custom type performs comprehensive validation to catch all possible errors.

3. **Clear error messages**: Provide clear and informative error messages to help users understand validation failures.

4. **Consider performance**: Be mindful of the performance impact of complex validation logic, especially for large datasets.

5. **Documentation**: Document your custom types thoroughly, including their purpose, validation rules, and usage examples.

By creating custom field types, you can extend Pydantic's capabilities to handle complex, domain-specific data structures while maintaining strong type checking and validation.