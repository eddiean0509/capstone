# Eblog

## Overview

eblog is a blogging platform built using Next.js and React. It allows users to create posts and reply to them, and includes features such as pagination and error handling. 

## Components

- `components`: Contains various React components used throughout the application, including:
  - `formError.js`: A component that displays form errors to the user.
  - `navbar.js`: A navigation bar component.
  - `pagination.js`: A pagination component used to display a set of results across multiple pages.
  - `postForm.js`: A form used to create and edit posts.
  - `replyForm.js`: A form used to reply to posts.

## Contexts

- `contexts`: Contains the application's context module used to share data between components.

## Pages

- `pages`: Contains the application's main pages and components used to build them, including:
  - `_app.js`: A custom App component used to initialize pages.
  - `_document.js`: A custom Document component used to customize the document rendered on the server.
  - `index.js`: The application's home page.
  - `post.js`: The application's post page.
  - `post/create.js`: The page for creating a new post.
  - `post/modify.js`: The page for modifying an existing post.
  - `reply/modify.js`: The page for modifying an existing reply.

## Styles

- `styles`: Contains CSS modules used to style the application's components and pages.

## Other Files

- `jsconfig.json`: A configuration file for Next.js.
- `lib/models.js`: Contains the models used by the application.
- `next.config.js`: A configuration file for Next.js.
- `package.json`: A file that lists the application's dependencies.
- `public`: Contains public files used by the application.
- `package-lock.json`: A lockfile that ensures the exact version of each dependency is installed.

## Running the Application

To run the application, clone the repository and install its dependencies:

```bash
npm install
npm run dev
```
This will start the Next.js development server, and you can view the frontend application in your
browser at `http://localhost:3000`


```
.
├── eblog
│   ├── README.md
│   ├── components
│   │   ├── formError.js
│   │   ├── navbar.js
│   │   ├── pagination.js
│   │   ├── postForm.js
│   │   └── replyForm.js
│   ├── contexts
│   │   └── context.js
│   ├── jsconfig.json
│   ├── lib
│   │   └── models.js
│   ├── next.config.js
│   ├── package-lock.json
│   ├── package.json
│   ├── pages
│   │   ├── _app.js
│   │   ├── _document.js
│   │   ├── index.js
│   │   ├── post
│   │   │   ├── create.js
│   │   │   └── modify.js
│   │   ├── post.js
│   │   └── reply
│   │       └── modify.js
│   ├── public
│   │   ├── favicon.ico
│   │   ├── images
│   │   │   └── hero-main.jpg
│   │   ├── next.svg
│   │   ├── thirteen.svg
│   │   └── vercel.svg
│   └── styles
│       ├── Home.module.css
│       └── globals.css
└── package-lock.json
```
