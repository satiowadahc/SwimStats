"""
Records.py

   Data collection of swimming stats

   Written by Chad A. Woitas AKA satiowadahc
   June 22, 2022

"""
import os.path
from typing import Optional, Dict


class SwimRecords:
    """
    Data Map for Daktronics RTD information
    """

    def __init__(self):

        self.data: Optional[Dict] = {}

    def load_config(self, file: str) -> None:
        """
        Load configuration and set up data records
        :param file: Path to file
        """

        if not os.path.exists(file):
            return

        try:
            with open(file, 'r', encoding="utf8") as map_file:

                # Read <Result .... />
                for line in map_file.readlines():

                    if "<Result " not in line:
                        continue
                    line = line.split(" ")
                    line = list(filter(None, line))
                    _record = {"value": None, "last_update": None}
                    offset = ""

                    # Read field="data"
                    for item in line:
                        if "=" not in item:
                            continue
                        i = item.split("=")
                        i[1] = i[1].strip("\"")
                        _record[i[0]] = i[1]
                        if "offset" in i[0]:
                            offset = i[1]
                    if "sampleData" in _record:
                        _record["value"] = _record["sampleData"]
                    self.data[offset] = _record

        except FileNotFoundError as file_error:
            print(f"Error in opening file: {file_error}")
        #
        # for key in self.data:
        #     print(key, self.data[key])

    def get_index(self, index: str):
        """
        Return the record at the given index
        :index: Record index to grab
        """
        if index in self.data:
            return self.data[index]
        raise ValueError(f"Data index not found {index}")


if __name__ == '__main__':
    testrecord = SwimRecords()

    testrecord.load_config("OS2-Swimming.txt")

    for record, value in testrecord.data.items():
        print(f"{record}: {value['value']}")

    print(testrecord.get_index(0))
