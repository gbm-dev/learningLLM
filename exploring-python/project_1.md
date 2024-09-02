# Practical Project 1: Simple Data Validation Application

## Project Overview
In this project, you will build a simple command-line application that validates various types of data using Pydantic. This project will help reinforce the concepts learned in the first three sections of the course.

## Project Goals
1. Create Pydantic models for different types of data
2. Implement a command-line interface for data input
3. Validate user input against Pydantic models
4. Handle and display validation errors
5. Provide helpful feedback to the user

## Project Description
You will create a "Data Validator" application that can validate different types of data such as:
- Personal Information (name, age, email)
- Product Information (name, price, category)
- Address Information (street, city, country, zip code)

The application will:
1. Prompt the user to choose a type of data to validate
2. Ask for relevant information based on the chosen type
3. Attempt to create a Pydantic model instance with the provided data
4. Display the validated data if successful, or show validation errors if not

## Implementation Steps

### 1. Set up the project
- Create a new Python file named `data_validator.py`
- Import necessary modules (including Pydantic)

### 2. Define Pydantic models
Create models for each data type, for example:

```python
from pydantic import BaseModel, EmailStr, conint, constr, confloat

class PersonalInfo(BaseModel):
    name: constr(min_length=2, max_length=50)
    age: conint(ge=0, le=120)
    email: EmailStr

class ProductInfo(BaseModel):
    name: constr(min_length=1, max_length=100)
    price: confloat(gt=0)
    category: str

class AddressInfo(BaseModel):
    street: str
    city: str
    country: str
    zip_code: str
```

### 3. Implement the command-line interface
- Create a main loop that presents options to the user
- Implement functions to gather input for each data type

### 4. Validate data and handle errors
- Attempt to create model instances with user input
- Catch and handle ValidationError exceptions
- Display helpful error messages or success confirmation

### 5. (Optional) Add data persistence
- Save validated data to a JSON file
- Implement a feature to view previously validated data

## Expected Outcome
Upon completion, you will have a functioning command-line application that demonstrates practical use of Pydantic for data validation. This project will reinforce your understanding of:
- Creating and using Pydantic models
- Handling user input and validation errors
- Applying constraints to fields
- Basic error handling and user interaction

## Bonus Challenges
1. Implement custom validators for specific fields
2. Add an option to export validated data to CSV format
3. Create a simple web interface using a micro web framework like Flask