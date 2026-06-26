import numpy as np
from numba import njit, prange

# globals configured by init()
w = 0
h = 0
cX = 0.0
cY = 0.0
maxIter = 255
scale = 1.0

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

def updateParameters(dcX, dcY):
    global cX, cY
    cX += dcX
    cY += dcY

@njit(parallel=True, fastmath=True)
def _julia_kernel(w, h, zoom, moveX, moveY, cX, cY, maxIter):
	out = np.zeros((h, w, 3), dtype=np.uint8)

	for y in prange(h):
		for x in range(w):
			zx = 1.5*(x - w/2)/(0.5*zoom*w) + moveX
			zy = 1.5*(y - h/2)/(0.5*zoom*h) + moveY
			i = maxIter
			while zx * zx + zy * zy < 4.0 and i > 1:
				zx2 = zx * zx
				zy2 = zy * zy
				new_zx = zx2 - zy2 + cX
				zy = 2.0 * zx * zy + cY
				zx = new_zx
				i -= 1

			if i == 1:
				# black
				out[y, x, 0] = 0
				out[y, x, 1] = 0
				out[y, x, 2] = 0
			else:
				if maxIter > 255:
					color_i = i % 255
				else:
					color_i = i * (255 // maxIter)

				r, g, b = hue_to_rgb(color_i / 255.0)

				out[y, x, 0] = r
				out[y, x, 1] = g
				out[y, x, 2] = b

	return out

@njit
def hue_to_rgb(t):
	# interpolates between RBG colors using t as a hue
	# t (0,1)
	h = t * 6.0 # *6 to see which sextant of the color wheel to use
	i = int(h)
	f = h - i

	# constant value and saturation
	v = 200.0 / 255.0
	s = 200.0 / 255.0

	# hsv to rgb formula
	p = v * (1.0 - s)
	q = v * (1.0 - s * f)
	t_val = v * (1.0 - s * (1.0 - f))

	if i == 0:
		r, g, b = v, t_val, p
	elif i == 1:
		r, g, b = q, v, p
	elif i == 2:
		r, g, b = p, v, t_val
	elif i == 3:
		r, g, b = p, q, v
	elif i == 4:
		r, g, b = t_val, p, v
	else:
		r, g, b = v, p, q

	return int(r * 255), int(g * 255), int(b * 255)


def generateJuliaArray(zoom=1.0, moveX=0.0, moveY=0.0):
	return _julia_kernel(w, h, zoom, moveX, moveY, cX, cY, maxIter)
