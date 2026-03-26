'''Module 3: count black and white pixels and compute the percentage of white pixels in a .jpg image and extrapolate points'''

from termcolor import colored
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd

# Load the images you want to analyze

filenames = [
    r"/Users/abhiramruthala/Module-3-Fibrosis/images/MASK_Sk658 Llobe ch010017.jpg",
    r"/Users/abhiramruthala/Module-3-Fibrosis/images/MASK_Sk658 Llobe ch010018.jpg",
    r"/Users/abhiramruthala/Module-3-Fibrosis/images/MASK_Sk658 Llobe ch010019.jpg",
    r"/Users/abhiramruthala/Module-3-Fibrosis/images/MASK_Sk658 Llobe ch010021.jpg",
    r"/Users/abhiramruthala/Module-3-Fibrosis/images/MASK_Sk658 Llobe ch010022.jpg",
    r"/Users/abhiramruthala/Module-3-Fibrosis/images/MASK_Sk658 Llobe ch010023.jpg",
    r"/Users/abhiramruthala/Module-3-Fibrosis/images/MASK_Sk658 Llobe ch010024.jpg",
    r"/Users/abhiramruthala/Module-3-Fibrosis/images/MASK_Sk658 Llobe ch010025.jpg",
    r"/Users/abhiramruthala/Module-3-Fibrosis/images/MASK_Sk658 Llobe ch010030.jpg",
    r"/Users/abhiramruthala/Module-3-Fibrosis/images/MASK_Sk658 Llobe ch010031.jpg"
]

# Enter the depth of each image (in the same order that the images are listed above; you can find these in the .csv file provided to you which is tilted: "Filenames and Depths for Students")

depths = [
    45,
    90,
    60,
    30,
    80,
    100,
    600,
    570,
    200,
    955
]

# Make the lists that will be used

images = []
white_counts = []
black_counts = []
white_percents = []

# Build the list of all the images you are analyzing

for filename in filenames:
    img = cv2.imread(filename, 0)
    images.append(img)

# For each image (until the end of the list of images), calculate the number of black and white pixels and make a list that contains this information for each filename.

for x in range(len(filenames)):
    _, binary = cv2.threshold(images[x], 127, 255, cv2.THRESH_BINARY)

    white = np.sum(binary == 255)
    black = np.sum(binary == 0)

    white_counts.append(white)
    black_counts.append(black)

# Print the number of white and black pixels in each image.

print(colored("Counts of pixel by color in each image", "yellow"))
for x in range(len(filenames)):
    print(colored(f"White pixels in image {x}: {white_counts[x]}", "white"))
    print(colored(f"Black pixels in image {x}: {black_counts[x]}", "black"))
    print()

# Calculate the percentage of pixels in each image that are white and make a list that contains these percentages for each filename

for x in range(len(filenames)):
    white_percent = (
        100 * (white_counts[x] / (black_counts[x] + white_counts[x])))
    white_percents.append(white_percent)

# Print the filename (on one line in red font), and below that line print the percent white pixels and depth into the lung where the image was obtained

print(colored("Percent white px:", "yellow"))
for x in range(len(filenames)):
    print(colored(f'{filenames[x]}:', "red"))
    print(f'{white_percents[x]}% White | Depth: {depths[x]} microns')
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


##############
# LECTURE 2: UNCOMMENT BELOW

# Interpolate a point: given a depth, find the corresponding white pixel percentage

# Input the microns at which you want to find the white pixel percentage, and then run the code to see how much it is and plot it on the graph
interpolate_depth = float(input(colored(
    "Enter the depth at which you want to interpolate a point (in microns): ", "yellow")))

# Create the interpolation function by organizing the different data architectures to the corresponding x and y axis.
x = depths 
y = white_percents

# You can also use 'quadratic', 'cubic', etc. We chose to use quadratic for our interpolation
i = interp1d(x, y, kind='quadratic')
interpolate_point = i(interpolate_depth)
# Print a statement to ensure that the interpolation had occurred.
print(colored(
    f'The interpolated point is at the x-coordinate {interpolate_depth} and y-coordinate {interpolate_point}.', "green"))

# Create two lists that append the interpolated point and its white pixel percentage.
depths_i = depths[:]
depths_i.append(interpolate_depth)
white_percents_i = white_percents[:]
white_percents_i.append(interpolate_point)


# make two plots: one that doesn't contain the interpolated point, just the data calculated from your images, and one that also contains the interpolated point (shown in red)
fig, axs = plt.subplots(2, 1)

# Make the first plot. Plot all points calculated by the code with its white pixel percentage. This doesn't consist of the interpolated point.
axs[0].scatter(depths, white_percents, marker='o', linestyle='-', color='blue') # Label all points with blue
axs[0].set_title('Plot of depth of image vs percentage white pixels')
axs[0].set_xlabel('depth of image (in microns)')
axs[0].set_ylabel('white pixels as a percentage of total pixels')
axs[0].grid(True)


# Make the second plot. Plot all points calculated by the code with its white pixel percentage. This one also has the interpolated point (shown in red).
axs[1].scatter(depths_i, white_percents_i, marker='o',
               linestyle='-', color='blue') # Label all points with blue
axs[1].set_title(
    'Plot of depth of image vs percentage white pixels with interpolated point (in red)')
axs[1].set_xlabel('depth of image (in microns)')
axs[1].set_ylabel('white pixels as a percentage of total pixels')
axs[1].grid(True)
# Highlight the interpolated point
axs[1].scatter(depths_i[len(depths_i)-1], white_percents_i[len(white_percents_i)-1],
               color='red', s=100, label='Highlighted point')


# Adjust layout to prevent overlap
plt.tight_layout()
# Show both graphs simultaneously
plt.show()
