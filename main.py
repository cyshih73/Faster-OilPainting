import math
import shutil
import random
import argparse
import numpy as np
import cv2, imageio
import os, subprocess
from _gradient import get_gradient

def draw_order(h, w, scale):
    order = []
    for i in range(0, h, scale):
        for j in range(0, w, scale):
            y = random.randint(-scale // 2, scale // 2) + i
            x = random.randint(-scale // 2, scale // 2) + j
            order.append((y % h, x % w))
    return order

def main(args):

    import time
    brush_width = int(args.brush_width)
    quant = float(args.palette)    # Color come from palette(limited colours)

    img_path = args.path.rsplit(".", -1) 

    if img_path[1] == 'gif':
        os.makedirs(img_path[0])
        # Convert gif into jpgs
        subprocess.call(('convert -verbose -coalesce %s %s/no.jpg' % (args.path, img_path[0])).split())
        imgs_path = [(img_path[0]+'/no-'+str(i)+'.jpg') for i in range(len(os.listdir(img_path[0])))]
    else:
        imgs_path = [args.path]

    # Process the image / gif
    result = []
    for path in imgs_path:
        print("\n" + path)
        img = cv2.imread(path)
        
        # Get the gradient of image (Using sobel, scharr, prewitt, or roberts)
        print("Gradient: "); s = time.time()
        r = 2 * int(img.shape[0] / 50) + 1
        Gx, Gy = get_gradient(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (r, r), args.gradient)
        Gh = np.sqrt(np.sqrt(np.square(Gx) + np.square(Gy)))    # Length of the ellipse
        Ga = (np.arctan2(Gy, Gx) / np.pi) * 180 + 90            # Angle of the ellipse
        print("%.4f secs." % float(time.time() - s))

        print("Drawing"); s = time.time()
        canvas = cv2.medianBlur(img, 11)    # Make the image artlistic
        order = draw_order(img.shape[0], img.shape[1], scale=brush_width*2)

        # Draw the ellipse
        colors = np.array(img, dtype=np.float)
        for i, (y, x) in enumerate(order):
            length = int(round(brush_width + brush_width * Gh[y, x]))
            # Select color
            if quant != 0: color = np.array([round(colors[y,x][0]/quant)*quant+random.randint(-5,5), 
                round(colors[y,x][1]/quant)*quant+random.randint(-5,5), round(colors[y,x][2]/quant)*quant+random.randint(-5,5)], dtype=np.float)
            else: color = colors[y,x]

            cv2.ellipse(canvas, (x, y), (length, brush_width), Ga[y, x], 0, 360, color, -1, cv2.LINE_AA)

        result.append(canvas)
        print("%.4f secs." % float(time.time() - s))

    # Output the result
    print("\nOutput the result")
    output_path = img_path[0]+'_result.'+img_path[1]
    if img_path[1] == 'gif':
        c, images = 0, []
        for canva in result:
            cv2.imwrite(img_path[0]+'/r-'+str(c)+'.jpg', canva); c += 1
        for i in range(c-1): images.append(imageio.imread(img_path[0]+'/r-'+str(i)+'.jpg'))
        from PIL import Image
        imageio.mimsave(output_path, images, duration=float(Image.open(args.path).info['duration']) / 1000)
        shutil.rmtree(img_path[0], ignore_errors=True)
    else:
        cv2.imwrite(output_path, result[0])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--brush_width', default=5, help="Scale of the brush strokes")
    parser.add_argument('--path', required=True, type=str, help="Target image path, gif of still image")
    parser.add_argument('--palette', default=0, help="Palette colours. 0 = Actual color")
    parser.add_argument('--gradient', default='sobel', help="Edge detection type. (sobel, scharr, prewitt, roberts)")
    args = parser.parse_args()
    main(args)
