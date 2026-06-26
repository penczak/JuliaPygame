import pygame
import math
import Julia2

pygame.init()
pygame.display.set_caption("Julia Fractal Exploration")

SCREEN_W, SCREEN_H = 1080, 720
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

# cX, cY = 0.26, 0.0016
cX, cY = -0.8, 0.156
scale = 0.5

Julia2.init(pcX=cX, pcY=cY, pscale=scale, maxW=SCREEN_W, maxH=SCREEN_H)

moveX, moveY = 0.0, 0.0
zoom = 1.0

clock = pygame.time.Clock()

def make_surface():
	arr = Julia2.generateJuliaArray(zoom=zoom, moveX=moveX, moveY=moveY)
	arr = arr.swapaxes(0, 1)
	lowres_surface = pygame.surfarray.make_surface(arr)
	scaled_surface = pygame.transform.scale(lowres_surface, (SCREEN_W, SCREEN_H))
	return lowres_surface, scaled_surface

def increaseZoom(zoom, zoomOut=False):
	scale = 1.05
	# scale = math.e
	return zoom / scale if zoomOut else zoom * scale

def updateParameters(dcx, dcy):
	stepSize = 1.0 / (1200.0 * zoom)
	Julia2.updateParameters(dcx * stepSize, dcy * stepSize)

def translate(moveX, moveY, direction):
	stepSize = 1.0 / (12.0 * zoom)
	if direction == "LEFT":
		return (moveX - stepSize, moveY)
	elif direction == "RIGHT":
		return (moveX + stepSize, moveY)
	elif direction == "UP":
		return (moveX, moveY - stepSize)
	elif direction == "DOWN":
		return (moveX, moveY + stepSize)
	return (moveX, moveY)

surfaceImage, scaledSurface = make_surface()

running = True
needs_redraw = True

while running:

	changed = False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

	keys = pygame.key.get_pressed()

	if keys[pygame.K_k]:
		zoom = increaseZoom(zoom, zoomOut=False)
		changed = True

	if keys[pygame.K_j]:
		zoom = increaseZoom(zoom, zoomOut=True)
		changed = True

	if keys[pygame.K_LEFT]:
		moveX, moveY = translate(moveX, moveY, "LEFT")
		changed = True

	if keys[pygame.K_RIGHT]:
		moveX, moveY = translate(moveX, moveY, "RIGHT")
		changed = True

	if keys[pygame.K_UP]:
		moveX, moveY = translate(moveX, moveY, "UP")
		changed = True

	if keys[pygame.K_DOWN]:
		moveX, moveY = translate(moveX, moveY, "DOWN")
		changed = True

	if keys[pygame.K_d]:
		updateParameters(1, 0)
		changed = True

	if keys[pygame.K_a]:
		updateParameters(-1, 0)
		changed = True

	if keys[pygame.K_w]:
		updateParameters(0, 1)
		changed = True

	if keys[pygame.K_s]:
		updateParameters(0, -1)
		changed = True

	if changed:
		surfaceImage, scaledSurface = make_surface()
		needs_redraw = True

	if needs_redraw:
		screen.blit(scaledSurface, (0, 0))
		pygame.display.flip()
		needs_redraw = False

	clock.tick(120)

pygame.quit()
