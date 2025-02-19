import re
from datetime import datetime

# ... other code ...

if self.fields:
    # ... other code ...

    if self.fields:
        start_time_str = self.fields[0].get("clientTimestampStartTime")
        end_time_str = self.fields[0].get("clientTimestampEndTime")

        if start_time_str or end_time_str:
            mongo_query["required.clientTimestamp"] = {}  # Initialize for regex

            if start_time_str:
                start_time = datetime.fromisoformat(start_time_str)
                start_time_str_for_regex = start_time.strftime("%Y-%m-%dT%H:%M:%S")

                # Regex for >= start_time (inclusive)
                mongo_query["required.clientTimestamp"]["$gte"] = start_time_str_for_regex

            if end_time_str:
                end_time = datetime.fromisoformat(end_time_str)
                end_time_str_for_regex = end_time.strftime("%Y-%m-%dT%H:%M:%S")

                # Regex for <= end_time (inclusive)
                mongo_query["required.clientTimestamp"]["$lte"] = end_time_str_for_regex

            mongo_query["required.clientTimestamp"] = {
                "$gte": {"$regex": "^" + mongo_query["required.clientTimestamp"]["$gte"] + ".*"},
                "$lte": {"$regex": "^" + mongo_query["required.clientTimestamp"]["$lte"] + ".*"}
            }

        # ... other code ...
