# this module sets up to run a cygwin rsync command from a windows python program
import os.path
import pathlib
import unittest

class PathComponents:
    def __init__(self, windows_path):
        pw = pathlib.PureWindowsPath(str(windows_path))
        self.drive_letter = ""
        self.drive_label = ""
        self.component_list = ""
    
    def windows_path(self):
        return 

cygwin_root = "/cygdrive"
def path_windows_to_cygwin(windows_path) -> str:
    pass

def windows_os_path_to_cygwin_path(windows_path: str) -> pathlib.PosixPath:
    x = pathlib.PureWindowsPath(windows_path)
    drive = x.drive
    drive_letter = drive[0].lower()
    y = list(x.parts)
    w = ["/cygdrive", drive_letter]
    z = ["/cygdrive", drive_letter] + list(x.parts)[1:]
    pz = "/".join(z)
    pp = pathlib.PurePosixPath("/".join(z))
    ppp = pathlib.Path(pz)
    print(pp)
    return pp

if __name__ == '__main__':

    class TestCygwinPaths(unittest.TestCase):
        def test_poaths(self):
            x = pathlib.PureWindowsPath("D:\\Lightroom\\2008")
            drive = x.drive
            drive_letter = drive[0].lower()
            y = list(x.parts)
            w = ["/cygdrive", drive_letter]
            z = ["/cygdrive", drive_letter] + list(x.parts)[1:]
            pz = "/".join(z)
            pp = pathlib.PurePosixPath("/".join(z))
            ppp = pathlib.Path(pz)
            print(pp)

        def test_conv(self):
            x = os.path.realpath(".")
            x = os.path.join("c:", "\\", "Users", "Lightroom", "Projects")
            y = windows_os_path_to_cygwin_path(x)
            print(y)

        def test_windows_path(self):
            x = pathlib.WindowsPath("D:\\Lightroom\\2008")
            y = windows_os_path_to_cygwin_path(x)
            print(y)

        def test_os_path(self):
            x = os.path.realpath(".")
            print(x)

        def test_home(self):
            x = pathlib.Path.home()
            print(x, type(x).__name__)

    unittest.main()