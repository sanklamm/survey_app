# Flask Survey App

This is a survey app written in Flask.

## Overview
This Flask app can be used to conduct surveys with custom questions. A user needs a valid token to participate in the survey and the token gets invalidated after submitting the form.  
Users have roles (participants and admins) which are used to protect some routes (admin stuff).

You can create new questions and generate new tokens all within the app. The admin can even use the backend to view or edit all tables defined in the model.

## Features

### Questions
You can define all questions for the survey via the admin backend. You can define
* the question
* the form element to enter the answer
* up to 20 answers per question
* a category for each question

### Templates
The app has custom templates for
* index
* login
* new questions
* new tokens
* the survey

### User
To acces to a survey it is required to have a token. The token is 6 chars and numbers long and can only be used once.  
There are two kinds of users: The normal user who takes part in the survey and the admin who can create new questions and tokens and has access to the admin backend where also is a CRUD interface to the DB tables.

### Admin Interface
A user with admin roles has access to the admin backend where she can
* create new tokens
* create new questions
* view, edit or delete the database tables

### Generating Forms and Templates
Primary goals of this app were to create the form elements and the resulting template dynamically from questions saved in the DB.  
To achieve this I wrote a function that reads the entire Questions table and builds f-strings representing code for the survey form.  
This f-string gets executed at runtime.

To dynamically produce the template for the survey form I relied on macros.