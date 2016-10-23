from SimpleCV import 
img = Image('tape.png')
blobs = img.binarize().morphClose().findBlobs()
blobs.image = img 
blobs[-1].drawHoles()
img.show()