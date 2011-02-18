# mike 2009 - this script will read from the dns zone files, 
# and import the data to the database
# this is an initial script, for first time setups 
# read dns from zonefiles and import to database
#
# DEPRECATED - needs refactoring... 

import sys,os, logging, re
sys.path.append('/home/project/dev/')
os.environ['DJANGO_SETTINGS_MODULE'] ='project.settings'

from django.core.management import setup_environ
from portal import settings
setup_environ(settings)

from pyipaddr.models import *
from services.models import *
from tickets.models import *

import ipaddr
import os
from time import strftime
import datetime

class ReadDNS:

	zonefile_directory = ''
	logfile = '/home/project/dev/project/LOG_ReadDNS.log'

	def logit(self, data):
		nows = datetime.datetime.now()
		datestr = '%s/%s/%s %s:%s:%s' % (
			str(nows.month),
			str(nows.day),
			str(nows.year),
			str(nows.hour),
			str(nows.minute),
			str(nows.second),
		)


		o=open(self.logfile,'a')
		o.write('%s : %s\n' % (datestr, data))
		o.close()



	# write from zonefile to DB
	def insert_ptr_records(self):

		for i in os.listdir(self.zonefile_directory):

			# get the db.filename
			# if theres ptr in line, 2get data split by Tabs
			# check sample zonefile for return list elements0
			if 'db.' in i:
				zonefile = i
				zonefileget = DNSZonefiles.objects.filter(name=str(zonefile))
				if len(zonefileget) > 0:
					zonefileget_obj = zonefileget[0]
					for x in open('%s/%s' % (self.zonefile_directory,zonefile), 'r').readlines():
						# get the ptr through each line of ZONEFILE
						if 'PTR' in x and 'IN' in x and not 'localhost' in x and not ';' in x:
							self.logit('LINEDAT = %s' % (x))
							data_split = x.split('\t')
							ip_zone = zonefile.split('.')
							ip_customer = '%s.%s.%s.%s' % (
								ip_zone[3],ip_zone[2],ip_zone[1],
								data_split[0].replace('\t','').replace('\n','')
							)
							hostget=Hosts.objects.filter(address=ip_customer)
							cust=Customer.objects.filter(name='None')[0]
							if len(hostget) > 0:
								cust=hostget[0].subnet.customer

							else:
								self.logit('No Hosts in Database for %s' % (ip_customer))
								print 'No Hosts in Database for %s' % (ip_customer)
								

							# first check if the shits there
							dns_check = DNS.objects.filter(
								record_type='PTR', zonefile=zonefileget_obj, points_to=data_split[3].replace('\t','').replace('\n',''),
								entryname = data_split[0].replace('\t','').replace('\n','')
							)
							if len(dns_check) > 0:
								self.logit('!ReadDNSZones.py - insert_ptr_records() : Skipping Add PTR entryname=%s, points_to=%s for Customer: %s' % (
										data_split[0].replace('\t','').replace('\n',''),
										data_split[3].replace('\t','').replace('\n',''),cust
									)
								)
							else:
								dnsin = DNS(
									record_type='PTR',zonefile=zonefileget_obj,
									priority='0',
									points_to=data_split[3].replace('\t','').replace('\n',''),
									entryname=data_split[0].replace('\t','').replace('\n',''),
									customer=cust,updateflag='n'
								)
								dnsin.save()
								




				else:
					self.logit('No zonefile in Database for %s' % (zonefile))
					print 'No zonefile Database row for %s' % (zonefile)
	
			

	def insert_a_records(self):
		for i in os.listdir(self.zonefile_directory):
			if 'db.' in i:
				zonefile = i
				zonefileget = DNSZonefiles.objects.filter(name=str(zonefile))

				if len(zonefileget) > 0:
					zonefile_obj = zonefileget[0]
					
					for x in open('%s/%s' % (self.zonefile_directory, zonefile), 'r').readlines():
						#self.logit(x)
						if 'A' in x and 'IN' in x and not 'localhost' in x and not ';' in x and not 'CNAME' in x and not 'SOA' in x:
							print 'LINEDAT = %s' % (x)
							data_split = x.split('\t')
							ipaddr=data_split[3].replace('\t','').replace('\n','')
							hostget = Hosts.objects.filter(address=str(ipaddr))
							cust = Customer.objects.filter(name='None')[0]

							if len(hostget) > 0:
								cust = hostget[0].subnet.customer
							else:
								self.logit('No Hosts in Database for %s' % (ipaddr))
								print 'No Hosts in database for %s' % (ipaddr)

							if not '.' in str(data_split[0].replace('\t','').replace('\n','')):
								dns_check = DNS.objects.filter(
									record_type='A', zonefile=zonefile_obj,
									points_to=data_split[3].replace('\t','').replace('\n',''),
									entryname=data_split[0].replace('\t','').replace('\n','')
								)
								if len(dns_check) > 0:
									self.logit('!ReadDNSZones.py - insert_a_records() : Skipping Add "A" entryname=%s, points_to=%s for Customer: %s' % (
											data_split[0].replace('\t','').replace('\n',''),
											data_split[3].replace('\t','').replace('\n',''),cust
										)
									)
								else:
	
									dnsin = DNS(
										record_type='A', zonefile=zonefile_obj, 
										priority=0,
										points_to=data_split[3].replace('\t','').replace('\n',''),
										entryname=data_split[0].replace('\t','').replace('\n',''),
										customer=cust, updateflag='n'
									)
									dnsin.save()

							else:
								self.logit('no dots in entryname sorry! :P')


				else:
					self.logit('No Zonefile in Database for %s' % (zonefile))
					print 'No Zonefile in Database for %s' % (zonefile)


			




