import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://attendancedb-9c94f-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')
data = {
    "810":
        {
            "name": "Lionel Messi",
            "major": "Aerodynamics",
            "starting_year": 2010,
            "total_attendance": 843,
            "standing": "A+",
            "year": 5,
            "last_attendance_time": "2024-10-02 00:54:34"
        },
    "811":
        {
            "name": "Sunil Chhetri",
            "major": "aerospace",
            "starting_year": 2011,
            "total_attendance": 258,
            "standing": "A",
            "year": 3,
            "last_attendance_time": "2024-10-02 00:54:34"
        },
    "815":
        {
            "name": "Neymar Jr.",
            "major": "qantum",
            "starting_year": 2010,
            "total_attendance": 400,
            "standing": "A",
            "year": 4,
            "last_attendance_time": "2024-10-02 00:54:34"
        },
    "809":
        {
            "name": "sudhanshu sharma",
            "major": "Computer science",
            "starting_year": 2021,
            "total_attendance": 210,
            "standing": "A",
            "year": 4,
            "last_attendance_time": "2024-10-02 00:54:34"
        },
}

for key,value in data.items():
    ref.child(key).set(value)