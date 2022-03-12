import pygame
import math
import copy

pygame.init()
screen = pygame.display.set_mode((500, 500))
run = True
start = []
coor_lst = []
s = False
sp = []

data = [
		[(0, 0, 255), [[0, 0], [4, 3]]], 
		[(255, 255, 0), [[1, 2], [6, 3]]], 
		[(255, 102, 0), [[1, 0], [6, 9]]], 
		[(255, 0, 0), [[4, 1], [8, 2]]], 
		[(0, 255, 0), [[5, 9], [8, 3]]], 
		[(0, 255, 255), [[1, 3], [6, 6]]],
		[(255, 102, 255), [[0, 2], [4, 4]]], 
		[(153, 0, 0), [[2, 4], [2, 7]]]
		]
status = [[0 for i in range(10)] for j in range(10)]

def update(screen):
	screen.fill((0, 0, 0))
	for i in data:
		pygame.draw.rect(screen, i[0], (i[1][0][0]*50, i[1][0][1]*50, 49, 49))
		pygame.draw.rect(screen, i[0], (i[1][-1][0]*50, i[1][-1][1]*50, 49, 49))
		for j in i[1][1:-1]:
			pygame.draw.rect(screen, i[0], (j[0]*50, j[1]*50, 49, 49))
		for j in i[1]:
			status[j[1]][j[0]] = 1

def check_start():
	global start, coor_lst, s, sp
	if pygame.mouse.get_pressed()[0]:
		coor = pygame.mouse.get_pos()
		coor = [math.floor(coor[0]/50), math.floor(coor[1]/50)]
		for i in data:
			if coor in i[1][1:-1]:
				index = data[data.index(i)][1].index(coor)
				for j in data[data.index(i)][1][index:-1]:
					status[j[1]][j[0]] = 0
				if start and i[0] == start[0]:
					data[data.index(i)][1] = [*data[data.index(i)][1][0:index+1], data[data.index(i)][1][-1]]
					start = i
					coor_lst = []
				elif start and s and i[0] != start[0]:
					data[data.index(i)][1] = [*data[data.index(i)][1][0:index], data[data.index(i)][1][-1]]
				else:
					data[data.index(i)][1] = [*data[data.index(i)][1][0:index+1], data[data.index(i)][1][-1]]
					start = i
					coor_lst = []
				s = True
			elif sp and sp == coor and s and sp in start[1]:
				for j in data[data.index(start)][1][1:-1]:
					status[j[1]][j[0]] = 0
				data[data.index(start)][1] = [data[data.index(start)][1][0], data[data.index(start)][1][-1]]
				coor_lst = []
				break
			elif (coor == i[1][-1] or coor == i[1][0]) and not s:
				for j in data[data.index(i)][1][1:-1]:
					status[j[1]][j[0]] = 0
				data[data.index(i)][1] = [data[data.index(i)][1][0], data[data.index(i)][1][-1]]
				coor_lst = []
				start = i
				sp = coor
				s = True
				break
		print(start)
	else:
		s = False
		#start = []

def check_linked():
	if s and pygame.mouse.get_pressed()[0]:
		coor = pygame.mouse.get_pos()
		coor = [math.floor(coor[0]/50), math.floor(coor[1]/50)]
		if (sp == start[1][0] and coor == start[1][-1]) or (sp == start[1][-1] and coor == start[1][0]):
			pass
		else:
			pass

def get_neighbour(i, j):
	return [[i+1, j], [i-1, j], [i, j+1], [i, j-1]]

def check_movement():
	if start and pygame.mouse.get_pressed()[0]:
		coor = pygame.mouse.get_pos()
		coor = [math.floor(coor[0]/50), math.floor(coor[1]/50)]
		if not coor_lst: coor_lst.append(coor)
		if start and coor in get_neighbour(*coor_lst[-1]) and not status[coor[1]][coor[0]]:
			coor_lst.append(coor)
			pygame.draw.rect(screen, start[0], (coor[0]*50, coor[1]*50, 50, 50))
			data[data.index(start)][1].insert(len(data[data.index(start)][1])-1, coor)
		else:
			status[coor[1]][coor[0]] = 0


while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	update(screen)
	check_start()
	check_movement()
	check_linked()
	pygame.display.update()