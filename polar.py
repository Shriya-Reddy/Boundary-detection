#!/usr/local/bin/python3
#
# Authors: spulagam, srbulusu, svalaval
#
# Ice layer finder
# Based on skeleton code by D. Crandall, November 2021
#

from PIL import Image
from numpy import *
import numpy as np
from scipy.ndimage import filters
import sys
import imageio
import copy
import decimal

# calculate "Edge strength map" of an image                                                                                                                                      
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_boundary(image, y_coordinates, color, thickness):
    #print("y cordinates and length", y_coordinates, len(y_coordinates))
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

def draw_asterisk(image, pt, color, thickness):
    for (x, y) in [ (pt[0]+dx, pt[1]+dy) for dx in range(-3, 4) for dy in range(-2, 3) if dx == 0 or dy == 0 or abs(dx) == abs(dy) ]:
        if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
            image.putpixel((x, y), color)
    return image


# Save an image that superimposes three lines (simple, hmm, feedback) in three different colors 
# (yellow, blue, red) to the filename
def write_output_image(filename, image, simple, hmm, feedback, feedback_pt):
    new_image = draw_boundary(image, simple, (255, 255, 0), 2)
    new_image = draw_boundary(new_image, hmm, (0, 0, 255), 2)
    new_image = draw_boundary(new_image, feedback, (255, 0, 0), 2)
    new_image = draw_asterisk(new_image, feedback_pt, (255, 0, 0), 2)
    imageio.imwrite(filename, new_image)

def viterbi_value(emission_probability, viterbi_table, row, col):
    viterbi_value = []
 
    probability_weights = [0.8, 0.8, 0.8, 0.80, 0.88, 0.99999]
    for k in range(len(emission_probability)):
  
        if abs(k-row) == 10 :
            transitional_probability_value = 0.0
        elif abs(k-row) == 9 :
            transitional_probability_value = 0.0
        elif abs(k-row) == 8 :
            transitional_probability_value = 0.0
        elif abs(k-row) == 7 :
            transitional_probability_value = 0.0
        elif abs(k-row) == 6 :
            transitional_probability_value = 0.0
        elif abs(k-row) == 5 :
            transitional_probability_value = 0.0
        elif abs(k-row) == 4 :
            transitional_probability_value = 0.0
        elif abs(k-row) == 3 :
            transitional_probability_value = 0.3
        elif abs(k-row) == 2 :
            transitional_probability_value = 0.5
        elif abs(k-row) == 1 :
            transitional_probability_value = 0.7
        elif abs(k-row) == 0 :
            transitional_probability_value = 0.9
        else:
            transitional_probability_value = 0
        viterbi_value_before = viterbi_table[k][col-1]
        viterbi_value.append((transitional_probability_value*viterbi_value_before))
    
    emission_value = (emission_probability[row][col])   
    return (emission_value * max(viterbi_value))


# main program
#
if __name__ == "__main__":

    if len(sys.argv) != 6:
        raise Exception("Program needs 5 parameters: input_file airice_row_coord airice_col_coord icerock_row_coord icerock_col_coord")

    input_filename = sys.argv[1]
    gt_airice = [ int(i) for i in sys.argv[2:4] ]
    gt_icerock = [ int(i) for i in sys.argv[4:6] ]

    # load in image 
    input_image = Image.open(input_filename).convert('RGB')    
    image_array = array(input_image.convert('L'))
    


    
    # # compute edge strength mask -- in case it's helpful. Feel free to use this.

    
    edge_strength_variable = edge_strength(input_image)
    col_array = []
    simple_air_ice_array = []
    simple_ice_rock_array = []
    hmm_air_ice = []
    count = 0
    difference_edge_full = []
    hmm_ice_rock = []
    emission_probability = [[0 for i in range(len(edge_strength_variable[0]))] for j in range(len(edge_strength_variable))]
    edge_strength_variable = [[edge_strength_variable[j][i] for i in range(len(edge_strength_variable[0]))] for j in range(len(edge_strength_variable))  ]


    ######emission probability#####
    # for i in range(len(edge_strength_variable[0])):
    #     sum1 = 0
    #     for j in range(len(edge_strength_variable)):
    #         sum1 = sum1+edge_strength_variable[j][i]
    #     for j in range(len(edge_strength_variable)):
    #         emission_probability[j][i] = edge_strength_variable[j][i]/sum1

    
    
    for i in range(len(edge_strength_variable)):
        for j in range(len(edge_strength_variable[0])):
            emission_probability[i][j] = (edge_strength_variable[i][j]/image_array[i][j])



    for i in range(len(emission_probability[0])):
        col_array = []
        for j in range(0,len(emission_probability)):
            col_array.append(emission_probability[j][i])
        simple_air_ice_array.append(col_array.index(max(col_array)))

    indexes = int(mean(simple_air_ice_array)+10)

    emission_probability_copy = copy.deepcopy(emission_probability)

    
    emission_probability_array = np.array(emission_probability_copy)
    for i in range(0,len(emission_probability_array[0])):
        emission_probability_array[0:indexes,i] = 0
    emission_probability_copy = emission_probability_array

    
    for i in range(len(emission_probability_copy[0])):
        col_array = []
        for j in range(len(emission_probability_copy)):
            col_array.append(emission_probability_copy[j][i])
        simple_ice_rock_array.append(col_array.index(max(col_array)))

    
    viterbi_table = [[0 for i in range(len(edge_strength_variable[0]))] for j in range(len(edge_strength_variable))]
    for r in range(0,len(edge_strength_variable)):
        viterbi_table[r][0] = (1/len(edge_strength_variable)) * emission_probability[r][0]



    for i in range(1,len(emission_probability[0])):
        for j in range(0,len(emission_probability)):
            viterbi_table[j][i] = viterbi_value(emission_probability, viterbi_table, j, i)

    
    array_em = np.array(viterbi_table)
    array_em_t = array_em.T
    for row in array_em_t:
        row = list(row)
        hmm_air_ice.append(row.index(max(row)))

    
    indexes = int(mean(hmm_air_ice)+10)
    emission_probability_copy = copy.deepcopy(emission_probability)
    emission_probability_array = np.array(emission_probability_copy)
    for i in range(0,len(emission_probability_array[0])):
        emission_probability_array[0:indexes,i] = 0
    emission_probability_copy = emission_probability_array

    
    viterbi_table_ice_rock = [[0 for i in range(len(edge_strength_variable[0]))] for j in range(len(edge_strength_variable))]
    for r in range(0,len(edge_strength_variable)):
        viterbi_table_ice_rock[r][0] = (1/len(edge_strength_variable)) * emission_probability_copy[r][0]
    for i in range(1,len(emission_probability_copy[0])):
        for j in range(0,len(emission_probability_copy)):
            viterbi_table_ice_rock[j][i] = viterbi_value(emission_probability_copy, viterbi_table_ice_rock, j, i)
   


    
    array_em = np.array(viterbi_table_ice_rock)
    array_em_t = array_em.T
    for row in array_em_t:
        row = list(row)
        hmm_ice_rock.append(row.index(max(row)))
     
    
    for i in range(len(emission_probability)):
        sum1 = 0
        sum1 = sum1+emission_probability[j][gt_airice[0]]
    
    emission_probability_air_ice_feedback = copy.deepcopy(emission_probability)
    for y in range(len(emission_probability_air_ice_feedback)):
        if y == gt_airice[1]:
            emission_probability_air_ice_feedback[y][gt_airice[0]] = sum1
        else:
            emission_probability_air_ice_feedback[y][gt_airice[0]] = 0
    
    viterbi_table_air_ice_feedback = [[0 for i in range(len(edge_strength_variable[0]))] for j in range(len(edge_strength_variable))]
    for r in range(0,len(edge_strength_variable)):
        viterbi_table_air_ice_feedback[r][0] = (1/len(edge_strength_variable)) * emission_probability_air_ice_feedback[r][0]
    for i in range(1,len(emission_probability_copy[0])):
        for j in range(0,len(emission_probability_copy)):
            viterbi_table_air_ice_feedback[j][i] = viterbi_value(emission_probability_air_ice_feedback, viterbi_table_air_ice_feedback, j, i)
    
    feedback_air_ice = []    
    array_em = np.array(viterbi_table_air_ice_feedback)
    array_em_t = array_em.T
    for row in array_em_t:
        row = list(row)
        feedback_air_ice.append(row.index(max(row)))

    
    indexes = int(mean(feedback_air_ice)+10)
    emission_probability_copy = copy.deepcopy(emission_probability)
    emission_probability_array = np.array(emission_probability_copy)
    for i in range(0,len(emission_probability_array[0])):
        emission_probability_array[0:indexes,i] = 0
    emission_probability_copy = emission_probability_array
    
    
    for i in range(len(emission_probability_copy)):
        sum1 = 0
        sum1 = sum1+emission_probability_copy[j][gt_icerock[1]]
    
    emission_probability_ice_rock_feedback = copy.deepcopy(emission_probability_copy)
    for y in range(len(emission_probability_ice_rock_feedback)):
        if y == gt_icerock[1]:
            emission_probability_ice_rock_feedback[y][gt_icerock[0]] = sum1
        else:
            emission_probability_ice_rock_feedback[y][gt_icerock[0]] = 0
    
    viterbi_table_ice_rock_feedback = [[0 for i in range(len(edge_strength_variable[0]))] for j in range(len(edge_strength_variable))]
    for r in range(0,len(edge_strength_variable)):
        viterbi_table_ice_rock_feedback[r][0] = (1/len(edge_strength_variable)) * emission_probability_ice_rock_feedback[r][0]
    for i in range(1,len(emission_probability_copy[0])):
        for j in range(0,len(emission_probability_copy)):
            viterbi_table_ice_rock_feedback[j][i] = viterbi_value(emission_probability_ice_rock_feedback, viterbi_table_ice_rock_feedback, j, i)

    
    feedback_ice_rock = []    
    array_em = np.array(viterbi_table_ice_rock_feedback)
    array_em_t = array_em.T
    for row in array_em_t:
        row = list(row)
        feedback_ice_rock.append(row.index(max(row)))


    imageio.imwrite('edges.png', uint8(255 * edge_strength(input_image) / (amax(edge_strength(input_image)))))


    #airice_simple = []
    airice_simple = simple_air_ice_array
    #airice_simple = [ image_array.shape[0]*0.25 ] * image_array.shape[1]
    #airice_hmm = []
    airice_hmm = hmm_air_ice
    #airice_hmm = [ image_array.shape[0]*0.5 ] * image_array.shape[1]
    #airice_feedback = []
    airice_feedback = feedback_air_ice
    #airice_feedback= [ image_array.shape[0]*0.75 ] * image_array.shape[1]

    #icerock_simple = []
    icerock_simple = simple_ice_rock_array
    #icerock_simple = [ image_array.shape[0]*0.25 ] * image_array.shape[1]
    #icerock_hmm = []
    icerock_hmm = hmm_ice_rock
    #icerock_hmm = [ image_array.shape[0]*0.5 ] * image_array.shape[1]
    #icerock_feedback = []
    icerock_feedback = feedback_ice_rock
    #icerock_feedback= [ image_array.shape[0]*0.75 ] * image_array.shape[1]

    # Now write out the results as images and a text file
    input_image_copy = copy.deepcopy(input_image)
    write_output_image("air_ice_output.png", input_image_copy, airice_simple, airice_hmm, airice_feedback, gt_airice)
    write_output_image("ice_rock_output.png", input_image, icerock_simple, icerock_hmm, icerock_feedback, gt_icerock)
    input_image_copy = copy.deepcopy(input_image)
    with open("layers_output.txt", "w") as fp:
        for i in (airice_simple, airice_hmm, airice_feedback, icerock_simple, icerock_hmm, icerock_feedback):
            fp.write(str(i) + "\n")
