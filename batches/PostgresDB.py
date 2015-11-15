#!/usr/bin/python
import psycopg2
import types


class PostgresDB:


	"""
		MySQLDB implements MySQLdb python library with specific methods and the use of a property file for connection
		Version : 0.5
	"""

	conf = []	
	def __init__ (self, properties):

		#Sets property file
		self.properties_file = open(properties)
		self.parsePropertyFile()



	def connect (self):
		try:
			self.db_connection =  psycopg2.connect("dbname='"+self.conf[1]+"' user='"+self.conf[2]+"' host='"+self.conf[0]+"' password='"+self.conf[3]+"'")
		
		except:
			print "I am unable to connect to the database"
			
		self.cursor = self.db_connection.cursor()

	def disconnect (self):
		self.db_connection.close()

	def executeQuery (self, queries):
		"""
			function executeQuery
			- IN : self, queries (String or List)
			- OUT : void
			
			This function allows to execute one or various queries. If the queries argument is a list, all quereies are committed together
		"""
		if type(queries) == types.StringType :
			
			try :
				self.cursor.execute(queries)
				self.db_connection.commit()
			except :
				self.db_connection.rollback()
				
		elif type(queries) == types.ListType :
			try :
				
				for query in queries :
					self.cursor.execute (query)

				self.db_connection.commit ()
			except :
				self.db_connection.rollback()
				
				
	def parsePropertyFile (self):

		"""
			parameters order :

			- Host
			- DB name
			- User
			- Password
		"""

		lines = self.properties_file.readlines ()

		i=0
		for line in lines :
			self.conf.append(line.rstrip('\n').split('=')[1])

	def getConf (self):
		return self.conf

	def setConf (self, new_conf):
		self.conf = new_conf

	def getDBConnection(self):
		return self.db_connection

	def setDBConnection(self, new_db_connection):
		self.db_connection = new_db_connection

	def rollback (self) :
		self.db_connection.rollback()
