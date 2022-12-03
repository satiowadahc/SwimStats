"""
Records.py

   Data collection of swimming stats

   Written by Chad A. Woitas AKA satiowadahc
   June 22, 2022

"""
import os.path
from typing import Optional, Dict


class SwimRecords:

    def __init__(self):

        self.data: Optional[Dict] = {}

    def load_config(self, file):
        """Load configuration and set up data records"""

        if not os.path.exists(file):
            return None

        try:
            with open(file, 'r') as f:

                # Read <Result .... />
                for line in f.readlines():

                    if "<Result " not in line:
                        continue
                    line = line.split(" ")
                    line = list(filter(None, line))
                    record = {"value": None, "last_update": None}
                    offset = ""

                    # Read field="data"
                    for item in line:
                        if "=" not in item:
                            continue
                        i = item.split("=")
                        i[1] = i[1].strip("\"")
                        record[i[0]] = i[1]
                        if "offset" in i[0]:
                            offset = i[1]
                    if "sampleData" in record.keys():
                        record["value"] = record["sampleData"]
                    self.data[offset] = record

        except Exception as E:
            print(E)
        #
        # for key in self.data:
        #     print(key, self.data[key])


if __name__ == '__main__':
    testrecord = SwimRecords()

    testrecord.load_config("OS2-Swimming.txt")
