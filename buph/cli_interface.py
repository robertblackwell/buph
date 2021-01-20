import argparse

#
# define global argument and options
#
def define_global_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('--version, -v', dest='version',
                        help='Print version ')
    parser.add_argument('--dry-run', dest='dry_run', action='store_true',
                        help='Dry run flag passed to rsync .\n Default false')

    parser.add_argument('--quiet', dest='quiet', action='store_true',
                        help='Run rsync with -q flag')


    parser.add_argument('--bu-type', dest='bu_type',
                        help='The type of backup c = catalogs, p = catalogued photos, u = uncatalogued photos')

    parser.add_argument('--bu-tranche', dest='bu_tranche',
                        help='Valid values are 0, 1, 2')

    parser.add_argument('--to-drive', dest='to_drive',
                        help='The destination drive letter for the backup. Must have one of the valid backup volume name. Only consider E/e F/f G/g H/h')

    parser.add_argument('--log-actions', dest='log_actions', action='store_true',
                        help='Creates a log of all cli commands and their output.')

    parser.add_argument('--action-logfile', dest='log_path',
                        help='path of file for logging actions. Default ./simpli_log.log')



def define_cli_interface() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Backup Blackwell LR photo library.")
    parser.add_argument('-v', '--version', action="store_true",
                        help="Prints the version number.")
    define_global_args(parser)
    return parser