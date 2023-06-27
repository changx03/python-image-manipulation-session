import os
from PIL import Image, ImageOps
from multiprocessing import Pool
from functools import partial

def crop_and_equalize_image(input_image_path, output_dir):
    """
    Crop the bottom 100 pixels off an image and equalize its histogram.
    """
    image = Image.open(input_image_path)
    width, height = image.size
    new_height = height - 100  # subtract 100 pixels from the original height
    image = image.crop((0, 0, width, new_height))  # parameters are left, upper, right, lower
    
    # equalize the histogram
    image = ImageOps.equalize(image)
    
    # Generate the output image path
    filename = os.path.basename(input_image_path)
    output_image_path = os.path.join(output_dir, filename)
    
    image.save(output_image_path)
    print(f'Processed {filename}')

def process_images(input_dir, output_dir):
    """
    Process all images in a directory using multiple processes.
    """
    # Make the output directory if it doesn't already exist
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all image file paths
    image_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) 
                   if f.lower().endswith((".jpg", ".png"))]

    # Get the number of processes from the Slurm environment variable
    processes = int(os.getenv('SLURM_CPUS_PER_TASK', default=4))

    # Use a multiprocessing Pool
    with Pool(processes=processes) as pool:
        # Use functools.partial to make a new function where the output directory is already given
        func = partial(crop_and_equalize_image, output_dir=output_dir)
        # Map the function to the image files, distributing the work among the processes in the Pool
        pool.map(func, image_files)

if __name__ == "__main__":
    input_dir = "images/images"
    output_dir = "equalized_images"

    process_images(input_dir, output_dir)
