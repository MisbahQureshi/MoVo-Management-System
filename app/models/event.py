from app.extensions import mongo

class Event:
    @staticmethod
    def generate_event_id():
        """Generate a unique event ID in the format 'Evn001', 'Evn002', ..."""
        try:
            last_event = mongo.db.events.find_one(sort=[("event_id", -1)])
            if last_event and "event_id" in last_event:
                last_id_num = int(last_event["event_id"][3:])
                new_id_num = last_id_num + 1
            else:
                new_id_num = 1
            return f"Evn{new_id_num:03d}"
        except Exception as e:
            return None

    @staticmethod
    def create_event(name, description, start_date, end_date, volunteer_ids, employee_id):
        """Create a new event and insert it into the events collection."""
        event_id = Event.generate_event_id()
        if event_id:
            event_data = {
                'event_id': event_id,
                'name': name,
                'description': description,
                'start_date': start_date,
                'end_date': end_date,
                'volunteers': volunteer_ids,
                'employee_id': employee_id,  # Associate the logged-in user as the employee
                'tasks': []  # Initialize an empty list of tasks
            }
            try:
                mongo.db.events.insert_one(event_data)
                return event_data
            except Exception as e:
                return None
        return None
