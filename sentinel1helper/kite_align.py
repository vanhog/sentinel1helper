from kite import Scene
import matplotlib.pyplot as plt
import numpy as np 
import os
from matplotlib import cm, colors

#primary_scene = Scene.load('/media/hog/docCrucial1T/msc_grond_noemi/volume_opti/data/events/roenne/insar_float32_losturn/tl5_l2b_a_044_01_mscaoi_f32_foccov_losturn.npz')
primary_scene = Scene.load('/media/hog/hogsandisc/data/mscthesisdata/insar_float32_losturn_v1/tl5_l2b_a_117_02_mscaoi_f32_foccov_losturn.npz')
noisecoords = primary_scene.covariance.noise_coord
sourceeps = primary_scene.quadtree.epsilon
sourcenan = primary_scene.quadtree.nan_allowed
sourcemintile = primary_scene.quadtree.tile_size_min
sourcemaxtile = primary_scene.quadtree.tile_size_max
sourcetitle = primary_scene.meta.scene_title
sourceID = primary_scene.meta.scene_id
sourceorbit = primary_scene.meta.orbital_node
sourcesatellite = primary_scene.meta.satellite_name
#sourceblack   = primary_scene.quadtree.config.leaf_blacklist
sourcepolygm  = primary_scene.config.polygon_mask
print('noisecoords:\t', noisecoords)
print('eps: \t', sourceeps)
print('nan: \t', sourcenan)
print('tilemin:\t', sourcemintile)
print('tilemax:\t', sourcemaxtile)
#print('polyonm:\t', sourcepolygm)
print('Satellite:\t', sourcesatellite)
print('Orbit:\t', sourceorbit)
target_scene = Scene.load('/home/hog/Downloads/tl5_a_117_02_mscaoi_Sent1ABfilt.npz')
target_scene.config.polygon_mask = sourcepolygm
target_scene.quadtree.epsilon = sourceeps
target_scene.quadtree.nan_allowed = sourcenan
target_scene.quadtree.tile_size_min = sourcemintile
target_scene.quadtree.tile_size_max = sourcemaxtile
target_scene.meta.scene_title = sourcetitle
target_scene.meta.scene_id = sourceID
target_scene.meta.orbital_node = sourceorbit 
target_scene.meta.satellite = sourcesatellite
#target_scene.quadtree.config.leaf_blacklist = sourceblack
target_scene.covariance.noise_coord = noisecoords
#covfull = target_scene.covariance.covariance_matrix
out_filename = os.path.basename(os.path.realpath(primary_scene.meta.filename))
out_dir = '/media/hog/hogsandisc/data/mscthesisdata/insar_float32_losturn_v3/'
out_path = out_dir + out_filename
target_scene.save(out_path)
print('happy days')