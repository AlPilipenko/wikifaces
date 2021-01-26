import os
class Config():
    "To protect from malware and hackers"
    SECRET_KEY = os.environ.get('WF_PASS')
    UPLOAD_FOLDER = 'wikifaces/static/temp_images/'
    MAX_CONTENT_LENGTH = 1920 * 1920
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
    TEMPLATES_AUTO_RELOAD = True
    SESSION = {}
