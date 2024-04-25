# from google.colab.patches import cv2_imshow
import cv2
import numpy as np
 
img = cv2.imread('Images/map_5088_png.rf.d34c5c339a19f9fba7f1ae8018fd321a.jpg')
print(img.shape)
cv2.imshow(img)
 
cropped_image = img[3:36, 30:309]
 
cv2.imshow(cropped_image)
 
cv2.imwrite("Cropped Image.jpg", cropped_image)
 
cv2.waitKey(0)
cv2.destroyAllWindows()


# import cv2
# from PIL import Image

# image = cv2.imread('Images/map_57.png')
# cv2.imshow('Image with Bounding Box', image)

# # Define the coordinates of the bounding box
# # x, y, width, height = 258, 469, 91, 10

# x, y, width, height = 13, 41, 44, 484
# x1, y1, width1, height1 = 72, 609, 490, 692

# # x1, y1, width1, height1 = 191, 18, 292, 32

# # shifting x,y from center of image to top left

# x = x*700
# y = y*500
# width = width*700
# height = height*500
# x = x - (width//2)
# y = y - (height//2)

# x1 = x1*700
# y1 = y1*500
# width1 = width1*700
# height1 = height1*500
# x1 = x1 - (width1//2)
# y1 = y1 - (height1//2)

# # Draw the bounding box on the image
# color = (0, 255, 0)  # BGR color format (green in this case)
# thickness = 2
# color1 = (255, 0, 0)

# cv2.rectangle(image, (x, y), (x + width, y + height), color, thickness)

# # cv2.rectangle(image, (x1, y1), (x1 + width1, y1 + height1), color1, thickness)

# # Display the image
# cv2.imshow('Image with Bounding Box', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # {
# #     "boxes": [
# #         {
# #             "label": "Dataset",
# #             "x": "976.88",
# #             "y": "445.00",
# #             "width": "73.75",
# #             "height": "812.50"
# #         },
# #         {
# #             "label": "Title",
# #             "x": "1070.63",
# #             "y": "25.00",
# #             "width": "258.75",
# #             "height": "27.50"
# #         },
# #         {
# #             "label": "Map",
# #             "x": "498.13",
# #             "y": "426.25",
# #             "width": "793.75",
# #             "height": "600.00"
# #         }
# #     ],
# #     "height": 882,
# #     "key": "1967.png",
# #     "width": 1202
# # }