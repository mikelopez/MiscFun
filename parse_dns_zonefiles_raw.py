import os

# Author: Marcos Lopez - Parse raw dns zone files on Bind9
# Publicizing for self reference purposes only, but feel free to use and/or modify it
# Written for Digiport and originally designed to clean up tab/space combinations on 
# configuration syntax to later be parsed by other tasks

class ParseDNSFiles:


	testfile = ''
	append_list = []

	output_to_file = []
	
	def start_it(self):
		for i in open(self.testfile, 'r').readlines():
			if not ';' in i and \
				not 'TTL' in i and \
				not 'SOA' in i and \
				not 'Serial' in i and \
				not 'Refresh' in i and \
				not 'Retry' in i and \
				not 'Expire' in i and \
				not 'Negative' in i and \
				not 'NS' in i and \
				not len(i.replace('\n','')) < 3:
				
				#print i.replace('\n','')
				
				#self.append_list.append(i.replace('\n','').replace('\r','').replace('\t','  '))
				first_replace = i.replace('\n','').replace('\r','').replace('\t',' ')
				replacespaces = first_replace.replace('          ',' ').replace('         ',' ').replace('        ',' ').replace('       ',' ').replace('      ',' ').replace('     ',' ').replace('    ',' ').replace('   ',' ').replace('  ',' ')

				self.append_list.append(replacespaces)


			else:
				self.output_to_file.append(i.replace('\n',''))
				


	
	
	
	def remove_spaces_from_list(self):
		for i in self.append_list:
			print i.split(' ')

		
	def create_new_file(self):
		for i in self.append_list:
			strs = ''
			for x in i.split(' '):
				strs += '%s\t' % (x)
			self.output_to_file.append(strs)


		openwr = open('/home/user/dev/portal/dnszones/parseddns/%s' % (self.testfile), 'a')
		for i in self.output_to_file:
			openwr.write('%s\n' % (i))






