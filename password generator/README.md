# Password Generator

**CODSOFT Python Programming Internship - Task 3**

A Python-based interactive password generator that creates strong, cryptographically random passwords with two convenient modes: Auto Generate for quick password creation and Interactive Mode for full customization.

## Features

- **Two Generation Modes**:
  - **Auto Generate (Quick)**: Instantly generates 5 passwords with default settings (12 characters, all character types)
  - **Interactive Mode (Custom)**: Full customization with user-defined preferences
- **Password Length**: 4-16 characters (customizable in Interactive Mode)
- **Multiple Passwords**: Generate at least 5 passwords at once
- **Character Type Selection**: Choose from:
  - Uppercase letters (A-Z)
  - Lowercase letters (a-z)
  - Numbers (0-9)
  - Special characters (!@#$%^&*, etc.)
- **Interactive Clipboard Copy**: Choose whether to copy passwords to clipboard
- **Optional File Saving**: Save passwords to a text file when needed
- **Clean Exit**: Program exits after generating passwords
- **Input Validation**: Comprehensive validation for all user inputs
- **Error Handling**: Graceful handling of clipboard and file operations

## Installation

1. Install Python 3.6 or higher
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the password generator:
```bash
python password_generator.py
```

### Auto Generate Mode (Quick)
Perfect for when you need strong passwords fast:
1. Select option 1 from the menu
2. Get 5 passwords instantly (12 characters each, all character types)
3. Choose to copy to clipboard
4. Optionally save to file
5. Program exits automatically

### Interactive Mode (Custom)
Full control over password generation:
1. Select option 2 from the menu
2. Specify password length (4-16 characters)
3. Choose how many passwords to generate (minimum 5)
4. Select which character types to include
5. Choose to copy to clipboard
6. Optionally save to file
7. Program exits automatically

## Code Structure

### Core Functions
- `generate_password()`: Main password generation logic with character pool building
- `display_menu()`: User interface menu display
- `get_password_preferences()`: Interactive preference collection
- `auto_generate_mode()`: Quick password generation with defaults
- `save_to_file()`: File saving functionality with error handling
- `main()`: Application entry point and main loop

### Character Sets Used
- **Lowercase**: `string.ascii_lowercase` (a-z)
- **Uppercase**: `string.ascii_uppercase` (A-Z)  
- **Numbers**: `string.digits` (0-9)
- **Special**: `string.punctuation` (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)

## Technical Details

- **Language**: Python 3.6+
- **Dependencies**: 
  - `pyperclip`: Clipboard operations
  - `random`: Cryptographically secure random generation
  - `string`: Character set definitions
  - `os`: File operations
- **Security**: Uses `random.choice()` for cryptographically secure password generation
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Project Structure
```
password generator/
├── password_generator.py    # Main application
├── README.md               # Project documentation  
├── SYSTEM_ARCHITECTURE.md  # Technical architecture
└── requirements.txt        # Python dependencies
```

## Security Considerations

- **Randomness**: Uses Python's `random` module for secure password generation
- **Character Pool**: Comprehensive character sets for maximum entropy
- **No Storage**: Passwords are not stored in memory after generation
- **User Control**: Full control over character types and length
- **Clipboard Security**: Optional clipboard usage with user consent

## Contributing

This project is part of the CODSOFT internship program and demonstrates:
- Interactive command-line applications
- User input validation and error handling
- File I/O operations
- Clipboard integration
- Modular function design
- Security best practices for password generation

## License

This project is for educational purposes as part of the CODSOFT internship program.
