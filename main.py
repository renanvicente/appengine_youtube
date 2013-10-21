import jinja2
import os
import urllib
import webapp2
import cgi

from apiclient.discovery import build

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

REGISTRATION_INSTRUCTIONS = """
    You must set up a project and get an API key to run this code. <br> 
    Steps: <br>
    1.  Visit <a href="https://developers.google.com/youtube/v3/code_samples/python_appengine#create-api-key"
    target='_top'>https://developers.google.com/youtube/v3/code_samples/python_appengine#create-api-key</a> 
    for instructions on setting up a project and key. Make sure that you have 
    enabled the YouTube Data API (v3) for your project. 
    You do not need to set up OAuth credentials for this project. <br>
    2.  Once you have obtained a key, search for the text 'REPLACE_ME' in the 
    code and replace that string with your key. <br> 
    3.  Click the reload button above the output container to view the new output. """

# Set API_KEY to the "API key" value from the "Access" tab of the
# Google APIs Console http://code.google.com/apis/console#access
# Please ensure that you have enabled the YouTube Data API and Freebase API
# for your project.
API_KEY = "AIzaSyCR5In4DZaTP6IEZQ0r1JceuvluJRzQNLE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class MainPage(webapp2.RequestHandler):
    def get(self):
      if API_KEY == "REPLACE_ME":
        self.response.write(REGISTRATION_INSTRUCTIONS)
      else:
        self.response.headers['Content-type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())

    def post(self):
      QUERY_TERM = self.request.get('search')
      youtube = build(
        YOUTUBE_API_SERVICE_NAME, 
        YOUTUBE_API_VERSION, 
        developerKey=API_KEY
      )
      search_response = youtube.search().list(
        q=QUERY_TERM,
        part="id,snippet",
        maxResults=25
      ).execute()
  
      videos = []
      
  
      for search_result in search_response.get("items", []):
        videos.append(search_result)
      videos.pop(0)
  
      template_values = {
        'videos': videos
      }
  
      self.response.headers['Content-type'] = 'text/html'
      template = JINJA_ENVIRONMENT.get_template('index.html')
      self.response.write(template.render(template_values))


        
class ShowVideo(webapp2.RequestHandler):

    def get(self):
        v = self.request.get('v')
        youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=API_KEY
      )
        search_response = youtube.search().list(
          relatedToVideoId=v,
          part="id,snippet",
          maxResults=10,
          type="video"
        ).execute()
    
        videos = []
    
    
        for search_result in search_response.get("items", []):
          videos.append(search_result)
    
        template_values = {
          'videos': videos,
          'touch': v
        }
    
        self.response.headers['Content-type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

        

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/search', ShowVideo),
], debug=True)

