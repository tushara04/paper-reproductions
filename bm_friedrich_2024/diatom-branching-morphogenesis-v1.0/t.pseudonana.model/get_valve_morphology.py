import numpy as np
import skimage as skm
import skimage.measure as mea
import skimage.morphology as mrph
from skimage.draw import circle

ds0 = 0.8*0.4 # <--check it before the run! global variable

# *********************** Valve size estimate in um**2 ***********************

def valve_size_estiamte(skel_in,mf,ds):
    chull = mrph.convex_hull_image(skel_in)*1
    A = np.sum(chull*1)/(mf*ds0)**2
    return A

# ****************************  valve centroid  ****************************

def find_valve_center(skel):
    chull = mrph.convex_hull_image(skel)*1
    props = mea.regionprops(chull)
    # make convex hul and then find its centroid
    O_x = props[0].centroid[1]
    O_y = props[0].centroid[0]  
    # array output
    v_cen = np.array([O_x,O_y])
    return(v_cen)

# ****************************   Tips count    ****************************

import mahotas as mh

def tips_pos(skel_path):
    # straight and diadonally connected tips
    EP_s0_ker=np.array([[0, 0, 0],[0, 1, 0],[2, 1, 2]])
    EP_d0_ker=np.array([[0, 2, 1],[0, 1, 2],[0, 0, 0]])
    # varying position of the tips 
    EP_s1_ker = EP_s0_ker.T 
    EP_s2_ker = np.fliplr(EP_s1_ker)
    EP_s3_ker = np.flipud(EP_s0_ker)
    # varying position of the tips
    EP_d1_ker = EP_d0_ker.T #2
    EP_d2_ker = np.fliplr(EP_d1_ker)
    EP_d3_ker = np.fliplr(EP_d0_ker)
    EP_list  = [EP_s0_ker,EP_s1_ker,EP_s2_ker,EP_s3_ker,\
                EP_d0_ker,EP_d1_ker,EP_d2_ker,EP_d3_ker]
    # create a dummy array
    EP_all = np.zeros(np.shape(skel_path))
    for kers in EP_list:
        EP=mh.morph.hitmiss(skel_path,kers)
        EP_all = EP + EP_all
    # mark pixels' position in 2d-array   
    return(np.nonzero(EP_all))


# ****************************   Branches count    ****************************

def branch_pos(skel_path):
    # y0- y1- and t0- oriented branches
    EP_y0_ker=np.array([[1, 0, 1],[2, 1, 2],[2, 1, 2]])
    EP_y1_ker=np.array([[0, 2, 1],[1, 1, 2],[0, 1, 0]])
    EP_t0_ker=np.array([[0, 0, 0],[1, 1, 1],[2, 1, 2]])
    EP_d0_ker=np.array([[1, 2, 1],[2, 1, 2],[1, 2, 0]])
    # varying position of the branches 
    EP_y01_ker = EP_y0_ker.T 
    EP_y02_ker = np.fliplr(EP_y01_ker)
    EP_y03_ker = np.flipud(EP_y0_ker)
    # varying position of the branches
    EP_y11_ker = EP_y1_ker.T 
    EP_y12_ker = np.fliplr(EP_y11_ker)
    EP_y13_ker = np.flipud(EP_y11_ker)
    # varying position of the branches
    EP_t01_ker = EP_t0_ker.T 
    EP_t02_ker = np.fliplr(EP_t01_ker)
    EP_t03_ker = np.flipud(EP_t0_ker)
    # varying position of the branches
    EP_d01_ker = EP_d0_ker.T 
    EP_d02_ker = np.fliplr(EP_d01_ker)
    EP_d03_ker = np.flipud(EP_d0_ker)
    
    EP_list  = [EP_y0_ker,EP_y01_ker,EP_y02_ker,EP_y03_ker,\
                EP_y1_ker,EP_y11_ker,EP_y12_ker,EP_y13_ker,\
                EP_t0_ker,EP_t01_ker,EP_t02_ker,EP_t03_ker,\
                EP_d0_ker,EP_d01_ker,EP_d02_ker,EP_d03_ker]
    # create a dummy array
    EP_all = np.zeros(np.shape(skel_path))
    for kers in EP_list:
        EP=mh.morph.hitmiss(skel_path,kers)
        EP_all = EP + EP_all
    # mark pixels' position in 2d-array    
    return(np.nonzero(EP_all))

# ****************************   find cross-connections    ****************************

from skimage.graph import route_through_array
"""
def find_cross_connections(skel,branch_indx,v_cen,mf):
    # adjacency matrix for branch to brach path
    N = len(branch_indx[0])
    adjacency_M = np.zeros((N,N))

    branch_indx_merged = np.stack((branch_indx[0], branch_indx[1]), axis=-1) # y,x coordinates
    for i in range(N):
        for j in range(N):
            b1 = branch_indx_merged[i,:]
            b2 = branch_indx_merged[j,:]
            adjacency_M[i,j] = np.sqrt(np.sum((b1-b2)**2))
            
    thr_lengh = 155 # critical crc lenght in nm
    thr_lengh_pxls = thr_lengh*mf*ds0/1000
    adjacency_M_l15 = 1*(adjacency_M<thr_lengh_pxls)
    adjacency_M_tria = np.tril(adjacency_M_l15, k=-1) # removing symmetrical ellemets

    adjacency_M_tria_corrected = np.copy(adjacency_M_tria)
    s = 0 # counter of the progression 
    for k,m in zip(np.nonzero(adjacency_M_tria)[0],np.nonzero(adjacency_M_tria)[1]):
        s=s+1
        pr = s/len(np.nonzero(adjacency_M_tria)[0])
        print("%2.2f" % (pr), end="\r")
    
        pos1 = [branch_indx_merged[k,0],branch_indx_merged[k,1]]
        pos2 = [branch_indx_merged[m,0],branch_indx_merged[m,1]]
    
        path_list = np.asarray(route_through_array(1-skel,\
                                                   pos1, pos2,fully_connected=True)[0])
        # comparing branch to branch distance to the path lenght of the graph
        if (1.2*adjacency_M[k,m] < len(path_list[:,0])): adjacency_M_tria_corrected[k,m] = 0
            
     # orientation_M
    Cos_a_M = np.zeros((N,N))
    eps = 1e-4 # prevent division by zero
    for i in range(N):
        for j in range(N):
            b1 = branch_indx_merged[i,:]
            b2 = branch_indx_merged[j,:]
        
            a = np.sqrt(np.sum(((b1+b2)/2 - np.array([v_cen[0],v_cen[1]]))**2))+eps
            b = np.sqrt(np.sum((b1/2-b2/2)**2))+eps
            c = np.sqrt(np.sum(((b2 - np.array([v_cen[0],v_cen[1]]))**2)))
            cos_gam = abs((a**2+b**2-c**2)/(2*a*b))
            Cos_a_M[i,j] = cos_gam
    Cos_a_M_0_2 = 1*(Cos_a_M<0.56)
    br_poin_perenumeration_M = adjacency_M_tria_corrected*Cos_a_M_0_2
    
    crc_path_list = [] # list for storing crc path

    for k,m in zip(np.nonzero(br_poin_perenumeration_M)[0],np.nonzero(br_poin_perenumeration_M)[1]):
    
        pos1 = [branch_indx_merged[k,0],branch_indx_merged[k,1]]
        pos2 = [branch_indx_merged[m,0],branch_indx_merged[m,1]]
    
        path_list = np.asarray(route_through_array(1-skel,\
                                               pos1, pos2,fully_connected=True)[0])
        crc_path_list.append(path_list)
        
    return(crc_path_list)



# ***********************   corrected number of branching points   ***********************

def corrected_number_of_branching_points(skel,mf):
    branch_indx = branch_pos(skel.astype(int))
    v_cen = find_valve_center(skel)
    my_list_of_crcs = find_cross_connections(skel,branch_indx,v_cen,mf)\
    
    # image for storing crc-path
    graph_crc= np.zeros(np.shape(skel))
    for i in my_list_of_crcs:
        graph_crc[i[:,0],i[:,1]] = 1
        
    # image for stroting branching pixels
    graph_brnh= np.zeros(np.shape(skel))
    graph_brnh[branch_indx[0],branch_indx[1]]=1
    # defining the annulus area 
    chull = 1*mrph.convex_hull_image(skel)
    props = mea.regionprops(chull)
    r_cen = int(0.25*np.sqrt(np.sum(chull)/np.pi))
    img = np.ones(np.shape(chull), dtype=np.uint8)
    rr, cc = circle(v_cen[0],v_cen[0], r_cen)
    img[rr, cc] = 0
    # removing PSS elemets (branches and cross-connections)
    labels1 = mea.label(img*graph_brnh)
    labels2 = mea.label(img*graph_crc)
    corrected_num_of_branches = labels1.max() - 2*labels2.max()

    return(corrected_num_of_branches)
"""

from skimage.graph import route_through_array

def corrected_number_of_branching_points(skel):
    skel = skel.astype(int)
    branch_indx = branch_pos(skel)
    tips_indx = tips_pos(skel)
    v_cen = find_valve_center(skel).astype(int)
    tips_indx_merged = np.stack((tips_indx[0], tips_indx[1]), axis=-1) # y,x coordinates
    branch_indx_merged = np.stack((branch_indx[0], branch_indx[1]), axis=-1) # y,x coordinates
    straight_skel = np.zeros(np.shape(skel))
    
    for k in range(len(branch_indx[0])):
        pos1 = [branch_indx_merged[k,0],branch_indx_merged[k,1]]
        pos2 = [v_cen[0],v_cen[1]]
    
        path_list = np.asarray(route_through_array(1-skel,pos1, pos2,fully_connected=True)[0]) 
        straight_skel[path_list[:,0],path_list[:,1]] =1
    

    for k in range(len(tips_indx[0])):
        pos1 = [tips_indx_merged[k,0],tips_indx_merged[k,1]]
        pos2 = [v_cen[0],v_cen[1]]
    
        path_list = np.asarray(route_through_array(1-skel,pos1, pos2,fully_connected=True)[0]) 
        straight_skel[path_list[:,0],path_list[:,1]] =1
        
    tips_indx1 = tips_pos(straight_skel.astype(int))
    tips_indx_merged1 = np.stack((tips_indx1[0], tips_indx1[1]), axis=-1) # y,x coordinates

    straight_skel1 = np.zeros(np.shape(skel))

    for k in range(len(tips_indx1[0])):
        pos1 = [tips_indx_merged1[k,0],tips_indx_merged1[k,1]]
        pos2 = [v_cen[0],v_cen[1]]
    
    path_list = np.asarray(route_through_array(1-straight_skel,pos1, pos2,fully_connected=True)[0]) 
    straight_skel1[path_list[:,0],path_list[:,1]] =1
        
    chull = 1*mrph.convex_hull_image(skel)
    props = mea.regionprops(chull)
    r_cen = int(0.25*np.sqrt(np.sum(chull)/np.pi))
    img = np.ones(np.shape(chull), dtype=np.uint8)
    rr, cc = circle(v_cen[0],v_cen[0], r_cen)
    img[rr, cc] = 0
    
    branch_indx1 = branch_pos(straight_skel1.astype(int))
    
    brnch_matrix = np.zeros(np.shape(skel))
    brnch_matrix[branch_indx1[0],branch_indx1[1]] = 1
    
    res = len(np.nonzero(brnch_matrix*img)[0])
    
    return(straight_skel1, res)

# ****************************   find cross-connections    ****************************

def average_rib_spacing(skl):
    se = mrph.disk(3)
    skeleton_dilated = mrph.binary_dilation(skl, selem=se)*1
    rib_to_rib_path = mrph.skeletonize((1-1*skeleton_dilated))
    
    chull = 1*mrph.convex_hull_image(skeleton_dilated)
    props = mea.regionprops(chull)
    #r_cen = int(0.30*np.sqrt(np.sum(chull)/np.pi))
    r_cen = 100
    
    O_cc = props[0].centroid[1]
    O_rr = props[0].centroid[0]
    img = np.zeros(np.shape(chull), dtype=np.uint8)
    rr, cc = circle(O_rr, O_rr, r_cen)
    img[rr, cc] = 1
    
    s_mask = chull - img 
    ske, distance = mrph.medial_axis((1-skl), return_distance=True)
    rib_spacing  = distance*s_mask*rib_to_rib_path*2
    
    ARS_m = rib_spacing[rib_spacing>0] # in nm
   
    return(ARS_m) 