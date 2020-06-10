import os

host= os.environ.get('MAHAR_DB_HOST', 'localhost')
db_name= os.environ.get('MAHART_DB_NAME', 'mahar')
mysql_user= os.environ.get('MAHAR_DB_USERNAME', 'root' )
mysql_password=os.environ.get('MAHAR_DB_PASSWORD', 'mysql_7621_*+-')

front_url = 'https://doplus.ir'
back_url = 'https://doplus.ir'
