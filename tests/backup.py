from typing import List
import sys
import os.path 
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from buph.scheduler import BackupType, BackupRequest
from buph.config import Config
from buph.drives import DestinationDrives
from buph.backup import backup, try_popen, rsync_help

if __name__ == '__main__':

    class TestBackup(unittest.TestCase):
        def test_popen(self):
            x = try_popen(["dir"], "c:\\")
            print(x)

        def test_rsync(self):
            rsync_help()

        def test_1(self):
            return
            config = Config()
            dest_drives = DestinationDrives()
            backup(config, dest_drives, BackupRequest(BackupType.CATALOGUED_IMAGE, 1, 0))
            backup(config, dest_drives, BackupRequest(BackupType.UNCATALOGUED_IMAGE, 0, 0))
            backup(config, dest_drives, BackupRequest(BackupType.CATALOG, 0, 0))
            pass

    unittest.main()