# Online Learning Management System (LMS)
  An Online Learning Management System (LMS) built with Django, Django REST Framework, PostgreSQL, Redis, JWT authentication, and Docker.
  This project demonstrates how to build a real-world, scalable backend system suitable for beginner to intermediate Django developers.


## Features

### User Roles
  Admin
     Manage users, courses, and categories
     Assign instructors
     Full platform control

  Instructor
   Create courses and lessons
   Upload videos and study materials
   Create assignments
   View student progress and submissions

 Student
   Enroll in courses
   Watch lesson videos
   Download materials
   Submit assignments
   Track learning progress


## Tech Stack

   Backend: Django, Django REST Framework
   Authentication: JWT
   Database: PostgreSQL
   Caching & Sessions: Redis
   API Documentation: Swagger (drf-spectacular / drf-yasg)
   Containerization: Docker & Docker Compose


##  Core Concepts Implemented

   Custom User Model
   Role-based access control (Admin, Instructor, Student)
   Django Groups & Permissions
   ModelViewSet-based APIs
   File uploads (videos, PDFs, assignments)
   Assignment submission & validation
   Student lesson progress tracking
   Redis caching & session storage
   JWT authentication & authorization
   Dockerized development environment

## Project Structure

  lms/
  ├── users/ # Custom user model & auth
  ├── courses/ # Categories, courses, lessons, assignments
  ├── enrollments/ # Student enrollments
  ├── core/ # Project settings
  ├── docker-compose.yml
  ├── Dockerfile
  ├── requirements.txt
  ├── .env
  └── README.md


## Authentication

   JWT-based authentication using Simple JWT
   Access & Refresh tokens
   Role-based permissions enforced at API level


## Redis Usage

  Redis is used for:
   Django sessions
   Caching frequently accessed GET endpoints
  
   Redis is selectively used, not applied automatically to every request.

## Docker Setup

### Prerequisites
   Docker
   Docker Compose

### Run the project
  docker-compose build
  docker-compose up -d

### Acess the API at
  http://127.0.0.1:8000
