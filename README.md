# BitrixProject
  This project is prototype of Bitrix24 platform, which provides a company with a full range of teamworking and social networking means. Our project as well as Bitrix24 itself is mostly intended for small and mid-scale businesses. 
  Using this service, company can manage all personal information, files, reports of employees. Also users can share posts with all users or in selected groups.
  Company admin can register users, assigning them a department (one of the departments of company). After that new user should log in and then update its profile data.
 
 Installation process:
 
* clone the repository
* cd bitrixproject
* create the virtualenv
* pip install -r requirements.txt
* python manage.py migrate
* python manage.py createsuperuser
* python manage.py runserver
* import postman collection
