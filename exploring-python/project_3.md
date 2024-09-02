# Practical Project 3: Full-Stack Application with Pydantic

## Project Overview
In this comprehensive project, you will build a full-stack inventory management system for a small e-commerce business. This project will integrate various aspects of Pydantic usage in a complex, real-world scenario.

## Project Goals
1. Develop a robust backend API using FastAPI and Pydantic
2. Create a frontend application using a modern framework (e.g., React)
3. Implement complex data models with nested structures and relationships
4. Use Pydantic for configuration management and environment variables
5. Implement advanced validation, including cross-field and conditional validation
6. Integrate with external services (e.g., payment gateway, shipping API) using Pydantic
7. Implement comprehensive testing and documentation

## Project Description
You will create an "Inventory Management System" that allows users to:
- Manage product inventory (add, update, delete products)
- Process orders and update inventory accordingly
- Generate reports on inventory status and sales
- Manage user roles and permissions
- Integrate with external services for payments and shipping

## Implementation Steps

### 1. Set up the project
- Create separate directories for backend and frontend
- Set up a PostgreSQL database for data persistence
- Configure development and production environments

### 2. Define complex Pydantic models
Create models for various entities in the system, for example:

```python
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"
    # ... other categories

class Product(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    price: float = Field(..., gt=0)
    category: ProductCategory
    stock_quantity: int = Field(..., ge=0)
    created_at: datetime
    updated_at: datetime

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    price_at_order: float

class Order(BaseModel):
    id: int
    user_id: int
    items: List[OrderItem]
    total_amount: float
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    @validator('total_amount')
    def check_total_amount(cls, v, values):
        if 'items' in values:
            calculated_total = sum(item.price_at_order * item.quantity for item in values['items'])
            if abs(v - calculated_total) > 0.01:  # Allow small float precision differences
                raise ValueError("Total amount does not match sum of item prices")
        return v

class User(BaseModel):
    id: int
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    is_admin: bool = False

class InventoryReport(BaseModel):
    generated_at: datetime
    total_products: int
    low_stock_products: List[Product]
    total_value: float

# ... more models as needed
```

### 3. Implement backend API
- Create FastAPI endpoints for all CRUD operations
- Implement complex business logic (e.g., order processing, inventory updates)
- Use Pydantic for request/response models and validation

### 4. Develop frontend application
- Create a React application for the user interface
- Implement state management (e.g., Redux) and API integration
- Use Pydantic models to type-check API responses (with a tool like quicktype)

### 5. Implement advanced features
- Role-based access control using Pydantic models
- Implement a plugin system for extensibility (e.g., custom report generation)
- Create a robust error handling and logging system

### 6. Integrate external services
- Implement a mock payment gateway integration
- Create a shipping cost calculator using an external API

### 7. Configuration management
- Use Pydantic's BaseSettings for managing environment-specific configurations
- Implement feature flags using Pydantic

### 8. Testing and documentation
- Write comprehensive unit and integration tests
- Generate detailed API documentation using Pydantic and FastAPI
- Create user and developer documentation

## Expected Outcome
Upon completion, you will have a fully functional inventory management system that demonstrates:
- Complex data modeling and validation with Pydantic
- Integration of Pydantic in a full-stack application
- Advanced features like plugin systems and role-based access control
- Practical usage of Pydantic for configuration and external service integration
- Comprehensive testing and documentation practices

## Bonus Challenges
1. Implement real-time updates using WebSockets
2. Add data visualization for inventory reports
3. Implement a recommendation system for related products
4. Create a mobile app version using React Native

This project will give you extensive experience in using Pydantic in a complex, real-world application, touching on almost all aspects covered in the course.
```

These two additional projects provide increasingly complex and realistic scenarios for applying Pydantic knowledge. They cover a wide range of topics from the course and allow students to gain practical experience in using Pydantic in different contexts, from API development to full-stack applications.