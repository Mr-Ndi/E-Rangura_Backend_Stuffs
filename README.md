# Sokoni

Sokoni is a web application designed to facilitate the buying and selling of products in a user-friendly environment. The backend provides essential functionality for user authentication, product management, and data handling.

## Features

- User authentication (login and registration)
- Product management (view, add, edit, delete)
- RESTful API endpoints for seamless interaction with the frontend
- Progress feedback during data fetching and login processes

## Technologies Used

- **Backend**: Django REST Framework
- **Database**: PostgreSQL (or specify any other database you are using)
- **Authentication**: JWT (JSON Web Tokens) for secure user sessions

## Installation

### Prerequisites

- Python (v3.6 or later)
- Django (v3.2 or later)
- PostgreSQL (or your chosen database)

### Clone the Repository

```
git clone https://github.com/Mr-Ndi/E-Rangura.git
cd E-Rangura/backend
```

### Setup Instructions

1. **Create a virtual environment (optional but recommended)**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install required packages**:
   ```
   pip install -r requirements.txt
   ```

3. **Run database migrations**:
   ```
   python manage.py migrate
   ```

4. **Create a superuser (optional)**:
   ```
   python manage.py createsuperuser
   ```

5. **Start the Django development server**:
   ```
   python manage.py runserver
   ```

## API Endpoints

### User Authentication

- **POST /api/users/login/**: Log in a user.
- **POST /api/users/register/**: Register a new user.

### Product Management

- **GET /api/store/products/**: Retrieve all products.
- **POST /api/store/products/**: Add a new product.
- **PUT /api/store/products/<id>/**: Update an existing product.
- **DELETE /api/store/products/<id>/**: Delete a product.

## Usage

1. Use tools like Postman or cURL to interact with the API endpoints.
2. Ensure that your database is running and accessible.
3. Test the endpoints for user authentication and product management.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgments

Thanks to all contributors and libraries used in this project.


### Notes:

- Replace `https://github.com/Mr-Ndi/E-Rangura.git` with your actual repository URL.
- Adjust any sections as necessary to better fit your project's specifics, especially if you have additional features or configurations.

Feel free to copy this text directly into your `README.md` file for the backend! If you need further modifications or additional sections, just let me know!