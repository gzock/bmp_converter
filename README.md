# Overview

This is BMP images converter for WaveShare display of Raspberry Pico

- https://www.waveshare.com/wiki/Pico-ResTouch-LCD-3.5
- https://www.waveshare.com/wiki/Pico-ResTouch-LCD-2.8

This tool can convert from various image formats to BMP Images.
e.g. png -> bmp

# Usage

* convert a jpg to bmp of supporting format for pico-restouch-lcd

```
$ python main.py show src.bmp
$ python main.py conv src.jpg out.bmp
```

* generate a clang code from bmp image
```
$ python gen_c_array.py sample.bmp bmp_image_array
```