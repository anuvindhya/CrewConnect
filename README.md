# CrewConnect - HR & Employee Management System

## 📌 Project Overview

**CrewConnect** is a Django-based HR and Employee Management System designed to simplify and manage employee-related activities within an organization.

The system provides separate functionalities for **HR** and **Employees**, allowing HR administrators to manage employees, departments, designations, leave requests, and employee information efficiently.

Employees can manage their profiles, apply for leave, view leave status, access the leave calendar, and manage account settings.

---

## 🚀 Features

### 👨‍💼 HR Features

* HR Dashboard
* Add and manage employees
* Manage employee details
* Create and manage departments
* Create and manage designations
* View employee information
* Manage leave requests
* Approve or reject employee leave
* View leave calendar
* Employee management system

### 👩‍💻 Employee Features

* Employee Dashboard
* View and update profile
* Apply for leave
* View leave history and status
* Access leave calendar
* Update account settings
* Change password
* View personal information

### 🔐 Authentication Features

* User login and logout
* Django Authentication
* Role-based access
* Password management
* Change password functionality
* SMTP-based email integration

---

## 🛠️ Tech Stack

| Technology            | Usage                        |
| --------------------- | ---------------------------- |
| Python                | Backend Programming Language |
| Django                | Web Framework                |
| SQLite                | Database                     |
| HTML                  | Web Page Structure           |
| CSS                   | Styling                      |
| Bootstrap             | Responsive UI Design         |
| JavaScript            | Client-side Interactivity    |
| Django ORM            | Database Operations          |
| Django Authentication | User Authentication          |
| SMTP                  | Email Integration            |
| Git                   | Version Control              |
| GitHub                | Source Code Repository       |

---

## 📂 Project Structure

```text
CrewConnect/
│
├── CrewConnect/          # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── hr/                   # HR application
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── employee/             # Employee application
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── templates/            # Common HTML templates
│
├── static/               # Static files
│   ├── css/
│   ├── js/
│   └── images/
│
├── manage.py
└── db.sqlite3
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
```

### 2. Navigate to the Project Folder

```bash
cd CrewConnect
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux/Mac

```bash
source .venv/bin/activate
```

### 5. Install Django

```bash
pip install django
```

### 6. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Superuser

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

Open the following address in your browser:

```text
http://127.0.0.1:8000/
```

---

## 🗄️ Database

The project currently uses **SQLite**, Django's default database.

Database file:

```text
db.sqlite3
```

Django ORM is used to perform database operations such as:

* Creating employee records
* Updating employee information
* Managing departments
* Managing designations
* Applying for leave
* Approving or rejecting leave requests

---

## 📧 Email Integration

CrewConnect supports email integration using **SMTP**.

SMTP can be used for functionalities such as:

* Password-related emails
* Employee notifications
* Leave notifications
* Account-related communication

---

## 🎯 Project Objectives

The main objective of CrewConnect is to:

* Simplify HR operations
* Manage employee information efficiently
* Provide a structured leave management system
* Improve communication between HR and employees
* Provide role-based access to different users
* Create a centralized employee management platform

---

## 🔮 Future Enhancements

Possible future improvements include:

* Attendance management
* Payroll management
* Employee document uploads
* Advanced reporting
* Email notifications
* Search and filtering
* Employee performance tracking
* REST API integration
* Deployment using cloud platforms

---

## 👩‍💻 Author

**Mandhakapu Anuvindhya**

B.Tech - Artificial Intelligence

### Skills

* Python
* Django
* HTML
* CSS
* JavaScript
* SqLite
* AI & Machine Learning

---

## 📜 License

This project is created for educational and learning purposes.

---

## ⭐ Support

If you like this project, consider giving the repository a **star ⭐ on GitHub**.
