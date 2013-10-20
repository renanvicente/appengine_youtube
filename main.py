import wsgiref.handlers
import webapp2
import urllib2
import json


class MainPage(webapp2.RequestHandler):
    def get(self):
        url = "http://gdata.youtube.com/feeds/api/standardfeeds/top_rated?v=2&alt=jsonc"
        data = urllib2.urlopen(url)
        parse_data = json.load(data)

        self.response.out.write('<html><body>')

        for item in parse_data['data']['items']:
            self.response.out.write('<p>Title: %s </p>' % item['title'])
            self.response.out.write('<p>Category: %s </p>' % item['category'])
            self.response.out.write('<p>ID: %s </p>' % item['id'])
            self.response.out.write('<p>Rating: %f </p>' % item['rating'])
            self.response.out.write('<p>URL: %s </p>' % item['player']['default'])

        self.response.write('</body></html>')

def main():
    application = webapp2.WSGIApplication(
            [('/', MainPage)],
            debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
