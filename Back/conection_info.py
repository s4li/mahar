import os

host= os.environ.get('MAHAR_DB_HOST', 'localhost')
db_name= os.environ.get('MAHART_DB_NAME', 'mahar')
mysql_user= os.environ.get('MAHAR_DB_USERNAME', 'root' )
mysql_password=os.environ.get('MAHAR_DB_PASSWORD', 'Salam159')

front_url = 'http://194.5.188.147:5555'
back_url = 'http://194.5.188.147:5000'
