'''
Author: Josh Eastman
Updated: 02/16/18
Version 1.0.0
Description: Based on link_image_handling from TwitterArtBot. Used to deal with the link provided
by PRAW and download the images.
'''

import urllib.request
import os
import logging

#If a link does not have .jpg at the end, add it
def ifNoExtensionAdd(url):
    if url[-4:] != '.jpg' and url[-4:] != '.png':
        new_url = url + '.jpg' 
        return new_url
    else:
        return url

def handleLink(url):
    #Check if imgur or reddit
    #To-Do: Add more sites for better compatiblity
    try:
        #Checks for the various states the imgur url can come in
        if url.find('i.imgur') != -1:
            fixed_url = ifNoExtensionAdd(url)
            image = fixed_url[20:]  #for imgur image, strip everything but id and .jpg
            return [True, fixed_url, image] #boolean for whether or not it failed
        
        elif url.find('imgur') != -1:
            jpg_url = ifNoExtensionAdd(url)       
            fixed_url = jpg_url[:8] + 'i.' + jpg_url[8:]  #Add i to imgur link if it's not there.          
            image = fixed_url[20:]  #for imgur image, strip everything but id and .jpg
            return [True, fixed_url, image] #boolean for whether or not it failed

        elif url.find('redd.it') != -1:
            fixed_url = ifNoExtensionAdd(url)            
            image = fixed_url[18:]  #for imgur image, strip everything but id and .jpg
            return [True, fixed_url, image] #boolean for whether or not it failed   
        else:
            #If not from a supported url, return False
            return [False, url, 'Not supported:']
        
    except:
        return[False, 'Unidentified error during handleLink', url]

#Moves the downloaded image to whever you would like to store it.
def moveImage(image_name, image_directory):
    file_location =  image_directory + image_name
    
    try:
        os.rename(image_name, file_location)
        
        return [True, file_location, 'Moved image to ' + file_location]
    except:
        os.remove(image_name)
        logging.warning(image_name + ' was deleted.')
        return [False, file_location, 'Failed to move file']

#Finds the image from the url and downloads it.
def getImage(url, image_location, image_directory):
    try:
        urllib.request.urlretrieve(url, image_location)
        logging.info(image_location + ' was downloaded.')       
        image_moved = moveImage(image_location, image_directory)

        if(image_moved[0]):
            logging.info(image_location + ' was moved to ' + image_directory)
            return [True, image_moved[1], 'Obtained and moved image to image folder']           
        else:
            return [False, url, image_moved[2] + ' | ' + image_moved[1]]
        
    except:
        return [False, url, 'Failed to get image']
       
#download image for each submission
def downloadAll(submission, IMAGE_DIRECTORY):
    link_result = handleLink(submission.url)
    #Make sure the handleLink didn't fail, the move onto getting the image
    if(link_result[0]):
        image_result = getImage(link_result[1], link_result[2], IMAGE_DIRECTORY)
        logging.info(link_result[1] + ' | ' + link_result[2])
    else:
        logging.error(link_result[1] + ' | ' + link_result[2])
    