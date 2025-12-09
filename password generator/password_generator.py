# Import required libraries
import random  # For generating random characters
import string  # For accessing character sets (letters, digits, punctuation)
import pyperclip  # For clipboard functionality
import os  # For file operations

def generate_password(length, use_uppercase=True, use_lowercase=True, use_numbers=True, use_special=True):
    """
    Generate a random password based on specified criteria.
    
    Args:
        length (int): The desired length of the password
        use_uppercase (bool): Include uppercase letters (A-Z)
        use_lowercase (bool): Include lowercase letters (a-z)
        use_numbers (bool): Include numbers (0-9)
        use_special (bool): Include special characters (!@#$, etc.)
    
    Returns:
        str: The generated password or error message
    """
    # Initialize empty string to store available characters
    characters = ""
    
    # Build character pool based on user preferences
    if use_lowercase:
        characters += string.ascii_lowercase  # Add a-z
    if use_uppercase:
        characters += string.ascii_uppercase  # Add A-Z
    if use_numbers:
        characters += string.digits  # Add 0-9
    if use_special:
        characters += string.punctuation  # Add !@#$%^&*()_+-=[]{}|;:,.<>?
    
    # Validate that at least one character type is selected
    if not characters:
        return "Error: At least one character type must be selected!"
    
    # Generate password by randomly selecting characters
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def display_menu():
    """
    Display the main menu with available options.
    Shows a formatted menu for user interaction.
    """
    print("\n" + "="*50)
    print("       PASSWORD GENERATOR")
    print("="*50)
    print("1. Auto Generate (Quick)")
    print("2. Interactive Mode (Custom)")
    print("3. Exit")
    print("="*50)

def get_password_preferences():
    """
    Get user preferences for password generation.
    Prompts user for password length, count, and character types.
    
    Returns:
        tuple: (length, count, use_uppercase, use_lowercase, use_numbers, use_special)
    """
    print("\n--- Password Configuration ---")
    
    # Get password length with validation (minimum 4, maximum 16)
    while True:
        try:
            length = int(input("Enter password length (4-16): "))
            if length < 4:
                print("Password length must be at least 4 characters.")
                continue
            if length > 16:
                print("Password length cannot exceed 16 characters.")
                continue
            break  # Valid input, exit loop
        except ValueError:
            print("Please enter a valid number.")
    
    # Get number of passwords to generate with validation (minimum 5)
    while True:
        try:
            count = int(input("How many passwords to generate (minimum 5)? "))
            if count < 5:
                print("Must generate at least 5 passwords.")
                continue
            break  # Valid input, exit loop
        except ValueError:
            print("Please enter a valid number.")
    
    # Get character type preferences (default is 'yes' for all)
    print("\n--- Character Types (press Enter for default: all enabled) ---")
    use_uppercase = input("Include uppercase letters? (Y/n): ").strip().lower() != 'n'
    use_lowercase = input("Include lowercase letters? (Y/n): ").strip().lower() != 'n'
    use_numbers = input("Include numbers? (Y/n): ").strip().lower() != 'n'
    use_special = input("Include special characters? (Y/n): ").strip().lower() != 'n'
    
    return length, count, use_uppercase, use_lowercase, use_numbers, use_special

def auto_generate_mode():
    """
    Auto-generate mode: Quickly generates 5 passwords with default settings.
    Default: 12 characters, all character types enabled.
    
    Returns:
        list: List of generated passwords
    """
    # Default settings for quick generation
    default_length = 12
    default_count = 5
    print("\n--- Auto Generate Mode ---")
    print(f"Generating {default_count} passwords with default settings:")
    print(f"  • Length: {default_length} characters")
    print(f"  • Character types: All (uppercase, lowercase, numbers, special)")
    
    # Generate multiple passwords with all character types
    passwords = []
    print(f"\n{'='*50}")
    print(f"   GENERATED PASSWORDS")
    print(f"{'='*50}")
    
    for i in range(default_count):
        password = generate_password(default_length, True, True, True, True)
        passwords.append(password)
        print(f"{i+1}. {password}")
    
    print(f"{'='*50}")
    
    # Ask user if they want to copy to clipboard
    copy_choice = input("\nCopy all passwords to clipboard? (Y/n): ").strip().lower()
    if copy_choice != 'n':
        try:
            all_passwords = '\n'.join(passwords)
            pyperclip.copy(all_passwords)
            print("✓ All passwords copied to clipboard!")
        except Exception as e:
            print(f"✗ Could not copy to clipboard: {e}")
    
    # Ask user if they want to save to file
    save_choice = input("\nSave passwords to file? (y/N): ").strip().lower()
    if save_choice == 'y':
        save_to_file(passwords)
    
    # Display final message with passwords
    print("\n" + "="*50)
    print("Here are your passwords:")
    for i, pwd in enumerate(passwords, 1):
        print(f"{i}. {pwd}")
    print("="*50)
    
    return passwords

def save_to_file(passwords):
    """
    Save generated passwords to a text file.
    
    Args:
        passwords (list): List of generated passwords to save
    """
    # Get filename from user (default: passwords.txt)
    filename = input("\nEnter filename (e.g., passwords.txt): ").strip()
    if not filename:
        filename = "passwords.txt"
    
    try:
        # Write passwords to file with formatting
        with open(filename, 'w') as f:
            f.write("Generated Passwords\n")
            f.write("="*50 + "\n\n")
            # Write each password with numbering
            for i, pwd in enumerate(passwords, 1):
                f.write(f"{i}. {pwd}\n")
        print(f"✓ Passwords saved to '{filename}'")
    except Exception as e:
        # Handle any file writing errors
        print(f"✗ Error saving to file: {e}")

def main():
    """
    Main function to run the password generator application.
    Handles the interactive menu loop and user interactions.
    """
    print("\nWelcome to the Password Generator!")
    
    # Main program loop
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-3): ").strip()
        
        # Option 1: Auto Generate Mode (Quick)
        if choice == '1':
            auto_generate_mode()
            # Exit after generating password
            print("\nThank you for using Password Generator! Stay secure! 🔒")
            break
        
        # Option 2: Interactive Mode (Custom)
        elif choice == '2':
            # Get user preferences for password generation
            length, count, use_upper, use_lower, use_nums, use_special = get_password_preferences()
            
            # Generate the requested number of passwords
            passwords = []
            print(f"\n{'='*50}")
            print(f"   GENERATED PASSWORD{'S' if count > 1 else ''}")
            print(f"{'='*50}")
            
            # Generate and display each password
            for i in range(count):
                password = generate_password(length, use_upper, use_lower, use_nums, use_special)
                passwords.append(password)
                print(f"{i+1}. {password}")
            
            print(f"{'='*50}")
            
            # Ask user if they want to copy all passwords to clipboard
            copy_choice = input("\nCopy all passwords to clipboard? (Y/n): ").strip().lower()
            if copy_choice != 'n':
                try:
                    # Join all passwords with newlines and copy
                    all_passwords = '\n'.join(passwords)
                    pyperclip.copy(all_passwords)
                    print("✓ All passwords copied to clipboard!")
                except Exception as e:
                    print(f"✗ Could not copy to clipboard: {e}")
            
            # Ask user if they want to save passwords to file
            save_choice = input("\nSave passwords to file? (y/N): ").strip().lower()
            if save_choice == 'y':
                save_to_file(passwords)
            
            # Display final message with passwords
            print("\n" + "="*50)
            print("Here are your passwords:")
            for i, pwd in enumerate(passwords, 1):
                print(f"{i}. {pwd}")
            print("="*50)
            
            # Exit after generating passwords
            print("\nThank you for using Password Generator! Stay secure! 🔒")
            break
        
        # Option 3: Exit program
        elif choice == '3':
            print("\nThank you for using Password Generator! Stay secure! 🔒")
            break
        
        # Invalid option
        else:
            print("\n✗ Invalid choice. Please select 1, 2, or 3.")

# Entry point of the program
if __name__ == "__main__":
    main()
