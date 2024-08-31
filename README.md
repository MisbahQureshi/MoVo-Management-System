# MOVO Management System

## Project Overview

The MOVO (Management of Volunteers Online) system is a web-based application designed to streamline the recruitment, management, and tracking of student volunteers for campus events. Built using Flask, a Python web framework, and MongoDB, a flexible NoSQL database, the system's main goal is to help administrators efficiently manage volunteer sign-ups, select participants, assign tasks, and track hours worked. The system prioritizes students with fewer or no volunteer hours, promoting fairness and equal opportunities.

## Modules and Features

### 1. Admin Login and Authentication
- Secure login system to ensure only authorized personnel can access the admin panel.
- Utilizes Flask's authentication system, integrated with MongoDB for storing and verifying admin credentials.

### 2. Volunteer Registration
- Admins can generate custom registration forms within the application or attach an external Google Form.
- Volunteers submit their information, including first name, last name, school email, student ID, and contact number.
- Flask forms and MongoDB are used for managing volunteer data.

### 3. Data Import and Management
- Admins can upload spreadsheets (e.g., from Google Forms) containing volunteer data.
- The system reads and imports this data into the appropriate MongoDB database.
- Utilizes Python libraries like pandas or openpyxl for handling spreadsheet data.

### 4. Volunteer and Event Databases
- **Volunteers Database:** Stores all registered volunteer information, including volunteering history (hours served).
- **Events Database:** Stores details of events, including the list of volunteers who applied, were selected, tasks assigned, and hours served.
- Managed using MongoDB collections.

### 5. Volunteer Selection and Task Assignment
- Admin panel to view volunteers who applied for an event, displaying relevant details such as volunteer history.
- Allows admins to select volunteers based on set criteria and assign specific tasks.
- Flask interface for admin control, MongoDB for querying and updating data.

### 6. Volunteer Hour Tracking and Award Management
- Automatically calculates total hours volunteered by each student across all events.
- Flags students who exceed 20 hours for an award at the end of the semester.
- Admin panel for managing awards, utilizing MongoDB and Flask.

### 7. Minimalistic Frontend Design
- A simple, minimalistic interface featuring only necessary elements such as the school logo, navigation, and essential forms.
- Developed with HTML, CSS, Bootstrap, and Flask rendering templates.

## System Flow

1. Admin Login
2. Form Generation/Attachment
3. Data Import
4. Volunteer Registration
5. Volunteer Selection
6. Task Assignment
7. Hour Tracking
8. Award Management


## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature/bugfix:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add your commit message here"
    ```
4. Push to the branch:
    ```bash
    git push origin feature/your-feature-name
    ```
5. Open a Pull Request on GitHub.


## Contact

For questions or inquiries, please contact misbahqureshie@gmail.com.

---

*This project is a course project.*
