import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('/home/amr/catkin_ws/src/turtlebot3/turtlebot3_navigation/scripts/pos-app-for-service-robot-firebase-adminsdk-7et03-c7457f5dcb.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pos-app-for-service-robot-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('table')
users_ref = ref.child('Home')
print(users_ref.get()["isActivated"])

