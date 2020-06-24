# Volunteer FUN!

## Introduction

Ever feel like helping the community by volunteering?
But have you found it hard to find the right project to volunteer for? 
Or did you find a project easily, but didn't really enjoy volunteering for them?

Don't worry, Volunteer FUN has you covered!

Volunteer FUN is an app to link volunteers to volunteer projects of their liking!
With Volunteer FUN, you can easily "volunteer" and have "FUN"!

## Motivation for project

A lot of people want to volunteer for some volunteer project.
They want to do this to help the community and also have fun along the way.

Most of the time, "helping the community" and "fun" don't go hand-in-in.
Majority of the people only fulfil one of these.

Volunteer FUN aims to match people with a volunteer project that best suits them.
That way, they can "help the community" and more importantly, have "FUN" at the same time!

## Installing Project Dependencies

Navigate to the project directory. It's recommended to create a python virtual environment to download your dependencies.
Instructions on setting up your python virtual environment and running it can be found [on this link](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

Once in your python virtual environment, run the below command in your command line.

```bash
pip install -r requirements.txt
``` 

## Starting the Project Server

### Backend

First, create a postgres database named (eg. _**"capstone_db"**_).
Then change the ```SQLALCHEMY_DATABASE_URI``` variable in ```starter/config.py``` to reflect your database's URI.

eg. (in ```starter/config.py```)
```python
SQLALCHEMY_DATABASE_URI = 'postgres://{}:{}@{}/{}'.format(
    '<Username>', '<Password>', 'localhost:5432', 'capstone_db')
```

Now to start the backend Flask server, navigate to the _**project**_ directory (not **_starter_** directory).
Next, run the below command in your command line.
Be sure you're in your python virtual environment before doing this.

```bash
export FLASK_APP=starter/app.py
flask run
```

### Testing

First, create a postgres database named (eg. _**"capstone_db_test"**_).
Then change the ```SQLALCHEMY_DATABASE_URI``` variable in ```starter/test_app.py``` to reflect your test database's URI.

eg. (in ```starter/test_app.py```)
```python
SQLALCHEMY_DATABASE_URI = 'postgres://{}:{}@{}/{}'.format(
            '<Username>', '<Password>', 'localhost:5432', 'capstone_db_test')
```

Now to execute the python unittest file, navigate to the _**project**_ directory (not **_starter_** directory).
Next, run the below command in your command line.
Be sure you're in your python virtual environment before doing this.

```bash
python -m starter.test_app
```

## RBAC controls

### Database Models(Tables)

1. _Project_ (_projects_): Table of the volunteer projects.
2. _Volunteer_ (_volunteers_): Table of the volunteers. 

### 1. Volunteer Coordinator

A volunteer coordinator's job is to manage the table of volunteers. Hence, they will be able to make ```GET, POST, PATCH, and DELETE``` requests on the volunteers table.

Their other job is to match volunteers with volunteer projects that best suit them.
Hence, they will also be able to make ```GET``` requests on the volunteer projects table.

### 2. Volunteer Manager

A volunteer manager's job is to overlook the whole process.
This includes managing all the volunteers and the volunteer projects.

Hence, they will be able to make all the requests a volunteer coordinator can make.
Apart from this, they will also be able to make ```POST, PATCH, and DELETE``` requests on the volunteer projects table.

### Summary

1. Volunteer Coordinator:
    + GET, POST, PATCH, DELETE volunteers
    + GET volunteer projects
    
2. Volunteer Manager:
    + GET, POST, PATCH, DELETE volunteers
    + GET, POST, PATCH, DELETE volunteer projects
    
### Generating JWTs

For testing purposes, you can use the below accounts to generate JWTs
    
1. Volunteer Coordinator
    + Username: coordinator@domain.com
    + Password: password1@
    
2. Volunteer Manager
    + Username: manager@domain.com
    + Password: password1@
    
## API Endpoints

### 1. GET /projects

Get a list of _**volunteer projects**_. The results are paginated in groups of 10 results per page.
The page is passed as a query parameter in the request url.

Returns **401** or **403** if any authentication issue arises.

##### Sample requests and responses:

###### 1. Success (200)

```bash
curl --location --request GET 'http://localhost:5000/projects' \
--header 'Authorization: Bearer <JWT>'
```

```json
{
  "count_projects": 1,
  "projects": [
    {
      "description": "Help fill up \"get well soon\" balloons, setup flowers in beautiful arrangements, and assist in helping the patients fell optimistic about their health.",
      "email": "abc@def.com",
      "id": 2,
      "name": "Hospital patients happiness program",
      "phone": "(123) 456-7890"
    }
  ],
  "success": true
}
```

###### 2. Success (200) with page 2

```bash
curl --location --request GET 'http://localhost:5000/projects?page=2' \
--header 'Authorization: Bearer <JWT>'
```

```json
{
  "count_projects": 1,
  "projects": [],
  "success": true
}
```

###### 3. 401 as no JWT passed

```bash
curl --location --request GET 'http://localhost:5000/projects'
```

```json
{
  "code": "invalid_claims",
  "message": "No authorization passed",
  "status_code": 401,
  "success": false
}
```

### 2. GET /volunteers

Get a list of _**volunteers**_. The results are paginated in groups of 10 results per page.
The page is passed as a query parameter in the request url.

Returns **401** or **403** if any authentication issue arises.

###### Sample requests and responses:

###### 1. Success (200)

```bash
curl --location --request GET 'http://localhost:5000/volunteers' \
--header 'Authorization: Bearer <JWT>'
```

```json
{
  "count_volunteers": 2,
  "success": true,
  "volunteers": [
    {
      "email": "abc@def.com",
      "id": 3,
      "name": "Ricky",
      "phone": "(123) 456-7890"
    },
    {
      "email": "abc@def.com",
      "id": 4,
      "name": "Ricky",
      "phone": "(123) 456-7890"
    }
  ]
}
```

###### 2. Success (200) with page 2

```bash
curl --location --request GET 'http://localhost:5000/volunteers?page=2' \
--header 'Authorization: Bearer <JWT>'
```

```json
{
  "count_volunteers": 2,
  "success": true,
  "volunteers": []
}
```

###### 3. 401 as no JWT passed

```bash
curl --location --request GET 'http://localhost:5000/volunteers'
```

```json
{
  "code": "invalid_claims",
  "message": "No authorization passed",
  "status_code": 401,
  "success": false
}
```

### 3. POST /projects

Add a _**volunteer project**_ to the projects table. 
The response includes the newly inserted project.

Returns **400** if incomplete or no project object is passed in the body.

Returns **401** or **403** if any authentication issue arises.

###### Sample requests and responses:

###### 1. Success (200)

```bash
curl --location --request POST 'http://localhost:5000/projects' \
--header '<JWT>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Hospital patients happiness program",
    "description": "Help fill up \"get well soon\" balloons, setup flowers in beautiful arrangements, and assist in helping the patients fell optimistic about their health.",
    "email": "abc@def.com",
    "phone": "(123) 456-7890"
}'
```

```json
{
  "project": {
    "description": "Help fill up \"get well soon\" balloons, setup flowers in beautiful arrangements, and assist in helping the patients fell optimistic about their health.",
    "email": "abc@def.com",
    "id": 3,
    "name": "Hospital patients happiness program",
    "phone": "(123) 456-7890"
  },
  "success": true
}
```

###### 2. 400 as empty/incomplete body

```bash
curl --location --request POST 'http://localhost:5000/projects' \
--header 'Authorization: Bearer <JWT>' \
--data-raw ''
```

```json
{
  "message": "Bad request",
  "status_code": 400,
  "success": false
}
```

###### 3. 401 as no JWT passed

```bash
curl --location --request POST 'http://localhost:5000/projects' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Hospital patients happiness program",
    "description": "Help fill up \"get well soon\" balloons, setup flowers in beautiful arrangements, and assist in helping the patients fell optimistic about their health.",
    "email": "abc@def.com",
    "phone": "(123) 456-7890"
}'
```

```json
{
  "code": "invalid_claims",
  "message": "No authorization passed",
  "status_code": 401,
  "success": false
}
```

###### 4. 403 as JWT doesn't include the required permission

```bash
curl --location --request POST 'http://localhost:5000/projects' \
--header 'Authorization: Bearer <JWT without the required permission>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Hospital patients happiness program",
    "description": "Help fill up \"get well soon\" balloons, setup flowers in beautiful arrangements, and assist in helping the patients fell optimistic about their health.",
    "email": "abc@def.com",
    "phone": "(123) 456-7890"
}'
```

```json
{
  "code": "unauthorized",
  "message": "Permission not found",
  "status_code": 403,
  "success": false
}
```

### 4. POST /volunteers

Add a _**volunteer**_ to the volunteers table. 
The response includes the newly inserted volunteer.

Returns **400** if incomplete or no volunteer object is passed in the body.

Returns **401** or **403** if any authentication issue arises.

###### Sample requests and responses:

###### 1. Success (200)

```bash
curl --location --request POST 'http://localhost:5000/volunteers' \
--header 'Authorization: Bearer <JWT>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Ricky",
    "email": "abc@def.com",
    "phone": "(123) 456-7890"
}'
```

```json
{
  "success": true,
  "volunteer": {
    "email": "abc@def.com",
    "id": 5,
    "name": "Ricky",
    "phone": "(123) 456-7890"
  }
}
```

###### 2. 400 as empty/incomplete body

```bash
curl --location --request POST 'http://localhost:5000/volunteers' \
--header 'Authorization: Bearer <JWT>' \
--data-raw ''
```

```json
{
  "message": "Bad request",
  "status_code": 400,
  "success": false
}
```

###### 3. 401 as no JWT passed

```bash
curl --location --request POST 'http://localhost:5000/volunteers' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Ricky",
    "email": "abc@def.com",
    "phone": "(123) 456-7890"
}'
```

```json
{
  "code": "invalid_claims",
  "message": "No authorization passed",
  "status_code": 401,
  "success": false
}
```

### 5. PATCH /projects/\<int:project_id>

Edit a _**volunteer project**_ from the projects table. 
The response includes the edited project.

Returns **400** if no volunteer project field is passed in the body.

Returns **404** if no project exists with the id passed in the path.

Returns **401** or **403** if any authentication issue arises.

###### Sample requests and responses:

###### 1. Success (200)

```bash
curl --location --request PATCH 'http://localhost:5000/projects/3' \
--header 'Authorization: Bearer <JWT>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "edit@def.com",
    "phone": "(098) 765-4321"
}'
```

```json
{
  "project": {
    "description": "Help fill up \"get well soon\" balloons, setup flowers in beautiful arrangements, and assist in helping the patients fell optimistic about their health.",
    "email": "edit@def.com",
    "id": 3,
    "name": "Hospital patients happiness program",
    "phone": "(098) 765-4321"
  },
  "success": true
}
```

###### 2. 400 as empty body

```bash
curl --location --request PATCH 'http://localhost:5000/projects/3' \
--header 'Authorization: Bearer <JWT>' \
--data-raw ''
```

```json
{
  "message": "Bad request",
  "status_code": 400,
  "success": false
}
```

###### 3. 404 as project with the passed id doesn't exist

```bash
curl --location --request PATCH 'http://localhost:5000/projects/1000000' \
--header 'Authorization: Bearer <JWT>' \
--data-raw ''
```

```json
{
  "message": "Not found",
  "status_code": 404,
  "success": false
}
```

###### 4. 401 as no JWT passed

```bash
curl --location --request PATCH 'http://localhost:5000/projects/3' \
--data-raw ''
```

```json
{
  "code": "invalid_claims",
  "message": "No authorization passed",
  "status_code": 401,
  "success": false
}
```

###### 5. 403 as JWT doesn't include the required permission

```bash
curl --location --request PATCH 'http://localhost:5000/projects/2' \
--header 'Authorization: <JWT without the required permission>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "edit@def.com",
    "phone": "(098) 765-4321"
}'
```

```json
{
  "code": "unauthorized",
  "message": "Permission not found",
  "status_code": 403,
  "success": false
}
```

### 6. PATCH /volunteers/\<int:volunteer_id>

Edit a _**volunteer**_ from the volunteers table. 
The response includes the edited volunteer.

Returns **400** if no volunteer field is passed in the body.

Returns **404** if no volunteer exists with the id passed in the path.

Returns **401** or **403** if any authentication issue arises.

###### Sample requests and responses:

###### 1. Success (200)

```bash
curl --location --request PATCH 'http://localhost:5000/volunteers/3' \
--header 'Authorization: Bearer <JWT>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "edit@def.com",
    "phone": "(098) 765-4321"
}'
```

```json
{
  "success": true,
  "volunteer": {
    "email": "edit@def.com",
    "id": 3,
    "name": "Ricky",
    "phone": "(098) 765-4321"
  }
}
```

###### 2. 400 as empty body

```bash
curl --location --request PATCH 'http://localhost:5000/volunteers/3' \
--header 'Authorization: Bearer <JWT>' \
--data-raw ''
```

```json
{
  "message": "Bad request",
  "status_code": 400,
  "success": false
}
```

###### 3. 404 as volunteer with the passed id doesn't exist

```bash
curl --location --request PATCH 'http://localhost:5000/volunteers/1000000' \
--header 'Authorization: Bearer <JWT>' \
--data-raw ''
```

```json
{
  "message": "Not found",
  "status_code": 404,
  "success": false
}
```

###### 4. 401 as no JWT passed

```bash
curl --location --request PATCH 'http://localhost:5000/volunteers/1000000' \
--data-raw ''
```

```json
{
  "code": "invalid_claims",
  "message": "No authorization passed",
  "status_code": 401,
  "success": false
}
```

### 7. DELETE /projects/\<int:project_id>

Delete a _**volunteer project**_ from the projects table. 
The response includes the deleted project.

Returns **404** if no project exists with the id passed in the path.

Returns **401** or **403** if any authentication issue arises.

###### Sample requests and responses:

###### 1. Success (200)

```bash
curl --location --request DELETE 'http://localhost:5000/projects/3' \
--header 'Authorization: Bearer <JWT>' \
--data-raw ''
```

```json
{
  "project": {
    "description": "Help fill up \"get well soon\" balloons, setup flowers in beautiful arrangements, and assist in helping the patients fell optimistic about their health.",
    "email": "edit@def.com",
    "id": 3,
    "name": "Hospital patients happiness program",
    "phone": "(098) 765-4321"
  },
  "success": true
}
```

###### 2. 404 as project with the passed id doesn't exist

```bash
curl --location --request DELETE 'http://localhost:5000/projects/1000000' \
--header 'Authorization: Bearer <JWT>' \
--data-raw ''
```

```json
{
  "message": "Not found",
  "status_code": 404,
  "success": false
}
```

###### 3. 401 as no JWT passed

```bash
curl --location --request DELETE 'http://localhost:5000/projects/1000000' \
--data-raw ''
```

```json
{
  "code": "invalid_claims",
  "message": "No authorization passed",
  "status_code": 401,
  "success": false
}
```

###### 4. 403 as JWT doesn't include the required permission

```bash
curl --location --request DELETE 'http://localhost:5000/projects/2' \
--header 'Authorization: Bearer <JWT without the required permission>' \
--data-raw ''
```

```json
{
  "code": "unauthorized",
  "message": "Permission not found",
  "status_code": 403,
  "success": false
}
```

### 8. DELETE /volunteers/\<int:volunteer_id>

Delete a _**volunteer**_ from the volunteers table. 
The response includes the deleted volunteer.

Returns **404** if no volunteer exists with the id passed in the path.

Returns **401** or **403** if any authentication issue arises.

###### Sample requests and responses:

###### 1. Success (200)

```bash
curl --location --request DELETE 'http://localhost:5000/volunteers/4' \
--header 'Authorization: Bearer <JWT>' \
--data-raw ''
```

```json
{
  "success": true,
  "volunteer": {
    "email": "abc@def.com",
    "id": 4,
    "name": "Ricky",
    "phone": "(123) 456-7890"
  }
}
```

###### 2. 404 as project with the passed id doesn't exist

```bash
curl --location --request DELETE 'http://localhost:5000/volunteers/1000000' \
--header 'Authorization: Bearer <JWT>' \
--data-raw ''
```

```json
{
  "message": "Not found",
  "status_code": 404,
  "success": false
}
```

###### 3. 401 as no JWT passed

```bash
curl --location --request DELETE 'http://localhost:5000/volunteers/1000000' \
--data-raw ''
```

```json
{
  "code": "invalid_claims",
  "message": "No authorization passed",
  "status_code": 401,
  "success": false
}
```
