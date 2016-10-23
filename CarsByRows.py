import cv2
import SimpleCV
import numpy as np
from matplotlib import pyplot as plt

# this just keeps things neat
class ParkingLotRow(object):
    top_left=None
    bot_right=None
    roi=None
    col_mean=None
    inverted_variance=None
    empty_col_probability=None
    empty_spaces=0
    total_spaces=None

    def __init__(self,top_left,bot_right,num_spaces):
        self.top_left = top_left
        self.bot_right = bot_right
        self.total_spaces = num_spaces

############################ BEGIN: TWEAKING PARAMETERS ###########################################
car_width = 8       #in pixels
thresh = 0.975      #used to determine if a spot is empty
############################### END: TWEAKING PARAMETERS ###########################################
parking_rows = []

# defines regions of interest, row 1 is on top, row 5 is on bottom, values determined empirically
parking_rows.append(ParkingLotRow((  1, 20),(496, 41),25))     #row 1
parking_rows.append(ParkingLotRow((  1, 87),(462,105),23))     #row 2
parking_rows.append(ParkingLotRow((  1,140),(462,158),23))     #row 3
parking_rows.append(ParkingLotRow((  1,222),(462,240),22))     #row 4
parking_rows.append(ParkingLotRow((  1,286),(462,304),22))     #row 5

#read image
img = cv2.imread('images/184813292.jpg')
img2 = img.copy()

#creates a template, its jsut a car sized patch of pavement
template = img[138:165,484:495]
m, n, chan = img.shape

#blurs the template a bit
template = cv2.GaussianBlur(template,(3,3),2)
h, w, chan = template.shape

# Apply template Matching 
res = cv2.matchTemplate(img,template,cv2.TM_CCORR_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)
#adds bounding box around template
cv2.rectangle(img,top_left, bottom_right, 255, 5)

#adds bounding box on ROIs
for curr_parking_lot_row in parking_rows:
    tl = curr_parking_lot_row.top_left
    br = curr_parking_lot_row.bot_right

    cv2.rectangle(res,tl, br, 1, 5)

#displays some intermediate results
plt.subplot(121),plt.imshow(res,cmap = 'gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
plt.title('Original, template in blue'), plt.xticks([]), plt.yticks([])

plt.show()

curr_idx = int(0)

#overlay on original picture
f0 = plt.figure(4)
plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB)),plt.title('Original')


for curr_parking_lot_row in parking_rows:
    #creates the region of interest
    tl = curr_parking_lot_row.top_left
    br = curr_parking_lot_row.bot_right

    my_roi = res[tl[1]:br[1],tl[0]:br[0]]

    #extracts statistics by column
    curr_parking_lot_row.col_mean = np.mean(my_roi, 0)
    curr_parking_lot_row.inverted_variance = 1 - np.var(my_roi,0)
    curr_parking_lot_row.empty_col_probability = curr_parking_lot_row.col_mean * curr_parking_lot_row.inverted_variance

    #creates some plots
    f1 = plt.figure(1)
    plt.subplot('51%d' % (curr_idx + 1)),plt.plot(curr_parking_lot_row.col_mean),plt.title('Row %d correlation' %(curr_idx + 1))

    f2 = plt.figure(2)
    plt.subplot('51%d' % (curr_idx + 1)),plt.plot(curr_parking_lot_row.inverted_variance),plt.title('Row %d variance' %(curr_idx + 1))

    f3 = plt.figure(3)
    plt.subplot('51%d' % (curr_idx + 1))
    plt.plot(curr_parking_lot_row.empty_col_probability),plt.title('Row %d empty probability ' %(curr_idx + 1))
    plt.plot((1,n),(thresh,thresh),c='r')

    #counts empty spaces
    num_consec_pixels_over_thresh = 0
    curr_col = 0

    for prob_val in curr_parking_lot_row.empty_col_probability:
        curr_col += 1

        if(prob_val > thresh):
            num_consec_pixels_over_thresh += 1
        else:
            num_consec_pixels_over_thresh = 0

        if (num_consec_pixels_over_thresh >= car_width):
            curr_parking_lot_row.empty_spaces += 1

            #adds mark to plt
            plt.figure(3)   # the probability graph
            plt.scatter(curr_col,1,c='g')

            plt.figure(4)   #parking lot image
            area = np.pi * (11)**2
            plt.scatter(curr_col + 2,curr_parking_lot_row.top_left[1] + 7, s=area, marker='s', c='g')

            #to prevent doubel counting cars, just reset the counter
            num_consec_pixels_over_thresh = 0

    #sets axis range, apparantlly they mess up when adding the scatters
    plt.figure(3)
    plt.xlim([0,n])

    #print out some stats
    print('found {0} cars and {1} empty space(s) in row {2}'.format(
        curr_parking_lot_row.total_spaces - curr_parking_lot_row.empty_spaces,
        curr_parking_lot_row.empty_spaces,
        curr_idx +1))

    curr_idx += 1

#plot some figures
plt.show()