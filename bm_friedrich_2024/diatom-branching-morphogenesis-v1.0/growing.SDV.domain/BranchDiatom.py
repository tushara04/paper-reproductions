import numpy as np
from skimage.draw import ellipse

import imageio
from skimage.transform import rescale

# ********************************  intitial condidtions  ********************************
def get_initial_seed(img,v_max,dx,nX,nY):
    pic = imageio.imread(img)    # image import
    nS = np.shape(pic[1])[0]     # getting image shape
    seed = pic[:,:,3]-pic[:,:,2]
    seed = seed/250              # grayscale normalization 
    seed = rescale(seed,  (73/dx)/nS, multichannel=False, anti_aliasing=True)

    N = nX
    U = np.ones((N,N))                   # making blank U and V matrices
    V = np.zeros((N,N))
    
    U = np.ones((nY,nX))         # making blank U and V matrices
    V = np.zeros((nY,nX))
    N2 = nX//2                   # putting the seed at the center
    r = int(np.shape(seed)[0])
    V[N2-r//2:N2+r//2+r%2, N2-r//2:N2+r//2+r%2]=v_max*seed # how deal with odd and even shapes

    return U, V

# ********************************  def laplacian for diffusion  ********************************
def laplacian(Z,dx):
    dy=dx
    Zcenter = Z[1:-1, 1:-1]
    Ztop = Z[0:-2, 1:-1]
    Zbottom = Z[2:, 1:-1]
    Zleft = Z[1:-1, 0:-2]
    Zright = Z[1:-1, 2:]
    
    return (Ztop + Zleft + Zbottom + Zright -
            4 * Zcenter) / dx**2

# ********************************  quenching sigmoid function  ********************************
def hill_func(C_cr,lam,c):
    h = C_cr**lam/(C_cr**lam+c**lam)
    return(h)

# ********************************  def SDV reflecting b.c.  ********************************
def SDV_ref_bc_indxs(U,r_r,c_r):

    SDV_el_z = np.zeros(np.shape(U))
    SDV_el_yp = np.zeros(np.shape(U))
    SDV_el_xp = np.zeros(np.shape(U))
    nX,nY = np.shape(U)[1],np.shape(U)[0]

    rr, cc = ellipse(r=nY//2, c=nX//2, r_radius=r_r, c_radius=c_r) 
    rr_yp, cc_yp = ellipse(r=nY//2+1, c=nX//2, r_radius=r_r, c_radius=c_r) 
    rr_xp, cc_xp = ellipse(r=nY//2, c=nX//2+1, r_radius=r_r, c_radius=c_r)
    
    SDV_el_z[rr, cc] = 1
    SDV_el_yp[rr_yp, cc_yp] = 1
    SDV_el_yp = SDV_el_yp - SDV_el_z

    SDV_el_xp[rr_xp, cc_xp] = 1
    SDV_el_xp = SDV_el_xp - SDV_el_z

    indx_yp = np.where(SDV_el_yp== 1)
    indx_ym = np.where(SDV_el_yp==-1)

    indx_xp = np.where(SDV_el_xp== 1)
    indx_xm = np.where(SDV_el_xp==-1)
    
    return([indx_yp,indx_ym,indx_xp,indx_xm])

# ********************************  def SDV reflecting b.c.  ********************************
def SDV_laplacian_expanding(Z,r_r,c_r,dx): 
    dy=dx
    indx_yp,indx_ym,indx_xp,indx_xm = SDV_ref_bc_indxs(Z,r_r,c_r)
    
    X_Y  = Z[1:-1, 1:-1]
    
    Z[indx_yp] = Z[indx_yp[0]-1,indx_yp[1]]
    Z[indx_ym[0]-1,indx_ym[1]] = Z[indx_ym[0],indx_ym[1]]
    
    Y_m  = Z[0:-2, 1:-1]    
    Y_p  = Z[2:  , 1:-1]
    
    d_yy   = (Y_p + Y_m - 2*X_Y)/dy**2 
    
    Z[indx_xp[0],indx_xp[1]] = Z[indx_xp[0],indx_xp[1]-1]
    Z[indx_xm[0],indx_xm[1]-1] = Z[indx_xm[0],indx_xm[1]]
    
    X_p  = Z[1:-1,   2:]
    X_m  = Z[1:-1, 0:-2]
    
    d_xx   = (X_p + X_m - 2*X_Y)/dx**2 
    
    return (d_yy+d_xx)









