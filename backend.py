import utils
import cfg

""" main user class """
class User:
	id_user = -1
	id_server = -1

	# fish points
	points = 0

	# identity (suffix to "fisher-")
	identity = ""

	# number of unique fish caught
	dex_count = 0

	# fix data not in acceptable ranges
	def limit_fix(self):
		self.id_user = int(self.id_user)

		if self.points < 0:
			self.points = 0
		
		if self.dex_count < 0:
			self.points = 0
	
	# create a new user and optionally retrieve from database
	def __init__(self, member):
		
		# get a user object from a member arg
		self.id_server = member.guild.id
		self.id_user = int(member.id)

		try:
			conn_info = utils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor()

			# Retrieve object

			cursor.execute(
                "SELECT  {}, {}, {} FROM users WHERE id_user = %s AND id_server = %s".format(
                    cfg.col_points,
                    cfg.col_identity,
					cfg.col_dex_count
				), (
					self.id_user,
					self.id_server
				))
			result = cursor.fetchone()

			if result != None:
				# Record found: apply the data to this object
				self.points = result[0]
				self.identity = result[1]
				self.dex_count = result[2]

		finally:
			# Clean up the database handles.
			cursor.close()
			utils.databaseClose(conn_info)
	
	def persist(self):
		try:
			conn_info = utils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor()

			# Save the object.
			cursor.execute(
				"REPLACE INTO users({}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s)".format(
					cfg.col_id_user,
					cfg.col_id_server,
					cfg.col_points,
					cfg.col_identity,
					cfg.col_dex_count,
				), (
					self.id_user,
					self.id_server,
					self.points,
					self.identity,
					self.dex_count,
				))

			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			utils.databaseClose(conn_info)

""" for storing dex entries """
class DexEntry:
	id_user = -1
	id_server = -1
	id_fish = ""

	# keeps track of how many of a species theyve caught. probably gonna remain un-used for now
	catch_count = 0

	def __init__(
		self,
		member = None,
		id_fish = None,
	):
		self.id_fish = id_fish
		self.id_user = member.id
		self.id_server = member.guild.id

		try:
			conn_info = utils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor()
			
			# Retrieve object
			cursor.execute("SELECT {} FROM dex_entries WHERE {} = %s AND {} = %s AND {} = %s".format(
				cfg.col_catch_count,
				cfg.col_id_user,
				cfg.col_id_server,
				cfg.col_id_fish,
				
			), (
				self.id_user,
				self.id_server,
				self.id_fish
			))
			result = cursor.fetchone()

			if result != None:
				# Record found: apply the data to this object.
				self.catch_count = result[0]
		
		finally:
			# Clean up the database handles.
			cursor.close()
			utils.databaseClose(conn_info)
	
	def persist(self):
		try:
			conn_info = utils.databaseConnect()
			conn = conn_info.get('conn')
			cursor = conn.cursor()
			
			# Retrieve object
			cursor.execute(
				"REPLACE INTO dex_entries({}, {}, {}, {}) VALUES (%s, %s, %s, %s)".format(
					cfg.col_id_user,
					cfg.col_id_server,
					cfg.col_id_fish,
					cfg.col_catch_count,
				), (
					self.id_user,
					self.id_server,
					self.id_fish,
					self.catch_count
				))
			
			conn.commit()
		finally:
			# Clean up the database handles.
			cursor.close()
			utils.databaseClose(conn_info)
