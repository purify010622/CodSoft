# Password Generator System Architecture

This document describes the system architecture and logical flow of the **Password Generator** application.

## 1. Overview
The Password Generator is a command-line interface (CLI) tool designed to create secure, random passwords based on user-defined criteria. It is implemented in Python as a standalone script.

## 2. Code Structure
The application is structured as a collection of modular functions orchestrating the user logic.

### Core Modules
*   **main()**: The entry point that handles the application loop and menu routing.
*   **generate_password()**: Core logic engine that constructs the password string using the `random` and `string` libraries.
*   **User Interface**: `display_menu()` and `get_password_preferences()` handle CLI input/output.
*   **Persistence**: `save_to_file()` handles writing the output to disk.
*   **Utilities**: `pyperclip` integration for clipboard operations.

## 3. Process Flowchart
The following Mermaid diagram illustrates the execution flow of the application:
```mermaid
flowchart TD
    Start([Start Application]) --> Init[Initialize Dependencies]
    Init --> MainMenu{Display Main Menu}
    
    MainMenu -->|Option 1| AutoGen[Auto Generate Mode]
    MainMenu -->|Option 2| CustomGen[Interactive Mode]
    MainMenu -->|Option 3| Exit([Exit Application])
    
    subgraph Auto_Generation_Flow
        AutoGen --> SetDefaults["Set Default Params\n(Length=12, All Chars)"]
        SetDefaults --> GenLoop1[Generate 5 Passwords]
        GenLoop1 --> CallGen1[[generate_password]]
    end
    
    subgraph Custom_Generation_Flow
        CustomGen --> GetPrefs[Get User Preferences]
        GetPrefs --> Validate{Validate Input}
        Validate -- Invalid --> GetPrefs
        Validate -- Valid --> GenLoop2[Generate N Passwords]
        GenLoop2 --> CallGen2[[generate_password]]
    end
    
    subgraph Output_Handling
        CallGen1 & CallGen2 --> Display[Display Passwords]
        Display --> Copy{Copy to Clipboard?}
        Copy -- Yes --> Clipboard[pyperclip.copy]
        Copy -- No --> Save{Save to File?}
        Save -- Yes --> FileIO[save_to_file]
        Save -- No --> FinalMsg
        Clipboard --> Save
    end
    
    FileIO --> FinalMsg[Display Success Message]
    FinalMsg --> End([End Session])

    subgraph Core_Logic
        CallGen2 --> BuildPool[Build Character Pool]
        BuildPool --> CheckPool{Pool Empty?}
        CheckPool -- Yes --> Error[Return Error]
        CheckPool -- No --> Randomize[Random Selection Loop]
        Randomize --> ReturnPwd[Return Password String]
    end
```

## 4. Key Dependencies
*   **Python 3.x**
*   **Standard Libraries**: `random`, `string`, `os`
*   **External Libraries**: `pyperclip` (for clipboard access)