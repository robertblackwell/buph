import typing
import subprocess 
import pathlib 
import os.path 
from datetime import datetime
import math
from buph.config import Config
from buph.drives import DestinationDrives

# class DestinationDrives:
#     def __init__(self):
#         self.drive_names = "BUP_PHOTO", "LR_DUP", "Photographs"
#         self.available_destination_drives = {}
#         self._discover_available_drives()

#     # def nbr_candidates_drives(self):
#     #     return len(self.drive_names)

#     def nbr_available_drives(self):
#         return len(self.available_destination_drives)


#     def _discover_available_drives(self):
#         for d in ["E:", "F:", "G:", "H:"]:
#             dn = getDriveName(d)
#             if dn is not None:
#                 self.available_destination_drives[dn] = d 

#     def drive_letter_for_volume(self, volname):
#         if volname in self.available_destination_drives:
#             return self.available_destination_drives[volname]
#         else:
#             return None

#     def drive_letter_for_index(self, index):
#         return self.drive_letter_for_volume(self.drive_names[index])

#     def drive_index(self, vol_name):
#         i = 0
#         for n in self.drive_names:
#             if n == vol_name:
#                 return i
#             i += 1
#         return None

#     # determines if a given destination drive is available
#     def is_drive_index_available(self, dest_number):
#         dest_volume_name = self.drive_names[dest_number]
#         flag = dest_volume_name in self.available_destination_drives is not None
#         return flag



# # gets the volume name from a drive letter
# # dont pass in C:
# # returns None if no drive has the passed in letter
# def getDriveName(driveletter):
#     child = subprocess.Popen(["cmd","/c vol "+driveletter], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     raw_bytes = child.communicate()
#     rc = child.returncode
#     if rc == 0:
#         vol_name = str(raw_bytes[0], "utf-8").split("\r\n")[0].split(" ").pop()
#     else:
#         vol_name = None
#     return vol_name
