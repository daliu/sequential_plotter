import matplotlib.pyplot as plt
import string, ast, numpy as np

import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.animation as animation

'''
This is a simple plotter that allows an individual to plot multiple histograms sequentially, but not simultaneously.
Load the first line with the names of your features in a list.
Load the second line with all your numeric data in a list of lists.
Follow the input instructions.
Have fun, and I hope this helps. :)
'''

MAGIC_NUMBER = 0 # Cannot be greater than # of attributes

# readfile = open("exports/ExportedArticles.csv", 'r')
# for k in range(2):
# readfile = open("50kimport/" + str(0) + "-CleanListForm.csv", "r")
readfile = open("50kimport/maxexport.csv", "r")
attributeList = ast.literal_eval(readfile.readline().translate(None, string.digits))

plotAttrs = []
for i in range(len(attributeList)):
	plotAttrs.append(list())

for line in readfile:
	line = ast.literal_eval(line)
	for idx, val in enumerate(line):
		try:
			plotAttrs[idx].append(float(val))
		except Exception as e:
			plotAttrs[idx].append(float(len(val)))

for attrdata in plotAttrs:
	fig, ax = plt.subplots()
	n, bins = np.histogram(attrdata, 500, normed=False)
	# get the corners of the rectangles for the histogram
	left = np.array(bins[:-1])
	right = np.array(bins[1:])
	bottom = np.zeros(len(left))
	top = bottom + n
	nrects = len(left)

	'''
	Here comes the tricky part -- we have to set up the vertex and path
	codes arrays using moveto, lineto and closepoly.
	For each rect: 1 for the MOVETO, 3 for the LINETO, 1 for the
	CLOSEPOLY; the vert for the closepoly is ignored but we still need
	it to keep the codes aligned with the vertices
	'''
	nverts = nrects*(1+3+1)
	verts = np.zeros((nverts, 2))
	codes = np.ones(nverts, int) * path.Path.LINETO
	codes[0::5] = path.Path.MOVETO
	codes[4::5] = path.Path.CLOSEPOLY
	verts[0::5,0] = left
	verts[0::5,1] = bottom
	verts[1::5,0] = left
	verts[1::5,1] = top
	verts[2::5,0] = right
	verts[2::5,1] = top
	verts[3::5,0] = right
	verts[3::5,1] = bottom

	barpath = path.Path(verts, codes)
	patch = patches.PathPatch(barpath, facecolor='green', edgecolor='yellow', alpha=0.5)
	ax.add_patch(patch)

	ax.set_xlim(left[0], right[-1])
	ax.set_ylim(bottom.min(), top.max())
	try:
		showAttribute = attributeList[MAGIC_NUMBER][0].replace(str(MAGIC_NUMBER).title(), "")
		plt.title("Histogram of %s Versus Frequency" % showAttribute)
		plt.ylabel("Number of Articles")
		plt.xlabel("Length/Number of: " + showAttribute)
		print("Now plotting: Histogram of " + showAttribute + " versus frequency.")
		plt.show()
	except IndexError as e:
		print("Attribute Doesn't Exist.")
		pass
	MAGIC_NUMBER += 1

