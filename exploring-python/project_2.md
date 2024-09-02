# Practical Project 2: Building a RESTful API with Pydantic and FastAPI

## Project Overview
In this project, you will build a RESTful API for a simple blog application using FastAPI and Pydantic. This project will demonstrate how to use Pydantic for request/response modeling, data validation, and integration with a database.

## Project Goals
1. Create a FastAPI application with Pydantic models
2. Implement CRUD operations for blog posts and comments
3. Integrate with a database (SQLite with SQLAlchemy)
4. Implement advanced validation techniques
5. Generate API documentation using Pydantic and FastAPI

## Project Description
You will create a "Blog API" that allows users to:
- Create, read, update, and delete blog posts
- Add comments to blog posts
- Retrieve posts with their comments
- Filter and sort blog posts

## Implementation Steps

### 1. Set up the project
- Create a new Python project and install required dependencies (FastAPI, Pydantic, SQLAlchemy, etc.)
- Set up the project structure

### 2. Define Pydantic models
Create models for blog posts and comments, for example:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    post_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    comments: List[Comment] = []

    class Config:
        orm_mode = True

class PostList(BaseModel):
    posts: List[Post]
    total: int
```

### 3. Set up database models and connection
- Create SQLAlchemy models corresponding to the Pydantic models
- Set up database connection and session management

### 4. Implement API endpoints
Create FastAPI route handlers for:
- Creating a new blog post
- Retrieving a single post and its comments
- Updating a blog post
- Deleting a blog post
- Listing all blog posts with pagination and filtering
- Adding a comment to a blog post

### 5. Implement advanced validation
- Add custom validators for specific fields (e.g., no profanity in post content)
- Implement dependency injection for user authentication (simulated)

### 6. Generate API documentation
- Use FastAPI's built-in Swagger UI integration
- Customize OpenAPI schema generation using Pydantic models

### 7. Write tests
- Implement unit tests for Pydantic models
- Create integration tests for API endpoints

## Expected Outcome
Upon completion, you will have a functioning RESTful API for a blog application that demonstrates:
- Integration of Pydantic with FastAPI
- Database operations with SQLAlchemy and Pydantic
- Advanced validation techniques
- API documentation generation
- Testing strategies for Pydantic-based APIs

## Bonus Challenges
1. Implement user authentication and authorization
2. Add rate limiting to API endpoints
3. Implement a caching layer for frequently accessed data
4. Create a simple front-end application to consume the API