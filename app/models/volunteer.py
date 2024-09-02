from bson import ObjectId
from app.extensions import mongo

class Volunteer:
    def __init__(self, first_name, last_name, email, student_id, contact_number):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.student_id = student_id
        self.contact_number = contact_number
        self.volunteer_hours = 0

    @classmethod
    def find_all(cls):
        return mongo.db.volunteers.find()

    @classmethod
    def find_by_id(cls, volunteer_id):
        return mongo.db.volunteers.find_one({'_id': ObjectId(volunteer_id)})
