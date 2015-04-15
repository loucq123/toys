import pygame
import random


def game_init():
	global BLACK, WHITE, GREEN, RED, BLUE, screenWidth, screenHeight, screen, clock
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	GREEN = (0, 255, 0)
	RED = (255, 0, 0)
	BLUE = (0, 0, 255)
	pygame.init()
	screenWidth = 800
	screenHeight = 600
	screen = pygame.display.set_mode([screenWidth, screenHeight])
	pygame.display.set_caption("Breakout")
	clock = pygame.time.Clock()

def setup_brikes():
	global pointsWithColor
	colors = [WHITE, GREEN, RED, BLUE]
	startPoints = [[x, 0, 100, 50] for x in range(0, 800, 100)]
	allPoints = [[item[0], item[1]+c, item[2], item[3]] for c in range(0, 200, 50) for item in startPoints]
	pointsWithColor = []
	for index in range(len(allPoints)):
		pointsWithColor.append([colors[index % 4], allPoints[index]])

def draw_bricks():
	for color, point in pointsWithColor:
		if color != None:
			pygame.draw.rect(screen, color, point)
	lines = [[[0, h], [800, h]] for h in range(50, 200, 50)]
	for item in lines:
		pygame.draw.line(screen, BLACK, item[0], item[1], 2)

def setup_paddle():
	global paddleX, paddleY, paddleSpeed, paddleWidth, paddleHeight
	paddleWidth = 90
	paddleHeight = 20
	paddleX = screenWidth/2 - paddleWidth/2
	paddleY = 580
	paddleSpeed = 0

def draw_paddle():
	global paddleX
	if paddleX <= 0:
		paddleX = 0
	if paddleX >= screenWidth - paddleWidth:
		paddleX = screenWidth - paddleWidth
	paddleX += paddleSpeed 
	pygame.draw.rect(screen, WHITE, [paddleX, paddleY, paddleWidth, paddleHeight])

def setup_ball():
	global ballColor, ballX, ballY, ballXSpeed, ballYSpeed, ballRadius, lowerBrikes
	lowerBrikes = pointsWithColor[24:]
	ballColor = GREEN
	ballRadius = 15
	ballX = screenWidth / 2
	ballY = screenHeight - ballRadius - paddleHeight
	ballXSpeed = random.randrange(4)
	ballYSpeed = random.randrange(4)

def brike_reflect():
	global ballColor, ballYSpeed
	'''
	if ballY <= 200 + ballRadius:
		for color, brike in pointsWithColor:
			if color != None:
				if ballX >= brike[0] and ballX <= brike[0] + brike[2] and ballY <= brike[1] + brike[3] + ballRadius:
					ballColor = color
					color = None
					if brike[1] > 0:
						brike = [brike[0], brike[1]-50, brike[2], brike[3]]
					ballYSpeed = - ballYSpeed'''
	if ballY <= 200 + ballRadius and ballY > 0:
		for index in range(len(pointsWithColor)):
			if pointsWithColor[index][0] != None:
				if ballX >= pointsWithColor[index][1][0] and \
				   ballX <= pointsWithColor[index][1][0] + pointsWithColor[index][1][2] and \
				   ballY <= pointsWithColor[index][1][1] + pointsWithColor[index][1][3] + ballRadius:
				   		ballColor = pointsWithColor[index][0]
				   		pointsWithColor[index][0] = None
				   		if pointsWithColor[index][1][1] > 0:
				   			pointsWithColor[index][1] = [pointsWithColor[index][1][0], pointsWithColor[index][1][1]-50, \
				   										 pointsWithColor[index][1][2], pointsWithColor[index][1][3]]
				   		ballYSpeed = -ballYSpeed
				   		break
def draw_ball():
	# circle(Surface, color, pos, radius, width=0)
	global ballX, ballY, ballXSpeed, ballYSpeed
	ballX += ballXSpeed
	ballY += ballYSpeed
	brike_reflect()
	if ballX <= ballRadius or ballX >= screenWidth - ballRadius:
		ballXSpeed = -ballXSpeed
	elif ballY <= ballRadius or ballY >= screenHeight - ballRadius:
		ballYSpeed = -ballYSpeed
	ballX += ballXSpeed
	ballY += ballYSpeed
	pygame.draw.circle(screen, ballColor, [ballX, ballY], ballRadius)

def draw():
	draw_bricks()
	draw_paddle()
	draw_ball()

def setup_game():
	global paddleX, paddleY, paddleSpeed
	game_init()
	setup_brikes()
	setup_paddle()
	setup_ball()
	done = False
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					paddleSpeed = -5
				elif event.key == pygame.K_RIGHT:
					paddleSpeed = 5
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					paddleSpeed = 0
				elif event.key == pygame.K_RIGHT:
					paddleSpeed = 0
		screen.fill(BLACK)
		draw()
		pygame.display.flip()
		clock.tick(60)
	pygame.quit()


if __name__ == '__main__':
	setup_game()