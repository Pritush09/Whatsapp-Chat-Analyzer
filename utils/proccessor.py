
import re
import pandas as pd
from typing import List
from datetime import datetime

import re
import pandas as pd
from typing import List
from datetime import datetime

class PreprocessTxTFile:
    # Supports both 12hr and 24hr timestamps with sender
    pattern = r"^(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}(?:\s?[APMapm]{2})?) - ([^:]+): (.*)"
    
    # Matches system messages with no sender
    system_pattern = r"^\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}(?:\s?[APMapm]{2})? - (?!.*:).*"

    def __init__(self, text_file):
        self.textfile = text_file

    def get_all_msgs(self):
        messages = []
        current_message = ""

        for line in self.textfile:
            if re.match(self.system_pattern, line):
                continue  # Skip system messages
            
            if re.match(self.pattern, line):
                if current_message:
                    messages.append(current_message.strip())
                current_message = line
            else:
                current_message += line

        if current_message:
            messages.append(current_message.strip())

        return messages

    def convert_to_df(self, messages: List) -> pd.DataFrame:
        data = []
        for msg in messages:
            match = re.match(self.pattern, msg)
            if match:
                date_str, time_str, sender, message = match.groups()
                # Try parsing both 12-hour and 24-hour formats
                for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y %I:%M %p", "%m/%d/%y %H:%M", "%m/%d/%y %I:%M %p"):
                    try:
                        timestamp = datetime.strptime(f"{date_str} {time_str}", fmt)
                        break
                    except ValueError:
                        continue
                else:
                    continue  # Skip unparseable lines

                data.append({
                    "datetime": timestamp,
                    "User": sender.strip(),
                    "message": message.strip()
                })

        df = pd.DataFrame(data)
        if df.empty:
            return df

        # Enrich with date/time components
        df['Year'] = df['datetime'].dt.year
        df['month'] = df['datetime'].dt.month_name()
        df['day'] = df['datetime'].dt.day
        df['day_name'] = df['datetime'].dt.day_name()
        df['hour'] = df['datetime'].dt.hour
        df['minutes'] = df['datetime'].dt.minute
        df['month_num'] = df['datetime'].dt.month
        df["only_date"] = df["datetime"].dt.date

        df = df[df.message != "<Media omitted>"]

        return df

    def preprocess(self):
        msgs = self.get_all_msgs()
        # You can uncomment for debugging:
        # print(msgs[:5])
        return self.convert_to_df(msgs)
