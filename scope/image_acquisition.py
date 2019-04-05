import os
import freeimage
import numpy as np
def get_image_sequence_simple(scope, position_data, out_dir, lamp=None):
    '''
        lamp - List of the form (exposure time, lamp_name)
    '''
    # Different filter set 
    # New acquisition sequences
    # On the wiki filter set
    # Here double check the name of the filters
    lamp_dict = {'uv': 'dapi', 'red':'cy5'}
    scope.camera.live_mode=False
    # ~/device/acquisition_sequencer 
    scope.camera.acquisition_sequencer.new_sequence()
    # This part is hard-coded, maybe it's ok. 
    #########################################
    # Current setting: TL: 10ms; Cy5:500ms at intensity=255,
    # Dapi : 10ms at intensity = 255. 
    # Major change of calling 
    #########################################
    scope.camera.acquisition_sequencer.add_step(25,'TL', tl_intensity=255)
    scope.camera.acquisition_sequencer.add_step(25,'UV')
    scope.camera.acquisition_sequencer.add_step(500,'CY5')
    # Add new lamp, there are only two lamps, Dapi and cy5. 
    if lamp is not None: scope.camera.acquisition_sequencer.add_step(lamp[0],lamp[1])
    # Deal with output directory. 
    if not os.path.isdir(out_dir): os.mkdir(out_dir)
    # Take images at given positions. 
    for pos_num, this_position_data in enumerate(position_data):
        # Why do we have to pass this location?
        scope.nosepiece.position = this_position_data[0]
        # x,y,z positions
        scope.stage.position = this_position_data[1:]
        my_images = scope.camera.acquisition_sequencer.run() 
        freeimage.write(my_images[0], out_dir+os.path.sep+'_{:03d}_bf.png'.format(pos_num))
        if lamp is not None: 
            freeimage.write(my_images[1], out_dir+os.path.sep+'_{:03d}_'.format(pos_num)+lamp_dict[lamp[1]]+'.png')
            # Here added the Cy5 image
            freeimage.write(my_images[2], out_dir+os.path.sep+'_{:03d}_'.format(pos_num)+lamp_dict[lamp[2]]+'.png')  

def get_image_sequence(scope, position_data, out_dir, lamp=None):
    '''
        lamp - List of lists of the form [[lamp_exposure1,lamp_name1],...]
    '''
    
    #if lamp is None:
        #lamp = [[2, 'TL']]
    #if not any([arg[1] is 'TL' for arg in lamp]):
        #lamp.append([2,'TL'])
        
    
    lamp_dict = {'cyan':'gfp','green_yellow':'RedmChr'}
    
    scope.camera.live_mode=False
    scope.camera.acquisition_sequencer.new_sequence()
    for lamp_exposure, lamp_name in lamp:
        if lamp_name is not 'TL': scope.camera.acquisition_sequencer.add_step(lamp_exposure, lamp_name)
        else: scope.camera.acquisition_sequencer.add_step(lamp_exposure, lamp_name, tl_intensity=255)
    if not os.path.isdir(out_dir): os.mkdir(out_dir)
    for pos_num, this_position_data in enumerate(position_data):
        scope.nosepiece.position = this_position_data[0]
        scope.stage.position = this_position_data[1:]
        my_images = scope.camera.acquisition_sequencer.run() 

        for (lamp_exposure, lamp_name, this_image) in zip([arg[0] for arg in lamp],[arg[1] for arg in lamp], my_images):
            if lamp_name is 'TL': freeimage.write(this_image, out_dir+os.path.sep+'_{:03d}_bf_{}_ms'.format(pos_num,lamp_exposure)+'.png')
            else: freeimage.write(this_image, out_dir+os.path.sep+'_{:03d}_'.format(pos_num)+lamp_dict[lamp_name]+'_{}_ms'.format(lamp_exposure)+'.png')

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
        else:
            for z in z_stack:
                new_position = position
                new_position[3] = z
                new_positions.append(new_position)
                
    new_positions = sorted(new_positions)
    return new_positions



