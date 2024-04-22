# Errors Doc

## General Structure
All error responses with status code 4xx, will have a same schema.
The schema will be like:

**This is a sample,
You could read more about real error codes from error_code list section**

**Sample 1:**

    {
        "error_code": "QuotaExceeded",
        "message": "public ip's count that allowed to becreated per namespace is 5 and you used 6",
        "rules": [{
            "description": "public ip's count that allowed to be created per namespace",
            "is_passed": False,
            "quota": 5,
            "used": 6,
        }]
    }

**Sample 2:**

    { 
        "error_code": "FieldError", 
        "message": "some message", 
        "field": "first_name"
    }

**Sample 3:**

    { 
        "error_code": "NotFoundFIP", 
        "message": "some message",
        "custom_field": "some value"
    }

Response will have a `errors` field that contains a list of error objects.
Error objects at least should have `error_code` and `message`.
Other fields will be varied base on `error_code`.
You could read about different `error_code` from error_code list section.

#error_code list

## QuotaExceeded
`QuotaExceeded`  `error_code` means, At least in one of the rules you don't have enough quota .

    {
        "error_code": "QuotaExceeded",
        "message": "You don't have enough quota.",
        "rules": [{
            "description": "public ip's count that allowed to be created per namespace",
            "is_passed": False,
            "quota": 5,
            "used": 6,
        }]
    }


## ValidationError
`ValidationError`  `error_code` means, at least one of the fields user sent didn't validate.

    {
        "error_code": "ValidationError",
        "message": "Invalid input parameters",
        "errors": {
            "name": "'Valid characters are: lowercase letters, digits, dash and underscore'"
        }
    }
