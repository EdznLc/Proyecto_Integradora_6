# Bonitas Fashions - Clothing Management System

This is a *Sales and Client Management Information System (SGCV)* developed as a Final Project for the Technological University of Durango. The system is designed to replace the manual administration of a small clothing business, offering essential CRUD functions and data reports offline.

## Technologies Used

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| *Language* | Python 3.8+ | Core system logic. |
| *Interface (GUI)* | Tkinter | Development of the User Interface (View Layer). |
| *Database* | MySQL | Local data storage (Model Layer). |
| *Reports* | Pandas & ReportLab | Data export to Excel and PDF formats. |
| *Architecture*| MVC (Model-View-Controller) | Separation of responsibilities. |

## Project Structure

The project adheres to a *Model-View-Controller (MVC)* architecture to ensure clear separation of concerns.

* main.py: Application entry point and initial administrator user check.
* conexionBD.py: Module responsible for establishing the local MySQL connection.
* *controller/*: Contains the business logic (funciones.py) and report handling (reportes.py).
* *model/*: Contains the DAO (Data Access Object) classes that execute SQL queries (CRUD operations).
* *view/*: Contains the graphical interface module (interfaces.py) built with Tkinter.

## Installation and Deployment Guide

Follow these steps to set up and run the application in your local environment (Desktop, Windows/macOS/Linux):

### 1. Environment Requirements
Ensure the following are installed:
* *Python 3.8+*.
* A local *MySQL* server (recommended: *XAMPP*).

### 2. Dependency Installation
Open the terminal in the main project folder (e.g., PF_INTEGRADORA/) and run the following command to install all necessary libraries (Pandas, ReportLab, MySQL Connector):

```bash
pip install -r requirements.txt
3. Database Configuration
Start Server: Open XAMPP and click Start for both Apache and MySQL.

Create DB: Access phpMyAdmin (http://localhost/phpmyadmin/). Create the database with the exact name: bd_ventaropa.

Import Tables: Import the bd_ventaropa.sql script to create the necessary tables (usuarios, clientes, and ventas).

4. System Execution
Once the database is configured, run the application from the terminal:

Bash

python main.py
5. Initial Credentials (Admin)
The system automatically creates an initial administrator user upon the first startup:

Email: admin@sistema.com

Password: admin123

Development Team
This project was developed by Team 06 of the 4th Semester in Multiplatform Software Development:

Bueno Cao Romero Erik Gabriel

Guillen Lopez Jose Alberto

Jimenez Delgado Luis Hector

Lomas Corral Edson

Meraz Sida Fernando
