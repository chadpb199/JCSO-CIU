import argparse
from PIL import Image
from pathlib import Path
from pillow_heif import register_heif_opener
    
def heic_to_jpg(heic_dir, jpg_dir):
    # specifically convert the heic images in a certain directory to jpg
    
    #register HEIF opener with PIL
    register_heif_opener()
    
    # get the list of files to convert from the heic_dir
    heic_dir = Path(heic_dir)
    heics = [path for path in heic_dir.rglob("*.heic")]
            
    for path in heics:
        with Image.open(path) as im:
            print(f"Converting {path.name} to JPEG...")
            rgb_im = im.convert("RGB")
            # save the converted file to the destination directory or the same directory if none specified
            if jpg_dir != None:
            	rgb_im.save(Path(jpg_dir).parent / Path(str(path.stem) + ".jpg"), format="JPEG")
            else:
            	rgb_im.save(path.parent / Path(str(path.stem) + ".jpg"), format="JPEG")
            print("Done.")
    
    if input("Unlink .heic files? (Y/n)") == "Y":
        for path in heics:
            print(f"Unlinking {path.name}...")
            path.unlink()
            print("Done.")
    
    
if __name__ == "__main__":
    # get the target and destination dirs from args
    parser = argparse.ArgumentParser(
        prog="HEIC to JPG Converter")
    parser.add_argument("target")
    parser.add_argument("-d", "--destination")
    args = parser.parse_args()

    heic_to_jpg(heic_dir = args.target, jpg_dir=args.destination)