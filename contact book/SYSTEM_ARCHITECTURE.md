# Contact Book System Architecture

This document details the architecture of the **SmartConnect Contact Management System**, a desktop GUI application.

## 1. Overview
SmartConnect is a modern desktop application for managing contacts. It features a responsive graphical user interface built with `CustomTkinter`, uses `SQLite` for local data persistence, and includes secure User Authentication (Login/Signup).

## 2. Technical Stack
*   **Framework**: CustomTkinter (Modern wrapper around Python's Tkinter)
*   **Database**: SQLite3 (Local file persistence: `contacts.db`)
*   **Security**: `bcrypt` (Password hashing)
*   **Language**: Python 3.x

## 3. Architecture Components

### Frontend (UI Layer)
*   **MainWindow**: The primary container hosting navigation tabs.
*   **LoginWindow**: Dedicated UI for authentication.
*   **Forms**: Input fields for contact details (Name, Phone, Email, Address).
*   **ContactList**: Scrollable frame rendering contact cards.

### Backend (Logic Layer)
*   **AuthSystem**: Manages user sessions, hashing, and access control.
*   **DatabaseManager**: Abstraction layer for SQL queries (CRUD operations).

## 4. System Logic & Data Flow

```mermaid
classDiagram
    class Application {
        +run()
        +show_login()
        +show_dashboard()
    }
    class AuthSystem {
        +login(email, pass)
        +signup(email, pass)
        +hash_password()
    }
    class Database {
        +connect()
        +add_contact()
        +get_contacts()
        +delete_contact()
    }
    
    Application --> AuthSystem : Authenticates via
    Application --> Database : Reads/Writes Data
    AuthSystem --> Database : Verifies Credentials

    note for Database "Stores data in contacts.db\n(Encrypted passwords)"
```

```mermaid
flowchart TD
    Start([Launch App]) --> DBInit[Initialize SQLite DB]
    DBInit --> CheckSession{Valid Session?}
    
    CheckSession -- No --> LoginUI[Show Login Screen]
    LoginUI --> UserInput[User Enters Creds]
    UserInput --> AuthCheck{Verify Creds}
    AuthCheck -- Invalid --> Error[Show Error] --> LoginUI
    AuthCheck -- Valid --> Dashboard
    
    CheckSession -- Yes --> Dashboard[Load Dashboard]
    
    subgraph Dashboard_Operations
        Dashboard --> List[View All Contacts]
        Dashboard --> Add[Add New Contact]
        Dashboard --> Search[Search Contacts]
        
        Add --> Validate{Validate Input}
        Validate -- OK --> SQLInsert[(Insert into SQLite)]
        SQLInsert --> Refresh[Refresh UI]
    end
```