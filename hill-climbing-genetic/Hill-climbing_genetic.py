# Problem 2 Urban planning
# use hill climbing and genetic algorithms to determine the ideal location of industry, commerce, and residential sections a city.
# ---------------------------------------------------------------
# Symbols and rules:
# X:former toxic waste site.
#	Industrial zones within 2 tiles take a penalty of -10.
#	Commercial and residential zones within 2 tiles take a penalty of -20.
#	You cannot build directly on a toxic waste site.
# S:scenic view.
#	Residential zones within 2 tiles gain a bonus of 10 points.
#	If you wish, you can build on a scenic site but it destroys the view.
# 0...9:how difficult it is to build on that square.
#		You will receive a penalty of that many points to put anything on that square.
# You will have to place industrial, residential, and commercial tiles on the terrain.
# Industrial tiles benefit from being near other industry.  For each industrial tile within 2, there is a bonus of 3 points.
# Commercial sites benefit from being near residential tiles.  For each residential tile within 3 squares, there is a bonus of 5 points.
# However, commercial sites do not like competition.  For each commercial site with 2 squares, there is a penalty of 5 points.
# Residential sites do not like being near industrial sites.  For each industrial site within 3 squares there is a penalty of 5 points.
# However, for each commercial site with 3 squares there is a bonus of 5 points.
# --------------------------------------------------------------
# --------------------------------------------------------------
# package
from time import time
from random import sample,seed,random,randint
from copy import copy
import os
# --------------------------------------------------------------

class UrbanPlaning(object):

	def __init__(self):
		self._ori_map = []
		# the original map, input as a 2-dimensional list
		#		e.g. X,1,2,4
		#			 3,4,S,3
		#			 6,0,2,3
		#			 input as [['X','1','2','4'],['3','4','S','3'],['6','0','2','3']]
		self._Ind = int()
		# number of indudstrial zones
		self._Com = int()
		# number of commercial zones
		self._Res = int()
		# number of residential zones
		self._aval_pos = []
		# position of available tile (not X), e.g [(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3)]
		self._X_pos = []
		# position of X, e.g. [(0,0)]
		self._S_pos = []
		# position of S, e.g. [(0,2)]

	def printsample(self,file_path):
		self.get_para(file_path)
		print('The original map is:')
		self.print_map(self._ori_map)
		print('There should be %d industrial tiles, %d commercial tiles, %d residential tiles\n' %(self._Ind,self._Com,self._Res))


	def planing_cases(self,file_path,maxtime = 9.9,method = 'hill_climbing',fname="_answer"):
		'''
			get printable outcome and out put to a file. method could be "hill_climbing" or "genetic".
			Input:
			file_path
			method
		'''
		# check method
		if method not in ('hill_climbing','genetic'):
			raise AttributeError("invalid method %s" % method)
		else:
			self.get_para(file_path)
			print('Start planing, using %s' % method)
			if method == 'hill_climbing':
				spent_time,best_score,best = self.hill_climbing(maxtime)
			else:
				spent_time,best_score,best = self.genetic(maxtime)

			print('The best score for this case: %d. \nWe fisrt achieved this score at %f seconds.' %(best_score,spent_time))
			print('The final map is:')
			final_map = self.get_map(best)
			self.print_map(final_map)
		#if not os.path.exists('answers'):
		#	os.mkdir('answers')
			doc_path = method +fname+'.txt'
			self.write_doc(spent_time,best_score,final_map,doc_path)
			print('the result has been written in %s' %doc_path)



	def write_doc(self,spent_time,best_score,final_map,doc_path):
		'''
			write outcomes to a file.
		'''
		with open(doc_path, 'w') as f:
			f.write('The best score for this case: %d. \nWe first achieved this score at %f seconds.\n' %(best_score,spent_time))
			for row in final_map:
				for element in row:
					f.write(element+'\t')
				f.write('\n')
			f.write('Here,I means industrial tiles, C means commercial tiles and R means residential tiles.\n')

	def hill_climbing(self,maxtime = 10):
		'''
			given original_map, use hill climbing with restarts.
			Input:
			maxtime: maxtime for the program to run
			Output:
			best_score: The score for this map
			spent_time: At what time that score was first achieved, in seconds
			final_map: The map, with the various industrial, commercial, and residential sites marked as I, C, R
		'''
		try:
			start = time()
			#set seed
			seed(start)
			# best score ever get
			best_score = -float('inf')
			# number of industrial + number of commercial + number of residential
			total = self._Ind + self._Com + self._Res
			# position with highest score
			best = []
			while time() - start < maxtime:
				current = self.ran_allocate()
				current_score = self.score(current)
				while True:
					for i in range(total):
						better,better_score = self.choose(current,i)
						if len(better) == 0:
							continue
						current = sample(better,1)[0]

					if better_score <= current_score:
						break
					current_score = better_score

				if current_score > best_score:
					best_score = current_score
					best = current
					stop = time()

			spent_time = stop - start
			if len(best) != total:
				raise AssertionError('missing something')
			return spent_time,best_score,best
		except FileNotFoundError as e:
			print('file not exist:',e)
		except ValueError as e:
			raise

	def genetic(self, maxtime = 10, max_population = 250):
		'''
			Use genetic algorithm, run for 10s, default max population is 250.
			Output:
			best_score: The score for this map
			spent_time: At what time that score was first achieved, in seconds
			best: The map, with the various industrial, commercial, and residential sites marked as I, C, R
		'''
		try:
			start = time()
			seed(start)
			best_score = -float('inf')
			# get population
			population = []
			scores = [] # scores for every individual
			# randomly generate population
			for _ in range(max_population):
				population.append(self.ran_allocate())
			# calculate scores
			scores = [self.score(pos) for pos in population]
			# begin loop
			# run maxtime
			while time()-start < maxtime:
				# calculate scores
				# select reproduction
				# calculate probabilites, using roulette
				# select top 10% survive
				new_population = [ population[index] for index in self.findtop(scores,int(0.1*max_population))]
				# Crossing over and mutation
				for _ in range(max_population):
					parent1,parent2 = self.pick_parents(scores,population,roulette=False)
					new_population.append(self.cross_over(parent1,parent2))
				# culling 10%
				new_scores = [self.score(pos) for pos in new_population]
				x = []
				x = self.findbottom(new_scores,int(0.1*max_population))
				ind = set(range(len(new_population))).difference(set(x))
				population = [new_population[index] for index in ind]
				# update scores
				scores = [self.score(pos) for pos in population]
				if max(scores) > best_score:
					spent_time = time() - start
					best_score = max(scores)

			best = population[scores.index(best_score)]
			return spent_time, best_score, best
		except FileNotFoundError as e:
			print('file not exist:',e)
		except ValueError as e:
			raise
		except AssertionError as e:
			raise

	def roulettegenetic(self, maxtime = 10, max_population = 250):
		'''
			Use genetic algorithm, run for 10s, default max population is 250.
			Output:
			best_score: The score for this map
			spent_time: At what time that score was first achieved, in seconds
			best: The map, with the various industrial, commercial, and residential sites marked as I, C, R
		'''
		try:
			start = time()
			seed(start)
			best_score = -float('inf')
			# get population
			population = []
			scores = [] # scores for every individual
			# randomly generate population
			for _ in range(max_population):
				population.append(self.ran_allocate())
			# calculate scores
			scores = [self.score(pos) for pos in population]
			# begin loop
			# run maxtime
			while time()-start < maxtime:
				# calculate scores
				# select reproduction
				# calculate probabilites, using roulette
				# select top 10% survive
				new_population = [ population[index] for index in self.findtop(scores,int(0.1*max_population))]
				# Crossing over and mutation
				for _ in range(max_population):
					parent1,parent2 = self.pick_parents(scores,population,roulette=True)
					new_population.append(self.cross_over(parent1,parent2))
				# culling 10%
				new_scores = [self.score(pos) for pos in new_population]
				x = []
				x = self.findbottom(new_scores,int(0.1*max_population))
				ind = set(range(len(new_population))).difference(set(x))
				population = [new_population[index] for index in ind]
				# update scores
				scores = [self.score(pos) for pos in population]
				if max(scores) > best_score:
					spent_time = time() - start
					best_score = max(scores)

			best = population[scores.index(best_score)]
			return spent_time, best_score, best
		except FileNotFoundError as e:
			print('file not exist:',e)
		except ValueError as e:
			raise
		except AssertionError as e:
			raise

	def get_para(self,file_path):
		'''
			given file where the first 3 lines are the number of industrial, commercial, and residential locations (respectively), read the original map, number of industrial, commercial and residential zones.
			Input: text of the file
			Output:
			ori_map: a 2-dimentional list.
				e.g. X,1,2,4
					 3,4,S,3
					 6,0,2,3
					 input as [['X','1','2','4'],['3','4','S','3'],['6','0','2','3']]
			Ind: number of industrial zones
			Com: number of commercial zones
			Res: number of residence zones
			tz: number of total available zones (X occupied zones not included)
			aval_pos: position of available tile (not X), e.g [(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3)]
		'''
		lines = []
		with open(file_path) as fp:
			for line in fp.readlines():
				lines.append(line.strip())
		self._Ind = int(lines[0])
		self._Com = int(lines[1])
		self._Res = int(lines[2])
		self._ori_map = [row.split(',') for row in lines[3:]]
		self._X_pos = []
		self._S_pos = []
		for i,row in enumerate(self._ori_map):
			for j,element in enumerate(row):
				if element != 'X':
					self._aval_pos.append((i,j))
				else:
					self._X_pos.append((i,j))
				if element == 'S':
					self._S_pos.append((i,j))
		tz = len(self._aval_pos)
		# check duplicates
		self._X_pos = set(self._X_pos)
		self._S_pos = set(self._S_pos)
		# check if numbers of zones to be planed are more than available ones
		if self._Ind + self._Com + self._Res > tz:
			raise ValueError('number of indudstrial, commercial and residential zones are more than available zones')


	def ran_allocate(self):
		'''
			randomly allocate Industrial, commercial and residencial zones.
			Input:
			Output:
			position: a list, included industrial, commercial and residencial positions.
		'''
		# choose industrial zone,commercial zone and redidential zone
		position = sample(self._aval_pos, self._Ind+self._Com+self._Res)
		return  position

	def score(self,position):
		'''
			given the current position of industrial, commercial and residential zones, calculate its score
			Input:
			position: list of cordinates
			Output:
			score: total score
		'''
		I,C,R = self.getICR(position)
		# calculate difficulty
		diff = 0
		penalty = 0
		bonus = 0
		# check if scenary is occupied
		flag = 0

		for cor in position:
			if self._ori_map[cor[0]][cor[1]] != 'S':
				diff += int(self._ori_map[cor[0]][cor[1]])
			else:
				flag = 1
		for cor in I:
			penalty += 10 * len(self.find(cor,self._X_pos,2))
			bonus += 3 * (len(self.find(cor,I,2)) -1 )
		for cor in C:
			penalty += 20 * len(self.find(cor,self._X_pos,2))
			penalty += 5 * (len(self.find(cor,C,2)) - 1)
			bonus += 5 * len(self.find(cor,R,3))
		for cor in R:
			penalty += 20 * len(self.find(cor,self._X_pos,2))
			penalty += 5 * len(self.find(cor,I,3))
			bonus += 5 * len(self.find(cor,C,3))
			if flag == 0:
				bonus += 10 * len(self.find(cor,self._S_pos,2))
		score = bonus - diff - penalty
		return score

	def roulette(self,scores):
		'''
			calculate the accumulated probabilites.
			Input:
			scores: list
			Output:
			prob: list
		'''
		p = 0
		mini = min(scores)
		scorescopy = [(s - mini) for s in copy(scores)]
		s = sum(scorescopy)
		if s == 0:
			s = len(scorescopy)
			return  [1/s for score in scorescopy]
		prob = []
		for score in scorescopy:
			p += score/ s
			prob.append(p)
		prob[-1] = 1
		return prob

	def get_map(self,position):
		'''
			change postion to a final map
			Input: position
			Output: final_map
		'''
		I,C,R = self.getICR(position)
		final_map = self._ori_map.copy()
		for cor in I:
			final_map[cor[0]][cor[1]] = 'I'
		for cor in C:
			final_map[cor[0]][cor[1]] = 'C'
		for cor in R:
			final_map[cor[0]][cor[1]] = 'R'
		return final_map

	def pick_parents(self,scores,population,roulette = False):
		'''select two parents for genetic algorithm to corss over. Output: parent1, parent2'''
		# choose parent with probabilites
		p1 = random()
		p2 = random()
		parenta = []
		parentb = []
		if roulette:
			prob = self.roulette(scores)
			for i, weight in enumerate(prob):
				p1 -= weight
				p2 -= weight
				if p1 < 0:
					parenta = population[i]
				if p2 < 0:
					parentb = population[i]
				if len(parenta) * len(parentb) != 0:
					return parenta, parentb
		else:
			parenta,parentb = sample(population,2)
			return parenta,parentb



	def getICR(self,position):
		'''get I, C, R form a postion list'''
		I = position[:self._Ind].copy()
		C = position[self._Ind:(self._Ind+self._Com)].copy()
		R = position[-self._Res:].copy()
		return I, C, R

	def cross_over(self,parenta,parentb,mrate = 0.05):
		'''cross over two parents, with 0.05 chance to mutate and get a new individual'''
		I1,C1,R1 = self.getICR(parenta)
		I2,C2,R2 = self.getICR(parentb)

		Ipos = set(I1).union(set(I2))
		Cpos = set(C1).union(set(C2))
		Rpos = set(R1).union(set(R2))

		newI = sample(Ipos,self._Ind)
		newC = sample(Cpos,self._Com)
		newR = sample(Rpos,self._Res)

		# check if there is duplicates
		for i,cor in enumerate(newC):
			if cor in newI:
				aval = Cpos.difference(set(newC+newI))
				if len(aval) != 0:
					newC[i] = sample(aval,1)[0]
				else:
					aval = set(copy(self._aval_pos)).difference(set(newI+newC))
					newC[i] = sample(aval,1)[0]

		for i,cor in enumerate(newR):
			if cor in (newI + newC):
				aval = Rpos.difference(set(newI+newC+newR))
				if len(aval) != 0:
					newR[i] = sample(aval,1)[0]
				else:
					aval = set(copy(self._aval_pos)).difference(set(newI+newC+newR))
					newR[i] = sample(aval,1)[0]

		new = newI+newC+newR
		# mutate
		if random() < mrate:
			i = randint(0,len(new)-1)
			aval = set(copy(self._aval_pos)).difference(set(new))
			new[i] = sample(aval,1)[0]

		if len(set(new)) != len(new):
			raise AssertionError

		return new


	def findtop(self,scores,k):
		'''
			given a list, e.g. scores, find the top k in the list and return their index.
			Output:
			top: a list of index
		'''
		tops = scores[:k]
		tops.sort(reverse = True)
		top = []
		for i,score in enumerate(scores[k:]):
			if score > tops[-1]:
				tops[-1] = score
				tops.sort(reverse = True)
		# keep 5 differnent index in top
		for s in tops:
			idx = scores.index(s)
			while idx in top:
				idx = scores[idx+1:].index(s)+idx+1
			top.append(idx)
		if len(top) != k:
			raise AssertionError
		return top

	def findbottom(self,scores,k):
		'''
			given a list, e.g. scores, find the bottom k in the list and return their index.
			Output:
			bottom: a list of index
		'''
		bottoms = scores[:k]
		bottoms.sort()
		bottom = []
		for i,score in enumerate(scores[k:]):
			if score < bottoms[-1]:
				bottoms[-1] = score
				bottoms.sort()
		# keep 5 differnent index in top
		for s in bottoms:
			idx = scores.index(s)
			while idx in bottom:
				idx = scores[idx+1:].index(s)+idx+1
			bottom.append(idx)
		if len(bottom) != k:
			raise AssertionError
		return bottom

	def print_map(self,a_map):
		'''
			print goodlooking map
		'''
		for row in a_map:
			s = ''
			for element in row:
				s = s + element + '\t'
			print(s+'\n')



	def choose(self,current,num):
		'''
			from all successors, choose the one with highest score
			Input:
			current: current position, which is a list
			num: the number of point which we are going to move. e.g. (1,2) means the third point in second section(Commercial zones)
			Output:
			answer: a list of highest successors
			better: the better score the new answer get, or the same old score
		'''
		answer = []
		move = current[num] # get the point which would be moved
		scores = []  # store all the scores of possible moves
		positions = [] # store all the possible moves
		better = self.score(current)
		available = list(set(self._aval_pos).difference(set(current)))
		aval = self.find(move,available,1)
		if len(aval) == 0:
			return answer,better
		for cor in aval:
			position = copy(current)
			position[num] = cor
			positions.append(position)
			scores.append(self.score(position))
		# if better = max, we will allow it to move, which is sideway hill climbing.
		if better >= max(scores):
			return answer,better
		else:
			better = max(scores)
			for i,sc in enumerate(scores):
				if sc == better:
					answer.append(positions[i])
			return answer,better



	def mdistance(self,x,y):
		'''
			calculate the mahatten distance between two point x,y
			Input:
			x: tuple, cordinates of x. e.g. (0,0)
			y: tuple, cordinates of y. e.g. (0,1)
			Output:
			d: mahatten distance of x,y e.g. 1
		'''
		d = abs(x[0]-y[0]) + abs(x[1]-y[1])
		return d

	def find(self,x,Pos,md):
		'''
			find if there is point in Pos list that is md tiles within x
			Input:
			x: cordinate tuple of x
			Pos: list of cordinates
			md: int, max distence
			Output:
			points : a list, all the point that qualified
		'''
		points = []
		for cor in Pos:
			if self.mdistance(x,cor) <= md:
				points.append(cor)
		return points

# now, we'll define our main function which actually starts the planing
def main(args):
    print("START")
    ######################################################
    ##     could use either direct or indirect path     ##
    ##          please put your file path here          ##
    ######################################################
    file_path = str(input('please input your file path, could be either direct or indirect path.\n>')).strip()
    ######################################################
    UP = UrbanPlaning()
    # print the original case
    UP.printsample(file_path)
    #--------------
    choice = str(input('please input A for hill climbing or B for genetic algorithm.\n>')).strip()
    method = {'a':'hill_climbing','b':'genetic'}
    UP.planing_cases(file_path,method=method[choice.lower()])
    #---------------
    # if you would like to run both, please remove the '#' of following lines and add '#' to the lines between two long dash.
    #UP.planing_cases(file_path,method='hill_climbing')
    #UP.planing_cases(file_path,method='genetic')



if __name__ == "__main__":
    import sys
    main(sys.argv)

