import typing
import subprocess 
import pathlib 
import os.path 
from datetime import datetime
import math
import unittest
from buph.scheduler import BackupType, BackupRequest
from buph.config import Config
from buph.drives import DestinationDrives

def rsync_cmd(opts, from_path, to_path):
    cmd = "rsync %s %s %s" % (opts, from_path, to_path)
    return cmd

def bu_catalogued_photos(tranche, source_dir_path, destination_dir):
    for t in tranche:
        src = os.path.join(source_dir_path, t)
        print("bu_catalogued_photos       ", rsync_cmd("-arvc", src, destination_dir))

def bu_uncatalogued_photos(tranche, source_dir_path, destination_dir):
    for t in tranche:
        src = os.path.join(source_dir_path, t)
        print("bu_uncatalogued_photos     ", rsync_cmd("-arvc", src, destination_dir))

def bu_catalogs(tranche, source_dir_path, destination_dir):
    for t in tranche:
        src = os.path.join(source_dir_path, t)
        print("bu_catalogs                ", rsync_cmd("-arvc", src, destination_dir))

def backup(config: Config, destination_drives: DestinationDrives, request: BackupRequest):

    bu_for_set = [
        bu_catalogued_photos,
        bu_uncatalogued_photos,
        bu_catalogs
    ]
    source_dir = [
        config.cataloged_photos_source_dir(),
        config.uncatalogued_photos_source_dir(),
        config.catalog_source_dir()
    ]
    destination_dir_funcs = [
        config.cataloged_photos_destination_dir,
        config.uncatalogued_photos_destination_dir,
        config.catalog_destination_dir
    ]
    s = int(request.type)
    f = bu_for_set[s]
    tranche = config.tranche_sets[s][request.tranche_index]
    src_dir = source_dir[s]
    dest_drive_letter =  destination_drives.drive_letter_for_index(request.destination_drive_index)
    dest_dir = destination_dir_funcs[s](dest_drive_letter)
    if not os.path.isdir(src_dir):
        raise Exception("%s is not a directory" % (src_dir))
    if not os.path.isdir(dest_dir):
        raise Exception("%s is not a directory" % (dest_dir))
    # src_drive, src_path = os.path.splitdrive(src_dir)
    # dest_dir = os.path.join(dest_drive_letter, src_path)
    # 
    # these functions perform rsync src_dir/tranch[i]  dest_dir
    # 
    f(tranche, src_dir, dest_dir)

if __name__ == '__main__':

    class TestBackup(unittest.TestCase):
        def test_1(self):
            config = Config()
            dest_drives = DestinationDrives()
            backup(config, dest_drives, BackupRequest(BackupType.CATALOGUED_IMAGE, 1, 0))
            backup(config, dest_drives, BackupRequest(BackupType.UNCATALOGUED_IMAGE, 0, 0))
            backup(config, dest_drives, BackupRequest(BackupType.CATALOG, 0, 0))
            pass

    unittest.main()