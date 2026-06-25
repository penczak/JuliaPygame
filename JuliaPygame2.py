import pygame
import math
import Julia2

pygame.init()
pygame.display.set_caption('Julia Fractal Exploration')

w, h = 1080, 720
screen = pygame.display.set_mode((w, h))

cX, cY = 0.26, 0.0016
scale = 0.5   # you can increase once performance is better

Julia2.init(pcX=cX, pcY=cY, pscale=scale)

moveX, moveY = 0.0, 0.0
zoom = 1.0

def make_surface():
    arr = Julia2.generateJuliaArray(zoom=zoom, moveX=moveX, moveY=moveY)
    # arr is (h, w, 3), but pygame.surfarray.make_surface wants (w, h, 3)
    arr = arr.swapaxes(0, 1)
    return pygame.surfarray.make_surface(arr)

surfaceImage = make_surface()

def increaseZoom(zoom, zoomOut=False):
    return zoom / math.e if zoomOut else zoom * math.e

def translate(moveX, moveY, direction):
    stepSize = 1 / (3 * zoom)
    if direction == 'LEFT':
        return (moveX - stepSize, moveY)
    elif direction == 'RIGHT':
        return (moveX + stepSize, moveY)
    elif direction == 'UP':
        return (moveX, moveY - stepSize)
    elif direction == 'DOWN':
        return (moveX, moveY + stepSize)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            changed = False

            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_k:
                zoom = increaseZoom(zoom, zoomOut=False)
                changed = True
            elif event.key == pygame.K_j:
                zoom = increaseZoom(zoom, zoomOut=True)
                changed = True
            elif event.key == pygame.K_LEFT:
                moveX, moveY = translate(moveX, moveY, 'LEFT')
                changed = True
            elif event.key == pygame.K_RIGHT:
                moveX, moveY = translate(moveX, moveY, 'RIGHT')
                changed = True
            elif event.key == pygame.K_UP:
                moveX, moveY = translate(moveX, moveY, 'UP')
                changed = True
            elif event.key == pygame.K_DOWN:
                moveX, moveY = translate(moveX, moveY, 'DOWN')
                changed = True

            if changed:
                surfaceImage = make_surface()

    # scale the low-res fractal to full screen
    scaled = pygame.transform.scale(surfaceImage, (w, h))
    screen.blit(scaled, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
