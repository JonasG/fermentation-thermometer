import urllib2
import sys
import threading

def setup_timer():
    one_hour_in_seconds = 3600.0
    t = threading.Timer(one_hour_in_seconds, read_and_store_temp)
    t.start()

def read_and_store_temp():
    current_temp = read_current_temp()
    sys.stdout.write('Current temp: ' + str(current_temp) + ' C\n')
    push_temp_to_datastore(current_temp)

    setup_timer()

def read_current_temp():
    # TODO: we should read this from a sensor.
    return 10

def push_temp_to_datastore(current_temp):
    req = urllib2.Request(url='http://fermentation-temperature.appspot.com/',
                        data='temperature=' + str(current_temp))
    f = urllib2.urlopen(req)
    sys.stdout.write('Data from storage: ' + f.read() + '\n')

if __name__ == '__main__':
    setup_timer()
