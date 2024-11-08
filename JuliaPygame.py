import pygame
from PIL import Image, ImageFilter
import math
import numpy as np
import Julia

pygame.init()
pygame.display.set_caption('Julia Fractal Exploration 🚀')

w, h = 1080, 720
screen = pygame.display.set_mode((w, h))

cX, cY = 0.26, 0.0016 # spiral four leaf clover values
# cX, cY = -0.8, 0.156
scale = 0.1

# Julia.init will set your configuration values in Julia.py for generateJuliaBitmap() to use
Julia.init(pcX = cX, pcY = cY, pscale = scale)

moveX, moveY = 0, 0 # initial translation values
zoom = 1 # initial zoom value

image = Julia.generateJuliaBitmap(zoom = zoom)
mode = image.mode
size = image.size
data = image.tobytes()
surfaceImage = pygame.image.fromstring(data, size, mode)

def newJulia():
	image = Julia.generateJuliaBitmap(zoom = zoom, moveX = moveX, moveY = moveY)
	mode = image.mode
	size = image.size
	data = image.tobytes()
	surfaceImage = pygame.image.fromstring(data, size, mode)

	return surfaceImage

def increaseZoom(zoom, zoomOut=False):
	if not zoomOut:
		newZoom = zoom * math.exp(1)
	else:
		newZoom = zoom / math.exp(1)
	return newZoom

def translate(moveX, moveY, direction):
	# step size is inversely proportional to zoom so that when you are very zoomed in
	# 	the translation is proportionally small. high zoom => small step. 
	stepSize = 1/(3*zoom)

	if direction == 'LEFT':
		return (moveX-stepSize, moveY)
	elif direction == 'RIGHT':
		return (moveX+stepSize, moveY)
	elif direction == 'UP':
		return (moveX, moveY-stepSize)
	elif direction == 'DOWN':
		return (moveX, moveY+stepSize)

infoLevel = 1
crosshairActive = False

def drawInfoText():
	FONT_SIZE = 24
	myFont = pygame.font.SysFont(pygame.font.get_default_font(), FONT_SIZE)

	y_offset = 10
	x_offset = 10
	if crosshairActive:
		# at int(w/2) draw a black line and at int(w/2)+1 draw a white line etc.
		crosshairSurface = pygame.Surface((1,h))
		pygame.draw.line(crosshairSurface, (0,0,0), (0,0), (0,h))
		screen.blit(crosshairSurface, (int(w/2),0))
		crosshairSurface = pygame.Surface((w,1))
		pygame.draw.line(crosshairSurface, (0,0,0), (0,0), (w,0))
		screen.blit(crosshairSurface, (0,int(h/2)))
		crosshairSurface = pygame.Surface((1,h))
		pygame.draw.line(crosshairSurface, (255,255,255), (0,0), (0,h))
		screen.blit(crosshairSurface, (int(w/2)+1,0))
		crosshairSurface = pygame.Surface((w,1))
		pygame.draw.line(crosshairSurface, (255,255,255), (0,0), (w,0))
		screen.blit(crosshairSurface, (0,int(h/2)+1))
	# infoLevel: 0 -> none ; 1 -> zoom and position ; 2 -> zoom and position with many decimals
	if infoLevel == 0:
		return
	elif infoLevel == 1:
		# "C = (X, Y)" with a drop shadow
		textSurface = myFont.render('C = ({0}, {1})'.format("{:.3f}".format(cX), "{:.3f}".format(cY)), True, (0, 0, 0))
		screen.blit(textSurface, (x_offset,y_offset))
		textSurface = myFont.render('C = ({0}, {1})'.format("{:.3f}".format(cX), "{:.3f}".format(cY)), True, (255, 255, 255))
		screen.blit(textSurface, (x_offset-1,y_offset-1))
		y_offset += FONT_SIZE # move down the screen after each line of text by FONT_SIZE

		# "Zoom: X.XX" with a drop shadow
		textSurface = myFont.render('Zoom: {0}'.format("{:.2f}".format(zoom)), True, (0, 0, 0))
		screen.blit(textSurface, (x_offset,y_offset))
		textSurface = myFont.render('Zoom: {0}'.format("{:.2f}".format(zoom)), True, (255, 255, 255))
		screen.blit(textSurface, (x_offset-1,y_offset-1))
		y_offset += FONT_SIZE # move down the screen after each line of text by FONT_SIZE

		# "Position: (X, Y)" with a drop shadow
		textSurface = myFont.render('Position: ({0}, {1})'.format("{:.2f}".format(moveX), "{:.2f}".format(moveY)), True, (0, 0, 0))
		screen.blit(textSurface, (x_offset,y_offset))
		textSurface = myFont.render('Position: ({0}, {1})'.format("{:.2f}".format(moveX), "{:.2f}".format(moveY)), True, (255, 255, 255))
		screen.blit(textSurface, (x_offset-1,y_offset-1))
	elif infoLevel == 2:
		# "C = (X, Y)" with a drop shadow
		textSurface = myFont.render('C = ({0}, {1})'.format("{:.8f}".format(cX), "{:.8f}".format(cY)), True, (0, 0, 0))
		screen.blit(textSurface, (x_offset,y_offset))
		textSurface = myFont.render('C = ({0}, {1})'.format("{:.8f}".format(cX), "{:.8f}".format(cY)), True, (255, 255, 255))
		screen.blit(textSurface, (x_offset-1,y_offset-1))
		y_offset += FONT_SIZE # move down the screen after each line of text by FONT_SIZE

		# "Zoom: e^X = X" with a drop shadow
		textSurface = myFont.render('Zoom: e^{0} = {1}'.format(int(math.log(zoom)), "{:.12f}".format(zoom)), True, (0, 0, 0))
		screen.blit(textSurface, (x_offset,y_offset))
		textSurface = myFont.render('Zoom: e^{0} = {1}'.format(int(math.log(zoom)), "{:.12f}".format(zoom)), True, (255, 255, 255))
		screen.blit(textSurface, (x_offset-1,y_offset-1))
		y_offset += FONT_SIZE

		# "Position: (X, Y)" with a drop shadow
		textSurface = myFont.render('Position: ({0}, {1})'.format("{:.24f}".format(moveX), "{:.24f}".format(moveY)), True, (0, 0, 0))
		screen.blit(textSurface, (x_offset,y_offset))
		textSurface = myFont.render('Position: ({0}, {1})'.format("{:.24f}".format(moveX), "{:.24f}".format(moveY)), True, (255, 255, 255))
		screen.blit(textSurface, (x_offset-1,y_offset-1))

### game loop ###

# after any change to the generateJuliaBitmap parameters, redraw the bitmap by calling newJulia(). 

running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
			elif event.key == pygame.K_k:
				# 'k' to zoom in
				zoom = increaseZoom(zoom, zoomOut=False)
				surfaceImage = newJulia()
			elif event.key == pygame.K_j:
				# 'j' to zoom out
				zoom = increaseZoom(zoom, zoomOut=True)
				surfaceImage = newJulia()
			elif event.key == pygame.K_LEFT:
				# left arrow to move left
				(moveX, moveY) = translate(moveX, moveY, 'LEFT')
				surfaceImage = newJulia()
			elif event.key == pygame.K_RIGHT:
				# right arrow to move right
				(moveX, moveY) = translate(moveX, moveY, 'RIGHT')
				surfaceImage = newJulia()
			elif event.key == pygame.K_UP:
				# up arrow to move up
				(moveX, moveY) = translate(moveX, moveY, 'UP')
				surfaceImage = newJulia()
			elif event.key == pygame.K_DOWN:
				# down arrow to move down
				(moveX, moveY) = translate(moveX, moveY, 'DOWN')
				surfaceImage = newJulia()
			elif event.key == pygame.K_i:
				# 'i' to adjust info level
				infoLevel += 1
				if infoLevel > 2:
					infoLevel = 0
			elif event.key == pygame.K_c:
				crosshairActive = not crosshairActive

	# scale up the bitmap to be the size of the screen
	surfaceImage = pygame.transform.scale(surfaceImage, (w,h))
	# put the bitmap onto the screen
	screen.blit(surfaceImage, (0,0))

	drawInfoText()

	# update the screen
	pygame.display.flip()