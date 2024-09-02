# 2.6. Nested Models

Pydantic allows you to create complex data structures by nesting models within other models. This feature is particularly useful when dealing with hierarchical or relational data. This section covers how to create and work with nested models.

## Creating Models within Models

To create nested models, you simply use one Pydantic model as a field type in another model:

```python
from pydantic import BaseModel
from typing import List

class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class User(BaseModel):
    name: str
    email: str
    address: Address

# Creating an instance with nested data
user = User(
    name="John Doe",
    email="john@example.com",
    address={
        "street": "123 Main St",
        "city": "Anytown",
        "country": "USA",
        "postal_code": "12345"
    }
)

print(user)
# Output: name='John Doe' email='john@example.com' address=Address(street='123 Main St', city='Anytown', country='USA', postal_code='12345')

# Accessing nested data
print(user.address.city)  # Output: Anytown
```

## Handling Complex Data Structures

Nested models can be used to represent more complex data structures, including lists of models and deeply nested structures:

```python
from pydantic import BaseModel
from typing import List, Optional

class Comment(BaseModel):
    id: int
    content: str
    author: str

class Post(BaseModel):
    id: int
    title: str
    content: str
    comments: List[Comment]

class Blog(BaseModel):
    name: str
    url: str
    posts: List[Post]

# Creating a complex nested structure
blog = Blog(
    name="My Tech Blog",
    url="https://mytechblog.com",
    posts=[
        Post(
            id=1,
            title="Introduction to Pydantic",
            content="Pydantic is a great library for data validation...",
            comments=[
                Comment(id=1, content="Great post!", author="Alice"),
                Comment(id=2, content="Thanks for sharing", author="Bob")
            ]
        ),
        Post(
            id=2,
            title="Advanced Pydantic Features",
            content="Let's explore some advanced features of Pydantic...",
            comments=[]
        )
    ]
)

print(blog.posts[0].comments[0].author)  # Output: Alice
```

## Advantages of Nested Models

1. **Type Safety**: Nested models ensure type safety at multiple levels of your data structure.
2. **Validation**: Each nested model performs its own validation, ensuring data integrity throughout the structure.
3. **Clear Structure**: Nested models provide a clear and intuitive representation of complex data structures.
4. **Reusability**: You can reuse nested models in different contexts, promoting code reuse.

## Best Practices for Nested Models

1. **Avoid Deep Nesting**: While Pydantic supports arbitrary levels of nesting, too many levels can make your models hard to read and use. Consider flattening your structure if it becomes too complex.

2. **Use Type Hints**: Always use type hints for nested models to improve readability and enable better IDE support.

3. **Consider Optional Fields**: Use `Optional` for fields that might not always be present in nested structures.

4. **Validate at the Right Level**: Ensure that validation logic is implemented at the appropriate level in your nested structure.

5. **Use Aliases for Flexibility**: If your nested data might come from sources with different field names, consider using aliases to map between them.

```python
from pydantic import BaseModel, Field

class Coordinate(BaseModel):
    lat: float = Field(..., alias="latitude")
    lon: float = Field(..., alias="longitude")

class Location(BaseModel):
    name: str
    coord: Coordinate

loc = Location(name="Eiffel Tower", coord={"latitude": 48.8584, "longitude": 2.2945})
print(loc)
# Output: name='Eiffel Tower' coord=Coordinate(lat=48.8584, lon=2.2945)
```

By effectively using nested models, you can create rich, type-safe representations of complex data structures in your Python applications.