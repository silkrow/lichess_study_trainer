from chapter import Chapter

class Study:
	'''
	Class: Study
	Attributes:
		chapters		: list of Chapter objects
		name			: string, name of the study
		study_id		: string, study_id for api calls
		author			: string, author of this study
		-_- possibly other meta data to keep track of
	'''

	def __init__(self, study_id, author, name):
		self.study_id = study_id
		self.pgn = ""
		self.chapters = []
		self.author = author
		self.name = name



	def id(self):
		return self.study_id

	def add_chapter(self, chapter):
		self.chapters.append(chapter)

	def total_chapters(self):
		return len(self.chapters)