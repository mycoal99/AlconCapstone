import os
import sys
import argparse
import sqlite3
from patient import Patient
import json
from typing import List


### SET UP DATABASE PATH-----------------------------------------------------------
with open('db-config.json') as f:
    config = json.load(f)


PATH = config['database-local-path']
DATABASE_NAME = config['database-name']
DATABASE_MODEL = config['database-model']

try:
    if not os.path.exists(PATH):
        os.makedirs(PATH)
except:
    print("[EXCEPTION]: database irectory path is not valid.")

DATABASE_NAME = PATH + '/' + DATABASE_NAME



### ---------------------------------------------------------------------------


connect = sqlite3.connect(DATABASE_NAME)

cur = connect.cursor()

# print(cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='patients'").fetchall())
if not cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='patients'").fetchall():
    cur.execute("""CREATE TABLE patients (
                    id INTEGER PRIMARY KEY,
                    firstname text,
                    lastname text,
                    DOB text,
                    left_eye_template text,
                    right_eye_template text,
                    surgery text
                )""")
  if not curr.execute("SELECT count(*) FROM sqlite_master WHERE type='index' and name='ix_patients_lastname_firstname').fetchall():
    curr.execute("""
                CREATE INDEX ix_patients_lastname_firstname ON patients (lastname, firstname);
                CREATE INDEX ix_patiients_surgery ON patients (surgery);
                """)

connect.close()


### ------------------------------------------------------------------------------------
###                 SUPPORTED FUNCTIONS
### ------------------------------------------------------------------------------------

def add_patient(firstname:str, lastname:str, DOB:str, left_eye_template, right_eye_template, surgery:str):
    '''
        Input:
            * patient_id (str): the id of the patient, which is automatically incremented by the database.
            firstname (str): patient's firstname
            lastname (str): patient's lastname
            DOB (str): patient's date of birth
            left_eye_template (.mat): the template generated/extracted from the image of patient's eye
        Output:
            void

    '''
    try:
        patient = Patient(None, firstname, lastname, DOB, left_eye_template, right_eye_template, surgery)
        insert_new_patient(patient)
    except:
        print("[EXCEPTION] The order of fields are: firstname, lastname, date of birth, left_eye_template, right_eye_template, surgery")
def insert_new_patient(patient:Patient):
    '''
        Input:
            patient (Patient)
        Output:
            void

    '''
    connect = sqlite3.connect(DATABASE_NAME)
    cur = connect.cursor()
    with connect:
        cur.execute("INSERT INTO patients VALUES (:id, :firstname, :lastname, :DOB, :left_eye_template, :right_eye_template, :surgery)", 
        {'id': patient.patient_id, 'firstname':patient.firstname, 'lastname':patient.lastname, 'DOB':patient.DOB, 'left_eye_template':patient.left_eye_template, 'right_eye_template':patient.right_eye_template, 'surgery':patient.surgery})
    connect.close()

def remove_patient(id:int):
    '''
        Remove patient by id.
        Input:
           id (int): patient_id
        Output:
            Void

    '''
    connect = sqlite3.connect(DATABASE_NAME)
    cur = connect.cursor()
    patient_list = []
    with connect:
        patient_list = cur.execute("DELETE FROM patients WHERE id=:id", {'id':id}).fetchall()
    connect.close()

def remove_patient_by_firstname(firstname:str):
    '''
    Remove patient by firstname.
        Input:
            firstname (str): patient's firstname
        Output:
            Void

    '''
    connect = sqlite3.connect(DATABASE_NAME)
    cur = connect.cursor()
    patient_list = []
    with connect:
        patient_list = cur.execute("DELETE FROM patients WHERE firstname=:firstname", {'firstname':firstname}).fetchall()
    connect.close()

def remove_patient_by_lastname(lastname:str):
    '''
    Remove patient by lastname.
        Input:
            lastname (str): patient's lastname
        Output:
            Void

    '''
    connect = sqlite3.connect(DATABASE_NAME)
    cur = connect.cursor()
    patient_list = []
    with connect:
        patient_list = cur.execute("DELETE FROM patients WHERE lastname=:lastname", {'lastname':lastname}).fetchall()
    connect.close()


def get_patient_by_id(id:int):
    '''
    Returns a list of patients by id.
        Input:
            id (str): the id of the patient
        Output:
            jsonfile: list of patients found in json format

    '''
    connect = sqlite3.connect(DATABASE_NAME)
    cur = connect.cursor()
    patient_list = []
    with connect:
        patient_list = cur.execute("SELECT * FROM patients WHERE id=:id", {'id':id}).fetchall()
    connect.close()
    return json_format(patient_list)

def get_patient_by_firstname(firstname:str):
    '''
    Returns a list of patients by firstname.
        Input:
            firstname (str): patient's firstname
        Output:
            jsonfile: list of patients found in json format
    '''
    connect = sqlite3.connect(DATABASE_NAME)
    cur = connect.cursor()
    patient_list = []
    with connect:
        patient_list = cur.execute("SELECT * FROM patients WHERE firstname=:firstname", {'firstname':firstname}).fetchall()
    connect.close()
    return json_format(patient_list)

def get_patient_by_lastname(lastname:str):
    '''
    Returns a list of patients by lastname.
        Input:
            lastname (str): patient's lastname
        Output:
            jsonfile: list of patients found in json format
    '''
    connect = sqlite3.connect(DATABASE_NAME)
    cur = connect.cursor()
    patient_list = []
    with connect:
        patient_list = cur.execute("SELECT * FROM patients WHERE lastname=:lastname", {'lastname':lastname}).fetchall()
    connect.close()
    return json_format(patient_list)

def get_patient_by_DOB(DOB:str):
    '''
    Returns a list of patients by date of birth.
        Input:
            DOB (str): patient's date of birth
        Output:
            jsonfile: list of patients found in json format
    '''
    connect = sqlite3.connect(DATABASE_NAME)
    cur = connect.cursor()
    patient_list = []
    with connect:
        patient_list = cur.execute("SELECT * FROM patients WHERE DOB=:DOB", {'DOB':DOB}).fetchall()
    connect.close()
    return json_format(patient_list)

def get_patient_by_left_eye_template(left_eye_template):
    '''
    Returns a list of patients by template of the left eye.
        Input:
            left_eye_template (.mat): the template generated/extracted from the image of patient's LEFT eye
        Output:
            jsonfile: list of patients found in json format

    '''
    connect = sqlite3.connect(DATABASE_NAME)
    cur = connect.cursor()
    patient_list = []
    with connect:
        patient_list = cur.execute("SELECT * FROM patients WHERE left_eye_template=:left_eye_template", {'left_eye_template':left_eye_template}).fetchall()
    connect.close()
    return json_format(patient_list)

def get_patient_by_right_eye_template(right_eye_template):
    '''
    Returns a list of patients by template of the right eye.
        Input:
            right_eye_template (.mat): the template generated/extracted from the image of patient's RIGHT eye
        Output:
            jsonfile: list of patients found in json format

    '''
    connect = sqlite3.connect(DATABASE_NAME)
    cur = connect.cursor()
    patient_list = []
    with connect:
        patient_list = cur.execute("SELECT * FROM patients WHERE right_eye_template=:right_eye_template", {'right_eye_template':right_eye_template}).fetchall()
    connect.close()
    return patient_list

def get_patient_by_surgery(surgery:str):
    '''
    Returns a list of patients by the surgery scheduled for the patient.
        Input:
            surgery: the surgery operated on the patient
        Output:
            jsonfile: list of patients found in json format

    '''
    connect = sqlite3.connect(DATABASE_NAME)
    cur = connect.cursor()
    patient_list = []
    with connect:
        patient_list = cur.execute("SELECT * FROM patients WHERE surgery=:surgery", {'surgery':surgery}).fetchall()
    connect.close()
    return json_format(patient_list)

def get_patient_count():
    '''
    Returns the total count of all patients in the database.
        Input:
            None
        Output:
            count (int): the total count of all patients in the database

    '''
    connect = sqlite3.connect(DATABASE_NAME)
    cur = connect.cursor()
    count = 0
    with connect:
        count = cur.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
    connect.close()
    return count

def get_all_patients():
    '''
    Returns a list of patients by id.
        Input:
            None
        Output:
            jsonfile: list of patients found in json format

    '''
    connect = sqlite3.connect(DATABASE_NAME)
    cur = connect.cursor()
    patient_list = []
    with connect:
        patient_list = cur.execute("SELECT * FROM patients").fetchall()
    connect.close()
    return json_format(patient_list)



def clear_all_patients():
    '''
    Remove all the patients in the database.
        Input:
            None
        Output:
            void

    '''
    connect = sqlite3.connect(DATABASE_NAME)
    cur = connect.cursor()
    with connect:
        cur.execute("DELETE FROM patients")
    connect.close()
    
def json_format(patients):
    '''
    Json-format the patient info.
        Input:
            patients (List): list of patients returned from a query.
        Output:
            jsonfile (json): list of patients in json format.

    '''
    if patients is None or len(patients) < 1:
        print("[EXCEPTION] no patient found.")
        return -1
    jsonfile = []
    for patient in patients:
        entry = {}
        for field in range(len(DATABASE_MODEL)):
            entry[DATABASE_MODEL[field]] = patient[field]
        jsonfile.append(entry)
    return json.dumps(jsonfile, indent=4)
    
### ------------------------------------------------------------------------------------
###                 CONSOLE
### ------------------------------------------------------------------------------------
if __name__=="__main__":
    print("MAIN")
    parser = argparse.ArgumentParser(description='List the content of a folder')
    parser.add_argument('--add',nargs=6, metavar='', type=str, 
        help='adds patient to database: --add [FIRSTNAME] [LASTNAME] [DOB] [LEFT-EYE] [RIGHT-EYE] [SURGERY]')
    parser.add_argument('--find',nargs="+", metavar='', type=str, 
        help='returns a list of patient(s) from database: --find [FIELD] [CONTENT] ||| [FIELD]: all, id, firstname, lastname, dob, lefteye, righteye, surgery.')
    parser.add_argument('--remove',nargs=2, metavar='', type=str,
        help='removes patient to database: --remove [FIELD] [CONTENT] ||| [FIELD]: id, firstname, lastname.')
    parser.add_argument('--count', action='store_true',
        help='returns a list of patients in database: --count')
    
    args = parser.parse_args()
    
    # print(args, sys.argv)
    if args.add:
        firstname = args.add[0]
        lastname = args.add[1]
        dob = args.add[2]
        left_eye_template = args.add[3]
        right_eye_template = args.add[4]
        surgery = args.add[4]
        add_patient(firstname, lastname, dob, left_eye_template, right_eye_template, surgery)
    elif args.find:
        field = args.find[0]
        if field == 'all':
            print(get_all_patients())
        else:
            content = args.find[1]
            fields = {
            "id": get_patient_by_id, 
            "firstname":get_patient_by_firstname, 
            "lastname": get_patient_by_lastname, 
            "dob": get_patient_by_DOB, 
            "lefteye": get_patient_by_left_eye_template, 
            "righteye": get_patient_by_right_eye_template, 
            "surgery": get_patient_by_surgery
                }
            
            if field not in fields:
                print("not valid field. Supported fields: ", fields.keys())
            else:
                if field == 'id':
                    content = int(content)
                print(fields[field](content))
    elif args.remove:
        print(args.remove)
    elif args.count:
        print(get_patient_count())
    else: 
        # do nothing
        pass


### ------------------------------------------------------------------------------------
###     TEST CASES

# print("all patients")
# add_patient("abby", "wysopal", "1/1/1990","left-eye-template", "right-eye-template", "iris surgery")
# add_patient("kiet", "nguyen", "4/3/1990","left-eye-template2", "right-eye-template2", "iris surgery2")
# add_patient("ryan", "mitchell", "1/2/1990","left-eye-template3", "right-eye-template3", "iris surgery3")
# add_patient("michael", "hau", "1/2/1990","left-eye-template4", "right-eye-template4", "iris surgery3")
# add_patient("brent", "luker", "1/2/1990","left-eye-template5", "right-eye-template5", "iris surgery2")

# print(get_patient_by_surgery("iris surgery2"))
# print(get_all_patients())
# print(remove_patient(6))
# print(get_all_patients())
# print(get_patient_count())
