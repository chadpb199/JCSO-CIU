import argparse
from PIL import Image
from pathlib import Path
    
def cr2_to_jpg(cr2_dir, jpg_dir):
    # specifically convert the images in a certain directory to jpg
    
    # get the list of files to convert from the cr2_dir
    cr2_dir = Path(cr2_dir)
    cr2s = [path for path in cr2_dir.rglob("*.CR2")]
            
    for path in cr2s:
        with Image.open(path) as im:
            print(f"Converting {path.name} to JPEG...")
            rgb_im = im.convert("RGB")
            # save the converted file to the destination directory or the same directory if none specified
            if jpg_dir != None:
            	rgb_im.save(Path(jpg_dir).parent / Path(str(path.stem) + ".jpg"), format="JPEG")
            else:
            	rgb_im.save(path.parent / Path(str(path.stem) + ".jpg"), format="JPEG")
            print("Done.")
    
    if input("Unlink .CR2 files? (Y/n)") == "Y":
        for path in cr2s:
            print(f"Unlinking {path.name}...")
            path.unlink()
            print("Done.")
    
    
if __name__ == "__main__":
    # get the target and destination dirs from args
    parser = argparse.ArgumentParser(
        prog="CR2 to JPG Converter")
    parser.add_argument("target")
    parser.add_argument("-d", "--destination")
    args = parser.parse_args()

    cr2_to_jpg(cr2_dir = args.target, jpg_dir=args.destination)