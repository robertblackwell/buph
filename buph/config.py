import typing
import subprocess 
import pathlib 
import os.path 
from datetime import datetime
import math

class Config:
    def __init__(self):

        self.tranches_catalogued_photos = [
            ["2005", "2005", "2006", "2007Sweden", "2008", "2009", "2009Russia-Rob", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2017-nw-mogfest"],
            ["2018*", "2019", "2020", "Kodak", "Specials", "Wedding-Richard&Lizzie"],
        ]
        self.tranches_uncatalogued_photos = [
            ["BeforeLightRoom", "BeforeLightRoom_2"]
        ]
        self.tranches_catalogs =[
            [
            "Catalog-12-18-strict",
            "Catalog-12TO18",
            "Catalog-2005-6-7-8",
            "Catalog-2008",
            "Catalog-2019-2020",
            "Catalog-8604warren",
            "Catalog-All",
            "Catalog-Australia2019",
            "Catalog-Master",
            "Catalog-SouthAmerica",
            "Kodak",
            ]
        ]
        self.tranche_sets = [
            self.tranches_catalogued_photos,
            self.tranches_uncatalogued_photos,
            self.tranches_catalogs
        ]
        self.destination_dirs = [
            "LR_DUP", "BUP_PHOTO", "Photographs"
        ]

    def number_tranches_catalogued_photos(self):
        return len(self.tranches_catalogued_photos)
    
    def number_tranches_uncatalogued_photos(self):
        return len(self.tranches_uncatalogued_photos)
    
    def number_tranches_catalogues(self):
        return len(self.tranches_catalogs)
    
    # determines how many distinct backup runs there should be - a run is a (tranche, a single destination)
    def number_of_backup_runs(self):
        runs_count = len(self.tranches_catalogued_photos) + len(self.tranches_uncatalogued_photos) + len(self.tranches_catalogs)
        return runs_count * len(self.destination_dirs)
    
    def catalog_source_dir(self) -> pathlib.WindowsPath:
        return pathlib.Path(pathlib.Path.home(), "Pictures", "LightRoom")
    
    def cataloged_photos_source_dir(self) -> pathlib.WindowsPath:
        return pathlib.Path("D:\\LightRoom")
    
    def uncatalogued_photos_source_dir(self) -> pathlib.WindowsPath:
        return pathlib.Path("D:\\")

    def catalog_destination_dir(self, drive_letter) -> pathlib.WindowsPath:
        drive_letter = drive_letter.upper()
        return pathlib.Path(drive_letter+":", "\\", "Catalogs")
    
    def cataloged_photos_destination_dir(self, drive_letter)  -> pathlib.WindowsPath:
        drive_letter = drive_letter.upper()
        return pathlib.Path(drive_letter+":", "\\", "LightRoom")
    
    def uncatalogued_photos_destination_dir(self, drive_letter)  -> pathlib.WindowsPath:
        drive_letter = drive_letter.upper()
        return pathlib.Path(drive_letter+":", "\\", "uncatalogued")
