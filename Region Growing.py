import cv2
import pydicom
from PIL import Image, ImageTk
import matplotlib.pylab as plt
import cv2
import numpy as np
from skimage.morphology import binary_dilation
from skimage.segmentation import clear_border
from skimage.color import label2rgb
from skimage.measure import label
from skimage.morphology import flood
from skimage.morphology import binary_dilation


def mouse_clic(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        src = param.copy()

        cv2.floodFill(src, None, (x, y),255)
        cv2.imshow('Fill zone', src)

def binview(img, mask, color='r', dilate_pixels=1):
    """
    Displays a gray or color image 'img' overlaid by color pixels determined a by binary image 'mask'. It is useful to
    display the edges of an image.

    Args:
        img: gray scale image (X-ray)
        mask: binary image that works as mask
        color: string to define pixel color.
                'r': red (default)
                'g': green
                'b': blue
                'y': yellow
                'c': cyan
                'm': magenta
                'k': black
                'w': white

        dilate_pixels (int): Number of pixels used for dilate the mask.

    Returns:
        img_color (ndarray): output image with a mask overlaid.
    """

    # Defines colors
    # colors = {
    #     'r': np.array([255, 0, 0]),
    #     'g': np.array([0, 255, 0]),
    #     'b': np.array([0, 0, 255]),
    #     'y': np.array([255, 255, 0]),
    #     'c': np.array([0, 255, 255]),
    #     'm': np.array([255, 0, 255]),
    #     'k': np.array([0, 0, 0]),
    #     'w': np.array([255, 255, 255])
    # }
    #
    colors = {
        'r': np.array([1, 0, 0]),
        'g': np.array([0, 1, 0]),
        'b': np.array([0, 0, 1]),
        'y': np.array([1, 1, 0]),
        'c': np.array([0, 1, 1]),
        'm': np.array([1, 0, 1]),
        'k': np.array([0, 0, 0]),
        'w': np.array([1, 1, 1])
    }
    # Create a RGB image from grayscale image.
    img_color = np.dstack((img, img, img))

    # Ensure do not modify the original color image and the mask
    img_color = img_color.copy()

    mask_ = mask.copy()
    # mask_ = dilate(mask_, np.ones((g, g), np.uint8))
    mask_ = binary_dilation(mask_, np.ones((dilate_pixels, dilate_pixels)))

    # Now black-out the area of the mask
    # img_fg = bitwise_and(img, img, mask=mask_)

    # Defines the pixel color used for the mask in the figure.
    cc = colors[color]
    #
    # for i in range(3):
    #     img_color[:, :, i] = cc[i] * img_fg

    # remove artifacts connected to image border
    cleared = clear_border(mask_)
    if np.all(cleared):
        mask_ = cleared

    # label image regions
    label_image = label(mask_)
    img_color = label2rgb(label_image, image=img_color, colors=[cc], bg_label=0)

    return img_color  # add(img_color, img_color)

def region_growing(img, seed_point, tolerance=20):
    """
    Args:
        img (ndarray): image
        seed_point (tuple): define the seed point.
        tolerance: a float or int value to define the maximal difference of grayvalues in the region. According to the
                   documentation in scikit-image, if tolerance is provided, adjacent points with values within plus 
                   or minus tolerance from the seed point are filled (inclusive).

    Returns:
        mask (ndarray): output binary image
    """
    mask = flood(img, seed_point, tolerance=tolerance)
    mask = binary_dilation(mask, np.ones((3, 3)))

    return mask


    main()

def on_click(event,x,y,flags,params):
    global x1,y1
    if event==cv2.EVENT_LBUTTONDOWN:
        x1=x
        y1=y
        th = 20.5 # threshold
        #si, sj = (120, 190)  # Seed
        si, sj = (y, x)  # Seed
        print(x,y)
        print(th)
        mask = region_growing(resized, (si, sj), tolerance=th)
        seg = binview(resized, mask, 'g')
        #final=cv2.multiply(resized, mask)
        cv2.imwrite('Final.png',seg)
        cv2.imshow('Ventana',seg)
        cv2.waitKey(0)
        

x1=0
y1=0
# Cargar imagen DICOM
ds = pydicom.dcmread('./RX/FABI290MRG.dcm')
img = (ds.pixel_array)
imgNorm = (255-(img / img.max()*255)).astype('uint8')
scale_percent = 20 # percent of original size
width = int(imgNorm.shape[1] * scale_percent / 100)
height = int(imgNorm.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(imgNorm, dim, interpolation = cv2.INTER_AREA)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(3,3))
resized = clahe.apply(resized)



cv2.namedWindow('Ventana')
cv2.setMouseCallback('Ventana',on_click)
cv2.imshow('Ventana', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""th = 40  # threshold
#si, sj = (120, 190)  # Seed
si, sj = (y1, x1)  # Seed

#mask = region_growing(resized, (si, sj), tolerance=th)

seg = binview(resized, mask, 'g')
cv2.namedWindow('Ventana')
cv2.setMouseCallback('Ventana',on_click)
cv2.imshow('Ventana', resized)
cv2.waitKey(0)
cv2.imshow('Ventana',seg)
cv2.waitKey(0)"""
# Waiting 0ms for user to press any key

  
# Using cv2.destroyAllWindows() to destroy
# all created windows open on screen

"""fig, ax = plt.subplots(1, 3, figsize=(14, 8))
ax[0].imshow(img, cmap='gray')
ax[0].plot(sj, si, 'r+')
ax[0].axis('off')
ax[1].imshow(mask, cmap='gray')
ax[1].axis('off')
ax[2].imshow(seg)
ax[2].axis('off')
plt.tight_layout()
plt.show()"""
# Crear imagen de PIL y PhotoImage de Tkinter



# Definir el punto de semilla (en este caso, el píxel en la posición 100, 100)

# Definir los criterios de similitud (en este caso, la diferencia de intensidad de gris)
"""criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

# Aplicar el algoritmo de crecimiento de región
mask = cv2.floodFill(resized, None, seed, 255, loDiff=0, upDiff=0, flags=cv2.FLOODFILL_FIXED_RANGE)
#imgFinal=mask*resized
#im = Image.fromarray(imgFinal)
# Visualizar los resultados
cv2.namedWindow('Ventana')
cv2.setMouseCallback('Ventana',onClick)
while(1):
    cv2.imshow('Ventana',mask[1])
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()"""