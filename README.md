<<<<<<< HEAD
# Training & Placement Management System — Django Web Application

A **comprehensive Training & Placement Portal** built with Django that simplifies and automates the workflow of training and placement activities in an institute.
The system provides **role-based dashboards** for all users (Admin, TPO, Staff, and Students) with a secure authentication system to manage placement drives, training materials, and student registrations.

---

## Features Implemented

### 1. Student Portal

- **Full Authentication System:**
  Students log in using their roll number and password (Django’s built-in `User` model).

- **Student Dashboard:**
  Displays personal details like `Full Name`, `Roll Number`, and `Branch`.

- **Drive Registration:**
  - View all available placement drives.
  - View drives already registered for.
  - Register for a drive (duplicate registration prevented through backend validation).

- **View Materials:**
  Access all uploaded **Verbal**, **Aptitude**, and **Technical** training materials.

- **Resume Management:**
  Upload and view personal resumes securely.

---

### 2. Staff & Admin Portal

- **Full Authentication System:**
  Each staff member (TPO, trainers, coordinators, etc.) logs in using a `User` account linked to a `StaffProfile`.

- **Role-Based Dashboards:**
  Each role sees a dynamic dashboard with tools specific to their responsibilities:

  | Role | Features |
  |------|-----------|
  | **TPO / Associate TPO / Head Corporate** | Add, edit, and delete placement drives. View all registered students. |
  | **Verbal Trainer** | Upload and delete Verbal Materials. |
  | **Aptitude Trainer** | Upload and delete Aptitude Tests. |
  | **Technical / Global Trainer** | Upload and delete Technical Materials. |
  | **Department Coordinator** | View, add, edit, and delete students for their department only. |

- **Admin Dashboard** (`/site-admin/dashboard/`):
  - Access for site superusers only.
  - Manage all **Contact Us** messages.
  - Add, edit, and delete staff profiles and assign roles.
  - Promote staff members to admin level.

---

### 3. General Features

- **Contact Us Page:**
  Public form for inquiries, saved to `ContactMessage` model for admin review.

- **T&P Team Page:**
  Static page listing all Training & Placement Cell core team members.

- **Media & File Handling:**
  Handles uploads for student resumes and training materials securely.

---

## Tech Stack

| Component | Technology |
|------------|-------------|
| **Language** | Python 3.12 |
| **Framework** | Django 5.2.4 |
| **Database** | SQLite (development), PostgreSQL (recommended for production) |
| **Frontend** | HTML, CSS (Orange + White theme) |
| **Core Logic** | Django Templating Engine, Django ORM, `django.contrib.auth` |

---

## Setup Instructions

1.  **Clone Repository**
    ```bash
    git clone <your-repo-url>
    cd tandp_ms
    ```
2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate      # On Linux/Mac
    venv\Scripts\activate         # On Windows
    ```
3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5.  **Create Superuser**
    ```bash
    python manage.py createsuperuser
    ```
6.  **Configure Admin Access**
    * Log in to `/admin/` after running the server.
    * Navigate to Staff Profiles and create a profile for your superuser.
    * Assign the role `tpo` or `admin` to enable full access.
7.  **Run Server**
    ```bash
    python manage.py runserver
    ```

### Access Routes

| Route | Description |
|---|---|
| `/` | Home Page |
| `/student/login/` | Student Login |
| `/staff/login/` | Staff Login (for all staff roles) |
| `/site-admin/login/` | Custom Admin Login (for superuser) |
| `/site-admin/dashboard/` | Custom Admin Dashboard |
| `/admin/` | Default Django Admin Panel |

---

## Future Enhancements (Planned)

-   Email notifications for:
    -   New placement drives
    -   Contact form submissions
-   Search & filter options for students and drives.
-   Export registered student lists to CSV/Excel.

---

## Contributor

-   **Developer:** Sri Vaishnavi Bhaskara
-   **Email:** srivaishnavi.bhaskara@gmail.com
-   **GitHub:** srivaishnavi26

*Last updated: October 2025*
