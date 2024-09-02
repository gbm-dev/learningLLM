# 2.7. Model Inheritance

Pydantic supports model inheritance, allowing you to create hierarchies of models. This feature is useful for creating specialized versions of base models or for sharing common fields across multiple models. This section covers how to use model inheritance and composition techniques in Pydantic.

## Extending Models

To create a new model that inherits from an existing one, simply subclass the base model:

```python
from pydantic import BaseModel
from datetime import datetime

class BaseItem(BaseModel):
    id: int
    created_at: datetime = Field(default_factory=datetime.now)

class Book(BaseItem):
    title: str
    author: str
    pages: int

class Electronics(BaseItem):
    name: str
    brand: str
    price: float

# Using the inherited models
book = Book(id=1, title="1984", author="George Orwell", pages=328)
phone = Electronics(id=2, name="Smartphone", brand="TechCo", price=599.99)

print(book)
# Output: id=1 created_at=datetime.datetime(2023, 5, 1, 12, 0, 0, 123456) title='1984' author='George Orwell' pages=328

print(phone)
# Output: id=2 created_at=datetime.datetime(2023, 5, 1, 12, 0, 0, 123457) name='Smartphone' brand='TechCo' price=599.99
```

In this example, both `Book` and `Electronics` inherit the `id` and `created_at` fields from `BaseItem`.

## Overriding Fields

You can override fields from the base model in the child model:

```python
from pydantic import BaseModel, Field

class BaseUser(BaseModel):
    name: str
    email: str = Field(..., regex=r"[^@]+@[^@]+\.[^@]+")

class AdminUser(BaseUser):
    email: str = Field(..., regex=r"[^@]+@admin\.[^@]+")
    privileges: List[str]

# This will work
regular_user = BaseUser(name="John", email="john@example.com")

# This will work
admin_user = AdminUser(name="Alice", email="alice@admin.com", privileges=["create", "delete"])

# This will raise a validation error
# AdminUser(name="Bob", email="bob@example.com", privileges=["read"])
```

In this example, `AdminUser` overrides the `email` field with a more restrictive regex pattern.

## Mixin Classes and Composition

Mixin classes are a way to add functionality to models without using inheritance. They're particularly useful when you want to add the same set of fields or methods to multiple unrelated models:

```python
from pydantic import BaseModel
from datetime import datetime

class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class UserMixin(BaseModel):
    username: str
    email: str

class Post(TimestampMixin, UserMixin):
    title: str
    content: str

class Comment(TimestampMixin, UserMixin):
    post_id: int
    text: str

post = Post(username="john_doe", email="john@example.com", title="Hello, World!", content="This is my first post.")
comment = Comment(username="jane_doe", email="jane@example.com", post_id=1, text="Great post!")

print(post)
# Output: created_at=datetime.datetime(...) updated_at=datetime.datetime(...) username='john_doe' email='john@example.com' title='Hello, World!' content='This is my first post.'

print(comment)
# Output: created_at=datetime.datetime(...) updated_at=datetime.datetime(...) username='jane_doe' email='jane@example.com' post_id=1 text='Great post!'
```

In this example, both `Post` and `Comment` use the `TimestampMixin` and `UserMixin` to include common fields.

## Best Practices for Model Inheritance

1. **Use Inheritance Judiciously**: While inheritance can be powerful, overuse can lead to complex hierarchies. Use it when there's a clear "is-a" relationship between models.

2. **Prefer Composition**: For sharing functionality across unrelated models, consider using mixins or composition over deep inheritance hierarchies.

3. **Be Careful with Field Overrides**: When overriding fields, ensure that the new definition is compatible with the base definition to avoid unexpected behavior.

4. **Document Inherited Behavior**: Clearly document which fields and behaviors are inherited in your model classes.

5. **Use Abstract Base Classes**: For creating base models that shouldn't be instantiated directly, consider using Python's `abc` module:

```python
from abc import ABC
from pydantic import BaseModel

class Animal(BaseModel, ABC):
    name: str
    species: str

class Dog(Animal):
    breed: str

class Cat(Animal):
    lives_left: int = 9

# This will work
dog = Dog(name="Buddy", species="Canis familiaris", breed="Labrador")

# This will work
cat = Cat(name="Whiskers", species="Felis catus")

# This will raise a TypeError
# animal = Animal(name="Generic", species="Animalus genericus")
```

By using model inheritance effectively, you can create more maintainable and DRY (Don't Repeat Yourself) code when working with related data structures in your Pydantic models.