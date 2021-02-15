import os
import freeimage
import numpy as np
import pickle

def get_image_sequence(scope, positions, out_dir, lamp = None):
    '''
    Main function of image acquisition. 
    Take pictures according to pre-determined positions.
    ==Input==
    scope: ScopeClient instance
    positions: a list of positions acquired.
    out_dir: string of output directory.
    lamp: a list of lists of the form [[lamp1_exposure, lamp1_name]]
    '''
    # Check if the output directory is created
    if not os.path.isdir(out_dir): os.mkdir(out_dir)
    # Create a lookbook for position number and the coordinate
    phone_book = {}
    for pos_num, this_position_data in enumerate(positions):
        phone_book[str(pos_num)] = this_position_data
    with open(out_dir + os.path.sep + 'phonebook.pkl', 'wb') as handle:
        pickle.dump(phone_book, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # Doublecheck if this is the correct way of running this. 
    lamp_dict = {'uv': 'dapi', 'red':'cy5', 'TL':'trans'}
    scope.camera.live_mode = False
    scope.camera.acquisition_sequencer.new_sequence()
    for lamp_exposure, lamp_name in lamp:
        if lamp_name is not 'TL':
            # Don't need to set non-TL intensity, since they will be default at maximum
             scope.camera.acquisition_sequencer.add_step(lamp_exposure, lamp_name)
        else:
            scope.camera.acquisition_sequencer.add_step(lamp_exposure, lamp_name, tl_intensity = 255)

    # Take pictures.
    for pos_num, this_position_data in enumerate(positions):
        scope.nosepiece.position = this_position_data[0]
        # x, y, z postions
        scope.stage.position = this_position_data[1:]
        my_images = scope.camera.acquisition_sequencer.run()
        for (lamp_exposure, lamp_name, this_image) in zip([arg[0] for arg in lamp],[arg[1] for arg in lamp], my_images):
            freeimage.write(this_image, out_dir+os.path.sep+'{:03d}_'.format(pos_num)+lamp_dict[lamp_name]+'.png')


def get_objpositions(scope):
    '''
    Get coordinates from GUI for image taking.
    ==Input==
    scope: ScopeClient instance
    ==Output==
    positions: a list of coordinates (z axis unique for one location, run get_z_
    stack for expanding to z stack)
    '''
    # Initialize an empty list to hold positions
    positions = []
    print('Press enter after each poisitions has been found, press control-c to end')
    while True:
        try:
            input()
        except KeyboardInterrupt:
            break
        positions.append(scope.stage.position)
        # Record the nose piece, AKA which objective to use.
        positions[-1].insert(0, scope.nosepiece.position)
        print('Position {}:{}'.format(len(positions), tuple(positions[-1])), end = '')
    return positions 

def get_z_stack(positions, step):
    '''
    return a z-stack of coordinate based on input positions and the step change.
    the default is 11 images total centering on the original input z value for each 
    xy location.
    ==Input==
    positions: a list of positions
    step: a float of a step each image should take. 
    ==Output==
    positions_z: a list of positions with z-stack coordinates added. 
    '''
    complete_positions = []
    num_of_image = 10
    for a_position in positions:
        # Only get the z coordinate 
        z_position = a_position[-1]
        print('what is z', z_position)
        xy_position = a_position[0:3]
        print('xy position is ,', xy_position)
        # Get the minimum and maximum z value for the z stack pictures
        min_z, max_z = [z_position - num_of_image/2*step, z_position + (num_of_image/2+ 1)*step]
        # create the z_step image. 
        z_stack = np.arange(min_z, max_z, step)
        # Remove the original z value.
        print('what is new z stack', z_stack)
        # Create extra coordinates for image-taking
        a_position_zvalues = []
        for z_value in z_stack:
            new_position = a_position[0:3] 
            new_position.append(z_value)
            a_position_zvalues.append(new_position)
            print('new_position', new_position)
        complete_positions.extend(a_position_zvalues)
    return complete_positions
