import pygame


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
	colors = [BLACK, GREEN, RED, BLUE]
	startPoints = [[x, 0, 100, 50] for x in range(0, 800, 100)]
	allPoints = [[item[0], item[1]+c, item[2], item[3]] for c in range(0, 200, 50) for item in startPoints]
	pointsWithColor = []
	for index in range(len(allPoints)):
		pointsWithColor.append([colors[index % 4], allPoints[index]])

def draw_bricks():
	isOver = True
	for color, point in pointsWithColor:
		if color != None:
			isOver = False
			pygame.draw.rect(screen, color, point)
	lines = [[[0, h], [800, h]] for h in range(50, 200, 50)]
	for item in lines:
		pygame.draw.line(screen, WHITE, item[0], item[1], 2)
	if isOver:
		setup_end_page("You win!")

def setup_paddle():
	global paddleX, paddleY, paddleSpeed, paddleWidth, paddleHeight
	paddleWidth = 100
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
	pygame.draw.rect(screen, BLACK, [paddleX, paddleY, paddleWidth, paddleHeight])

def setup_ball():
	global ballColor, ballX, ballY, ballXSpeed, ballYSpeed, ballRadius
	ballColor = GREEN
	ballRadius = 15
	ballX = screenWidth / 2
	ballY = screenHeight - ballRadius - paddleHeight


def brike_reflect():
	global ballColor, ballYSpeed
	if ballY <= 200 + ballRadius and ballY > 0:
		for index in range(len(pointsWithColor)):
			if pointsWithColor[index][0] != None:
				if ballX >= pointsWithColor[index][1][0] and \
				   ballX <= pointsWithColor[index][1][0] + pointsWithColor[index][1][2] and \
				   ballY <= pointsWithColor[index][1][1] + pointsWithColor[index][1][3] + ballRadius:
				   		ballColor = pointsWithColor[index][0]
				   		pointsWithColor[index][0] = None
				   		if pointsWithColor[index][1][1] > 0:
				   			pointsWithColor[index][1] = [pointsWithColor[index][1][0], \
				   										 pointsWithColor[index][1][1]-50, \
				   										 pointsWithColor[index][1][2], \
				   										 pointsWithColor[index][1][3]]
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
	elif ballY <= ballRadius or (ballY >= screenHeight - ballRadius - paddleHeight and \
		ballX >= paddleX and ballX <= paddleX + paddleWidth):
			ballYSpeed = -ballYSpeed
	elif ballY >= screenHeight - ballRadius:
		setup_end_page("You lose")

	ballX += ballXSpeed
	ballY += ballYSpeed
	pygame.draw.circle(screen, ballColor, [ballX, ballY], ballRadius)

def draw():
	draw_bricks()
	draw_paddle()
	draw_ball()

def display_text_helper(word, pos, isCenter=True):
	text = font.render(word, True, BLUE)
	bias = font.size(word)    # returns width and height
	if isCenter:
		newPos = [pos[0] - bias[0]/2, pos[1] - bias[1]/2]
	else:
		newPos = pos
	screen.blit(text, newPos)
	return [newPos, bias]

def is_mouse_in_button(button):
	"""
	Button is like this, [[startpointX, startpointY], [width, height]]
	return True if mouse in the button, else False
	"""
	point = button[0]
	width = button[1][0]
	height = button[1][1]
	pos = pygame.mouse.get_pos()
	x = pos[0]
	y = pos[1]
	if (x > point[0]) and (x < point[0] + width) and (y > point[1]) and (y < point[1] + height):
		return True
	else:
		return False

def setup_first_page():
	global startPos, exitPos, aboutPos
	displayWord1 = "Start"
	displayWord2 = "Exit"
	displayWord3 = "About"
	startPos = display_text_helper(displayWord1, [screenWidth/2, screenHeight/2 - textHeight])
	exitPos = display_text_helper(displayWord2, [screenWidth/2, screenHeight/2])
	aboutPos = display_text_helper(displayWord3, [screenWidth/2, screenHeight/2 + textHeight])

def setup_second_page():
	global easyPos, normalPos, hardPos, backtrackPos
	displayWord1 = "Choose Mode:"
	displayWord2 = "EASY"
	displayWord3 = "NORMAL"
	displayWord4 = "HARD"
	displayWord5 = "BACKTRACK"
	display_text_helper(displayWord1, [screenWidth/2, screenHeight/2 - 2*textHeight])
	easyPos = display_text_helper(displayWord2, [screenWidth/2, screenHeight/2 - textHeight])
	normalPos = display_text_helper(displayWord3, [screenWidth/2, screenHeight/2])
	hardPos = display_text_helper(displayWord4, [screenWidth/2, screenHeight/2 + textHeight])
	backtrackPos = display_text_helper(displayWord5, [screenWidth/2, screenHeight/2 + 2*textHeight])


def setup_third_page():
	displayWord1 = "This is a classic game --- breakout based on pygame."
	displayWord2 = "Contact me: loucq123@gmail.com"
	displayWord3 = "Click to backtrack."
	displayWord4 = "GOOD LUCK!"
	displayWord5 = "HAVE FUN!"
	displayWord6 = "Version 1.0416"
	displayWord7 = "Built by Lou Chaoqi"
	display_text_helper(displayWord1, [0, 0], False)
	display_text_helper(displayWord2, [0, textHeight], False)
	display_text_helper(displayWord3, [0, 2*textHeight], False)
	display_text_helper(displayWord4, [screenWidth/2, screenHeight/2 - textHeight/2])
	display_text_helper(displayWord5, [screenWidth/2, screenHeight/2 + textHeight/2])
	display_text_helper(displayWord6, [0, screenHeight-textHeight], False)
	display_text_helper(displayWord7, [530, screenHeight-textHeight], False)

def setup_end_page(message):
	displayWord1 = message
	displayWord2 = "Play again"
	displayWord3 = "Exit"
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			elif event.type == pygame.MOUSEBUTTONDOWN and is_mouse_in_button(againPos):
				setup_game()
			elif event.type == pygame.MOUSEBUTTONDOWN and is_mouse_in_button(exitPos):
				pygame.quit()
		display_text_helper(displayWord1, [screenWidth/2, screenHeight/2 - textHeight])
		againPos = display_text_helper(displayWord2, [screenWidth/2, screenHeight/2])
		exitPos = display_text_helper(displayWord3, [screenWidth/2, screenHeight/2 + textHeight])
		clock.tick(60)
		pygame.display.flip()

def instruction_pages():
	# Pos = [[startpointX, startpointY], [width, height]]
	global font, textHeight
	# Font(filename, size) -> Font
	# The size is the height of the font in pixels. 
	# If the filename is None the Pygame default font will be loaded.
	textHeight = 36
	font = pygame.font.Font(None, textHeight)
	displayInstructions = True
	page = 1
	while displayInstructions:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			elif page == 1 and event.type == pygame.MOUSEBUTTONDOWN and is_mouse_in_button(startPos):
				page = 2
			elif page == 1 and event.type == pygame.MOUSEBUTTONDOWN and is_mouse_in_button(exitPos):
				pygame.quit()
			elif page == 1 and event.type == pygame.MOUSEBUTTONDOWN and is_mouse_in_button(aboutPos):
				page = 3
			elif page == 3 and event.type == pygame.MOUSEBUTTONDOWN:
				page = 1
			elif page == 2:
				if event.type == pygame.MOUSEBUTTONDOWN and is_mouse_in_button(easyPos):
					newgame(1)
					return 
				elif event.type == pygame.MOUSEBUTTONDOWN and is_mouse_in_button(normalPos):
					newgame(2)
					return 
				elif event.type == pygame.MOUSEBUTTONDOWN and is_mouse_in_button(hardPos):
					newgame(3)
					return 
				elif event.type == pygame.MOUSEBUTTONDOWN and is_mouse_in_button(backtrackPos):
					page = 1
		screen.fill(BLACK)
		if page == 1:
			setup_first_page()
		elif page == 2:
			setup_second_page()
		elif page == 3:
			setup_third_page()
		clock.tick(60)
		pygame.display.flip()

def newgame(mode=1):
	global ballXSpeed, ballYSpeed
	game_init()
	setup_brikes()
	setup_paddle()
	setup_ball()
	if mode == 1:
		ballXSpeed = 1
		ballYSpeed = 2
	elif mode == 2:
		ballXSpeed = 2
		ballYSpeed = 3
	elif mode == 3:
		ballXSpeed = 4
		ballYSpeed = 5

def setup_game():
	global paddleX, paddleY, paddleSpeed
	newgame()
	instruction_pages()
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
		screen.fill(WHITE)
		draw()
		pygame.display.flip()
		clock.tick(60)
	pygame.quit()

if __name__ == '__main__':
	setup_game()