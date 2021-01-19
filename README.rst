Backup Blackwell Photos and LR Catalogs
=======================================

 This is a backup program for Nina Blackwell's photos. It covers
 - photos that are part of a Lightroom catalog
 - the lightroom catalogs
 - two directories BeforeLightroom and BeforeLightroom2 that are not part of a catalog
 
 This program is to be scheduled to run as a Windows service or a cygwin cron job
 
 Significant requirements or conditions:
 - there are multiple data sources and destinations.
   - Sources
       -   the catalogs are in c:\Pictures\Lightroom\Catalog-*\*
       -   the catalogued images are in D:\LightRoom\[19* 20* Kodak Specials Wedding*]
       -   the non catalogued images are in D:\BeforeLightRoom*
   - Destinations
       -   Internal backup drive probably E: named LR_DUP
           -   D:\LightRoom\[19* 20* Kodak Specials Wedding*] backed up to E:\LightRoom\[19* 20* Kodak Specials Wedding*]
           -   D:\BeforeLightroom\* backed up to E:\BeforeLightroom\*
           -   Catalogues in c:\Pictures\Lightroom\Catalog-*\* -> E:\Lightroom\Catalogues\Catalog-*
       -   External portable (extfat) drive F: or G: BUP_PHOTO (dont know the drive letter so use X as a place holder)
           -   D:\LightRoom\[19* 20* Kodak Specials Wedding*] backed up to X:\LightRoom\[19* 20* Kodak Specials Wedding*]
           -   D:\BeforeLightroom\* backed up to X:\BeforeLightroom\*
           -   Catalogues in c:\Pictures\Lightroom\Catalog-*\* -> X:\Lightroom\Catalogues\Catalog-*
       -   External non portable (apply HFS+) drive F: or G: Photographs (dont know the drive letter so use Y as a place holder)
           -   D:\LightRoom\[19* 20* Kodak Specials Wedding*] backed up to Y:\LightRoom\[19* 20* Kodak Specials Wedding*]
           -   D:\BeforeLightroom\* backed up to X:\BeforeLightroom\*
           -   Catalogues in c:\Pictures\Lightroom\Catalog-*\* -> Y:\Lightroom\Catalogues\Catalog-*
 - other considerations
   -   backups need to be automated with something like cron 
   -   too much data to do all sources to even one destination in a single go - a schedule of what next is required
       -   need to do some timings to find out how much can go in a single job
       -   probably need to keep a record of what has been done so the backup code knows what is next
   -   the images are static except for new images as LightRoom never edits an image
       -   use rsync to prevent copying duplicate data
   -   the external drives may or may not be attached and hence there is a need to discover what destinations
       are available and identify them by volume name not drive letter. Letters are determined by order of connection

