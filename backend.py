import cfg

from queries import SqlQuery

""" main user class """
class User:
	id_user = -1
	id_server = -1

	display_name = ""

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
		self.display_name = member.display_name

		query = SqlQuery(
			table = cfg.tab_users,
			target_cols = (
				cfg.col_points,
				cfg.col_identity,
				cfg.col_dex_count,
				cfg.col_display_name,
			),
			key_cols = (cfg.col_id_user, cfg.col_id_server),
			key_vals = (self.id_user, self.id_server)
		)
		
		result_arr = query.select()
		
		if (len(result_arr) != 0):
			result = result_arr[0]

			if result != None:
				# Record found: apply the data to this object
				self.points = result[0]
				self.identity = result[1]
				self.dex_count = result[2]
	
	def persist(self):
		SqlQuery(
			table = cfg.tab_users,
			target_cols = (
				cfg.col_id_user, 
				cfg.col_id_server, 
				cfg.col_points, 
				cfg.col_identity, 
				cfg.col_dex_count,
				cfg.col_display_name,
			),
			target_vals = (
				self.id_user,
				self.id_server,
				self.points,
				self.identity,
				self.dex_count,
				self.display_name,
			)
		).replace()

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

		query = SqlQuery(
			table = cfg.tab_dex_entries,
			target_cols = [cfg.col_catch_count],
			key_cols = (cfg.col_id_user, cfg.col_id_server, cfg.col_id_fish),
			key_vals = (self.id_user, self.id_server, self.id_fish)
		)

		result_arr = query.select()
		
		if (len(result_arr) != 0):
			result = result_arr[0]

			if result != None:
				# Record found: apply the data to this object.
				self.catch_count = result[0]
	
	def persist(self):
		SqlQuery(
			table = cfg.tab_dex_entries,
			target_cols = (cfg.col_id_user, cfg.col_id_server, cfg.col_id_fish, cfg.col_catch_count),
			target_vals = (self.id_user, self.id_server, self.id_fish, self.catch_count)
		).replace()
		
""" timeline class which updates clocks/date/weather """
class Timeline:
	id_server = -1

	clock = 0
	weather = cfg.weather_default
	day = 0

	time_lasttick = 0

	global_catch_count = 0

	def __init__(self, id_server = None):
		if(id_server != None):
			self.id_server = id_server

			result_arr = SqlQuery(
				table = cfg.tab_timelines,
				target_cols = (
					cfg.col_time_lasttick,
					cfg.col_clock,
					cfg.col_weather,
					cfg.col_day,
					cfg.col_global_catch_count,
				),
				key_cols = [cfg.col_id_server],
				key_vals = [id_server],
			).select()

			if (len(result_arr) != 0):
				result = result_arr[0]

				self.time_lasttick = result[0]
				self.clock = result[1]
				self.weather = result[2]
				self.day = result[3]
				self.global_catch_count = result[4]

	def persist(self):
		SqlQuery(
			table = cfg.tab_timelines,
			target_cols = (
				cfg.col_id_server,
				cfg.col_time_lasttick,
				cfg.col_clock,
				cfg.col_weather,
				cfg.col_day,
				cfg.col_global_catch_count,
			),
			target_vals = (
				self.id_server,
				self.time_lasttick,
				self.clock,
				self.weather,
				self.day,
				self.global_catch_count,
			)
		).replace()