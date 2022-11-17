from pathlib import Path
from PIL import Image, ImageDraw
from library.imagefunctions import imageprocess
import multiprocessing as mp

test_path = 'test_data'
output_path = 'output'

#Set raw path to test data for now
raw_path = test_path

# Initialise multiprocessing pool
pool = mp.Pool(mp.cpu_count())

# Generate Path objects
raw_path = Path.cwd().joinpath('test_data','images')
imfiles = raw_path.glob("*.JPG")

# # Print filepath we're working on and process filename
# for filepath in imfiles:
#     print(filepath)
#     imageprocess(filepath, output_path)

[pool.apply(imageprocess, args=(filepath, output_path)) for filepath in imfiles]
# [pool.apply(imageprocess, args=(filepath, output_path)) for filepath in imfiles]