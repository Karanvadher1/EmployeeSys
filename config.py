class Config:
    SECRET_KEY = '79d3ed48afbe765ef04ff25d21a36ef4'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres',pw='postgres',url='127.0.0.1:5432',db='Employee_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False