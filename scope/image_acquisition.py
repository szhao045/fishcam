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
    position_data = positions[1]
    #########################################
    # Current setting: TL: 10ms; Cy5:500ms at intensity=255,
    # Dapi : 10ms at intensity = 255. 
    # Major change of calling 
    #########################################
    # Take pictures for the original spots
    for this_position_data in position_data:
        # Why do we have to pass this location?
        scope.nosepiece.position = this_position_data[0]
        # x,y,z positions
        scope.stage.position = this_position_data[1:]
        my_images = scope.camera.acquisition_sequencer.run()
        freeimage.write(my_images[0], out_dir+os.path.sep
        +'_{:03d}_'.format(this_position_data[1])+ '_{:03d}_'.format(this_position_data[2]) 
        + '_{:06d}_'.format(this_position_data[3])+'.png')
        if lamp is not None: 
            # Add UV image
            freeimage.write(my_images[1], out_dir + os.path.sep
        +'_{:03d}_'.format(this_position_data[1])+ '_{:03d}_'.format(this_position_data[2]) 
        + '_{:06d}_'.format(this_position_data[3])+'.png')
            # Here added the Cy5 image
            freeimage.write(my_images[2], out_dir+os.path.sep+os.path.sep
        +'_{:03d}_'.format(this_position_data[1])+ '_{:03d}_'.format(this_position_data[2]) 
        + '_{:06d}_'.format(this_position_data[3])+'.png') 
    # Only saving the cy5 image
    cy5_position = positions[2]
    for this_position_data in cy5_position:
        scope.nosepiece.position = this_position_data[0]
        scope.stage.position = this_position_data[1]
        my_images = scope.camera.acquisition_sequencer.run()
        if lamp is not None:
            freeimage.write(my_images[2], out_dir+os.path.sep+os.path.sep
        +'_{:03d}_'.format(this_position_data[1])+ '_{:03d}_'.format(this_position_data[2]) 
        + '_{:06d}_'.format(this_position_data[3])+'.png') 

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
        if len(positions) <= 2:
            z_min = positions[1][2]
            z_max = positions[2][2]
    # Calculate all the z-stack coordinate.
    interval = (z_max - z_min)/10
    z_stack = range(z_min, z_max, step = interval)
    new_positions = []
    for position in positions:
        if len(position) != 4:
            for z in z_stack:
                new_position = position
                new_position.insert(3,z)
                new_positions.append(new_position)
    new_positions = sorted(new_positions)
    return (positions, new_positions)