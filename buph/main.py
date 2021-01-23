from typing import Union, List
import sys

import time
from datetime import datetime, timedelta
from timeit import default_timer as timer

from buph.logger import buph_logger
from buph.backup import backup, BackupOptions
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

def backup_options_from_cli(args) -> BackupOptions:
    buopts = BackupOptions()
    buopts.dryrun = args.dry_run
    x = args.quiet
    buopts.quiet = args.quiet
    return buopts


def backup_from_cli_args(
    config: Config, 
    dest_drives: DestinationDrives, 
    scheduler: Scheduler, 
    backup_options: BackupOptions,
    args
):
    buph_logger.info("Backup bu-type %s to-drive: %s" % (args.bu_type, args.to_drive))
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
    req = BackupRequest(bu_type, bu_tranche, ix)
    backup(config, dest_drives, req, backup_options)

def backup_from_schedule(
    config: Config, 
    dest_drives: DestinationDrives, 
    scheduler: Scheduler, 
    backup_options: BackupOptions
):
    request = scheduler.backup_request_for_today()
    backup(config, dest_drives, request, backup_options)

def time_now_as_str():
    now_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    return now_time

def elapsed_time_as_str(start_time):
    elap = str(timedelta(seconds=timer() - start_time))
    return elap

__version__ = "1.0.1"


def main():
    start_time = timer()
    try:
    
        parser = define_cli_interface()
        args = parser.parse_args()
        if args.version:
            print(__version__)
            sys.exit(0)

        buph_logger.info("buph starting at %s" % (time_now_as_str()))

        backup_options = backup_options_from_cli(args)

        if (args.bu_type or args.to_drive) and not (args.to_drive and args.bu_type):
            buph_logger.info("Cannot specify only one and to-drive")
            sys.exit(1)

        config = Config()
        dest_drives = DestinationDrives(config)
        scheduler = Scheduler(config, dest_drives)

        if args.day_num:
            daynum = args.day_num
            request = scheduler.backup_request_for_daynumber(daynum)
            backup(config, dest_drives, request, backup_options)

        # perform the backup specified on cli
        elif args.bu_type and args.to_drive:
            buph_logger.info("Backup bu-type %s to-drive: %s" % (args.bu_type, args.to_drive))
            backup_from_cli_args(config, dest_drives, scheduler, backup_options, args)
        else:
            # perform the next backup in the schedule
            backup_from_schedule(config, dest_drives, scheduler, backup_options)
   
    except Exception: 
        buph_logger.exception("Exception in main")
    
    buph_logger.info("buph completed at %s elapsed time %s" % (time_now_as_str(), elapsed_time_as_str(start_time)))
    