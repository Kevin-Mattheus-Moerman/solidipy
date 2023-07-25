import mcpi.minecraft
import time
import numpy as np

mc = mcpi.minecraft.Minecraft.create();

## Control parameters
fileNameSave = "/home/pi/Desktop/out.stl" # Output STL file name
plateBlockID    = 57 # The build plate is made of this. Use 57 to use DIAMOND_BLOCK elements which also appear "grid like" which may be helpful
boundaryBlockId = 20 # This defines the boundary box block, 20 = GLASS and therefore transparent
grownBlockID    = 41 # The block type to show the growing process. Using 41 = gold turns the structure to gold when hit
wh = 25 # Half width of build space, using n creates a cube the size of (2*n)+1

############################## DEFINE FUNCTIONS

# Create function to convert subscript indices to linear indices
def sub2ind(siz,I,J,K):    
    k = np.cumprod(siz)
    ind = 1 + I + J*k[0] + K*k[1]
    return ind-1

# Create function to convert linear indices to subscript indices
def ind2sub(siz,ind):    
    k = np.cumprod(siz)
    ind+=1
    A=np.zeros((np.size(ind),3),dtype=int) #Initializing output array
    for q in reversed(range(0,3)): #For all dimensions
        if q==0: #First 1st dimension
            A[:,0]=np.remainder(ind-1,k[0])               
        else:
            p=np.remainder(ind-1,k[q-1]) + 1 # "previous"
            A[:,q]=(ind-p)/k[q-1] # Current        
            ind=p #Set indices as "previous"            
    return A[:,0],A[:,1],A[:,2]

# Function to export quad faces and vertices to a triangulation in an STL file
def toSTL(F,V,fileName):
    with open(fileName, "w") as f:
        f.write("solid part \n")
        for i in range(0,np.size(F,0)):        
    
            f.write("  facet normal 1 0 0 \n")
            f.write("    outer loop \n")
            for j in range(0,3):
                f.write("      vertex  %.2f" % V[F[i,j],0][0] + " %.2f" % V[F[i,j],1][0] + " %.2f \n" % V[F[i,j],2][0])    
            
            f.write("    endloop \n")
            f.write("  endfacet \n")
    
            f.write("  facet normal 1 0 0 \n")
            f.write("    outer loop \n")
            for j in [2,3,0]:
                f.write("      vertex  %.2f" % V[F[i,j],0][0] + " %.2f" % V[F[i,j],1][0] + " %.2f \n" % V[F[i,j],2][0])    
            
            f.write("    endloop \n")
            f.write("  endfacet \n")
            f.write("endsolid part \n")

# Function to convert a Boolean array to quad faces and vertices (treating true entries and cube shaped elements)
def bool2facesVertices(L):
    
    # Create an array of row, column, slice coordinates for element centres
    ijk_tuple = np.nonzero(L) # tuple containing coordinates
    numElements = np.size(ijk_tuple)//3 # The number of elements 
    ijk = np.reshape(ijk_tuple,(3,numElements)).T  # Convert to array

    # Create faces array 
    Fi = np.zeros((numElements*6,4),dtype=int) # Allocation for face row coordinates 
    Fj = np.zeros((numElements*6,4),dtype=int) # Allocation for face column coordinates 
    Fk = np.zeros((numElements*6,4),dtype=int) # Allocation for face slice coordinates 
    for i in range(0,numElements):        
        Fi[i              ,:] = np.array([ijk[i,0]  , ijk[i,0]+1, ijk[i,0]+1, ijk[i,0]  ]) # Top
        Fi[i+numElements  ,:] = np.array([ijk[i,0]  , ijk[i,0]+1, ijk[i,0]+1, ijk[i,0]  ]) # Bottom
        Fi[i+numElements*2,:] = np.array([ijk[i,0]  , ijk[i,0]+1, ijk[i,0]+1, ijk[i,0]  ]) # Front
        Fi[i+numElements*3,:] = np.array([ijk[i,0]  , ijk[i,0]+1, ijk[i,0]+1, ijk[i,0]  ]) # Back
        Fi[i+numElements*4,:] = np.array([ijk[i,0]  , ijk[i,0]  , ijk[i,0]  , ijk[i,0]  ]) # Side 1
        Fi[i+numElements*5,:] = np.array([ijk[i,0]+1, ijk[i,0]+1, ijk[i,0]+1, ijk[i,0]+1]) # Side 1
    
        Fj[i              ,:] = np.array([ijk[i,1]+1, ijk[i,1]+1, ijk[i,1]  , ijk[i,1]  ]) # Top
        Fj[i+numElements  ,:] = np.array([ijk[i,1]  , ijk[i,1]  , ijk[i,1]+1, ijk[i,1]+1]) # Bottom
        Fj[i+numElements*2,:] = np.array([ijk[i,1]  , ijk[i,1]  , ijk[i,1]  , ijk[i,1]  ]) # Front
        Fj[i+numElements*3,:] = np.array([ijk[i,1]+1, ijk[i,1]+1, ijk[i,1]+1, ijk[i,1]+1]) # Back
        Fj[i+numElements*4,:] = np.array([ijk[i,1]  , ijk[i,1]+1, ijk[i,1]+1, ijk[i,1]  ]) # Side 1
        Fj[i+numElements*5,:] = np.array([ijk[i,1]+1, ijk[i,1]  , ijk[i,1]  , ijk[i,1]+1]) # Side 1
    
        Fk[i              ,:] = np.array([ijk[i,2]  , ijk[i,2]  , ijk[i,2]  , ijk[i,2]  ]) # Top
        Fk[i+numElements  ,:] = np.array([ijk[i,2]+1, ijk[i,2]+1, ijk[i,2]+1, ijk[i,2]+1]) # Bottom
        Fk[i+numElements*2,:] = np.array([ijk[i,2]  , ijk[i,2]  , ijk[i,2]+1, ijk[i,2]+1]) # Front
        Fk[i+numElements*3,:] = np.array([ijk[i,2]+1, ijk[i,2]+1, ijk[i,2]  , ijk[i,2]  ]) # Back
        Fk[i+numElements*4,:] = np.array([ijk[i,2]+1, ijk[i,2]+1, ijk[i,2]  , ijk[i,2]  ]) # Side 1
        Fk[i+numElements*5,:] = np.array([ijk[i,2]+1, ijk[i,2]+1, ijk[i,2]  , ijk[i,2]  ]) # Side 1
        
    # Create the face index array 
    F = sub2ind((np.size(L,0)+1,np.size(L,1)+1,np.size(L,2)+1),Fi,Fj,Fk) # Quad faces
    
    # Get face occurance count
    Fs=np.sort(F,axis=1) # Sorting in column direction so face 1 2 3 4 is viewed as the same as 4 3 2 1 for instance
    Fs_uni,ind1,ind2,c = np.unique(Fs,return_index=True, return_inverse=True, return_counts=True, axis=0) # Get unique faces and face occurance counts
    F = F[ind1[c==1]] # Keep only the unique faces that occured once (i.e. boundary faces)
    
    # Check which nodes are used
    indUsed = np.unique(F) # We actually only need coordinates for these nodes 
    
    # Fix face indices in anticipation of a reduced coordinate set
    indFix1 = np.matrix(range(0,np.size(indUsed))).T
    indFix2 = np.zeros((np.max(F)+1,1),dtype=int)
    indFix2[indUsed]=indFix1
    F = indFix2[F] # The new face array 
        
    #Create coordinate array
    I,J,K=ind2sub((np.size(L,0)+1,np.size(L,1)+1,np.size(L,2)+1),indUsed)
    
    #Creating element cornder coordinates 
    V=np.zeros((np.size(indUsed),3),dtype=float) 
    V[:,0]=I-0.5
    V[:,1]=J-0.5
    V[:,2]=K-0.5
    
    return F,V

############################## END OF FUNCTIONS

mc.player.setPos(0,1,0) # Places player 1 above floor/origin

# Get player tile to act as origin
x, y, z = mc.player.getTilePos()
y-=1 # Shift down so floor is under, not at, player
mc.postToChat("Origin = " + str(x) + ", " + str(y) + ", " + str(z))

# Create build plate
airID=0

# Clear the space with air
mc.setBlocks(x-wh, y, z-wh, x+wh, y+2*wh, z+wh, airID)

# Make a build plate
mc.setBlocks(x-wh, y, z-wh, x+wh, y, z+wh, plateBlockID)

# Make a glass boundary box
mc.setBlocks(x-wh, y, z-wh, x+wh, y+2*wh, z-wh, boundaryBlockId)
mc.setBlocks(x-wh, y, z+wh, x+wh, y+2*wh, z+wh, boundaryBlockId)
mc.setBlocks(x-wh, y, z-wh, x-wh, y+2*wh, z+wh, boundaryBlockId)
mc.setBlocks(x+wh, y, z-wh, x+wh, y+2*wh, z+wh, boundaryBlockId)
mc.setBlocks(x-wh, y+2*wh, z-wh, x+wh, y+2*wh, z+wh, boundaryBlockId)

# Define structure boolean matrix
s=wh*2-1 #Matrix size
L = np.full((s,s,s), False, dtype=bool) # To store the build
LV = np.full((s,s,s), False, dtype=bool) # To keep track of visited blocks

#While loop to wait for a hit event
mc.postToChat("Build your structure from solid blocks.")
mc.postToChat("Right-click hit your structure with sword when done.")
while True:
    hits = mc.events.pollBlockHits()
    if len(hits)>0:
        mc.postToChat("Great hit! Cloning structure to memory...")

        hit=hits[0] # Get first hit         
        xc=[hit.pos.x]
        yc=[hit.pos.y]
        zc=[hit.pos.z]
        mc.setBlock(xc[0],yc[0],zc[0], grownBlockID)
        break 

    time.sleep(0.25)
    
# Grow structure
while True:
    #Start empty "new" coordinate sets
    xn=[] 
    yn=[]
    zn=[]
    for ip  in range(0,len(xc)): #Loop over all check sites
        
        # Current check middle
        xm=xc[ip]
        ym=yc[ip]
        zm=zc[ip]
        
        # Loop over 3x3x3=27 connected neighbourhood of middle
        for xs in [-1,0,1]: 
            for ys in [-1,0,1]:
                for zs in [-1,0,1]:                    
                    # Coordinates to check now
                    xx=xm+xs
                    yy=ym+ys
                    zz=zm+zs
                    
                    # Convert to matrix indices
                    i = zz-1+wh-z
                    j = xx-1+wh-x
                    k = yy-1-y
                    
                    # Proceed if these are valid indices
                    if all(ind>-1 for ind in [i,j,k]) and all(ind<s for ind in [i,j,k]):                      
                        if LV[i,j,k]==False: #If not visited yet
                            print("Checking xyz: " + str(xx)+ "," + str(yy) + "," + str(zz) + ", ijk:" + str(i)+ "," + str(j) + "," + str(k))
                            LV[i,j,k]=True #Now set to visited
                            blockIdNow = mc.getBlock(xx, yy, zz) #Get block id
                            if blockIdNow!=0: # If not air                                
                                #mc.postToChat("Adding block at " + str(xx) + "," + str(yy) + "," + str(zz) + ", with id: " + str(blockIdNow))
                                mc.setBlock(xx, yy, zz, grownBlockID)
                            
                                #Add/grow to newly found set
                                xn.append(xx)
                                yn.append(yy)
                                zn.append(zz)
                            
                                L[i,j,k]=True #Keep this block for model                                
                    
    if len(xn)==0: # No new entries so we can stop
        mc.postToChat("No longer growing!")
        break
    else: 
        xc=xn
        yc=yn
        zc=zn
                
mc.postToChat("Cloning completed.")
                
mc.postToChat("Building surface geometry... ")

F,V = bool2facesVertices(L)

# Export to STL file
mc.postToChat("Saving STL file... ")
toSTL(F,V,fileNameSave)

mc.postToChat("All done! Happy printing!")
