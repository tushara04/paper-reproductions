from scipy import ndimage as ndi
import numpy as np

from skimage.filters import threshold_local

import skimage as skm
from skimage.morphology import skeletonize,remove_small_objects,label
from skimage import morphology

from skimage.transform import rescale
from skimage.filters import gaussian

from skimage.morphology import disk,binary_dilation
from skimage.morphology import binary_erosion

###############################################################################################################################
def skeletonize_TEM_GS(img,mf,dsf):
    #(3)args: image file [.png, .tiff, .bmp],resolution [pxls/um],downscale factor [~45%]
    
    median_size = 0.04                   # in um: for median smoothing 
    median_pxs = int(median_size*mf*dsf) # targeted lenght in pxls
    
    gaussian_R_um = 0.115                # in um: pixel neighborhood
    gaussian_R_pxls = mf*dsf*gaussian_R_um
    
    image_rescaled = rescale(img, dsf, anti_aliasing=True,multichannel=False)
    image_rescaled1 = ndi.median_filter(skm.util.img_as_float(image_rescaled), size=median_pxs)
    binary_local = image_rescaled1 > threshold_local(image_rescaled1, block_size =25,\
                                        method='gaussian',offset=0.04,param=gaussian_R_pxls)#offset:0.04
    
    #******************************** skeletonizing ********************************
    mask = binary_local
    path_ske = skeletonize(1-mask).astype(np.uint16)  
    label_pxl = morphology.label(path_ske)
    path_ske1 = morphology.remove_small_objects(label_pxl,min_size=600)
    path_ske1 = (path_ske1>0)
    
    return(path_ske, path_ske1)

###############################################################################################################################
from skimage.morphology import convex_hull_image,binary_closing
from skimage import filters
import pixel_pruning as pxlpr

def prune_skeleton(bin_mask,mf,dsf):
    
    # protect the tips and remove outer cycles
    selem = disk(int(0.04*mf*dsf))  # fill out areas smaller than 50nm
    closed = binary_closing(bin_mask, selem)
    ske_open =  skeletonize(closed) # skeletonize again

    chull = convex_hull_image(ske_open)*1
    r_polg = np.sqrt(np.sum(chull)/np.pi) # derive the radius from its area
    sel = disk(int(r_polg*0.03))          # shirink down the convex hull by 3%
    chull_eroded = binary_erosion(chull, selem = sel)
    
    edge_roberts = filters.roberts(chull_eroded) 
    edge_roberts = np.where(edge_roberts>0, 1, edge_roberts)
    arr = (edge_roberts)   # adding 1pxl-wide convex to protec the tips
    pattern_surr =  np.where((edge_roberts+ske_open)>0,1,(edge_roberts+ske_open)).astype(int)
    
    #path_skel_fin0 = pxlpr.pruning(pattern_surr, 0) - edge_roberts #prunn up to 50 nm
    path_skel_fin0 = pxlpr.pruning(pattern_surr, (int(0.2*mf*dsf))) - edge_roberts #prunn up to 50 nm
    path_skel_fin0 = path_skel_fin0.astype(int)
    
    label_pxl = morphology.label(path_skel_fin0) # remove convex cut-off
    path_skel_fin = morphology.remove_small_objects(label_pxl,min_size=100)
    
    return(path_skel_fin)
###############################################################################################################################
from skimage.measure import regionprops
from skimage.morphology import convex_hull_image

def valve_props(ske_bin,mf,dsf):
    
    chull = convex_hull_image(ske_bin)*1
    label_img = label(chull)
    props = regionprops(label_img)
    
    O_x = props[0].centroid[1]
    O_y = props[0].centroid[0]
    
    R_ef = props[0].perimeter/(2*np.pi)/(mf*dsf)   # in um
    Val_s = props[0].area/((mf*dsf)**2)            # in um^2
    
    return(O_x,O_y,R_ef,Val_s)  
