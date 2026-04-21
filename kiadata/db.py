import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="kiacar"
)
mycursor = mydb.cursor()

sql_query = """
CREATE TABLE IF NOT EXISTS dealers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    website VARCHAR(255),
    dealer_name VARCHAR(255),
    address TEXT,
    phone1 VARCHAR(255),
    phone2 VARCHAR(255),
    city_name VARCHAR(100),
    state_name VARCHAR(100),
    dealer_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
mycursor.execute(sql_query)