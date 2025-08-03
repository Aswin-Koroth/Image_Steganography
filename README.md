# Image Steganography

A method to hide a `WxH` black and white image inside a color `WxH` RGB image. The image to be hidden is automatically converted to black and white.

## How It Works

The core principle is to encode the brightness value of each pixel from the black and white image into the Red, Green, and Blue (RGB) values of the corresponding pixel in the color image.

This is achieved by modifying the last digit of each of the R, G, and B values to represent the three digits of the brightness value.

### Encoding Example

Let's take one pixel from the secret image and one from the host image.

*   **Secret Image Pixel (Black & White):**
    *   Brightness Value: `148`

*   **Host Image Pixel (RGB):**
    *   Original RGB Values: `(242, 193, 174)`

The three digits of the brightness value (`1`, `4`, `8`) are used to replace the last digit of each RGB component:

*   The **R** value `242` becomes `241` (to encode the `1`).
*   The **G** value `193` becomes `194` (to encode the `4`).
*   The **B** value `174` becomes `178` (to encode the `8`).

*   **Resulting Encoded Pixel:**
    *   New RGB Values: `(241, 194, 178)`

