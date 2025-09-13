# AssessmentProject

This is a **Django-based Employee Management API** using **MongoEngine** (MongoDB ODM) for database operations. The project provides CRUD functionalities, search, aggregation, JWT authentication, pagination, and schema validation for employees.

---

## 📂 Project Structure

AssessmentProject/
├── assessment/ # Django project configuration
├── employees/ # Django app for managing employees
├── venv/ # Virtual environment
├── db.sqlite3 # Default database (not used, MongoDB is primary)
├── manage.py # Django management script
├── setup_index.py # MongoDB index setup script
├── README.md # Project documentation


---

## ✅ Features

- Add, update, delete, and list employees.
- Filter employees by department.
- Search employees by skills.
- Calculate average salary by department.
- JWT authentication for secure endpoints.
- MongoDB index on `employee_id` for faster lookups.
- Schema validation using MongoDB JSON schema.
- Pagination of employee listing.
  
---

## 📦 Technologies Used

- Python 3.x
- Django 4.x
- Django REST Framework
- MongoEngine (ODM for MongoDB)
- MongoDB
- JWT Authentication (`djangorestframework-simplejwt`)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/amit8585/AssessmentProject.git
cd AssessmentProject

2️⃣ Create and Activate Virtual Environment
python -m venv venv
venv\Scripts\activate    # For Windows
source venv/bin/activate # For Mac/Linux
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run MongoDB Server

Make sure MongoDB is installed and running on localhost:27017.

python setup_index.py



6️⃣ Run the Server

python manage.py runserver
The API will be available at http://127.0.0.1:8000/.

🔐 Authentication

Use JWT tokens to access protected routes.

Get Token
curl -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"your_password\"}"


Access Protected Endpoints

Add the token to your request headers:

curl -X GET http://127.0.0.1:8000/employees/ -H "Authorization: Bearer <your-access-token>"


📖 API Endpoints

GET /employees/ – List employees.

POST /employees/ – Add an employee.

GET /employees/{employee_id}/ – Get employee details.

PUT /employees/{employee_id}/ – Update employee.

DELETE /employees/{employee_id}/ – Delete employee.

GET /employees/search/?skill=<skill> – Search employees by skill.

GET /employees/avg_salary/ – Get average salary by department.

POST /api/token/ – Obtain JWT token.

POST /api/token/refresh/ – Refresh JWT token.

📂 Notes

MongoDB is required for this project. Install MongoDB and ensure it is running before starting the server.

JWT Authentication is used for securing endpoints.

MongoEngine is used instead of Django's default ORM.

You can expand this project by adding more features like file uploads, reporting, and advanced analytics.
