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
        
        :param collections: A list of MongoDB collections (e.g., ['volunteers', 'events']).
        :param sheet_names: A list of sheet names to assign to each collection.
                            If None, it will use collection names.
        :return: Excel file ready for download.
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
        
        :param collection_name: The MongoDB collection where data should be inserted.
        :return: None
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
        
        # Required fields
        required_fields = [
            "volunteer_id", "name", "email",
            "student_id", "phone", "volunteer_hours",
            "status", "event_id", "schedule", "awards_id"
        ]
        
        # Validate fields
        missing_fields = [field for field in required_fields if field not in df.columns]
        if missing_fields:
            flash(f"Missing required fields: {', '.join(missing_fields)}")
            return None
        
        # Data Transformation
        def transform_field(field, default):
            try:
                return json.loads(field) if isinstance(field, str) else field
            except json.JSONDecodeError:
                return default
        
        for field in ["event_id", "schedule", "awards_id"]:
            df[field] = df[field].apply(lambda x: transform_field(x, []))
        
        # Clean unnecessary fields
        df = df[required_fields]
        
        try:
            data_dict = df.to_dict(orient='records')
            if data_dict:
                mongo.db[collection_name].insert_many(data_dict)
                flash(f"Data successfully imported to {collection_name} collection!")
            else:
                flash('No data to import!')
        except Exception as e:
            flash(f"Error inserting data: {str(e)}")