

cpdef center_center(int centerx, int centery, tuple size):
	cdef int width, height
	width = <int>size[0]
	height = <int>size[1]

	return (centerx - (width / 2), centery - (height / 2))


cpdef center_top(int centerx, int top, tuple size):
	cdef int width, height
	width = <int>size[0]
	height = <int>size[1]

	return (centerx - (width / 2), top)


cpdef center_bottom(int centerx, int bottom, tuple size):
	cdef int width, height
	width = <int>size[0]
	height = <int>size[1]

	return (centerx - (width / 2), bottom - height)


cpdef right_top(int right, int top, tuple size):
	cdef int width, height
	width = <int>size[0]
	height = <int>size[1]

	return (right - width, top)


cpdef right_bottom(int right, int bottom, tuple size):
	cdef int width, height
	width = <int>size[0]
	height = <int>size[1]

	return (right - width, bottom - height)


cpdef collidepoint(int x, int y, int w, int h, tuple pos):
		cdef int px, py
		px = <int>pos[0]
		py = <int>pos[1]

		return px >= x and px <= x + w and py >= y and py <= y + h