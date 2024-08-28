import os

def find_duplicate_files(directory):
    files_seen = {}
    found_dupe = False
    print("\nSearching directory for duplicate files.")

    for file in os.listdir(directory):

        file_name_without_extension = os.path.splitext(file)[0]

        if file_name_without_extension in files_seen:
            found_dupe = True
            dupe_file = files_seen[file_name_without_extension]

            print(f"""Duplicate found: File A "{file}" and File B "{dupe_file}" """)

            file_to_remove = input("Select file to remove (A, B, or IGNORE): ").upper()

            if file_to_remove == "A":
                os.remove(os.path.join(directory, file))
                print(f"{file} was removed.")

            elif file_to_remove == "B":
                os.remove(os.path.join(directory, dupe_file))
                print(f"{dupe_file} was removed.")

            elif file_to_remove == "IGNORE":
                print("Neither file was removed.")
                continue

        else:
            files_seen[file_name_without_extension] = file
            print(".")

    if found_dupe:
        print("Search complete.\n")
    else:
        print("No duplicate files located.\n")

find_duplicate_files(input("Enter file directory to search for duplicate files: "))
