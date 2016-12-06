This is app created by me - marq
You can use it and share it if you want!!!
Works only on Unix workstations!!!

How to run this up:
1. Download Python v2.7
2. Install pip (should be already installed with Python)
3. Download files from git repo
4. Set up virtual environment - it is good practice
5. Run command in main directory of app: pip install -r requirement.txt - isn't updated!!! - require manual installation of sam packages.
6. Run: python manage.py shell
7. Run commands:
   db.create_all()
   db.insert_roles()
   User.generate_fake()
   Item.generate_fake()
8. Set environment variables:
   MAIL_USERNAME
   MAIL_PASSWORD
   FLASKY_ADMIN
   and update of config.py file (email server settings - current set for gmail)
6. Execute command: python manage.py db upgrade (migrations directory added to repo)
6. To run this app execute command in main directory of app:
   python manage.py runserver --host 0.0.0.0
