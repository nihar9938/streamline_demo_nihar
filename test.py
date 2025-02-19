from pymongo import MongoClient
from datetime import datetime

# ... (connection string and setup as before)

def fetch_data_by_date_interval(start_date_str, end_date_str, date_format="%Y-%m-%dT%H:%M:%S.%f%z"):
    """Fetches data within a date interval, handling timezone offsets."""
    try:
        start_date = datetime.strptime(start_date_str, date_format)
        end_date = datetime.strptime(end_date_str, date_format)

        # Construct MongoDB query
        mongo_query = {}
        if self.fields is not None:  # Use existing field filters if provided
            mongo_query.update(self.fields[0])  # Assuming self.fields is defined in the class
        mongo_query["required.appID"] = self.appId  # Always filter by appId

        # Add date range filter to the query
        mongo_query["required.clientTimestamp"] = {  # Assuming your date field is named "required.clientTimestamp"
            "$gte": {"$dateFromString": {"dateString": start_date_str, "format": date_format}},
            "$lte": {"$dateFromString": {"dateString": end_date_str, "format": date_format}}
        }

        self.mongo_docs = self.db.find(mongo_query)
        return list(self.mongo_docs)  # Convert cursor to list before returning

    except Exception as e:
        error = str(e)
        getLogger.logAPIMsg(error, 'ERROR')  # Assuming getLogger is defined
        return None



class GetLatestAuditAPIData():  # Assuming this is your class
    def __init__(self, appId, format, fields=None): # Added fields parameter
        # ... existing code ...
        self.fields = fields # Store fields parameter

    async def _validate_query_(self):
        try:
            # ... existing code ...

            if self.fields is None:
                self.mongo_docs = self.db.find({"required.appID": self.appId})
            elif self.fields is not None:
                mongo_query = {}
                mongo_query["required.appID"] = self.appId
                mongo_query.update(self.fields[0])
                self.mongo_docs = self.db.find(mongo_query)

            # ... existing code ...
        except Exception as e:
            # ... existing code ...

    def getData(self, start_date_str=None, end_date_str=None):  # Modified to accept date range
        try:
            if start_date_str and end_date_str:  # If date range is provided
                results = fetch_data_by_date_interval(start_date_str, end_date_str)
                if results is None:
                    return []  # Return empty list on error
                return results
            else:  # If no date range, use existing logic
                return list(self.mongo_docs)  # Convert cursor to list

        except Exception as e:
            error = str(e)
            getLogger.logAPIMsg(f"Exception occurred in getData: {error}", 'ERROR')
            return []  # Return empty list on error

# Example usage:
app_id = "your_app_id"
format = "json" # or whatever format you use
fields = [{"required.userID": "some_user_id"}] # Example filter

# Initialize the class with fields if needed
api_data_fetcher = GetLatestAuditAPIData(app_id, format, fields)

start_date_str = "2024-12-02T12:38:00.000-05:00"
end_date_str = "2024-12-02T12:47:30.000-05:00"

# Fetch data with date range
data_with_range = api_data_fetcher.getData(start_date_str, end_date_str)
print("Data with date range:", data_with_range)

# Fetch data without date range (using existing filters if provided)
data_without_range = api_data_fetcher.getData()
print("Data without date range:", data_without_range)

# Convert to Date type in MongoDB (if not already done)
# convert_to_date()  # Implement this function as shown in the previous response
