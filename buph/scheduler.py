import typing
import subprocess 
import pathlib 
import os.path 
from datetime import datetime
import math
import unittest
from enum import IntEnum
from buph.config import Config
from buph.drives import DestinationDrives 

# returns the number of today in the year
def day_of_year() -> int:
    return datetime.now().timetuple().tm_yday  # returns 1 for January 1st

class BackupType(IntEnum):
    CATALOGUED_IMAGE = 0
    UNCATALOGUED_IMAGE = 1
    CATALOG = 2

class BackupRequest:
    def __init__(self, butype, tranche, drive_index):
        self.type = butype
        self.tranche_index = tranche
        self.destination_drive_index = drive_index 

class Scheduler:
    def __init__(self, config: Config, destination_drives: DestinationDrives):
        self.config = config
        self.destination_drives = destination_drives
    
    # determines how many distinct backup runs there should be - a run is a (tranche, a single destination)
    def _number_of_backup_runs(self):
        runs_count = self.config.number_tranches_catalogued_photos() \
            + self.config.number_tranches_uncatalogued_photos() \
            + self.config.number_tranches_catalogues()
        return runs_count * self.destination_drives.nbr_available_drives()

    # which run number should we execute today
    def _todays_run_number(self):
        res = day_of_year() % self._number_of_backup_runs()
        return res


    # determine the tranche set, tranche and destination for a daynumber
    def _tranche_set_tranche_and_destination_for_a_daynumber(self, day_number):
        nbr = self._number_of_backup_runs()
        run_number = day_number % self._number_of_backup_runs()
        dest_number = run_number % self.destination_drives.nbr_available_drives()
        tmp = math.floor(run_number / self.destination_drives.nbr_available_drives())
        
        if tmp < self.config.number_tranches_catalogued_photos():
            result = (0, tmp, dest_number)
        elif tmp < self.config.number_tranches_catalogued_photos() + self.config.number_tranches_uncatalogued_photos():
            result = (1, tmp - self.config.number_tranches_catalogued_photos(), dest_number)
        else:
            result = (2, tmp - self.config.number_tranches_catalogued_photos() - self.config.number_tranches_uncatalogued_photos(), dest_number)
        return result
        ts, t, d = result
        while not self.destination_drives.is_drive_index_available(d):
            print("d is %d" % (d))
            d = (d + 1) % self.destination_drives.nbr_available_drives()
        return (ts, t, d)

    def backup_request_for_daynumber(self, daynumber):
        ts, t, d = self._tranche_set_tranche_and_destination_for_a_daynumber(daynumber)
        return BackupRequest(BackupType(ts), t, d)

    def backup_request_for_today(self):
        return self.backup_request_for_daynumber(day_of_year())

if __name__ == '__main__':

    class TestScheduler(unittest.TestCase):
        def test_enum(self):
            typ = BackupType(1)
            self.assertEqual(typ, BackupType.UNCATALOGUED_IMAGE)

        def test_request(self):
            req = BackupRequest(BackupType.CATALOGUED_IMAGE, 2, 1)
            self.assertEqual(req.type, BackupType.CATALOGUED_IMAGE)
            self.assertEqual(req.tranche_index, 2)
            self.assertEqual(req.destination_drive_index, 1)

        def test_create(self):
            config = Config()
            destination_drives = DestinationDrives()
            scheduler = Scheduler(config, destination_drives)
            self.assertNotEqual(scheduler, None)
            x = scheduler._number_of_backup_runs()
            for i in range(10):
                req0 = scheduler.backup_request_for_daynumber(i)
                print(req0.type, req0.tranche_index, req0.destination_drive_index)
    
        def test_schedule(self):
            pass

    unittest.main()