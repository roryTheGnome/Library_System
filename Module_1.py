import re
import json
import pandas as pd

from pathlib import Path

#i was going to use plain open and change the config file but then i found this:
# https://www.w3schools.com/python/python_file_open.asp
#so i did some experiment and i guess it worked, yey me!
with open("example_basic_config.json", "r") as f:
    figs = json.load(f)

checker = [re.compile(p) for p in figs["acceptable_formats"]]

data = Path("data")

combinedData = []

for file in data.iterdir():

    if not file.is_file():
        continue
#all the print statetments below are not needed in my project but i use them in case of an bug so im gonna keep them till submit
    if any(p.fullmatch(file.name) for p in checker):
        print(f"Valid file found: {file.name}")
        try:

            if file.suffix == ".xlsx":

                df = pd.read_excel(file)

            elif file.suffix == ".csv":

                df = pd.read_csv(file)

            else:

                print("Only .xlsx and csv")
                continue

            print("Yey")

            #df.to_excel("my_data.xlsx")

            combinedData.append(df)

        except Exception as e:
            print(f"Error here {file.name}: {e}")

    else:
        print(f"Deleting: {file.name}")
        file.unlink()

if combinedData:

    result=pd.concat(combinedData, ignore_index=True)
    result.to_excel("my_data.xlsx")

    print("Added succesfully")

else:

    print("Nothing to see here")


"""
Installs I had for this module:
pip install pandas
pip install openpyxl
"""