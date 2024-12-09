import pandas as pd
from io import BytesIO
from app.extensions import mongo
from flask import send_file, request, flash
import json

class ExcelHandler:
    
    @staticmethod
    def export_to_excel(collections, sheet_names=None):
        """
        Export one or multiple collections from MongoDB to an Excel file.
        """
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for idx, collection_name in enumerate(collections):
                data = list(mongo.db[collection_name].find())
                if not data:
                    continue
                df = pd.DataFrame(data)
                sheet_name = sheet_names[idx] if sheet_names else collection_name
                df.to_excel(writer, index=False, sheet_name=sheet_name)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name="exported_data.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    @staticmethod
    def import_from_excel(collection_name):
        """
        Import data from an uploaded Excel file into a MongoDB collection.
        """
        if 'file' not in request.files:
            flash('No file part')
            return None
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return None
        
        try:
            df = pd.read_excel(file)
        except Exception as e:
            flash(f"Error reading Excel file: {str(e)}")
            return None

        # Define collection-specific required fields and transformations
        collection_schemas = {
            "volunteers": {
                "required_fields": [
                    "volunteer_id", "name", "email",
                    "student_id", "phone", "volunteer_hours",
                    "status", "event_id", "schedule", "awards_id"
                ],
                "nested_fields": ["event_id", "schedule", "awards_id"]
            },
            "tasks": {
                "required_fields": [
                    "task_id", "name", "description",
                    "date", "event_id", "volunteer_ids"
                ],
                "nested_fields": ["volunteer_ids"]
            },
            "events": {
                "required_fields": [
                    "event_id", "date", "description",
                    "name", "volunteer_id", "employee_id",
                    "start_date", "end_date"
                ],
                "nested_fields": ["volunteer_id"]
            }
        }
        
        schema = collection_schemas.get(collection_name)
        if not schema:
            flash(f"Unsupported collection: {collection_name}")
            return None

        # Validate fields
        missing_fields = [field for field in schema["required_fields"] if field not in df.columns]
        if missing_fields:
            flash(f"Missing required fields: {', '.join(missing_fields)}")
            return None

        # Data Transformation
        def transform_field(field, default):
            try:
                return json.loads(field) if isinstance(field, str) else field
            except json.JSONDecodeError:
                return default
        
        for field in schema["nested_fields"]:
            df[field] = df[field].apply(lambda x: transform_field(x, []))
        
        # Clean unnecessary fields
        df = df[schema["required_fields"]]
        
        try:
            data_dict = df.to_dict(orient='records')
            if data_dict:
                mongo.db[collection_name].insert_many(data_dict)
                flash(f"Data successfully imported to {collection_name} collection!")
            else:
                flash('No data to import!')
        except Exception as e:
            flash(f"Error inserting data: {str(e)}")
