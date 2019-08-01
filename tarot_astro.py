#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Python module for cutting TAROT images and performing astrometry.net
# Martin Blazek, IAA, Granada, Spain, alf@iaa.es
# July 2019
#
# Example:
# python tarot_astro.py tarot.fits 
#
# Image is cut into 4 pieces with prefixes C1_, C2_, C3 and C4_
# In each subimage the basic WCS keywords are erased
# Then astrometry.net is performed
# You need to install locally astrometry.net and to download following indeces files: index-4204-*.fits



import subprocess, sys, os
from astropy.io import fits


def cut_tarot(filename):
    extension1 = filename + "[1:1024,1:1024]"
    fileout1 = "C1_" + filename
    extension2 = filename + "[1:1024,1025:2048]"
    fileout2 = "C2_" + filename
    extension3 = filename + "[1025:2048,1:1024]"
    fileout3 = "C3_" + filename
    extension4 = filename + "[1025:2048,1025:2048]"
    fileout4 = "C4_" + filename
    
    subprocess.call(['ftcopy',extension1,fileout1,'clobber=yes'])
    subprocess.call(['ftcopy',extension2,fileout2,'clobber=yes'])
    subprocess.call(['ftcopy',extension3,fileout3,'clobber=yes'])
    subprocess.call(['ftcopy',extension4,fileout4,'clobber=yes'])


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
    
    subprocess.call(['fthedit', filename, 'CRVAL1', 'delete'])
    subprocess.call(['fthedit', filename, 'CRVAL2', 'delete'])
    subprocess.call(['fthedit', filename, 'CRPIX1', 'delete'])
    subprocess.call(['fthedit', filename, 'CRPIX2', 'delete'])
    
    

def perform_astrometry(filename):
    header = fits.getheader(filename)
    ra = str(header['CRVAL1'])
    dec = str(header['CRVAL2'])

    #erase_astrometry_header(filename)

    subprocess.call(['solve-field', filename, '--ra', ra, '--dec', dec, '--radius', '1', '--scale-units', 'degwidth', '--scale-low', '0.8', '--scale-high', '1.2', '--no-plots','--overwrite'])
    clean_astrometry_temp_files(filename)
    

if __name__ == "__main__":
    
    filename_argument = sys.argv[1]
    cut_tarot(filename_argument)
    
    filein1 = "C1_" + filename_argument
    filein2 = "C2_" + filename_argument
    filein3 = "C3_" + filename_argument
    filein4 = "C4_" + filename_argument
    perform_astrometry(filein1)
    perform_astrometry(filein2)
    perform_astrometry(filein3)
    perform_astrometry(filein4)
    

