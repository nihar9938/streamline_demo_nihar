import re
from datetime import datetime

# ... other code ...

if self.fields:
    # ... other code ...

    if self.fields:
        start_time_str = self.fields[0].get("clientTimestampStartTime")
        end_time_str = self.fields[0].get("clientTimestampEndTime")

        if start_time_str or end_time_str:
            timestamp_regex = {}

            if start_time_str:
                start_time = datetime.fromisoformat(start_time_str)
                start_time_str_for_regex = start_time.strftime("%Y-%m-%dT%H:%M:%S")  # Format for regex
                timestamp_regex["$gte"] = start_time_str_for_regex  # Greater than or equal to string

            if end_time_str:
                end_time = datetime.fromisoformat(end_time_str)
                end_time_str_for_regex = end_time.strftime("%Y-%m-%dT%H:%M:%S")    # Format for regex
                timestamp_regex["$lte"] = end_time_str_for_regex  # Less than or equal to string

            mongo_query["required.clientTimestamp"] = {"$regex": "^" + timestamp_regex["$gte"] + ".*", "$regex": "^" + timestamp_regex["$lte"] + ".*"}

        # ... other code ...
