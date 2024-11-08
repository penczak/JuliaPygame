from PIL import Image, ImageFilter
import math
import numpy as np
import colorsys

# goldenRatio = 1.61803398875

# cX is real part of complex number
# cY is imaginary part
# set up global variables once before running generateJuliaBitmap()
def init(pcX=-0.8, pcY=0.156, pscale = 0.2, pmaxIter = 255, maxW = 1080, maxH = 720):
	global w, h, cX, cY, maxIter, scale
	scale = pscale
	w, h = int(maxW*scale), int(maxH*scale)
	cX, cY = pcX, pcY
	maxIter = pmaxIter

# matrix multiplication? 
def generateJuliaBitmap(zoom=1, moveX=0, moveY=0):
	bitmap = Image.new("HSV", (w,h), "white")
	# load pixel data
	pixels = bitmap.load()
	for x in range(w):
		for y in range(h):
			zx = 1.5*(x - w/2)/(0.5*zoom*w) + moveX
			zy = 1.5*(y - h/2)/(0.5*zoom*h) + moveY
			i = maxIter
			while zx**2 + zy**2 < 4 and i > 1:
				# temp is next iter's real part 
				# new zx = real^2 - imag^2 + C(real)...(-imag^2 bc i^2 = -1)
				temp = zx**2 - zy**2 + cX
				# new zy is old real * old imag * 2 (this is from the cmplx num being squared and FOILing) + C(imag)
				# new zx (real component) is set to temp
				zy,zx = 2.0*zx*zy + cY, temp
				i -= 1

			# if i == maxIter-1:
			# 	pixels[x,y] = (0, 0, 255)
			# el
			if i == 1:
				pixels[x,y] = (0, 0, 0)
			else:
				if i > 255:
					i %= 255
				else:
					i *= int(255/maxIter)
				# pixels[x,y] = (i << colorTup[0]) + (i << colorTup[1]) + i*colorTup[2]
				pixels[x,y] = (255-i, 200, 200)

	bitmap = bitmap.convert('RGB')
	return bitmap

# init(pscale=0.5)
# generateJuliaBitmap().show()