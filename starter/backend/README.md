# Eblog

elog is a simple blog application built wiht a Flask backend and a Next.js frontend. Users can
create edit, and delete post and reply.


## Project Structure

```
├── README.md
├── config.py
├─ migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── eblog
│   ├── __init__.py
│   ├── auth.py
│   ├── models.py
│   └── views.py
├── eblog.db
├── test_eblog.py
└── requirements-dev.txt
```

### Backend Setup

1. virtualenv venv
`virtualenv venv`

2. source venv
`source venv/bin/activate`

3. pip install
`pip install -r requirements-dev.txt`  

4. flask export
`export FLASK_APP=pybo && export FLASK_DEBUG=true`

5. Then, run the Flask development server with `flask run`. The server should start on `http://127.0.0.1:5000`.


## Authentication

This API uses JWT-based authentication. To access any of the endpoints that require authentication, you need to include an `Authorization` header in your request with a valid JWT token.


## Auth0 User permissions

#### blog : all permissions

> ID: blog@ver.team / PW: !verteam1

`get:post` - Get the list and detail of posts on the board.
`post:post` - Write the post.
`put:post` - Edit existed posts.
`delete:post` - Delete existed posts.
`get:reply` - Get registered replys to posts.
`post:reply` - Write replys to existed posts.
`put:reply` - Edit existed replys.
`delete:reply` - Delete existed replys.
`vote:post` - Vote existed posts.
`vote:reply` - Vote existed replys.

#### neighbor : All permissions to the reply and get:post, vote:post

> ID: neighbor@ver.team / PW: !verteam1

`get:reply` - Get the list and detail of replys on the board.
`post:reply` - Write the reply.
`put:reply` - Edit existed replys.
`delete:reply` - Delete existed replys.
`vote:reply` - Vote existed replys.
`get:post` - Get registered replys to posts.
`vote:post` - Vote existed replys.
`vote:reply` - Vote existed replys.


## API endpoints

### Posts

- `GET /post/`: Get a list of posts
- `GET /post/<int:post_id>`: Get a specific post by ID
- `POST /post/`: Create a new post
- `PUT /post/<int:post_id>`: Modify an existing post by ID
- `DELETE /post/<int:post_id>`: Delete a specific post by ID
- `POST /post/<int:post_id>/vote`: Vote on a specific post by ID

#### GET '/post'

Returns a list of posts with pagination.
Query Parameters:
- `page`(optional): for pagenation
- `kw`(optional): for pagenation

#### Response
Body: JSON object with the following keys:  

- posts: An array of objects, each representing a post and its associated post. Each object contains the following keys:  
  - id: Unique identifier of the post.  
  - subject: Title of the post.  
  - content: Content of the post.  
  - create_date: Date and time when the post was created.  
  - user_id: Unique identifier of the user who created the post.  
  - username: Username of the user who created the post.  
  - replys: An array of objects, each representing an reply to the post. Each object contains the following keys:  
    - id: Unique identifier of the reply.  
    - post_id: Unique identifier of the post to which the reply belongs.  
    - content: Content of the reply.  
    - create_date: Date and time when the reply was created.  
    - user_id: Unique identifier of the user who created the reply.  
    - username: Username of the user who created the reply.  
- total: Total number of posts found.  
- page: Current page number.  
- per_page: Number of posts per page.  
- has_prev: Boolean indicating whether there is a previous page.  
- prev_num: Page number of the previous page.  
- page_nums: An array of page numbers for pagination navigation.  
- has_next: Boolean indicating whether there is a next page.  
- next_num: Page number of the next page.  
- kw: Keyword used for searching.  

Sample curl request:  
`curl -X GET http://127.0.0.1:5000/post`

#### Get '/post/<int:post_id>'
- Get detail of the post(id)  
- Returns: a JSON object with post inofermation.  

#### POST '/post'
- Create the post on the board  
- Request arguments: a JSON formatted oject with optional keys 'subject','content','user(username,email)'.
- Returns: a JSON object with success status true when new post was successfully added into the database.  

#### DELETE '/post/<int:post_id>'
- Delte existed post  
- Returns: a JSON object with success status true when the post was successfully deleted from the database.  

### Replys

- `GET /post/<int:post_id>/reply/<int:reply_id>`: Get a specific reply by ID
- `PUT /post/<int:post_id>/reply/<int:reply_id>`: Modify an existing reply by ID
- `POST /post/<int:post_id>/reply`: Create a new reply for a specific post
- `DELETE /post/<int:post_id>/reply/<int:reply_id>`: Delete a specific reply by ID
- `POST /post/<int:post_id>/reply/<int:reply_id>/vote`: Vote on a specific reply by ID

#### GET '/post/<int:post_id>/reply/<int:reply_id>'
- This endpoint returns the reply information corresponding to the given `post_id` and `reply_id`. If there is no reply that matches the given IDs, it returns a 404 error.  
- Returns: a JSON object with reply inofermation.  

#### POST '/post/<int:post_id>/reply'
- This endpoint allows users to create an reply for a given post.
- Request arguments: a JSON formatted object with optional keys 'content'
- Returns: a JSON object with success status true when the reply information was successfully added into the database.  

#### PUT '/post/<int:post_id>/reply/<int:reply_id>'
- Modify an existing reply to a post.
- Request arguments: a JSON formatted object with optional keys 'content'
- Returns: a JSON object with success status true when the reply information was successfully updated into the database.  

#### DELETE '/post/<int:post_id>/reply/<int:reply_id>'
- Delete an existing reply to a post.
- Request arguments: a JSON formatted object with optional keys 'content'
- Returns: a JSON object with success status true when the reply information was successfully deleted into the database.  


## Error Handling

The eBlog API has custom error handling for various error types, including:

- Bad Request (400)
- Not Found (404)
- Unprocessable (422)
- Authentication Error (AuthError)
- Required Error (RequiredError)

Error responses will include a JSON object with the error details.


## Testing

The testing of all endpoints was implemented with unittest. The command line interface run the test file:  
`python test_eblog.py`
