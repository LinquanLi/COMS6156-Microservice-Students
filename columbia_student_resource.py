import pymysql
from os import getenv


class ColumbiaStudentResource:

    def __init__(self):
        pass

    @staticmethod
    def _get_connection():
        conn = pymysql.connect(
            user=getenv("DBUSER"),
            password=getenv("DBPWD"),
            host=getenv("DBHOST"),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_by_template(limit=10, offset=0):
        sql = "SELECT * FROM f22_databases.columbia_students LIMIT %s OFFSET %s"
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql, args=(limit, offset))
        return cur.fetchall()

    @staticmethod
    def get_by_key(key):
        sql = "SELECT * FROM f22_databases.columbia_students where uni=%s"
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql, args=key)
        return cur.fetchone()

    @staticmethod
    def update_by_key(uni, student):
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        content = []
        if "first_name" in student:
            content.append("first_name = \"" + student["first_name"] + "\"")
        if "last_name" in student:
            content.append("last_name = \"" + student["last_name"] + "\"")
        if "middle_name" in student:
            content.append("middle_name = \"" + student["middle_name"] + "\"")
        if "email" in student:
            content.append("email = \"" + student["email"] + "\"")
        if "school_code" in student:
            content.append("school_code = \"" + student["school_code"] + "\"")
        sql = "UPDATE f22_databases.columbia_students SET " + ", ".join(content) + " WHERE uni=%s"
        cur.execute(sql, args=uni)
        result = cur.fetchone()

        return result

    @staticmethod
    def insert_by_key(student):
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        if "uni" not in student:
            raise ValueError("No uni")
        uni = student["uni"] if "uni" in student else ""
        first_name = student["first_name"] if "first_name" in student else ""
        last_name = student["last_name"] if "last_name" in student else ""
        middle_name = student["middle_name"] if "middle_name" in student else ""
        email = student["email"] if "email" in student else ""
        school_code = student["school_code"] if "school_code" in student else ""
        sql = "INSERT INTO f22_databases.columbia_students (uni, first_name, last_name, middle_name, email, " \
              "school_code) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(sql, args=(uni, first_name, last_name, middle_name, email, school_code))
        return

    @staticmethod
    def delete_by_key(uni):
        conn = ColumbiaStudentResource._get_connection()
        cur = conn.cursor()
        sql = "DELETE FROM f22_databases.columbia_students WHERE uni=%s"
        cur.execute(sql, args=uni)
        return
