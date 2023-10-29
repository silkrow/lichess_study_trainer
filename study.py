from chapter import Chapter

class Study:
	'''
	Class: Study
	Attributes:
		chapters		: list of Chapter objects
		index			: int, the index of this study in Trainer.studies list
		name			: string, name of the study
		id				: string, study_id for api calls
		author			: string, author of this study
		-_- possibly other meta data to keep track of
	'''

	def __init__(self, study_id, author, name):
		self.id = study_id
		self.pgn = ""
		self.chapters = []
		self.author = author
		self.name = name
		self.index = None

	def get_id(self):
		return self.id

	def get_name(self):
		return self.name

	def add_chapter(self, chapter):
		self.chapters.append(chapter)

	def total_chapters(self):
		return len(self.chapters)

	def get_chapters(self):
		return self.chapters

	def clear_chapters(self):
		self.chapters = []

	def assign_index(self, index):
		self.index = index

	def get_index(self):
		return self.index