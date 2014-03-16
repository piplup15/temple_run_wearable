import random
import diamond

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
		self.diamondMap= dict()

	def addRandomPath(self, numberRows, currentRow):
		self.cleanup(currentRow)
		columnBegin = int(random.random()*self.numColumns)
		columnEnd = int(random.random()*self.numColumns)
		path = self.depthFirstSearch((self.lastRow+1, columnBegin), (self.lastRow+numberRows, columnEnd))
		for newrow in range(self.lastRow+1, self.lastRow+1+numberRows):
			self.mapGrid[newrow] = []
			for col in range(self.numColumns):
				if (newrow, col) in path:
					self.mapGrid[newrow].append(1)
				else:
					self.mapGrid[newrow].append(0)
		self.verifySShape(self.lastRow+2,self.lastRow+numberRows-1)
		self.addDiamonds(self.lastRow+1, self.lastRow+numberRows)
		self.lastRow += numberRows
		numStraight = int(random.random()*10) + 5
		self.addAllBlocks(numStraight, currentRow)

	# for now, assume 3 rows
	def addFigureEightPath(self, numTimes, currentRow):
		self.cleanup(currentRow)
		index = 0
		for newrow in range(self.lastRow+1, self.lastRow+1+numTimes*5):
			if (index % 5) == 0 or (index % 5) == 4:
				self.mapGrid[newrow] = [0,1,0]
			elif (index % 5) == 1 or (index % 5) == 3:
				self.mapGrid[newrow] = [1,1,1]
			else:
				self.mapGrid[newrow] = [1,0,1]
			index += 1
		self.addDiamonds(self.lastRow+1, self.lastRow+numTimes*5)
		self.lastRow += numTimes*5
		numStraight = int(random.random()*10) + 5
		self.addAllBlocks(numStraight, currentRow)


	def addAllBlocks(self, numberRows, currentRow):
		self.cleanup(currentRow)
		for newrow in range(self.lastRow+1, self.lastRow+1+numberRows):
			self.mapGrid[newrow] = []
			for col in range(self.numColumns):
				self.mapGrid[newrow].append(1)
		#self.spawnSpikes((numberRows+1)/2, self.lastRow+1, self.lastRow+1+numberRows)
		self.addDiamonds(self.lastRow+1, self.lastRow+numberRows)
		self.lastRow += numberRows

	def addDiamonds(self, beginRow, endRow):
		for row in range(beginRow, endRow+1):
			putDiamond = random.random() > 0.5
			possibleDiamondLocations = []
			if putDiamond:
				for index in range(0,3):
					if self.mapGrid[row][index] == 1:
						possibleDiamondLocations.append(index)
				if len(possibleDiamondLocations) != 0:
					random.shuffle(possibleDiamondLocations)
					self.diamondMap[row] = diamond.Diamond(row, possibleDiamondLocations[0])

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
				if row in self.diamondMap.keys():
					del self.diamondMap[row]
				count += 1
			else:
				done = True
		self.firstRow += count

	def verifySShape(self, initialRow, finalRow):
		for row in range(initialRow, finalRow+1):
			if self.mapGrid[row] == [1,1,1]:
				if (self.mapGrid[row-1] == [0,0,1] and self.mapGrid[row+1] == [1,0,0]):
					self.mapGrid[row+1] = [1,1,0]
				elif (self.mapGrid[row-1] == [1,0,0] and self.mapGrid[row+1] == [0,0,1]):
					self.mapGrid[row+1] = [0,1,1]

	def spawnSpikes(self, number, lower, upper):
		while number > 0:
			row = int((upper-lower)*random.random()) + lower
			col = int(random.random()*3)
			if row-1 not in self.mapGrid.keys() or self.mapGrid[row-1][col] != 2:
				if row+1 not in self.mapGrid.keys() or self.mapGrid[row+1][col] != 2:
					self.mapGrid[row][col] = 2
					number -= 1