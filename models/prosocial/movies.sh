#!/bin/bash

ffmpeg -r 12 -f image2 -s 1920x1080 -i grid-g1-strategies_%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p grid-g1-strategies.mp4

ffmpeg -r 12 -f image2 -s 1920x1080 -i grid-g1-payoffs_%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p grid-g1-payoffs.mp4
