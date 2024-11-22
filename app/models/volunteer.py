from bson import ObjectId
from app.extensions import mongo

class Volunteer:
    def __init__(self, volunteer_id, first_name, last_name, email, student_id, contact_number, volunteer_hours=0, status='active', event_id=None, schedule=None, awards_id=None):
        self.volunteer_id = volunteer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.student_id = student_id
        self.contact_number = contact_number
        self.volunteer_hours = volunteer_hours
        self.status = status
        self.event_id = event_id if event_id else []  # Default to empty list if not provided
        self.schedule = schedule if schedule else []  # Default to empty list if not provided
        self.awards_id = awards_id if awards_id else []  # Default to empty list if not provided

    @classmethod
    def find_all(cls):
        """Retrieve all volunteers."""
        return mongo.db.volunteers.find()

    @classmethod
    def find_by_id(cls, volunteer_id):
        """Find a volunteer by their volunteer_id."""
        return mongo.db.volunteers.find_one({'volunteer_id': volunteer_id})

    @classmethod
    def find_by_object_id(cls, object_id):
        """Find a volunteer by their MongoDB ObjectId."""
        return mongo.db.volunteers.find_one({'_id': ObjectId(object_id)})

    @classmethod
    def create_volunteer(cls, volunteer_data):
        """Create a new volunteer in the database."""
        volunteer = {
            'volunteer_id': volunteer_data['volunteer_id'],
            'first_name': volunteer_data['first_name'],
            'last_name': volunteer_data['last_name'],
            'email': volunteer_data['email'],
            'student_id': volunteer_data['student_id'],
            'contact_number': volunteer_data['contact_number'],
            'volunteer_hours': volunteer_data.get('volunteer_hours', 0),
            'status': volunteer_data.get('status', 'active'),
            'event_id': volunteer_data.get('event_id', []),
            'schedule': volunteer_data.get('schedule', []),
            'awards_id': volunteer_data.get('awards_id', [])
        }
        try:
            mongo.db.volunteers.insert_one(volunteer)
            return volunteer
        except Exception as e:
            return None

    @classmethod
    def update_volunteer(cls, volunteer_id, update_data):
        """Update volunteer details."""
        try:
            mongo.db.volunteers.update_one(
                {'volunteer_id': volunteer_id},
                {'$set': update_data}
            )
            return True
        except Exception as e:
            return False

    @classmethod
    def delete_volunteer(cls, volunteer_id):
        """Delete a volunteer."""
        try:
            mongo.db.volunteers.delete_one({'volunteer_id': volunteer_id})
            return True
        except Exception as e:
            return False
