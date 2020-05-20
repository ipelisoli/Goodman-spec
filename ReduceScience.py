# Reduce science spectra

__version__ = '1.0'
__author__ = 'Ingrid Pelisoli'

# Importing packages
from pyraf import iraf
from pyraf.iraf import imred, ccdred
from pyraf.iraf import twodspec, apextract
from pyraf.iraf import onedspec
from pyraf.iraf import imutil

# Prompts for science files; format ['FILE1.fits','FILE2.fits',...]
science_in = input('Science files: ')
obj_in = ', '.join(science_in)

science_out = ["c" + name for name in science_in]
obj_out = ', '.join(science_out)

# Prompts for arc lamp file; format 'FILE.fits'
arc_in = input('Arc file: ')
arc_out = "c" + arc_in

print ("=== Running ccdproc for arc lamp ===")

ccdred.ccdproc.unlearn()
ccdred.ccdproc(arc_in, output=arc_out, ccdtype = "", fixpix='no',
               overscan='no', trim='yes', zerocor='yes', darkcor='no',
               flatcor='no', trimsec='[26:2071,105:880]', zero="../Zero.fits")
# Trimsec:
# Blue CCD: [12:2055,45:825]
# Red CCD: [26:2071,105:880]

print ("=== ccdproc finished ===")

print ("=== Running ccdproc for object ===")

ccdred.ccdproc.unlearn()
ccdred.ccdproc(obj_in, output=obj_out, ccdtype = "", fixpix='no',
               overscan='no', trim='yes', zerocor='yes', darkcor='no',
               flatcor='yes', trimsec='[26:2071,105:880]', zero="../Zero.fits",
               flat="../Flat.fits")

print ("=== ccdproc finished ===")

print ("=== Running apall for reference spectrum ===")

ref_spec = str(science_out[0])
print("Reference spectrum: %s"%(ref_spec))

Flags_obj = {'interactive':'yes', 'find':'no', 'recenter':'no', 'resize':'no',
             'edit':'yes', 'trace':'yes', 'fittrace':'yes', 'extract':'yes',
             'background':'median'}

apextract.apall(ref_spec, clean='yes', **Flags_obj)

if(len(science_in)>1):
    print ("=== Running apall for other spectra ===")

    other_spec = science_out[1:]
    other_spec = ','.join(other_spec)

    apextract.apall(other_spec, reference=ref_spec, clean='yes', **Flags_obj)

print ("=== Running apall for arc ===")

Flags_arc = {'interactive':'no', 'find':'no', 'recenter':'no', 'resize':'no',
             'edit':'yes', 'trace':'yes', 'fittrace':'no', 'extract':'yes',
             'background':'none'}

apextract.apall(arc_out, reference=ref_spec, **Flags_arc)

arc_oned = arc_out.replace(".fits", ".ms.fits")

onedspec.identify(arc_oned, function='legendre', order=4,
                  coordlist='gmos$data/CuAr_GMOS.dat')

print ("=== Applying wavelength solution ===")

obj_oned = [name.replace(".fits", ".ms.fits") for name in science_out]
obj_call = ['calL_' + name for name in obj_oned]
obj_calf = ['calF_' + name for name in obj_oned]

obj_oned = ', '.join(obj_oned)
obj_call = ', '.join(obj_call)
obj_calf = ', '.join(obj_calf)

imutil.hedit.unlearn()
imutil.hedit(obj_oned, fields="REFSPEC1", value=arc_oned, add='yes', addonly='no', verify='no')
onedspec.dispcor(obj_oned, output=obj_call)

print ("=== Applying flux calibration ===")

onedspec.calibrate.unlearn()
onedspec.calibrate(input=obj_call, output=obj_calf, extinct='yes', flux='yes',
                   extinction='onedstds$ctioextinct.dat',
                   sensitivity="../sens")

print ("### DONE ###")
