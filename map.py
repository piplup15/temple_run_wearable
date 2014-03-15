import random

class Map():
	def __init__(self, rows, columns):
		self.map = dict()
		for row in rows:
			for column in columns:
				self.map[row, column] = 1
		self.lastRow = row

	def addRow(self):
		for column in columns:
			val = random.random()
			if val > 0.8 and self.map[(self.lastRow, column)] == 1