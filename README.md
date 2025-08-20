# T&P Management System — Django Web Application

A Training & Placement portal built using Django to manage placement drives, contact messages, students, and staff (TPO & coordinators), with role-based dashboards and session-based student drive registration.

---

##  Features Implemented

### Admin Features
- Admin login using Django's built-in staff authentication.
- Dashboard showing:
  - Contact messages
  - Buttons to manage placement drives
  - View registered students
- Delete contact messages
- Add/Edit/Delete placement drives
- Admin can register new students via Django admin (backend only)

### Staff Features
- Staff members stored in `StaffProfile` with name, mobile, role, and linked Django user.
- Admin can create staff logins from admin panel and assign roles like:
  - Training & Placement Officer
  - Alumni Relations Officer
  - Department Coordinator, etc.
- Dashboard now shows logged-in staff's role and name.
- *(Future upgrade: show features based on that role)*

### Student Features
- Students stored in a custom `Student` model (name, roll number, email, phone, branch, graduation year, resume upload optional)
- Student portal:
  - View available placement drives
  - Register for drive (only once per drive)
- Registration stored in `Registration` model
- Session-based student access (`request.session['student_email']`)

### Contact Us Page
- Saves entries to database (ContactMessage model)
- Admin can view & delete messages from dashboard

### Static T&P Team Page
- Public page showing TPO Team members list (name, role, mobile, email)

---


---

##  Tech Stack

- **Language:** Python 3.12
- **Framework:** Django 5.2.4
- **Database:** SQLite (default)
- HTML, CSS (Orange + White theme)
- Templates using Django templating engine

---

## ⚙ Setup Instructions

1. **Clone repository**
   ```sh
   git clone <your-repo-url>
   cd TandP-Management-System   # or your folder name
````

2. **Create virtual env**

   ```sh
   python -m venv venv
   source venv/bin/activate   # (Use venv\Scripts\activate on Windows)
   ```

3. **Install packages**

   ```sh
   pip install -r requirements.txt
   ```

4. **Run migrations**

   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (admin)**

   ```sh
   python manage.py createsuperuser
   ```

6. **Run**

   ```sh
   python manage.py runserver
   ```

---

## ✅ Default Admin Access Routes

* `/admin/` — Django default admin panel
* `/admin_login/` — Custom Admin login page
* `/admin_dashboard/` — Secure dashboard (staff only)

---

##  Future Enhancements (Planned)

* Student login / registration (with model-based auth)
* Resume upload & display to admin
* Role-based dashboard per staff profile
* Email notifications on drive creation or contact submission
* Search/filter students & drives in admin dashboard
* Export to CSV

---

## Contributors

* Sri Vaishnavi (Developer)


---

*Last updated: August 2025*

