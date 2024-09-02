# 3.4. Root Validators

Root validators in Pydantic allow you to validate the entire model at once, enabling complex validation logic that involves multiple fields. This section covers how to use root validators and implement complex validation scenarios.

## Validating the Entire Model

Root validators are defined using the `@root_validator` decorator. They receive all the fields of the model as a dictionary and can perform validations or modifications on the entire data set.

Basic syntax:

```python
from pydantic import BaseModel, root_validator

class User(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str

    @root_validator
    def check_passwords_match(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')
        if password != confirm_password:
            raise ValueError('Passwords do not match')
        return values
```

In this example, the root validator checks if the password and confirm_password fields match.

## Complex Validation Logic

Root validators are particularly useful for implementing complex validation logic that involves multiple fields or requires external data.

### Example 1: Validating Related Fields

```python
from pydantic import BaseModel, root_validator
from datetime import date

class DateRange(BaseModel):
    start_date: date
    end_date: date
    duration: int

    @root_validator
    def check_dates_and_duration(cls, values):
        start = values.get('start_date')
        end = values.get('end_date')
        duration = values.get('duration')

        if all(v is not None for v in (start, end, duration)):
            calculated_duration = (end - start).days
            if calculated_duration != duration:
                raise ValueError(f'Duration must be {calculated_duration} days')
            if end <= start:
                raise ValueError('End date must be after start date')
        
        return values
```

### Example 2: Conditional Validation

```python
from pydantic import BaseModel, root_validator

class Payment(BaseModel):
    amount: float
    currency: str
    conversion_rate: float = None

    @root_validator
    def check_conversion_rate(cls, values):
        currency = values.get('currency')
        rate = values.get('conversion_rate')

        if currency != 'USD' and rate is None:
            raise ValueError('Conversion rate is required for non-USD currencies')
        if currency == 'USD' and rate is not None:
            raise ValueError('Conversion rate should not be provided for USD')
        
        return values
```

### Example 3: External Data Validation

```python
import httpx
from pydantic import BaseModel, root_validator

class GithubUser(BaseModel):
    username: str
    repository_count: int

    @root_validator
    def validate_github_data(cls, values):
        username = values.get('username')
        if username:
            response = httpx.get(f'https://api.github.com/users/{username}')
            if response.status_code == 200:
                github_data = response.json()
                values['repository_count'] = github_data['public_repos']
            else:
                raise ValueError(f'Unable to fetch GitHub data for {username}')
        return values
```

## Best Practices for Root Validators

1. **Use Pre-validation When Necessary**: If you need to modify input data before individual field validation, use `@root_validator(pre=True)`.

2. **Handle Missing Values**: Remember that some fields might be missing in the `values` dictionary, especially when using `@root_validator(pre=True)`.

3. **Return Modified Values**: Always return the `values` dictionary, even if you don't modify it.

4. **Keep It Focused**: While root validators can do a lot, try to keep each validator focused on a specific task for clarity.

5. **Error Messages**: Provide clear and specific error messages to help users understand validation failures.

6. **Avoid Side Effects**: Root validators should not have side effects outside of the model instance.

7. **Consider Performance**: For validators that perform expensive operations, consider caching or optimizing where possible.

By leveraging root validators, you can implement sophisticated validation logic that ensures the integrity and consistency of your data across multiple fields, making your Pydantic models more robust and reliable.