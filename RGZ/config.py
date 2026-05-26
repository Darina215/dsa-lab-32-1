class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/finance_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "super_secret_key"