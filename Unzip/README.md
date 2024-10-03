This is a small application to allow Detectives to extract .ZIP archives
without me having to come over to their workstations and use the Windows
PowerShell to do it.

For some reason, the Windows 11 File Explorer fails to extract .ZIP archives on
the Detectives' workstations. I haven't tried it on any other workstations in
the office. All it does is create the destination directory (if it didn't exist
already).

Apparently, based on my online research, SentinelOne doesn't play nice with the
Windows 11 File Explorer for some as yet unknown reason. I had initially
figured out that enabling the "Launch folder windows in separate processes"
option in the Folder options fixed the problem, but then County IT came in and
pushed a policy update to SentinelOne, thinking that would fix the issue. All
it did was break my original fix.

SentinelOne is apparently aware of the issue, but they do not have an ETA on a
fix as of this time.

This really shouldn't even be necessary. 7zip apparently works great still on
machines using SentinelOne. Unfortunately, County IT has blocked 7zip. When I
asked about it, I was told that 7zip isn't really necessary or used anymore.

If anyone else wants to use this for whatever reason, here you go.