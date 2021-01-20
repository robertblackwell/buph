import typing
import subprocess 
import pathlib 
import os.path 
from datetime import datetime
import math
from buph.config import Config
import unittest

if __name__ == '__main__':

    class TestConfig(unittest.TestCase):
        def test_src_dirs(self):
            config = Config()
            x1 = config.catalog_destination_dir("e")
            x2 = config.catalog_source_dir()
            x3 = config.cataloged_photos_destination_dir("e")
            x4 = config.cataloged_photos_source_dir()
            x5 = config.uncatalogued_photos_destination_dir("e")
            x6 = config.uncatalogued_photos_source_dir()
            n = type(x6).__name__
            self.assertEqual(type(x6).__name__, "WindowsPath")
            self.assertEqual(type(x5).__name__, "WindowsPath")
            self.assertEqual(type(x4).__name__, "WindowsPath")
            self.assertEqual(type(x3).__name__, "WindowsPath")
            self.assertEqual(type(x2).__name__, "WindowsPath")
            self.assertEqual(type(x2).__name__, "WindowsPath")
            y = str(x1)
            self.assertEqual(str(x1), "E:\\Catalogs")
            self.assertEqual(str(x2), "C:\\Users\\lightroom\\Pictures\\LightRoom")
            self.assertEqual(str(x3), "E:\\LightRoom")
            self.assertEqual(str(x4), "D:\\LightRoom")
            self.assertEqual(str(x5), "E:\\uncatalogued")
            self.assertEqual(str(x6), "D:\\")
            print(x1,x2,x3,x4,x5,x6)

    unittest.main()