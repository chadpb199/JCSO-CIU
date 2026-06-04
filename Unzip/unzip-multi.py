import zipfile
import os

dir = "C:\\Users\\cbyous\\OneDrive - Jackson County Missouri\\Downloads\\26-01192 FLOCK"

if __name__ == "__main__":
    zips = [os.path.join(dir, zip) for zip in os.listdir(path=dir)]
    
    for zip in zips:
        print(f"Extracting {zip}...")
        with zipfile.ZipFile(zip) as f:
            f.extractall(path="C:\\Users\\cbyous\\OneDrive - Jackson County Missouri\\Downloads\\26-01192 FLOCK")