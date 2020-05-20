# Correct wavelength to heliocentric and combine

__version__ = '1.0'
__author__ = 'Ingrid Pelisoli'

# Importing packages
from astropy.io import fits
from pyraf import iraf
from pyraf.iraf import onedspec
from pyraf.iraf import imutil
from pyraf.iraf import astutil

# Prompts for input science files; format ['FILE1.fits','FILE2.fits',...]
science_in = input('Input flux calibrated files: ')
obj_in = ', '.join(science_in)

# Prompts for output file; format 'FILE.fits'
output_file = input('Name for output file: ')

# SOAR location
sitelong = -70.73372
sitelat = -30.238
siteelev = 2378.

for infile in science_in:
    outfile = infile.replace('calF', 'dopcor')
    with fits.open(infile) as spec:
        header=spec[0].header
        date = header['OPENDATE']
        time = header['TIME']
        utstart = time[0:11]
        utend = time[16:27]
        ra = header['OBSRA']
        dec = header['OBSDEC']
    imutil.hedit.unlearn()
    imutil.hedit(infile, fields="OBJRA", value=ra, add='yes', addonly='no', verify='no')
    imutil.hedit(infile, fields="OBJDEC", value=dec, add='yes', addonly='no', verify='no')
    imutil.hedit(infile, fields="EPOCH", value='2000', add='yes', addonly='no', verify='no')
    imutil.hedit(infile, fields="DATE-OBS", value=date, add='yes', addonly='no', verify='no')
    imutil.hedit(infile, fields="UTOPEN", value=utstart, add='yes', addonly='no', verify='no')
    imutil.hedit(infile, fields="UTEND", value=utend, add='yes', addonly='no', verify='no')
    imutil.hedit(infile, fields="SITELONG", value=sitelong, add='yes', addonly='no', verify='no')
    imutil.hedit(infile, fields="SITELAT", value=sitelat, add='yes', addonly='no', verify='no')
    imutil.hedit(infile, fields="SITEELEV", value=siteelev, add='yes', addonly='no', verify='no')

    # Calculate vhelio and write to header
    astutil.rvcorrect(images=infile, imupdate='yes', observatory='soar')
    # Apply vhelop correction and saves to a new file
    onedspec.dopcor(input=infile, output=outfile, redshift="-vhelio", isvelocity='yes')

onedspec.scombine('dopcor*fits', output=output_file, combine='median', reject='sigclip')
