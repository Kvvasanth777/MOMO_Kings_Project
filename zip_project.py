import os
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile.ZipFile object
    for root, dirs, files in os.walk(path):
        for file in files:
            # Exclude existing db.sqlite3, any pyc, or zip file itself
            if 'db.sqlite3' in file or file.endswith('.pyc') or file.endswith('.zip') or '.git' in root or '__pycache__' in root:
                continue
            
            filepath = os.path.join(root, file)
            # Make path relative to project folder
            relpath = os.path.relpath(filepath, os.path.join(path, '..'))
            ziph.write(filepath, relpath)

if __name__ == '__main__':
    project_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(project_dir, 'momokings_project.zip')
    
    zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    # Zip the restaurant_management directory
    zipdir(os.path.join(project_dir, 'restaurant_management'), zipf)
    # Add requirements.txt and README.md
    if os.path.exists(os.path.join(project_dir, 'requirements.txt')):
        zipf.write(os.path.join(project_dir, 'requirements.txt'), 'requirements.txt')
    if os.path.exists(os.path.join(project_dir, 'README.md')):
        zipf.write(os.path.join(project_dir, 'README.md'), 'README.md')
    zipf.close()
    print(f"Project successfully compressed into {zip_path}")
