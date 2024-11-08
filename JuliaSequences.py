import Julia
import math
import os
# import numpy as np
# import colorsys

# rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
# hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

def createZoomSequence(numFrames, zoomSpeed=1, zoomRes=1, moveX=0, moveY=0):
	for i in range(numFrames):
		for j in range(zoomRes):
			pzoom = math.exp((i+(j/zoomRes)*zoomSpeed))
			# run the function
			filestring = 'zoom('+str(cX)+','+str(cY)+')'+'x'+"{:.2f}".format(pzoom)
			if os.path.exists(filestring+'.png'):
				print(filestring+" already rendered...")
				continue

			bitmap = Julia.generateJuliaBitmap(zoom=pzoom, moveX=moveX, moveY=moveY)

			bitmap.save(filestring+'.png')
			# bitmap.show()
			print(str(int((i+(j/zoomRes))*100/numFrames))+'% : '+filestring+' was saved...')

def createRotationSequence(numFrames, maxcX=-0.8, maxcY=-0.8, pscale=0.2, pmaxIter=255):
	# unit circle with rotation theta to make different x and y 
	for i in range(numFrames):
		a = i/numFrames
		theta = a*2*math.pi
		acX = math.cos(theta)*maxcX
		acY = math.sin(theta)*maxcY

		# for rotation sequences, Julia must be initialized for every frame because cX and cY will change every frame
		Julia.init(pcX=acX, pcY=acY, pscale = pscale, pmaxIter = pmaxIter, maxW = w, maxH = h)
		bitmap = Julia.generateJuliaBitmap()

		filestring = 'rot('+str(maxcX)+','+str(maxcY)+')'+'a'+"{:.3f}".format(theta)
		bitmap.save(filestring+'.png')
		# bitmap.show()

		print(str(int(a*100))+'% : '+filestring+' was saved...')


w, h = 1920, 1080

cX, cY = 0.26, 0.0016
scale = 0.05


# Julia.init will set your configuration values in Julia.py for generateJuliaBitmap() to use
Julia.init(pcX = cX, pcY = cY, pscale = scale, maxW = w, maxH = h)

createZoomSequence(numFrames=36, zoomRes=4, moveX=-0.50799164801110818, moveY=0.1005162266971976)
# createZoomSequence(numFrames=25, zoomRes=30, moveX=-0.4382288325466, moveY=-0.046645430614)
# offset zoom into spiral
# createZoomSequence(numFrames = 9, zoomRes=1, moveX=0.507, moveY=-0.1035)

# # # stuff to run overnight 
# createRotationSequence(numFrames=10, maxcX=0.26, maxcY=0.20, pscale=0.1)
# createZoomSequence(numFrames=1, pscale=0.25, zoomRes=1, pcX=0.0, pcY=0.5, pColorTup=(5,3,1))
# createZoomSequence(numFrames=15, pscale=1, zoomRes=6, pcX=-0.8, pcY=0.156)
# # # beyond e^15 zoom, it is just blank

# createZoomSequence(numFrames=8, pscale=1, zoomRes=6, pcX=-0.55, pcY=0.5)
