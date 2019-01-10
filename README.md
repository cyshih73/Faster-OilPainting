# Faster-OilPainting: 快速照片油畫化
NTU Interactive Computer Graphic, 2018 Fall Final term project

## Usage:
### Requirements
- python3
- numpy
- scipy
- imageio
- python-opencv

### Execution
```
main.py [-h] [--brush_width BRUSH_WIDTH] --path PATH
        [--palette PALETTE] [--gradient GRADIENT]
optional arguments:
  -h, --help            show this help message and exit
  --brush_width BRUSH_WIDTH
                        Scale of the brush strokes
  --path PATH           Target image path, gif of still image
  --palette PALETTE     Palette colours. 0 = Actual color
  --gradient GRADIENT   Edge detection type. (sobel, scharr, prewitt, roberts)
  
ex. python main.py --brush_width 5 --path [target_image]
```

## Results
More examples please refer to Faster-OilPainting/testdata

### .jpg
![Before](https://raw.githubusercontent.com/shihehe73/Faster-OilPainting/master/testdata/Obersee.jpg)
![After](https://raw.githubusercontent.com/shihehe73/Faster-OilPainting/master/testdata/Obersee_result.jpg)

![Before](https://raw.githubusercontent.com/shihehe73/Faster-OilPainting/master/testdata/hallstadt_winter.jpg)
![After](https://raw.githubusercontent.com/shihehe73/Faster-OilPainting/master/testdata/hallstadt_winter_result.jpg)

### .gif
![Before](https://raw.githubusercontent.com/shihehe73/Faster-OilPainting/master/testdata/g3.gif)
![After](https://raw.githubusercontent.com/shihehe73/Faster-OilPainting/master/testdata/g3_result.gif)

![Before](https://raw.githubusercontent.com/shihehe73/Faster-OilPainting/master/testdata/g2.gif)
![After](https://raw.githubusercontent.com/shihehe73/Faster-OilPainting/master/testdata/g2_result.gif)
