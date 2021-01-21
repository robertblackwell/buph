from typing import List
import subprocess 
from pathlib import WindowsPath 
import os.path 
from datetime import datetime
import math
import unittest
from buph.logger import buph_logger
from buph.scheduler import BackupType, BackupRequest
from buph.config import Config
from buph.drives import DestinationDrives
import buph.cygwin_rsync as cygwin

rsync_options = "-archW"
cygwin_bash = 'c:\\cygwin64\\bin\\bash'
cygwin_rsync = 'c:\\cygwin64\\home\\lightroom\\projects\\backup-photos\\rsync_run.sh'

class BackupOptions:
    def __init__(self):
        self.dryrun = False
        self.quiet = False

def try_popen(cmd: List[str], where: str) -> int:
    child = subprocess.Popen(cmd, cwd=where, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, encoding="utf-8")
    # stdout, stderr = child.communicate()

    while True:
        output = child.stdout.readline()
        if output == '' and child.poll() is not None:
            break
        if output:
            buph_logger.info(output.strip())
    rc = child.poll()
    return rc

def rsync_help():
    cmd_list = [cygwin_bash, "-l", cygwin_rsync, "-h"]
    buph_logger.info("rsync -h       %s" %(" ".join(cmd_list)))
    if try_popen(cmd_list, "c:\\Users\\lightroom") != 0:
        raise Exception("try_popen returns rc != 0")


def rsync_cmd(opts, from_path, to_path):
    cmd = "rsync %s %s %s" % (opts, from_path, to_path)
    return cmd

def backup_options_to_rsync_options(backup_options: BackupOptions) -> List[str]:
    opts = []
    if backup_options.dryrun: opts.append("--dry-run")
    if backup_options.quiet: 
        opts.append("--quiet")
    else:
        opts.append("-v")
    return opts

def bu_catalogued_photos(
    tranche, 
    source_dir_path: WindowsPath, 
    destination_dir: WindowsPath, 
    backup_options: BackupOptions
):
    for t in tranche:
        src = WindowsPath(source_dir_path, t)
        options_list = ["-archW"] + backup_options_to_rsync_options(backup_options)
        home = WindowsPath.home()
        cmd_list = cygwin.rsync_cmd(options_list, home, src, destination_dir)
        buph_logger.info("bu_catalogued_photos       %s" %(" ".join(cmd_list)))
        if try_popen(cmd_list, str(WindowsPath.home())) != 0:
            raise Exception("try_popen returns rc != 0")

def bu_uncatalogued_photos(
    tranche, 
    source_dir_path: WindowsPath, 
    destination_dir: WindowsPath, 
    backup_options: BackupOptions
):
    for t in tranche:
        src = WindowsPath(source_dir_path, t)
        options_list = ["-archW"] + backup_options_to_rsync_options(backup_options)
        home = WindowsPath.home()
        cmd_list = cygwin.rsync_cmd(options_list, home, src, destination_dir)
        buph_logger.info("bu_catalogued_photos       %s" %(" ".join(cmd_list)))
        if try_popen(cmd_list, str(WindowsPath.home())) != 0:
            raise Exception("try_popen returns rc != 0")

def bu_catalogs(
    tranche, 
    source_dir_path: WindowsPath, 
    destination_dir: WindowsPath, 
    backup_options: BackupOptions
):
    for t in tranche:
        src = WindowsPath(source_dir_path, t)
        options_list = ["-archW", "--exclude", "Backups", "--exclude", '*Previews.lrdata'] + backup_options_to_rsync_options(backup_options)
        home = WindowsPath.home()
        cmd_list = cygwin.rsync_cmd(options_list, home, src, destination_dir)
        buph_logger.info("bu_catalogued_photos       %s" %(" ".join(cmd_list)))
        if try_popen(cmd_list, str(WindowsPath.home())) != 0:
            raise Exception("try_popen returns rc != 0")

def backup(
    config: Config, 
    destination_drives: DestinationDrives, 
    request: BackupRequest,
    backup_options: BackupOptions
):

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
    rsync_extra_options = request.rsync_options

    tranche = config.tranche_sets[s][request.tranche_index]
    src_dir: WindowsPath = source_dir[s]
    dest_drive_letter =  destination_drives.drive_letter_for_index(request.destination_drive_index)
    dest_dir: WindowsPath  = destination_dir_funcs[s](dest_drive_letter)
    if not os.path.isdir(src_dir):
        raise Exception("%s is not a directory" % (src_dir))
    if not os.path.isdir(dest_dir):
        raise Exception("%s is not a directory" % (dest_dir))
    # src_drive, src_path = os.path.splitdrive(src_dir)
    # dest_dir = os.path.join(dest_drive_letter, src_path)
    # 
    # these functions perform rsync src_dir/tranch[i]  dest_dir
    # 
    f(tranche, src_dir, dest_dir, backup_options)

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