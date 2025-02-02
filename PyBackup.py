import os
import shutil

def backup_xlsx_files(source_dir="Raw/", backup_dir="Backups/"):
    # Ensure backup directory exists
    os.makedirs(backup_dir, exist_ok=True)
    
    # Loop through files in source directory
    for filename in os.listdir(source_dir):
        if filename.endswith(".xlsx"):  # Check for .xlsx files
            source_path = os.path.join(source_dir, filename)
            backup_path = os.path.join(backup_dir, filename)
            
            # Copy file to backup directory
            shutil.copy2(source_path, backup_path)
            print(f"Backed up: {filename}")

if __name__ == "__main__":
    backup_xlsx_files()
