""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py image_dir_path [apod_date]

Parameters:
  image_dir_path = Full path of directory in which APOD image is stored
  apod_date = APOD image date (format: YYYY-MM-DD)

History:
  Date        Author    Description
  2022-03-11  J.Dalby   Initial creation
"""
from ast import Return
from cgitb import text
from operator import truediv
import os
from platform import architecture
import sqlite3
from sre_constants import SUCCESS
from sys import argv, exit
from datetime import datetime, date
from hashlib import sha256
from typing import Text
from os import path
from urllib import response
import requests
import hashlib

def main():



    # Determine the paths where files are stored
    image_dir_path = get_image_dir_path()
    db_path = path.join(image_dir_path, 'apod_images.db')
    ima_path = path.join(argv[1], 'image.jpg')

    # Get the APOD date, if specified as a parameter
    apod_date = get_apod_date()

    # Create the images database if it does not already exist
    create_image_db(db_path)

    # Get info for the APOD
    apod_info_dict = get_apod_info(apod_date)

    #enclosing hash

    with open(ima_path, 'rb') as f:
        hash =f.read()
    
    # Download today's APOD"
    image_url =  apod_info_dict['hdurl']
    image_msg = download_apod_image(image_url)
    image_sha256 = hashlib.sha256(hash).hexdigest()
    image_size = os.path.getsize(ima_path)
    image_path = get_image_path(image_url, image_dir_path)

    # Print APOD image information
    print_apod_info(image_url, image_path, image_size, image_sha256,)

    # Add image to cache if not already present
    if not image_already_in_db(db_path, image_sha256):
        save_image_file(image_msg, image_path)
        add_image_to_db(db_path, image_path, image_size, image_sha256)

    # Set the desktop background image to the selected APOD
    set_desktop_background_image(image_path)

def get_image_dir_path():
    """
    Validates the command line parameter that specifies the path
    in which all downloaded images are saved locally.

    :returns: Path of directory in which images are saved locally
    """
    if len(argv) >= 2:
        dir_path = argv[1]
        if path.isdir(dir_path):
            print("Images directory:", dir_path)
            return dir_path
        else:
            print('Error: Non-existent directory', dir_path)
            exit('Script execution aborted')
    else:
        print('Error: Missing path parameter.')
        exit('Script execution aborted')

def get_apod_date():
    """
    Validates the command line parameter that specifies the APOD date.
    Aborts script execution if date format is invalid.

    :returns: APOD date as a string in 'YYYY-MM-DD' format
    """    
    if len(argv) >= 3:
        # Date parameter has been provided, so get it
        apod_date = argv[2]

        # Validate the date parameter format
        try:
            datetime.strptime(apod_date, '%Y-%m-%d')
        except ValueError:
            print('Error: Incorrect date format; Should be YYYY-MM-DD')
            exit('Script execution aborted')
    else:
        # No date parameter has been provided, so use today's date
        apod_date = date.today().isoformat()
    
    print("APOD date:", apod_date)
    return apod_date

def get_image_path(image_url, dir_path):
    """
    Determines the path at which an image downloaded from
    a specified URL is saved locally.

    :param image_url: URL of image
    :param dir_path: Path of directory in which image is saved locally
    :returns: Path at which image is saved locally
    """
    
    respons_e = requests.get(image_url)

    dir_path = path.join(argv[1], 'image.jpg')

    if respons_e.status_code == 200:
        with open (dir_path, 'wb') as fp:
            fp.write(respons_e.content)


    return dir_path
        

    

def get_apod_info(date):
    """
    Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    :param date: APOD date formatted as YYYY-MM-DD
    :returns: Dictionary of APOD info
    """    
    url_apod = "https://api.nasa.gov/planetary/apod"
      
    
    params ={
        'api_key':'YwVmnhtmOzEe4RScNIqhfdW4fV9To1SzjTHNBkZg',
        'date':date,
        'hd':'true'
    }
    
    resp_msg = requests.get( url_apod,params=params)
    dict = resp_msg.json()
    return dict

    
def print_apod_info(image_url, image_path, image_size, image_sha256):
    """
    Prints information about the APOD

    :param image_url: URL of image
    :param image_path: Path of the image file saved locally
    :param image_size: Size of image in bytes
    :param image_sha256: SHA-256 of image
    :returns: None
    """ 
    print("         image url ="+image_url)
    print (" image hash:" + image_sha256)
    print("size:"+ str(image_size) + " bytes")
    print("     image path:"+image_path)
  
    
    return None

def download_apod_image(image_url,):
    """
    Downloads an image from a specified URL.
    :param image_url: URL of image
    :returns: Response message that contains image data
    """

    respons_e = requests.get(image_url)

    

    ima_path = path.join(argv[1], 'image.jpg')

    if respons_e.status_code == 200:
        with open (ima_path, 'wb') as fp:
            fp.write(respons_e.content)
        
        print('downloading image from nasa......Success')
    else:
        print("failed")
        

    return respons_e

def save_image_file(image_msg, image_path):
    """
    Extracts an image file from an HTTP response message
    and saves the image file to disk.

    :param image_msg: HTTP response message
    :param image_path: Path to save image file
    :returns: None
    """
    dir = path.join(argv[1], 'image.jpg') 
    image_msg = download_apod_image()
    
    
    with open (dir, 'wb') as fp:
            fp.write(image_msg)

    return None

def create_image_db(db_path):
    """
    Creates an image database if it doesn't already exist.

    :param db_path: Path of .db file
    :returns: None
    """
    
    myConnection = sqlite3.connect(db_path +'.db')
    myConnection.commit()
    myConnection.close()
    
    return 

def add_image_to_db(db_path, image_path, image_size, image_sha256):
    """
    Adds a specified APOD image to the DB.

    :param db_path: Path of .db file
    :param image_path: Path of the image file saved locally
    :param image_size: Size of image in bytes
    :param image_sha256: SHA-256 of image
    :returns: None
    """

    return #TODO

def image_already_in_db(db_path, image_sha256):
    """
    Determines whether the image in a response message is already present
    in the DB by comparing its SHA-256 to those in the DB.

    :param db_path: Path of .db file
    :param image_sha256: SHA-256 of image
    :returns: True if image is already in DB; False otherwise
    """ 
    db_cxn =sqlite3.connect(db_path)
    db_cursor = db_cxn.cursor()

    db_cursor.execute("SELECT id FROM image WHERE sha256 = '" + image_sha256 + "'")
    result = db_cursor.fetchall()
    db_cxn.close()

    if len(result) > 0:
        print("Image is already in cache.")
        return True
    else:
        print("New image not in cache.")
        return False



def set_desktop_background_image(image_path):
    """
    Changes the desktop wallpaper to a specific image.

    :param image_path: Path of image file
    :returns: None
    """
    return #TODO

main()