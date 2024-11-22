import pandas as pd
from io import BytesIO
from app.extensions import mongo
from flask import send_file, request, flash
import os

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
        # Create a Pandas Excel writer using Openpyxl
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for idx, collection_name in enumerate(collections):
                # Fetch data from the MongoDB collection
                data = list(mongo.db[collection_name].find())
                
                # If data is empty, skip it
                if not data:
                    continue
                
                # Convert MongoDB data (which is a list of dicts) to a DataFrame
                df = pd.DataFrame(data)
                
                # Set the sheet name, default to collection name if sheet_names is None
                sheet_name = sheet_names[idx] if sheet_names else collection_name
                
                # Write the dataframe to the sheet
                df.to_excel(writer, index=False, sheet_name=sheet_name)
        
        # Save and get the Excel file
        output.seek(0)
        return send_file(output, as_attachment=True, download_name="exported_data.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    @staticmethod
    def import_from_excel(collection_name):
        """
        Import data from an uploaded Excel file into a MongoDB collection.
        
        :param collection_name: The MongoDB collection where data should be inserted.
        :return: None
        """
        # Check if the file is in the request
        if 'file' not in request.files:
            flash('No file part')
            return None
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return None
        
        # Read the Excel file into a pandas DataFrame
        try:
            df = pd.read_excel(file)
        except Exception as e:
            flash(f"Error reading Excel file: {str(e)}")
            return None
        
        # Insert data into the MongoDB collection
        try:
            # Convert DataFrame to a dictionary (to insert into MongoDB)
            data_dict = df.to_dict(orient='records')
            if data_dict:
                mongo.db[collection_name].insert_many(data_dict)
                flash(f"Data successfully imported to {collection_name} collection!")
            else:
                flash('No data to import!')
        except Exception as e:
            flash(f"Error inserting data: {str(e)}")
