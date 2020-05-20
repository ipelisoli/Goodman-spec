# Reduce standard star spectra

__version__ = '1.0'
__author__ = 'Ingrid Pelisoli'

# Importing packages
from pyraf import iraf
from pyraf.iraf import imred, ccdred
from pyraf.iraf import twodspec, apextract
from pyraf.iraf import onedspec
from pyraf.iraf import images, immatch
from pyraf.iraf import imutil

# Prompts for arc lamp file; format 'FILE.fits'
arc_in = input('Arc file: ')
arc_out = "c" + arc_in

# Prompts for science files; format ['FILE1.fits','FILE2.fits',...]
science_in = input('Science files: ')
obj_in = ', '.join(science_in)

# Creates list with output names for cccdproc processed files
science_out = ["c" + name for name in science_in]
obj_out = ', '.join(science_out)

print ("=== Running ccdproc for arc lamp ===")

ccdred.ccdproc.unlearn()
ccdred.ccdproc(arc_in, output=arc_out, ccdtype = "", fixpix='no',
               overscan='no', trim='yes', zerocor='yes', darkcor='no',
               flatcor='no', trimsec='[26:2071,105:880]', zero="../Zero.fits")

print ("=== ccdproc finished ===")

print ("=== Running ccdproc for object ===")

ccdred.ccdproc.unlearn()
ccdred.ccdproc(obj_in, output=obj_out, ccdtype = "", fixpix='no',
               overscan='no', trim='yes', zerocor='yes', darkcor='no',
               flatcor='yes', trimsec='[26:2071,105:880]', zero="../Zero.fits",
               flat="../Flat.fits")

# Trimsec:
# Blue CCD: [12:2055,45:825]
# Red CCD: [26:2071,105:880]

print ("=== ccdproc finished ===")

immatch.imcombine(obj_out, output="STD.fits")

print ("=== Running apall for spectrum ===")

Flags_obj = {'interactive':'yes', 'find':'no', 'recenter':'no', 'resize':'no',
             'edit':'yes', 'trace':'yes', 'fittrace':'yes', 'extract':'yes',
             'background':'median'}

apextract.apall("STD.fits", clean='yes', **Flags_obj)

print ("=== Running apall for arc ===")

Flags_arc = {'interactive':'no', 'find':'no', 'recenter':'no', 'resize':'no',
             'edit':'yes', 'trace':'yes', 'fittrace':'no', 'extract':'yes',
             'background':'none'}

apextract.apall(arc_out, reference="STD.fits", **Flags_arc)

print ("=== Running identify ===")

arc_oned = arc_out.replace(".fits", ".ms.fits")

onedspec.identify(arc_oned, function='legendre', order=4,
                  coordlist='gmos$data/CuAr_GMOS.dat')

print ("=== Applying wavelength solution ===")

imutil.hedit("STD.ms.fits", fields="REFSPEC1", value=arc_oned, add='yes', addonly='no', verify='no')
onedspec.dispcor("STD.ms.fits", output="calL_STD.ms.fits")

print ("=== Obtaining sensitivity function ===")

caldir = input("Directory containing calibration data: ")
starname = input("Standard star name in calibration list: " )

onedspec.standard("calL_STD.ms.fits", star_name=starname, caldir=caldir,
                  extinction='onedstds$ctioextinct.dat')

onedspec.sensfunc(standards="std", sensitivity="../sens", interactive='yes')
