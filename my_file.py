### Emma Steuer
import sys
import numpy as np
import math 


dictionary_of_data = {

    # Initialize a dictionary to fit all data in.

    'satellite': {},
    'user': {},
    'interferer': {},
    'user_connections': {}
}

def read_file(filename):

    '''This function opens a test case file and reads only the data.'''
    
    with open(filename) as f:
        content = f.readlines()
    test_cases=[]
    for line in content:
        
        if line[0] == "\n":
            line="#"
        li=line.strip()
        if not li.startswith("#"):
            split_line=li.split(' ')
            line_item=(split_line[0], int(split_line[1]), float(split_line[2]), float(split_line[3]), float(split_line[4]))
            test_cases.append(line_item)
    return test_cases

def dictionary_for_data(file_data):

    '''
    This function takes data from the test case file and loads it into the dictionary.
    '''

    for i in file_data:
        
        if i[0] == 'sat':
            dictionary_of_data['satellite'][i[1]] = np.array((i[2], i[3], i[4]))
            dictionary_of_data['user_connections'][i[1]] = []

        elif i[0] == 'user':
            dictionary_of_data['user'][i[1]] = np.array((i[2], i[3], i[4]))
  
        elif i[0] == 'interferer':
            dictionary_of_data['interferer'][i[1]] = np.array((i[2], i[3], i[4]))

        else:
            print("there's been an error, parsed incorrectly")
            return False

    return True

def angle_between_two_vectors(v1, v2):

    '''This function takes two vectors and finds the angle between them.'''

    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)

    return ((360/math.tau) * (np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))))
 
def any_connection_possible(user_location, satellite_location):

    '''
    This function checks to see if the user is able to see the satellite (45degree distance or less)
    and also checks to see if the interferring satellite's location is far enough away from the satellite.
    '''

    if 45.0 <= angle_between_two_vectors(user_location, satellite_location - user_location):
        return False

    for interferer_location in dictionary_of_data['interferer'].values():
        if 20.0 >= angle_between_two_vectors(satellite_location - user_location, interferer_location - user_location):
            return False

    return True

def color_connection_possible(color, sat_id, user_location):

    '''
    This function checks to see if there are two of the same color on the satellite, 
    if those beams are far enough away from each other.
    '''
    sat_location = dictionary_of_data['satellite'][sat_id]
    for beam in dictionary_of_data['user_connections'][sat_id]:
        if color == beam['color']:
            if 10.0 >= angle_between_two_vectors(sat_location - user_location, sat_location - dictionary_of_data['user'][beam['user']]):
                return False

    return True

def heuristic(sat_id):
    '''
    This function returns how many beams a satellite has currently.
    '''
    return len(dictionary_of_data['user_connections'][sat_id])

def run_through_scenario(dictionary_of_data):

    '''
    This function runs through each scenario. It does this heuristically, by finding which satellite has the least
    number of beams and the least number of colors so far.
    Then, it adds each beam and it's information to the dictionary.
    '''

    colors = ['A', 'B', 'C', 'D']

    sats_list = list(dictionary_of_data['satellite'].items())
    
    for user_id, user_location in dictionary_of_data['user'].items():
        
        best_score = float('inf')
        best_satellite = None
        best_color = None
        
        import random
        
        for _ in range(len(dictionary_of_data['satellite'])):
            sat_id, sat_location = random.choice(sats_list)

            current_score= heuristic(sat_id)
            
            if len(dictionary_of_data['user_connections'][sat_id]) >= 32:
                break
            
            if any_connection_possible(user_location, sat_location):
                for color in colors:
                    
                    if color_connection_possible(color, sat_id, user_location):
                        if current_score < best_score: 
                            best_score = current_score
                            best_satellite = sat_id
                            best_color = color
               

        if best_satellite is not None:
            dictionary_of_data['user_connections'][best_satellite].append({
                'user': user_id,
                'color': best_color,
            })

    for sat_id, sat_beams in dictionary_of_data['user_connections'].items():
        for index, beam in enumerate(sat_beams):
            print(f"sat {sat_id} beam {(index + 1)} user {beam['user']} color {beam['color']}")
    

def main():

    dictionary_for_data(read_file(sys.argv[1]))
    run_through_scenario(dictionary_of_data)
  
main()
