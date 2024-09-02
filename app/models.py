from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

mongo = PyMongo()
bcrypt = Bcrypt()

class Admin:
    @staticmethod
    def create_admin(username, password):
        """Create a new admin with a hashed password."""
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        mongo.db.admins.insert_one({
            'username': username,
            'password': hashed_password
        })

    @staticmethod
    def verify_admin(username, password):
        """Verify an admin's username and password."""
        admin = mongo.db.admins.find_one({'username': username})
        if admin and bcrypt.check_password_hash(admin['password'], password):
            return True
        return False

    @staticmethod
    def get_admin_by_username(username):
        """Retrieve an admin's data by username."""
        return mongo.db.admins.find_one({'username': username})

class Volunteer:
    @staticmethod
    def add_volunteer(data):
        """Add a new volunteer to the database."""
        mongo.db.volunteers.insert_one(data)

    @staticmethod
    def get_volunteer_by_roll_number(roll_number):
        """Retrieve a volunteer's data by roll number."""
        return mongo.db.volunteers.find_one({'roll_number': roll_number})

    @staticmethod
    def update_volunteer_hours(roll_number, hours):
        """Update the number of volunteer hours for an existing volunteer."""
        mongo.db.volunteers.update_one(
            {'roll_number': roll_number},
            {'$inc': {'hours': hours}}
        )

    @staticmethod
    def get_all_volunteers():
        """Retrieve all volunteers from the database."""
        return list(mongo.db.volunteers.find())

class Event:
    @staticmethod
    def add_event(data):
        """Add a new event to the database."""
        mongo.db.events.insert_one(data)

    @staticmethod
    def get_event_by_id(event_id):
        """Retrieve an event's data by its ID."""
        return mongo.db.events.find_one({'event_id': event_id})

    @staticmethod
    def get_all_events():
        """Retrieve all events from the database."""
        return list(mongo.db.events.find())

def init_db(mongo):
    """Initialize the database with necessary indexes and setup."""
    # Create indexes for unique fields in the collections
    mongo.db.admins.create_index('username', unique=True)
    mongo.db.volunteers.create_index('roll_number', unique=True)
    mongo.db.events.create_index('event_id', unique=True)
    
    # Additional initialization can be done here