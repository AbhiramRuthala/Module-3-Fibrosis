'''Module 3: count black and white pixels and compute the percentage of white pixels in a .jpg image and extrapolate points'''

from termcolor import colored
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd
import time

# Load the images you want to analyze

# Start time
start = time.time()

filenames = [
    r"/Users/abhiramruthala/Module-3-Fibrosis/images/MASK_Sk658 Llobe ch010017.jpg",
    r"/Users/abhiramruthala/Module-3-Fibrosis/images/MASK_Sk658 Llobe ch010018.jpg",
    r"/Users/abhiramruthala/Module-3-Fibrosis/images/MASK_Sk658 Llobe ch010019.jpg",
    r"/Users/abhiramruthala/Module-3-Fibrosis/images/MASK_Sk658 Llobe ch010021.jpg",
    r"/Users/abhiramruthala/Module-3-Fibrosis/images/MASK_Sk658 Llobe ch010022.jpg",
    r"/Users/abhiramruthala/Module-3-Fibrosis/images/MASK_Sk658 Llobe ch010023.jpg",
]

# Enter the depth of each image (in the same order that the images are listed above; you can find these in the .csv file provided to you which is tilted: "Filenames and Depths for Students")

depths = [
    45,
    90,
    60,
    30,
    80,
    100
]

def analyze_image(filename):
    """
    Improvement made: The original code used three separate for-loops:
    one to load images, one to count pixels, and one to calculate percentages.
    That meant Python had to iterate over the entire list of filenames three times,
    and all images had to be stored in memory simultaneously before any analysis began.

    This function bundles all of that work together, loading, thresholding, counting,
    and computing the percentage, so each image is fully processed and then discarded
    from memory before moving on to the next one. This is more memory-efficient and
    easier to read, debug, and maintain.
    """
    # Read the image in grayscale mode (0 = grayscale flag)
    img = cv2.imread(filename, 0)

    # Apply binary threshold: pixels above 127 become 255 (white), others become 0 (black)
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Count white and black pixels
    white = int(np.sum(binary == 255))
    black = int(np.sum(binary == 0))

    # Calculate the percentage of white pixels out of all pixels
    white_percent = 100 * white / (white + black)

    return white, black, white_percent


# Improvement made: Instead of three separate for-loops, this single list
# comprehension calls analyze_image() on every filename in one pass. The original code
# looped over the filenames once to load images, again to count pixels, and again to
# calculate percentages — unnecessarily repeating the same iteration three times.
results = [analyze_image(f) for f in filenames]

# Improvement made: zip(*results) unpacks all three return values from
# analyze_image() into separate tuples in one line. The original code built up
# white_counts, black_counts, and white_percents by appending to empty lists inside
# separate loops — more verbose and slower than unpacking everything at once here.
white_counts, black_counts, white_percents = zip(*results)

# Print the white and black pixel counts for each image
print(colored("Counts of pixels by color in each image", "yellow"))
for i, filename in enumerate(filenames):
    print(colored(f"White pixels in image {i}: {white_counts[i]}", "white"))
    print(colored(f"Black pixels in image {i}: {black_counts[i]}", "white"))
    print()

# Print the filename, white pixel percentage, and depth for each image
print(colored("Percent white px:", "yellow"))
for i, filename in enumerate(filenames):
    print(colored(f'{filename}:', "red"))
    print(f'{white_percents[i]:.4f}% White | Depth: {depths[i]} microns')
    print()

'''Write your data to a .csv file'''

# Create a DataFrame that includes the filenames, depths, and percentage of white pixels
df = pd.DataFrame({
    'Filenames': filenames,
    'Depths': depths,
    'White percents': white_percents
})

# Write that DataFrame to a .csv file

df.to_csv('Percent_White_Pixels.csv', index=False)

print("The .csv file 'Percent_White_Pixels.csv' has been created.")

'''the .csv writing subroutine ends here'''

# End time
end = time.time()

# Print time
print(f"Time taken to write .csv file: {end - start} seconds")

# Takes about 95 seconds to get 10,000 images.

# Used Claude to help fix the code and tell us how the changes given were improvements
# Anthropic. (2025). Claude. Claude.ai. https://claude.ai/new


##############
# LECTURE 2: UNCOMMENT BELOW

# # Interpolate a point: given a depth, find the corresponding white pixel percentage

# interpolate_depth = float(input(colored(
#     "Enter the depth at which you want to interpolate a point (in microns): ", "yellow")))

# x = depths
# y = white_percents

# # You can also use 'quadratic', 'cubic', etc.
# i = interp1d(x, y, kind='linear')
# interpolate_point = i(interpolate_depth)
# print(colored(
#     f'The interpolated point is at the x-coordinate {interpolate_depth} and y-coordinate {interpolate_point}.', "green"))

# depths_i = depths[:]
# depths_i.append(interpolate_depth)
# white_percents_i = white_percents[:]
# white_percents_i.append(interpolate_point)


# # make two plots: one that doesn't contain the interpolated point, just the data calculated from your images, and one that also contains the interpolated point (shown in red)
# fig, axs = plt.subplots(2, 1)

# axs[0].scatter(depths, white_percents, marker='o', linestyle='-', color='blue')
# axs[0].set_title('Plot of depth of image vs percentage white pixels')
# axs[0].set_xlabel('depth of image (in microns)')
# axs[0].set_ylabel('white pixels as a percentage of total pixels')
# axs[0].grid(True)


# axs[1].scatter(depths_i, white_percents_i, marker='o',
#                linestyle='-', color='blue')
# axs[1].set_title(
#     'Plot of depth of image vs percentage white pixels with interpolated point (in red)')
# axs[1].set_xlabel('depth of image (in microns)')
# axs[1].set_ylabel('white pixels as a percentage of total pixels')
# axs[1].grid(True)
# axs[1].scatter(depths_i[len(depths_i)-1], white_percents_i[len(white_percents_i)-1],
#                color='red', s=100, label='Highlighted point')


# # Adjust layout to prevent overlap
# plt.tight_layout()
# plt.show()
