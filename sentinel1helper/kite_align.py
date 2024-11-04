from kite import Scene
import matplotlib.pyplot as plt
import numpy as np 
import os
from matplotlib import cm, colors

#source_scene = Scene.load('/media/hog/docCrucial1T/msc_grond_noemi/volume_opti/data/events/roenne/insar_float32_losturn/tl5_l2b_a_044_01_mscaoi_f32_foccov_losturn.npz')
source_scene = Scene.load('/media/hog/Iomega HDD/mscdata/insar_float32_losturn/tl5_l2b_d_139_01_mscaoi_f32_foccov_losturn.npz')
noisecoords = source_scene.covariance.noise_coord
sourceeps = source_scene.quadtree.epsilon
sourcenan = source_scene.quadtree.nan_allowed
sourcemintile = source_scene.quadtree.tile_size_min
sourcemaxtile = source_scene.quadtree.tile_size_max
sourcetitle = source_scene.meta.scene_title
sourceID = source_scene.meta.scene_id
sourceorbit = source_scene.meta.orbital_node
sourcesatellite = source_scene.meta.satellite_name
#sourceblack   = source_scene.quadtree.config.leaf_blacklist
sourcepolygm  = source_scene.config.polygon_mask
print('noisecoords:\t', noisecoords)
print('eps: \t', sourceeps)
print('nan: \t', sourcenan)
print('tilemin:\t', sourcemintile)
print('tilemax:\t', sourcemaxtile)
#print('polyonm:\t', sourcepolygm)
print('Satellite:\t', sourcesatellite)
print('Orbit:\t', sourceorbit)
target_scene = Scene.load('/media/hog/Iomega HDD/mscdata/tl5_d_139_01_mscaoi_sent1ABmv.npz')
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
out_filename = os.path.basename(os.path.realpath(source_scene.meta.filename))
out_dir = '/media/hog/Iomega HDD/mscdata/'
out_path = out_dir + out_filename
target_scene.save(out_path)
print('happy days')