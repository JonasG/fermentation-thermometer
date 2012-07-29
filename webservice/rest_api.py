import webapp2

from google.appengine.ext import db
from google.appengine.api import users

class TemperatureReading(db.Model):
    temperature_celsius = db.FloatProperty()
    date = db.DateTimeProperty(auto_now_add=True)

def temperature_reading_key():
    return db.Key.from_path('Temperature', 'default_temperature_readings')

class RestApi(webapp2.RequestHandler):

    def get(self):
        result_html = '<html><head>'
        result_html += '<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>'
        result_html += '<script src="/js/highcharts.js" type="text/javascript"></script>'
        
        result_html += '<script type="text/javascript">\n'

        # result_html += 'var temperatures = [24.0, 23.5, 23.3, 23.8];\n'
        result_html += 'var temperatures = [];\n'

        result_html += "$.getJSON('/rest.json', function(data) { \
var items = []; \
\
$.each(data, function(key, val) { \
    if (key == 'temperature_celsius')\
    {\
        temperatures.push(val);\
    }\
}); \
\
});"

        result_html += "var timestamps = ['2012-07-28T12:00', '2012-07-28T12:01', '2012-07-28T12:02', '2012-07-28T12:03'];"

        result_html += "var chart1; \
        $(document).ready(function() { \
chart1 = new Highcharts.Chart({ \
chart: { \
renderTo: 'container', \
type: 'line' \
}, \
title: { \
text: \
'Temperature Readings' \
}, \
xAxis: \
{ \
categories: \
['Apples', \
'Bananas', \
'Oranges'] \
}, \
yAxis: \
{ \
title: \
{ \
text: \
'Fruit \
eaten' \
} \
}, \
series: \
[{ \
name: \
'Jane', \
data: temperatures \
}, \
{ \
name: \
'John', \
data: \
[5, \
7, \
3] \
}] \
}); \
});"

        result_html += '</script>'
        
        result_html += '</head><body>'
        result_html += '<div id="container" style="width: 100%; height: 400px"></div>'
        # result_html += '<table>'

        temperature_readings = db.GqlQuery("SELECT * "
                                           "FROM TemperatureReading "
                                           "WHERE ANCESTOR IS :1 "
                                           "ORDER BY date DESC",
                                           temperature_reading_key())

        # for entry in temperature_readings:
        # result_html += '<tr><td>' + str(entry.temperature_celsius) + '</td><td>' + str(entry.date) + '</td></tr>'

        # result_html += '</table>'
        result_html += '</body></html>'

        self.response.out.write(result_html)

    def post(self):
        temperature_in_celsius = float(self.request.get('temperature',
                                                 default_value=0.0))
        temperature_reading = TemperatureReading(parent=temperature_reading_key())
        temperature_reading.temperature_celsius = temperature_in_celsius
        temperature_reading.put()

class RealRestApi(webapp2.RequestHandler):

    def get(self):

        temperature_readings = db.GqlQuery("SELECT * "
                                           "FROM TemperatureReading "
                                           "WHERE ANCESTOR IS :1 "
                                           "ORDER BY date DESC LIMIT 10",
                                           temperature_reading_key())

        entry_strings = []
        for entry in temperature_readings:
            entry_strings.append('{temperature_celsius: ' +
                                 str(entry.temperature_celsius) + ', date: ' +
                                 str(entry.date) + '}')

        self.response.out.write(', '.join(entry_strings))

app = webapp2.WSGIApplication([('/', RestApi), ('/rest.json', RealRestApi)], debug=True)
