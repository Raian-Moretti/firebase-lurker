import os
import hashlib
import subprocess
import sys
import argparse
import re
import glob

# Define colors for terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKRED = '\033[91m'
    OKMEDIUMRED = '\033[38;2;207;55;55m'
    OKLIGHTRED = '\033[38;2;255;99;71m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Function to get shades of red for gradient-like effect in ASCII art
def get_red_shade(line_index, total_lines):
    # Generate shades of red from dark to light
    red_shades = [
        '\033[38;2;139;0;0m',    # Dark Red
        '\033[38;2;178;34;34m',  # Medium Dark Red
        '\033[38;2;207;55;55m',  # Medium Red
        '\033[38;2;255;99;71m',  # Light Red
    ]
    return red_shades[min(line_index // 2, len(red_shades) - 1)]  # Return the appropriate shade

# Function to calculate SHA-256 hash of an APK file for unique identification
def calculate_hash(apk_path):
    hasher = hashlib.sha256()  # Use SHA-256 hashing algorithm
    with open(apk_path, 'rb') as f:
        while chunk := f.read(8192):  # Read file in chunks to handle large files
            hasher.update(chunk)  # Update hash object with current chunk
    return hasher.hexdigest()  # Return the final hash value

# Extract Firebase URLs from the given content using regex
def extract_firebase_links(content):
    # Updated regex to match Firebase links, including firebaseapp.com and firebaseio.com
    regex = r'https?://(?:[^\s/]+\.firebaseapp\.com|[^\s/]+\.firebaseio\.com|[^\s/]+\.firebase\.com)[^\s<>]*'
    return re.findall(regex, content)  # Return all matched Firebase links

# Function to walk through the decompiled APK directory and check for Firebase links
def check_firebase_links(decompiled_dir):
    firebase_links = set()  # Use a set to avoid duplicate links
    # Walk through all files in the decompiled APK directory
    for root, _, files in os.walk(decompiled_dir):
        for file in files:
            # Look for files that could contain Firebase links (e.g., .xml and .json)
            if file.endswith('.xml') or file.endswith('.json'):
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()  # Read file content
                    links = extract_firebase_links(content)  # Extract Firebase links from file content
                    firebase_links.update(links)  # Add the links to the set
    return list(firebase_links)  # Return the list of Firebase links

# Function to decompile APK using apktool and store output in the specified directory
def decompile_apk(apk_path, output_dir, force):
    # Check if the output directory already exists and skip decompilation if 'force' flag is not set
    if os.path.exists(output_dir) and not force:
        print(f"{bcolors.WARNING}Skipping decompilation; destination directory ({output_dir}) already exists.{bcolors.ENDC}")
        return True  # Return True to indicate no errors occurred

    # Get the script's directory and find apktool jar dynamically
    script_path = os.path.dirname(os.path.abspath(__file__))
    apktool_path = glob.glob(f'{script_path}\\dependencies\\apktool_*.jar')  # Search for apktool jar file

    if apktool_path:
        # Construct the apktool command with the first matching apktool jar file
        apktool_cmd = [
            "java", "-jar", apktool_path[0],  # Use the found apktool jar file
            "d", "--output", output_dir, apk_path  # Decompile command
        ]
    else:
        print("No apktool JAR file found!")  # Notify the user if apktool is not found
        return False

    # Execute the apktool command using subprocess
    try:
        result = subprocess.run(apktool_cmd, capture_output=True, text=True, check=True)  # Run apktool
        return True  # Return True if the command executed successfully
    except subprocess.CalledProcessError as e:
        # Handle errors and display the error message
        print(f"{bcolors.FAIL}Apktool failed with exit status {e.returncode}. Please Try Again.{bcolors.ENDC}")
        print(f"Error Output: {e.stderr}")
        return False  # Return False if apktool fails

# ASCII art output with gradient effect
ascii_art_lines = [
"			@@@@@@@@   @@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@  @@@  @@@@@@@   @@@@@@@@",  
"			@@!       @@@@!  @@!  @@@       @@!  @@!  @@@  @@!  @@@  !@@            @@!",       
"			!@!      !!!!@!  !@!  @!@       !@!  !@   @!@  !@!  @!@  !@!            !@!",       
"			@!!!:!      !!@  @!@!!@!    @@!!!:!  @!@!@!@   @!@!@!@!  !!@@!!      @!!!:!",    
"			!!!!!:      !!!  !!@!@!     !!!!!!:  !!!@!!!!  !!!@!!!!   !!@!!!     !!!!!:",    
"			!!:         !!:  !!: :!!        !!:  !!:  !!!       !!!       !:!       !!:",       
"			:!:         :!:  :!:  !:!       :!:  :!:  !:!       !:!      !:!        :!:",       
"			 ::          ::  ::   :::   :: ::::  :::: :::       :::  :::: ::    :: ::::",    
"				                                                                   ",            
"			       @@@	  @@@    @@@  @@@@@@@@  @@@   @@@  @@@@@@@@  @@@@@@@@  	   ",
"			       @@@        @@@    @@@  @@!  @@@  @@!   !@@       @@!  @@!  @@@  	   ",
"		 	       !@@        !@@    !@@  !@!  @!@  !@!  @!@        !@!  !@!  @!@  	   ",
"			       !@!        !@!    !@!  @!@!!@!   @!@!!@!     @@!!!:!  @!@!!@!  	   ",
"			       !!@    	  !!@	 !!@  !!@!@!    !!@!@!      !!!!!!:  !!@!@!  	   ",
"			       !!@   	  !!@	 !!@  !!: :!!   !!: :!!         !!:  !!: :!!  	   ",
"			       !:!        !:!    !:!  :!:  !:!  :!:  !:!        :!:  :!:  !:!  	   ",
"			       :::: ::::  :::::: :::  :::   ::  :::    ::   :: ::::  :::   ::  	   ",
"				                                                                   ",   
]
# Print the ASCII art with gradient effect
for index, line in enumerate(ascii_art_lines):
    print(get_red_shade(index %9, len(ascii_art_lines)) + line + bcolors.ENDC)	
print(bcolors.OKRED + bcolors.BOLD + "\t\t\t\t\t    # Developed By Raian Moretti" + bcolors.ENDC)
print(bcolors.OKMEDIUMRED + bcolors.BOLD + "\t\t\t\t\t\t" + bcolors.ENDC)
print(bcolors.OKLIGHTRED + bcolors.BOLD + "\t\t\t\t\t# Credits to Shiv Sahni - @shiv__sahni" + bcolors.ENDC)

# Main function to handle argument parsing and flow control
def main():
    # Argument parsing for APK path and optional force flag
    parser = argparse.ArgumentParser(description='Scan APK for Firebase Misconfigurations.')
    parser.add_argument('--path', required=True, help='Path to the APK file.')  # APK file path argument
    parser.add_argument('--force', action='store_true', help='Force overwrite the output directory.')  # Force flag

    args = parser.parse_args()
    apk_path = args.path

    # Check if the provided APK path is valid
    if not os.path.isfile(apk_path):
        print(f"{bcolors.FAIL}APK File Not Found.{bcolors.ENDC}")  # Error if APK file doesn't exist
        sys.exit(1)

    print(f"{bcolors.OKGREEN}APK File Found.{bcolors.ENDC}")

    # Calculate hash and prepare output directory path
    apk_hash = calculate_hash(apk_path)
    output_dir = os.path.join(os.path.expanduser("~"), ".SourceCodeAnalyzer", f"{os.path.basename(apk_path)}_{apk_hash}")

    print(f"{bcolors.OKBLUE}Initiating APK Decompilation Process.{bcolors.ENDC}")

    if not decompile_apk(apk_path, output_dir, args.force):
        sys.exit(1)

    # Proceed to check for Firebase links
    firebase_links = check_firebase_links(output_dir)
    if firebase_links:
        print(f"{bcolors.OKGREEN}Firebase links found:{bcolors.ENDC}")
        for link in firebase_links:
            # Strip unwanted characters like </string> from the end
            clean_link = link.split('</')[0]  # Remove any unwanted trailing tags
            print(clean_link)
    else:
        print(f"{bcolors.WARNING}No Firebase links found.{bcolors.ENDC}")

    print(f"{bcolors.OKGREEN}Finished running Firebase scanner.{bcolors.ENDC}")

if __name__ == '__main__':
    main()
