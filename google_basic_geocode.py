#!/usr/bin/env python

# Author: Marcos Lopez - Basic Google geocoding - 2009

import os, urllib


class getLatLong:
	def __init__(self):
		self.lat = ''
		self.long = ''
		self.loop = ''
		self.addr = ''

	def startSetting(self):
		#addr = raw_input('\nAddress or (Lat,Long):')
		addr = self.addr
		if addr <> '':
			url = ''
			if addr[0] == '(':
				center = addr.replace('(','').replace(')','')
				lat,lng = center.split(',')
				url = 'http://maps.google.com/maps?q=%s+%s' % (lat,lng)
			else:
				url = 'http://maps.google.com/?q=' + urllib.quote(addr) + '&output=js'
				xml = urllib.urlopen(url).read()

			if '<error>' in xml:
				print '\nGoogle cannot interpret the address'
			else:
				#strip lat lng
				lat,lng = 0.0,0.0
				center = xml[xml.find('{center')+10:xml.find('}',xml.find('{center'))]
				center = center.replace('lat:','').replace('lng:','')
				lat,lng = center.split(',')
				url = 'http://maps.google.com/maps?q=%s+%s' % (lat,lng)

			if url<>'':
				self.lat	= lat
				self.long = lng


	def GetLatitude(self):
		return self.lat

	def GetLong(self):
		return self.long





if __name__ == '__main__':
	cl = GetLatLong()
	cl.addr = '200 SE 1 st miami fl 33131'
	cl.StartSetting()

	print cl.lat
	print cl.long


