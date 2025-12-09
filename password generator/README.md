# Password Generator

A Python-based interactive password generator that creates strong, random passwords with two convenient modes: Auto Generate for quick password creation and Interactive Mode for full customization.

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

## Installation

1. Install the required dependencies:
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

## Example

```
Welcome to the Password Generator!

==================================================
       PASSWORD GENERATOR
==================================================
1. Auto Generate (Quick)
2. Interactive Mode (Custom)
3. Exit
==================================================

Enter your choice (1-3): 1

--- Auto Generate Mode ---
Generating 5 passwords with default settings:
  • Length: 12 characters
  • Character types: All (uppercase, lowercase, numbers, special)

==================================================
   GENERATED PASSWORDS
==================================================
1. K9#mP2$xL5@q
2. T4!vW7%jN3*s
3. F1@dC8#gM2$p
4. R6^bH9&kL3#m
5. N5*qT8@wP1!x
==================================================

Copy all passwords to clipboard? (Y/n): y
✓ All passwords copied to clipboard!

Save passwords to file? (y/N): n

==================================================
Here are your passwords:
1. K9#mP2$xL5@q
2. T4!vW7%jN3*s
3. F1@dC8#gM2$p
4. R6^bH9&kL3#m
5. N5*qT8@wP1!x
==================================================

Thank you for using Password Generator! Stay secure! 🔒
```

## Requirements

- Python 3.6+
- pyperclip library (for clipboard functionality)

## Security Note

Generated passwords are cryptographically random and suitable for most use cases. Always store passwords securely using a password manager.
