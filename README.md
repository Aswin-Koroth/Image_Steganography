# Image_Steganography
Hide images inside images,can hide a **WxH** black and white image inside a **WxH** RGB image.  
(the image to hide is automatically converted to black and white)
# How it works 
The brightness value of each pixel of a black and white images is stored in red, green, blue values of each pixel in the RGB image.
### How?
brightness value of one pixel of a black and white image : (148)  
RGB values of one pixel of a rgb image : (242,193,174)  
RGB values of encoded image : (241,194,178)  
The last digit of RGB values is changed to each digit of brightness value.  
The value 148 is stored as 24(1), 19(4), 17(8).

