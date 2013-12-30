import os

import jinja2
import webapp2

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.db import stats

jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class TemperatureReading(db.Model):
    temperature_celsius = db.FloatProperty()
    date = db.DateTimeProperty(auto_now_add=True)

def temperature_reading_key():
    return db.Key.from_path('Temperature', 'default_temperature_readings')

class WebPage(webapp2.RequestHandler):

    def get(self):
        template = jinja_environment.get_template('status.html')
        self.response.out.write(template.render())

        temperature_readings = db.GqlQuery("SELECT * "
                                           "FROM TemperatureReading "
                                           "WHERE ANCESTOR IS :1 "
                                           "ORDER BY date DESC",
                                           temperature_reading_key())

    def post(self):
        temperature_in_celsius = float(self.request.get('temperature',
                                                        default_value=0.0))
        temperature_reading = TemperatureReading(parent=temperature_reading_key())
        temperature_reading.temperature_celsius = temperature_in_celsius
        temperature_reading.put()

class RestApi(webapp2.RequestHandler):

    def get(self):
        display_count = 96

        temperature_readings_last_two_days = db.GqlQuery("SELECT * "
                                                         "FROM TemperatureReading "
                                                         "WHERE ANCESTOR IS :1 "
                                                         "ORDER BY date DESC "
                                                         "LIMIT " + str(display_count),
                                                         temperature_reading_key())

        entry_strings = []
        for entry in temperature_readings_last_two_days:
            entry_strings.append('"' + str(entry.date) + '": ' +
                                 str(entry.temperature_celsius))

        self.response.content_type = 'application/json'
        self.response.out.write('{' + ', '.join(reversed(entry_strings)) + '}')

app = webapp2.WSGIApplication([('/', WebPage), ('/rest.json', RestApi)],
                              debug=False)
