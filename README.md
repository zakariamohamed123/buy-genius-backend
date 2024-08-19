# Buy Genius Backend

Welcome to the backend service of **Buy Genius**, an e-commerce platform designed to help users compute the marginal benefit and cost-benefit analysis of products from different retailers.

## Table of Contents
- [Overview](#overview)
- [Technologies](#technologies)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Database](#database)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)

## Overview

The **Buy Genius Backend** is a RESTful API built with Python Flask. It manages user authentication, retailer registration, product listings, and search functionality. The backend interacts with a PostgreSQL database and provides data to the React-based frontend.

## Technologies

- **Flask**: Python web framework used to build the API.
- **PostgreSQL**: Database for storing user, retailer, and product data.
- **SQLAlchemy**: ORM for database operations.
- **Flask-Migrate**: Tool for handling database migrations.
- **Render**: Platform for hosting the backend.

## Features

- **User Authentication**: Sign up, login, and session management.
- **Product Management**: Add, update, and delete products.
- **Retailer Management**: Retailer approval/rejection by admins.
- **Wishlist**: Add/remove items to/from wishlist.
- **Message System**: Users can send and receive messages.
- **Search Functionality**: Search products, retailers, and retrieve search history.

## API Endpoints

### Authentication
- **POST** `/signup`: Register a new user.
- **POST** `/login`: Authenticate a user and provide a token.
- **GET** `/check_session`: Check if the current session is valid.
- **DELETE** `/logout`: Log out the user.

### User Management
- **GET** `/users`: Retrieve all users.
- **GET** `/users/{userId}`: Retrieve a specific user's profile.
- **DELETE** `/users/{userId}`: Delete a user.

### Retailer Management
- **GET** `/retailers`: Retrieve all retailers.
- **POST** `/approve_retailer/{retailerId}`: Approve a retailer.
- **POST** `/reject_retailer/{retailerId}`: Reject a retailer.

### Product Management
- **GET** `/products`: Retrieve all products.
- **POST** `/products`: Add a new product.
- **PUT** `/products/{productId}`: Update a product.
- **DELETE** `/products/{productId}`: Delete a product.

### Wishlist
- **GET** `/wishlist`: Retrieve the current user's wishlist.
- **POST** `/wishlist`: Add a product to the wishlist.
- **DELETE** `/wishlist/{wishlistId}`: Remove a product from the wishlist.

### Messaging
- **GET** `/messages`: Retrieve all messages.
- **POST** `/messages`: Send a message.

### Search
- **POST** `/search_history`: Record a search term.
- **GET** `/search_history`: Retrieve the search history.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/buy-genius-backend.git
   cd buy-genius-backend
   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your PostgreSQL database**.

   Ensure PostgreSQL is running and create a database:

   ```bash
   createdb buygenius
   ```

## Environment Variables

Create a `.env` file in the project root and add the following:

```bash
FLASK_ENV=development
DATABASE_URL=postgresql://buygeniususer:securepassword@localhost/buygenius
SECRET_KEY=your_secret_key
```

## Database
Our database is deployed at: [https://buy-genius-backend.onrender.com]

This project uses **Flask-Migrate** for database migrations. After setting up your environment and PostgreSQL, you can run the following commands to create and apply migrations:

1. **Create migration**:

   ```bash
   flask db migrate -m "Initial migration"
   ```

2. **Apply migration**:

   ```bash
   flask db upgrade
   ```

## Running the Application

To run the Flask development server:

```bash
flask run
```

The backend will be available at `http://127.0.0.1:5000`.

## Testing

To run the tests:

```bash
pytest
```

Ensure you have test cases in place and that the backend behaves as expected.

## Deployment

This project is deployed on Render. To deploy:

1. Push your code to the `main` branch.
2. Set up your deployment on Render with the following settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `flask run --host=0.0.0.0`

## Contributing

Feel free to contribute to the **Buy Genius Backend** by following these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push to your branch and submit a pull request.

---
