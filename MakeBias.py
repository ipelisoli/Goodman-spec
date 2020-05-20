# Create master bias from individial *.fits exposures

__version__ = '1.0'
__author__ = 'Ingrid Pelisoli'

# Importing packages
from pyraf import iraf
from pyraf.iraf import imred, ccdred
import glob

# Creates list containing all fits files as input
bias_files = glob.glob('*.fits')
input_bias = open("bias_in", "w")
for line in bias_files:
  input_bias.write(line)
  input_bias.write("\n")
input_bias.close()

# Creates list with name for output ccdproc processed files
processed_bias_files = ["c" + name for name in bias_files]
output_bias = open("bias_out", "w")
for line in processed_bias_files:
  output_bias.write(line)
  output_bias.write("\n")
output_bias.close()

print ("### Begin Processing Goodman/Longslit Images ###")
print ("###")

print ("=== Running ccdproc ===")

ccdred.ccdproc.unlearn()
ccdred.ccdproc('@bias_in', output='@bias_out', ccdtype = "", fixpix='no',
               overscan='no', trim='yes', zerocor='no', darkcor='no',
               flatcor='no', trimsec='[26:2071,105:880]')

# Trimsec:
# Blue CCD: [12:2055,45:825]
# Red CCD: [26:2071,105:880]

print ("=== ccdproc finished ===")

print ("=== Creating Master Bias ===")

ccdred.zerocombine.unlearn()
ccdred.zerocombine('@bias_out', output="../Zero.fits", combine="median",
                   reject="sigclip", ccdtype = "")

print ("=== zerocombine finished ===")

print ("### DONE ###")
