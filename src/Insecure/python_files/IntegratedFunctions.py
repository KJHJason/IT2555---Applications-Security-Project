import uuid, sqlite3
from datetime import datetime
from __init__ import app
from dicebear import DAvatar, DStyle

def generate_id():
    """
    Generates a unique ID
    """
    return uuid.uuid4().hex

def get_image_path(userID, returnUserInfo=False):
    """
    Returns the image path for the user.
    
    If the user does not have a profile image uploaded, it will return a dicebear url.
    Else, it will return the relative path of the user's profile image.
    
    If returnUserInfo is True, it will return a tuple of the user's record.
    
    Args:
        - userID: The user's ID
        - returnUserInfo: If True, it will return a tuple of the user's record.
    """
    userInfo = user_sql_operation(mode="get_user_data", userID=userID)
    imageSrcPath = userInfo[5]
    if (not imageSrcPath):
        imageSrcPath = get_dicebear_image(userInfo[2])
    return imageSrcPath if (not returnUserInfo) else (imageSrcPath, userInfo)

def get_dicebear_image(username):
    """
    Returns a random dicebear image from the database
    
    Args:
        - username: The username of the user
    """
    av = DAvatar(
        style=DStyle.initials,
        seed=username,
        options=app.config["DICEBEAR_OPTIONS"]
    )
    return av.url_svg

def connect_to_database():
    """
    Connects to the database and returns the connection object
    
    Returns the sqlite3 connection object
    """
    return sqlite3.connect(app.config["SQL_DATABASE"], timeout=5)

def user_sql_operation(mode=None, **kwargs):
    """
    Do CRUD operations on the user table
    
    insert keywords: email, username, password
    login keywords: email, password
    get_user_data keywords: userID
    edit keywords: userID, username, password, email, profileImagePath
    delete keywords: userID
    """
    if (not mode):
        raise ValueError("You must specify a mode in the user_sql_operation function!")

    con = connect_to_database()
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS user (
        id PRIMARY KEY, 
        role TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE, 
        email TEXT NOT NULL UNIQUE, 
        password TEXT NOT NULL, 
        profile_image TEXT, 
        date_joined DATE NOT NULL,
        puchased_courses TEXT
    )""")
    returnValue = None
    if (mode == "insert"):
        emailInput = kwargs.get("email")
        usernameInput = kwargs.get("username")

        emailDupe = bool(cur.execute(f"SELECT * FROM user WHERE email='{emailInput}'").fetchall())

        usernameDupes = bool(cur.execute(f"SELECT * FROM user WHERE username='{usernameInput}'").fetchall())

        if (emailDupe or usernameDupes):
            con.close()
            returnValue = (emailDupe, usernameDupes)

        if (returnValue is None and not emailDupe and not usernameDupes):
            # add to the sqlite3 database
            userID = generate_id()
            passwordInput = kwargs.get("password")
            data = (userID, "Student", usernameInput, emailInput, passwordInput, None, datetime.now().strftime("%Y-%m-%d"), "[]")
            cur.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
            con.commit()
            returnValue = userID

    elif (mode == "login"):
        emailInput = kwargs.get("email")
        passwordInput = kwargs.get("password")
        cur.execute(f"SELECT id, role FROM user WHERE email='{emailInput}' AND password='{passwordInput}'")
        returnValue = cur.fetchall()
        if (not returnValue):
            returnValue = False
        else:
            returnValue = returnValue[0] # returnValue is a list of tuples.

    elif (mode == "get_user_data"):
        userID = kwargs.get("userID")
        cur.execute(f"SELECT * FROM user WHERE id='{userID}'")
        returnValue = cur.fetchall()[0]
        if (not returnValue):
            returnValue = False
    
    elif (mode == "edit"):
        userID = kwargs.get("userID")
        usernameInput = kwargs.get("username")
        emailInput = kwargs.get("email")
        passwordInput = kwargs.get("password")
        profileImagePath = kwargs.get("profileImagePath")
        statement = "UPDATE user SET "
        if (usernameInput is not None):
            statement += f"username='{usernameInput}', "

        if (emailInput is not None):
            statement += f"email='{emailInput}', "

        if (passwordInput is not None):
            statement += f"password='{passwordInput}', "

        if (profileImagePath is not None):
            statement += f"profile_image='{profileImagePath}'"

        statement += f" WHERE id='{userID}'"
        cur.execute(statement)
        con.commit()

    elif (mode == "delete"):
        userID = kwargs.get("userID")
        cur.execute(f"DELETE FROM user WHERE id='{userID}'")
        con.commit()

    con.close()
    return returnValue

def course_sql_operation(mode=None, **kwargs):
    """
    Do CRUD operations on the course table
    
    insert keywords: teacherID
    
    get_course_data keywords: courseID

    edit keywords: 
    """
    if (not mode):
        raise ValueError("You must specify a mode in the course_sql_operation function!")

    con = connect_to_database()
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS course (
        course_id PRIMARY KEY, 
        teacher_id TEXT NOT NULL,
        course_name TEXT NOT NULL,
        course_description TEXT,
        course_image_path TEXT,
        course_price TEXT NOT NULL,
        course_category TEXT NOT NULL,
        course_total_rating INT NOT NULL,
        course_rating_count INT NOT NULL,
        date_created DATE NOT NULL
    )""")
    if (mode == "insert"):
        course_id = generate_id()
        teacher_id = kwargs.get("teacherId")
        course_name = kwargs.get("courseName")
        course_description = kwargs.get("courseDescription")
        course_image_path = kwargs.get("courseImagePath")
        course_price = kwargs.get("coursePrice")
        course_category = kwargs.get("courseCategory")
        course_total_rating = 0
        course_rating_count = 0
        date_created = datetime.now().strftime("%Y-%m-%d")
        
        data = (course_id, teacher_id, course_name, course_description, course_image_path, course_price, course_category, course_total_rating, course_rating_count, date_created)
        cur.execute("INSERT INTO course VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
        con.commit()

    elif (mode == "get_course_data"):
        course_id = kwargs.get("courseId")
        cur.execute(f"SELECT * FROM course WHERE course_id='{course_id}'")
        returnValue = cur.fetchall()
        if (not returnValue):
            returnValue = False
    
    elif (mode == "edit"):
        course_id = kwargs.get("courseId")
        course_name = kwargs.get("courseName")
        course_description = kwargs.get("courseDescription")
        course_image_path = kwargs.get("courseImagePath")
        course_price = kwargs.get("coursePrice")
        course_category = kwargs.get("courseCategory")
        course_total_rating = kwargs.get("courseTotalRating")
        course_rating_count = kwargs.get("courseRatingCount")

    elif (mode == "delete"):
        course_id = kwargs.get("courseId")
        cur.execute(f"DELETE FROM course WHERE course_id='{course_id}'")
        con.commit()
        
    con.close()
    return