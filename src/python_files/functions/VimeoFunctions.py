from flask import url_for
from python_files.classes.Constants import CONSTANTS
import vimeo
from vimeo.auth import GrantFailed
from vimeo.exceptions import VideoUploadFailure

vimeoClient = vimeo.VimeoClient(
    key = CONSTANTS.VIMEO_CLIENT_ID,
    secret = CONSTANTS.VIMEO_CLIENT_SECRET,
    token = None
)

def authorise_vimeo(redirectUrl):
    vimeo_authorization_url = vimeoClient.auth_url(
        ['private'],           #SCOPES
        redirectUrl,           #REDIRECT_URL
        'Not a JWT'            #STATE
    )
    
    return vimeo_authorization_url

def get_vimeo_data(code):
    try:
        token, user, scope = vimeoClient.exchange_code(code, url_for('userBP.vimeoTesting', _external = True))
        print(token)
        print(user)
        print(scope)
        return token, user, scope
    except GrantFailed as error:
        print(error)
        return None, None, None

def vimeo_upload(videoFilePath):
    try:
        videoURI = vimeoClient.upload(videoFilePath)

        # Get the metadata response from the upload and log out the Vimeo.com url
        videoData = vimeoClient.get(videoURI + '?fields=link').json()
    except VideoUploadFailure as error:
        print(error)



