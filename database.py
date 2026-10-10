import mysql.connector as c
from mysql.connector import Error

host = "localhost"
user = "root"
password = "root"
database = "hospital_management"

def get_db_connection(Database=None):
    if Database is None:
        return c.connect(
            host=host, 
            user=user, 
            passwd=password,
            charset="utf8",
            collation="utf8_general_ci"
        )
    else:
        return c.connect(
            host=host, 
            user=user, 
            passwd=password,
            database=Database,
            charset="utf8",
            collation="utf8_general_ci"
        )
    
def setup_database():
    con=None
    cur=None

    try:
        con=get_db_connection()
        cur=con.cursor()

        query="CREATE DATABASE IF NOT EXISTS hospital_management"
        cur.execute(query)

        cur.close()
        con.close()
        cur=None
        con=None

        con= get_db_connection(database)
        cur=con.cursor()

        department_sql = """
            CREATE TABLE IF NOT EXISTS departments (
                department_id INT PRIMARY KEY,
                department_name VARCHAR(100) NOT NULL UNIQUE
            )
        """
        cur.execute(department_sql)


        patient_sql="""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INT PRIMARY KEY,
                patient_name VARCHAR(100) NOT NULL,
                age int NOT NULL,
                gender VARCHAR(20) NOT NULL,
                phone_number VARCHAR(20) NOT NULL ,
                address VARCHAR(255)
            )
        """
        cur.execute(patient_sql)

        doctor_sql = """
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INT PRIMARY KEY,
                doctor_name VARCHAR(100) NOT NULL,
                specialization VARCHAR(100) NOT NULL,
                phone_number VARCHAR(20) NOT NULL,
                department_id INT,
                FOREIGN KEY (department_id)
                    REFERENCES departments(department_id)
            )
        """
        cur.execute(doctor_sql)

        appointment_sql = """
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INT PRIMARY KEY,
                patient_id INT NOT NULL,
                doctor_id INT NOT NULL,
                appointment_date DATETIME NOT NULL,
                reason VARCHAR(255),
                status VARCHAR(30) NOT NULL DEFAULT 'Scheduled',
                FOREIGN KEY (patient_id)
                    REFERENCES patients(patient_id),
                FOREIGN KEY (doctor_id)
                    REFERENCES doctors(doctor_id)
            )
        """
        cur.execute(appointment_sql)

        room_sql = """
            CREATE TABLE IF NOT EXISTS rooms (
                ROOM_ID INT(10) PRIMARY KEY, 
                ROOM_TYPE VARCHAR(15), 
                BEDS_AVAILABLE INT(4),
                  CHARGE_PER_DAY INT(10)
            )
        """
        cur.execute(room_sql)

        admission_sql="""
            CREATE TABLE IF NOT EXISTS admissions(
                ADMISSION_ID INT PRIMARY KEY,
                PATIENT_ID INT NOT NULL,
                DOCTOR_ID INT NOT NULL,
                ROOM_ID INT,
                ADMISSION_DATE DATE NOT NULL,
                DISCHARGE_DATE DATE ,
                STATUS VARCHAR(20) NOT NULL DEFAULT "Admitted",
                FOREIGN KEY (PATIENT_ID) 
                    REFERENCES PATIENTS(PATIENT_ID),
                FOREIGN KEY (DOCTOR_ID) 
                    REFERENCES DOCTORS(DOCTOR_ID),
                FOREIGN KEY (ROOM_ID)
                    REFERENCES ROOMS(ROOM_ID)
            )
        """
        cur.execute(admission_sql)    

        con.commit()
        print("Database and tables created successfully!")

    except Error as e:
        print("MySQL error:", e)

        if con is not None and con.is_connected():
            con.rollback()

    finally:
        if cur is not None:
            cur.close()

        if con is not None and con.is_connected():
            con.close()


if __name__ == "__main__":
    setup_database()
