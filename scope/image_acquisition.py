import os
import freeimage
import numpy as np
def get_image_sequence_simple(scope, positions, out_dir, lamp=None):
    '''
        lamp - List of the form (exposure time, lamp_name)
    '''
    # Different filter set 
    # New acquisition sequences
    lamp_dict = {'uv': 'dapi', 'red':'cy5'}
    scope.camera.live_mode=False
    # ~/device/acquisition_sequencer 
    # This part is hard-coded, maybe it's ok. 
    # Unpack position_data into the two image and three image 
    #######################################################
    
    #######################################################
    position_data = positions[1]
    #########################################
    # Current setting: TL: 10ms; Cy5:500ms at intensity=255,
    # Dapi : 10ms at intensity = 255. 
    # Major change of calling 
    #########################################
    # Take pictures for the original spots
    for pos_num, this_position_data in enumerate(position_data):
        # Why do we have to pass this location?
        scope.nosepiece.position = this_position_data[0]
        # x,y,z positions
        scope.stage.position = this_position_data[1:]
        my_images = scope.camera.acquisition_sequencer.run()
        freeimage.write(my_images[0], out_dir+os.path.sep
        +'_{:03d}_'.format(this_position_data[1])+ '_{:03d}_'.format(pos_num)+'.png')
        if lamp is not None: 
            # Add UV image
            freeimage.write(my_images[1], out_dir + os.path.sep + '_{:03d}_'.format(pos_num)+'.png')
            # Here added the Cy5 image
            freeimage.write(my_images[2], out_dir+os.path.sep+os.path.sep + '_{:03d}_'.format(pos_num)+'.png')
    # Only saving the cy5 image
    cy5_position = positions[2]
    for pos_num, this_position_data in enumerate(cy5_position):
        scope.nosepiece.position = this_position_data[0]
        scope.stage.position = this_position_data[1]
        my_images = scope.camera.acquisition_sequencer.run()
        if lamp is not None:
            freeimage.write(my_images[2], out_dir+os.path.sep+os.path.sep + '_{:03d}_'.format(pos_num+ len(position_data))+'.png')

def get_objpositions(scope):
    """Return a list of interactively-obtained scope stage positions."""
    positions = []
    print('Press enter after each position has been found; press control-c to end')
    while True:
        try:
            input()
        except KeyboardInterrupt:
            break
        
        positions.append(scope.stage.position)
        # Calling the objective? 
        positions[-1].insert(0,scope.nosepiece.position)
        print('Position {}: {}'.format(len(positions), tuple(positions[-1])), end='')
        # Using the first created positions 
        if len(positions) <= 2:
            # Check if the first two positions are at the same location and specify the max and mean
            if [positions[0][1],positions[0][2]] is not positions[1][1]:
                print('Must specify z_max and z_min using a given coordinate!')
                break
            z_min = positions[0][-1]
            z_max = positions[1][-1]
            print('The z value should be {}'.format((z_min+z_max)/2), end = '')
    # Make sure max is bigger than min
    if z_min > z_max:
        z_min, z_max = z_max, z_min
    # Calculate all the z-stack coordinate.
    interval = (z_max - z_min)/10
    z_stack = np.arange(z_min, z_max, step = interval)
    z_stack.remove((z_min+z_max)/2)
    new_positions = []
    # Rewrite to have a new list of calculated z value
    for position in positions:
        for z_value in z_stack:
            new_position = position[0:3].append(z_value)
            new_positions.append(new_position)

    # Return a json file storing the 
    return (positions, new_positions)

    # Save out a file for matching numbers and images. 
