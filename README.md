# Goodman-spec
## Reduce SOAR/Goodman spectra

This repository contains my scripts to perform data reduction of SOAR/Goodman spectra.

The steps to be run are:

1. Download your data.

2. Organize your directory. Put bias and flat files in their own separate directory, and preferably do the same for files 
concerning the standard star.

3. In the Bias directory, run MakeBias.py (it will use *all* .fits files in that directory).

4. In the Flat director, run MakeFlat.py (also uses *all* .fits files in the directory).

5. In the Standard directory, run ReduceStandard.py. This script is interactive. It will first prompt for the arc lamp file. 
Next it will prompt for a list of science spectra, which should be input as ['FILE1.fits','FILE2.fits',...].
All the spectra will be combined into one file, and the extraction will run interactively.
The wavelength calibration will also run interactively by default.
Finally the code will prompt for the directory containing the calibration data, and the name of the
star in the calibration files. Extinction is set to ctioextinct.dat.
The last interactive step is the sensitivity function fitting.

6. In the directory containing science data, run ReduceSpec.py. The steps are similar to those followed for the standard star.
In this case, however, the spectra are not combined. The first spectrum in the list will be used as reference spectrum to
extract the other science spectra (interactively in case the aperture or background need adjustments) and the lamp spectrum
(without interaction). Of course data on the calibration directory will not be requested, but the sens.fits function generated
in the previous step will be used to flux calibrate the science spectra.

7. If you would like to combine all science spectra into one, run Correct_and_combine.py. It will apply a heliocentric
correction to the wavelengths of individual spetra, and then scombine them. The script will prompt for the list of spectra to 
be combined, in the format ['FILE1.fits','FILE2.fits',...], and then for the name of the output file (format 'FILE.fits').

It might be necessary to change the trimsec and/or the coordlist depending on your configuration.

This script is intended for personal use, therefore there should be plenty of limitations.
