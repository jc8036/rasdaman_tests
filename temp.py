# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib
import urllib2
import matplotlib.pyplot as plt
import numpy as np

lat = 56.
lon = 56.

url = 'http://localhost:8080/rasdaman/ows'
query = 'for i in (one_thousand) return encode(i[Lat(%s),Long(%s)],"csv")' % (str(lon), str(lat))
data = urllib.urlencode({'query': query})
request = urllib2.Request(url, data)
response_string = urllib2.urlopen(request).read()[1:-1]
response_list = [float(i) for i in response_string.split(',')]
plt.plot(response_list)
print (np.array(response_list)).mean()*365