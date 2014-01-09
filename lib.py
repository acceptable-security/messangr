from PIL import Image
import ImageFile
def imageSize(file):
	fs = len(open(file,'rb').read())
	gs = fs/1073741824.0
	if gs < 1.0:
		ms = fs/1048576.0
		if ms >= 1.0:
			return Image.open(file).size, round(ms,2), "MB"
		else:
			return Image.open(file).size, round(fs/1024.0,2),"KB"
	else:
		return Image.open(file).size, round(gs,2),"GB?"

if __name__ == "__main__":
	print "###################"
	print "messangr lib tests"
	print "image size : " + str(imageSize("static/uploads/a.jpg"))