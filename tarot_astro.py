#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Python module for cutting TAROT images and performing astrometry.net
# Martin Blazek, IAA, Granada, Spain, alf@iaa.es
# July 2019, v1.2
#
# Example:
# python tarot_astro.py tarot.fits 
#
# Image is cut into 4 pieces with prefixes C1_, C2_, C3 and C4_
# In each subimage the basic WCS keywords are erased
# Then astrometry.net is performed
# You need to install locally astrometry.net and to download following indeces files: index-4204-*.fits
# This version uses Heasoft ftcopy command

import subprocess, sys, os
from astropy.io import fits
import shutil


def cut_tarot(filename):
    
    extension1 = filename + "[1:1024,1:1024]"
    fileout1 = "D1_" + filename
    extension2 = filename + "[1:1024,1025:2048]"
    fileout2 = "D2_" + filename
    extension3 = filename + "[1025:2048,1:1024]"
    fileout3 = "D3_" + filename
    extension4 = filename + "[1025:2048,1025:2048]"
    fileout4 = "D4_" + filename
    
    shutil.copyfile(filename, fileout1)
    shutil.copyfile(filename, fileout2)
    shutil.copyfile(filename, fileout3)
    shutil.copyfile(filename, fileout4)
    
    hdul = fits.open(fileout1)
    fulltable = hdul[0].data
    subtable1 = fulltable[0:1023,0:1023]
    hdul[0].data = subtable1
    hdul.writeto(fileout1,overwrite=True)
    hdul.close()
 
    hdul = fits.open(fileout2)
    fulltable = hdul[0].data
    subtable2 = fulltable[0:1023,1024:2047]
    hdul[0].data = subtable2
    hdul.writeto(fileout2,overwrite=True)
    hdul.close()

    hdul = fits.open(fileout3)
    fulltable = hdul[0].data
    subtable3 = fulltable[1024:2047,0:1023]
    hdul[0].data = subtable3
    hdul.writeto(fileout3,overwrite=True)
    hdul.close()

    hdul = fits.open(fileout4)
    fulltable = hdul[0].data
    subtable4 = fulltable[1024:2047,1024:2047]
    hdul[0].data = subtable4
    hdul.writeto(fileout4,overwrite=True)
    hdul.close()
    
    #subprocess.call(['ftcopy',extension1,fileout1,'clobber=yes'])
    #subprocess.call(['ftcopy',extension2,fileout2,'clobber=yes'])
    #subprocess.call(['ftcopy',extension3,fileout3,'clobber=yes'])
    #subprocess.call(['ftcopy',extension4,fileout4,'clobber=yes'])


def clean_astrometry_temp_files(filename):
    fileroot = filename.split('.fits')
    os.remove(fileroot[0] + "-indx.xyls")
    os.remove(fileroot[0] + ".axy")
    os.remove(fileroot[0] + ".corr")
    os.remove(fileroot[0] + ".match")
    os.remove(fileroot[0] + ".rdls")
    os.remove(fileroot[0] + ".solved")
    os.remove(fileroot[0] + ".wcs")
    os.remove(fileroot[0] + ".fits")
    os.rename(fileroot[0] + ".new",fileroot[0] + ".fits") 

def erase_astrometry_header(filename):
    hdul = fits.open(filename)
    hdr = hdul[0].header
    del hdr['CRVAL1']
    del hdr['CRVAL2']
    del hdr['CRPIX1']
    del hdr['CRPIX2']
    hdul[0].header = hdr
    hdul.writeto(filename,overwrite=True)
    hdul.close()
    
    #subprocess.call(['fthedit', filename, 'CRVAL1', 'delete'])
    #subprocess.call(['fthedit', filename, 'CRVAL2', 'delete'])
    #subprocess.call(['fthedit', filename, 'CRPIX1', 'delete'])
    #subprocess.call(['fthedit', filename, 'CRPIX2', 'delete'])
    

def perform_astrometry(filename):
    header = fits.getheader(filename)
    ra = str(header['CRVAL1'])
    dec = str(header['CRVAL2'])

    erase_astrometry_header(filename)

    subprocess.call(['solve-field', filename, '--ra', ra, '--dec', dec, '--radius', '1', '--scale-units', 'degwidth', '--scale-low', '0.8', '--scale-high', '1.2', '--no-plots','--overwrite'])
    clean_astrometry_temp_files(filename)
    

if __name__ == "__main__":
    
    filename_argument = sys.argv[1]
    cut_tarot(filename_argument)
    
    filein1 = "D1_" + filename_argument
    filein2 = "D2_" + filename_argument
    filein3 = "D3_" + filename_argument
    filein4 = "D4_" + filename_argument
    
    perform_astrometry(filein1)
    perform_astrometry(filein2)
    perform_astrometry(filein3)
    perform_astrometry(filein4)
    

