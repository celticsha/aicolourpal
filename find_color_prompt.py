import numpy as np
import pandas as pd
from skimage.color import rgb2lab
    
def convert_to_rgb_tuple(color_string):
    # Split the string by spaces and convert each to an integer
    rgb_values = tuple(int(value) for value in color_string.split())
    return rgb_values

file_path = 'colours.csv'
color_data = pd.read_csv(file_path)

color_data['rgb'] = color_data['rgb'].apply(convert_to_rgb_tuple)

def rgb_to_lab(rgb):
    """Convert an RGB tuple to LAB color space."""
    rgb_normalized = np.array(rgb) / 255
    rgb_reshaped = rgb_normalized.reshape(1, 1, 3)
    lab = rgb2lab(rgb_reshaped)
    return lab[0, 0, :]

def calculate_ciede2000_similarity(image1_avg_rgb, image2_avg_rgb):
    lab1 = rgb_to_lab(image1_avg_rgb)
    lab2 = rgb_to_lab(image2_avg_rgb)
    return np.linalg.norm(lab1 - lab2)

def find_nearest_color(input_rgb,top_n):
    input_lab = rgb_to_lab(input_rgb)

    distances = [calculate_ciede2000_similarity(input_rgb, row['rgb']) for index, row in color_data.iterrows()]
    top_indices = np.argsort(distances)[:top_n]  
    top_colors = color_data.iloc[top_indices].copy()  
    top_colors['distance'] = np.sort(distances)[:top_n]  

    return top_colors

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)

def get_deviation_label(dev):
  if dev<5:
    return "excellent"
  if dev<15:
    return "good"
  if dev<30:
    return "reasonable"
  if dev<40:
    return "patchy"
  return "poor"

while True:
	hexv=input("Enter the hex value of the colour you would like to prompt?")

	input_rgb = hex_to_rgb(hexv)  # Input RGB color as floats

	top_colors = find_nearest_color(input_rgb,5)
	print()
	print(f"You chose {hexv} which is rgb({input_rgb}).")
	prompt_str=""
	c=0
	for i, row in top_colors.iterrows():
	  dev_label=get_deviation_label(row['deviation'])
	  if c==0:
	    print()
	    print(f"Your top match is:")
	    print(f"{row['prompt']}")
	    print(f"which generates colours with an average rgb value of {row['rgb']} (hex {row['hex']})")
	    print()
	    print(f"It has {dev_label} consistency.")
	    c=1
	  else:
	    
	    prompt_str+=row['prompt']+f" ({dev_label} consistency), "

	print()
	print(f"You might also like to try: {prompt_str}")




	#print(f"The closest color is: {closest_color_name} with RGB values {closest_color_rgb} and hex value {closest_color_hex}.")
	#print(f"The distance from your colour is {distance})"

