# this module sets up to run a cygwin rsync command from a windows python program
from pathlib import PurePosixPath, WindowsPath
from buph.logger import buph_logger
from typing import List

rsync_options = "-archW"
cygwin_bash = 'c:\\cygwin64\\bin\\bash'
cygwin_rsync = 'c:\\cygwin64\\home\\lightroom\\projects\\buph\\buph\\rsync_run.sh'

def path_windows_to_posix(p: WindowsPath) -> PurePosixPath:
    x = p
    drive = x.drive
    drive_letter = drive[0].lower()
    y = list(x.parts)
    w = ["/cygdrive", drive_letter]
    z = ["/cygdrive", drive_letter] + list(x.parts)[1:]
    pz = "/".join(z)
    pp = PurePosixPath("/".join(z))
    print(pp)
    return pp


def rsync_cmd(extra_options:List[str], cwd: WindowsPath, src_dir: WindowsPath, dest_dir: WindowsPath) -> List[str]:
    cmd = [
        cygwin_bash, "-l", 
        cygwin_rsync, 
        " ".join(extra_options),
        str(path_windows_to_posix(src_dir)), 
        str(path_windows_to_posix(dest_dir))]

    buph_logger.info("cygwin rsync_run(%s %s %s %s)" %(" ".join(extra_options), cwd, src_dir, dest_dir))
    return cmd