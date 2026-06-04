import json
import csv
import os
import argparse

parser = argparse.ArgumentParser(
    prog="JSON to CSV Converter",
    description="""
        A local script to convert .json files into .csv files,
        written to be more CJIS compliant than just plugging files obtained
        from search warrants into online conversion software.
        """,
    epilog="DET. C. BYOUS #51/0475")
    
parser.add_argument("json_path", help="target .json filepath")
parser.add_argument("csv_path", help="destination .csv filepath") 

def json_to_csv(json_path, csv_path):
    with open(json_path, "r", encoding="utf-8") as jf:
        data = json.load(jf)
        print(type(data))
        print(data.keys())
        
        with open(csv_path, "w", newline="") as cf:
            writer = csv.writer(cf)
            
            headers = data.keys()
            
            writer.writerow(headers)
            
            for item in data.items():
                writer.writerow(item.values())
                
if __name__=="__main__":
    args = parser.parse_args()
    json_to_csv(args.json_path, args.csv_path)