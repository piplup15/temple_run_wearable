import random

class MapGrid():
	def __init__(self, rows, columns):
		self.mapGrid = dict()
		for row in range(rows):
			self.mapGrid[row] = []
			for column in range(columns):
				self.mapGrid[row].append(1)
		self.numRows = rows
		self.numColumns = columns
		self.firstRow = 0
		self.lastRow = row

	def addRandomPath(self, numberRows, currentRow):
		self.cleanup(currentRow)
		columnBegin = int(random.random()*self.numColumns)
		columnEnd = int(random.random()*self.numColumns)
		print columnBegin
		print columnEnd
		path = self.depthFirstSearch((self.lastRow+1, columnBegin), (self.lastRow+numberRows, columnEnd))
		for newrow in range(self.lastRow+1, self.lastRow+1+numberRows):
			self.mapGrid[newrow] = []
			for col in range(self.numColumns):
				if (newrow, col) in path:
					self.mapGrid[newrow].append(1)
				else:
					self.mapGrid[newrow].append(0)
		self.lastRow += numberRows
		numStraight = int(random.random()*10) + 5
		self.addAllBlocks(numStraight, currentRow)

	def addAllBlocks(self, numberRows, currentRow):
		self.cleanup(currentRow)
		for newrow in range(self.lastRow+1, self.lastRow+1+numberRows):
			self.mapGrid[newrow] = []
			for col in range(self.numColumns):
				self.mapGrid[newrow].append(1)
		self.lastRow += numberRows

	def depthFirstSearch(self, startPos, endPos):
		boundsX = [startPos[0], endPos[0]]
		path = []
		return self.explore(startPos, endPos, path, boundsX)

	def explore(self, pos, target, path, boundsX):
		x,y = pos
		path.append(pos)
		if (pos == target):
			return path
		successors = []
		if (x >= boundsX[0] and x <= boundsX[1] and y+1 >= 0 and y+1 < self.numColumns):
			successors.append((x, y+1)) 
		if (x >= boundsX[0] and x <= boundsX[1] and y-1 >= 0 and y-1 < self.numColumns):
			successors.append((x, y-1))
		if (x-1 >= boundsX[0] and x-1 <= boundsX[1] and y >= 0 and y < self.numColumns):
			successors.append((x-1, y)) 
		if (x+1 >= boundsX[0] and x+1 <= boundsX[1] and y >= 0 and y < self.numColumns):
			successors.append((x+1, y))
		random.shuffle(successors)
		for successor in successors:
			if successor not in path:
				val = self.explore(successor, target, list(path), boundsX)
				if val != False:
					return val
		return False

	def cleanup(self, currentRow):
		done = False
		count = 0
		row = self.firstRow
		while not done:
			if row + count + 2 < currentRow:
				del self.mapGrid[row+count]
				count += 1
			else:
				done = True
		self.firstRow += count