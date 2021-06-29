import canvas as cv

canvas = None

def run (parentId):
    global canvas
    canvas = cv.Canvas (parentId)
