import os

host= os.environ.get('DOTEST_DB_HOST', 'localhost')
db_name= os.environ.get('DOTEST_DB_NAME', 'mahar')
mysql_user= os.environ.get('DOTEST_DB_USERNAME', 'root' )
mysql_password=os.environ.get('DOTEST_DB_PASSWORD', 'Salam159')