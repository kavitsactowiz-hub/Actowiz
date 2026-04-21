import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="rottentomatoes"
)
mycursor = mydb.cursor()


sql_query = """
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_name VARCHAR(255),
    poster_image TEXT,
    tomatometer VARCHAR(10),
    reviews_summary VARCHAR(50),
    description TEXT,
    what_to_know_title VARCHAR(255),
    what_to_know_desc TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
mycursor.execute(sql_query)

sql_query = """
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    reviewer_name VARCHAR(255),
    reviewer_source VARCHAR(255),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
);
"""
mycursor.execute(sql_query)

sql_query = """
CREATE TABLE IF NOT EXISTS cast_and_crew (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    castimage TEXT,
    casttitle VARCHAR(255),
    castcharacters VARCHAR(255),
    castcredits VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
);
"""
mycursor.execute(sql_query)

sql_query = """
CREATE TABLE IF NOT EXISTS videos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    thumbnail_title VARCHAR(255),
    thumbnail_url TEXT,
    video_link TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
);
"""
mycursor.execute(sql_query)