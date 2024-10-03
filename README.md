Some scripts and apps I have written to make my job easier.

For anyone who might be interested, the license applies to the entire repo.

CS Case Assignment Transfer contains several scripts intended to interact with
CentralSquare using the mouse and keyboard with pynput. I made this because
case assignments did not transfer from Omnigo. This script has already done
its job for me, so the .txt files would need to be updated with new cases if
it is needed in the future.

  - transfer.py is a script to assign cases to investigators.
    
  - tasks.py is a script to finish the investigative assignment tasks created
	after transfer.py is done.
    
  - fix.py is a script to fix the cases.txt file in case the transfer.py script
	is terminated prematurely.
    
  - cases.txt is the working file used by transfer.py to assign cases.
    
  - cases(copy).txt is the backup file containing the case numbers and
	investigator to be assigned.
    

Dupe Finder is a script that looks through a directory for duplicate files
excluding the file extensions, because Windows does not count files as
duplicates if they have different extensions. Allows user to choose which file
to delete, or neither.


Unzip is a small app that extracts a selected .ZIP archive to a selected
destination directory. I had to make this because SentinelOne doesn't play nice
with the Windows 11 File Explorer and broke the built-in Extract function. I
got awful sick of having to get into the PowerShell every time someone needed a
file extracted, and County IT doesn't like 7zip, apparently.
