import firebase_admin
from firebase_admin import credentials
from firebase_admin import db   # help to read write and manupulate the database

cred = credentials.Certificate("serviceAccountKey.json")   # generated key
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendencerealtime-44886-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "10714":
        {
            "name": "Sourabh kumar Mishra",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 60,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2023-05-10 00:54:34"
        },
    "10663":
        {
            "name": "Divya sharma",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 50,
            "standing": "B",
            "year": 2,
            "last_attendance_time": "2023-05-10 00:54:34"
        },
    "10667":
        {
            "name": "Ashish Thakur",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 40,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2023-05-10 00:54:34"
        }
}

# our uid is key and details are value
for key, value in data.items():
    ref.child(key).set(value)   # when u want to send data in specific director then u have to write child