from typing import Union, List
import sys
import subprocess 
import pathlib 
import os.path 
from datetime import datetime
import math
from buph.logger import buph_logger
from buph.backup import backup
from buph.config import Config
from buph.drives import DestinationDrives, getDriveName
from buph.scheduler import Scheduler, BackupRequest, BackupType
from buph.cli_interface import define_cli_interface

def backup_type_from_cli(cli_response):
    if cli_response == "c":
        return BackupType.CATALOG
    elif cli_response == "u":
        return BackupType.UNCATALOGUED_IMAGE
    elif cli_response == "p":
        return BackupType.CATALOGUED_IMAGE
    else:
        raise Exception("%s is an invalid backup type, one of 'c', 'p', 'u' expected")

def backup_tranche_from_cli(cli_tranche):
    if cli_tranche in ["0", "1"]:
        return int(cli_tranche)
    raise Exception("%s is an invalid backup ttranche, one of '0', '1' expected")

def to_drive_letter_from_cli(cli_drive_letter):
    dl = (cli_drive_letter+":").upper()
    return dl

def number_tranches(config: Config, bu_type: BackupType) -> int:
    f = [
        config.number_tranches_catalogued_photos,
        config.number_tranches_catalogues,
        config.number_tranches_uncatalogued_photos
    ]
    ix = int(bu_type)
    return f[ix]()

def backup_from_cli_args(
    config: Config, 
    dest_drives: DestinationDrives, 
    scheduler: Scheduler, 
    args, 
    rsync_options: List[str]=[]
):
    print("Backup bu-type %s to-drive: %s" % (args.bu_type, args.to_drive))
    bu_type = backup_type_from_cli(args.bu_type)
    if number_tranches(config, bu_type) > 1:
        if not args.bu_tranche:
            raise Exception("for this backup type require a bu-tranche option")
        bu_tranche = backup_tranche_from_cli(args.bu_tranche)
    else:
        bu_tranche = 0

    dl = to_drive_letter_from_cli(args.to_drive)
    vol_name = getDriveName(dl)
    ix = dest_drives.drive_index(vol_name)
    if ix is None:
        raise Exception("could not find volumen name for drive %s" % (dl))
    req = BackupRequest(bu_type, bu_tranche, ix, rsync_options)
    backup(config, dest_drives, req)

def backup_from_schedule(config: Config, dest_drives: DestinationDrives, scheduler: Scheduler, rsync_options: List[str] = []):
    request = scheduler.backup_request_for_today()
    request.rsync_options = rsync_options
    backup(config, dest_drives, request)


__version__ = "0.0.3"

def main():

    buph_logger.debug('Debug message, should only appear in the file.')
    buph_logger.info('Info message, should appear in file and stdout.')
    buph_logger.warning('Warning message, should appear in file and stdout.')
    buph_logger.error('Error message, should appear in file and stdout.')
    buph_logger.info("buph starting")
    
    parser = define_cli_interface()

    args = parser.parse_args()
    if args.version:
        print(__version__)
        sys.exit(0)

    rsync_options = []
    if args.dry_run:
        rsync_options.append("--dry-run")
    if args.quiet:
        rsync_options.append("-q")


    if (args.bu_type or args.to_drive) and not (args.to_drive and args.bu_type):
        buph_logger.info("Cannot specify only one and to-drive")
        sys.exit(1)

    config = Config()
    dest_drives = DestinationDrives()
    scheduler = Scheduler(config, dest_drives)

    # perform the backup specified on cli
    if args.bu_type and args.to_drive:
        buph_logger.info("Backup bu-type %s to-drive: %s" % (args.bu_type, args.to_drive))
        try:
            backup_from_cli_args(config, dest_drives, scheduler, args, rsync_options)
            # bu_type = backup_type_from_cli(args.bu_type)
            # if number_tranches(config, bu_type) > 1:
            #     if not args.bu_tranche:
            #         raise Exception("for this backup type require a bu-tranche option")
            #     bu_tranche = backup_tranche_from_cli(args.bu_tranche)
            # else:
            #     bu_tranche = 0

            # dl = to_drive_letter_from_cli(args.to_drive)
            # vol_name = getDriveName(dl)
            # ix = dest_drives.drive_index(vol_name)
            # req = BackupRequest(bu_type, bu_tranche, ix)
            # backup(config, dest_drives, req)
        except: 
            exception = sys.exc_info()[0]
            print("Exception", exception)
            raise(exception)

    else:
        # perform the next backup in the schedule
        try:
            backup_from_schedule(config, dest_drives, scheduler, rsync_options)
            # request = scheduler.backup_request_for_today()
            # backup(config, dest_drives, request)
        except:
            exception = sys.exc_info()[0]
            print("Exception", exception)
            raise(exception)

    # backup(config, dest_drives, BackupRequest(BackupType.CATALOGUED_IMAGE, 1, 0))
    # backup(config, dest_drives, BackupRequest(BackupType.UNCATALOGUED_IMAGE, 0, 0))
    # backup(config, dest_drives, BackupRequest(BackupType.CATALOG, 0, 0))
