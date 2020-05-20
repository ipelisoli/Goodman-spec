# Create master flat from individial *.fits exposures

__version__ = '1.0'
__author__ = 'Ingrid Pelisoli'

# Importing packages
from pyraf import iraf
from pyraf.iraf import imred, ccdred
import glob

# Creates lists for input and output files
flat_files = glob.glob('*.fits')
flat_in = ', '.join(flat_files)

processed_flat_files = ["c" + name for name in flat_files]
flat_out = ', '.join(processed_flat_files)

print ("### Begin Processing Goodman/Longslit Images ###")
print ("###")

print ("=== Running ccdproc ===")

ccdred.ccdproc.unlearn()
ccdred.ccdproc(flat_in, output=flat_out, ccdtype = "", fixpix='no',
               overscan='no', trim='yes', zerocor='yes', darkcor='no',
               flatcor='no', trimsec='[26:2071,105:880]', zero="../Zero.fits")

# Trimsec:
# Blue CCD: [12:2055,45:825]
# Red CCD: [26:2071,105:880]

print ("=== ccdproc finished ===")

print ("=== Creating Master Flat ===")

ccdred.zerocombine.unlearn()
ccdred.flatcombine(flat_out, output="../Flat.fits", combine="median",
                   reject="sigclip", ccdtype = "", process='no', subsets='no')

print ("=== flatcombine finished ===")

print ("### DONE ###")
