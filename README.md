# AntiScamShop


A Django project to track scam shops, user posts, comments, and authentication features.


### features:


* User can serach the shop name for seeing if the shop is scammer
* like and dislike feature
* authenticate system
* create edit delte post system that is in profile page
* and detail view and list view for the post with pagination


### how to run this project in my pc?

1. Clone the repository: 
git clone https://github.com/Hydarian/AntiScamShop.git
2. create virtual environment:
python -m venv venv
3. Activate the virtual environment:
venv\Scripts\activate
4. Install dependencies:
pip install -r requirements.txt
5. Apply migration:
python manage.py migrate
6. create a superuser (optional, for admin access):
python manage.py createsuperuser
7. Run the development server:
python manage.py runserver
8. Open your browser and go to:
http://127.0.0.1:8000/

Notes:
Password reset emails will appear in the console for development.
Media files, database, and migrations are ignored in Git. Use python manage.py migrate to set up the database locally.
