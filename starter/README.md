# Eblog - A simple blog

elog is a simple blog application built wiht a Flask backend and a Next.js frontend. Users can
create edit, and delete post and reply.

- frontend : next.js, react-bootstrap
- backend : flask, sqlalchemy
-  python v3.10.10

### Project structure
```
├── README.md
├── backend
│   ├── README.md
│   ├── __pycache__
│   ├── config.py
│   ├── eblog
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── auth.py
│   │   ├── models.py
│   │   └── views.py
│   ├── eblog.db
│   ├── migrations
│   │   ├── README
│   │   ├── __pycache__
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   ├── requirements-dev.txt
│   └── test_eblog.py
└── frontend
    ├── eblog
    │   ├── README.md
    │   ├── components
    │   ├── contexts
    │   ├── jsconfig.json
    │   ├── lib
    │   ├── next.config.js
    │   ├── package-lock.json
    │   ├── package.json
    │   ├── pages
    │   ├── public
    │   └── styles
    └── package-lock.json
```

### Backend

> backend directory contains the backend code of the application.

- `config.py` file contains the configuration settings of the Flask application.
- `eblog` directory contains the Flask blueprint module for the application.
- `migrations` directory contains the database migration scripts.
- `requirements-dev.txt` file contains the list of development dependencies.
- `test_eblog`.py file contains the unit tests for the application.

#### Backend Setup

1. virtualenv venv
`virtualenv venv`

2. source venv
`source venv/bin/activate`

3. pip install
`pip install -r requirements-dev.txt`  

4. flask export
`export FLASK_APP=pybo && export FLASK_DEBUG=true`

5. Then, run the Flask development server with `flask run`. The server should start on `http://127.0.0.1:5000`.

### Frontend

```bash
npm install
npm run dev
```
This will start the Next.js development server, and you can view the frontend application in your
browser at `http://localhost:3000`

### API info
forntend(cdn)  
`udacity-eddie.stage.ver.team`  
backend (api server reverse proxy)  
`eddie-api.ver.team/post`  
