#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import re
import os
import sys

from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageChops

def img_resize(imagePath, args):
    '''
    照片调整大小，然后保存图片
    '''
    fileName = os.path.basename(imagePath)
    imageName = os.path.splitext(fileName)[0]
    imageExte = os.path.splitext(fileName)[1]
    h = 0
    w = 0

    print("%s: resizing ..." % (fileName), end=" ")

    try:
        im = Image.open(imagePath)

        name = imageName

        if args.height > 0:
            h = args.height
            if args.width > 0:
                w = args.width
                name += "_%sx%s" % (w,h)
            else:
                w = int(im.size[0] / im.size[1] * h + 0.5)
                name += "_h%s" % h
        elif args.width > 0:
            w = args.width
            name += "_w%s" % w
            h = int(im.size[1] / im.size[0] * w + 0.5)
        elif args.scale > 0:
            w = int(im.size[0] * args.scale + 0.5)
            h = int(im.size[1] * args.scale + 0.5)
            name += "_s%s" % args.scale
        
        assert w > 0 and h > 0, "args is 0"
        
        # 缩放图片
        im = im.resize((w, h), Image.ANTIALIAS)

        # im.show()

        if not os.path.exists(args.out):
            os.mkdir(args.out)

        name += imageExte
        new_name = os.path.join(args.out, name)

        im.save(new_name, dpi=(args.dpi,args.dpi))

    except Exception as e:
        print("%s Failed." % (e.args))
        return

    print("Completed.")


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("-f", "--file", type=str,
                       help="image file path or directory")
    parse.add_argument("--height", default=0, type=int,
                       help="image output height, default is 0")
    parse.add_argument("--width", default=0, type=int,
                       help="image output width, default is 0")
    parse.add_argument("-o", "--out", default="./output",
                       help="image output directory, default is ./output")
    parse.add_argument("--scale", default=0, type=float,
                    help="image resize scale, default is 0")
    parse.add_argument("--dpi", default=220, type=float,
                    help="image output dpi, default is 220")

    args = parse.parse_args()

    if os.path.isdir(args.file):
        names = os.listdir(args.file)
        for name in names:
            image_file = os.path.join(args.file, name)
            img_resize(image_file, args)
    else:
        img_resize(args.file, args)


if __name__ == '__main__':
    main()
