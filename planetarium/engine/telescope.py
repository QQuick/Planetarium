import numscrypt as ns

class Telescope:
    def __init__ (self):
        '''Initialize constants
        '''
    
        dirVec0Plane = ns.array ((1, 0, 0))
        dirVec1Plane = ns.array ((0, 1, 0))

    def zoom (self, zoomFactor = 40):
        ''' Zoom by shifting image plane
        '''
    
        self.zoomFactor = zoomFactor
        self.zoomShift = 40 / zoomFactor
		self.supVecPlane = ns.array ((0, 0, -zoomShift / 6))
        
    def project (self, celestialBodyVec, rField, rScreen):
        '''Project a celestial body onto the screen
        
                             y                    * celestial body
                             |            *
                           \ |  *
                      *     \|
        eye *        z - - - + - - -
        (origin)             |\
                             | \
                             |  x
                        image plane
                        
        Let vs be the vector from the origin to the celestial body.
        Let vl be any vector that ends on the line through the origin and the celestial body.
        Then vl = a vs
        
        Let vp be any vector that ends on the image plane
        Let d the distance from the origin to the center of the image plane
        Let ux, uy and uz be the unitvectors in directions x, y and z respectively
        Then vp = b ux + c uy - d uz
        
        The star is shown on the image plane at the intersection with the line between eye and star.
        At his intersection:
        
        a vs = b ux + c uy - d uz ==>
        
        d uz = a vs - b ux + - uy ==>
        
                 (vsx)     (-1)     ( 0)
        d uz = a (vsy) + b ( 0) + c (-1)
                 (vsz)     ( 0)     ( 0)
        
               (vsx, -1,  0) (a)
        d uz = (vsy,  0, -1) (b) ==>
               (vsz,  0,  0) (c)
               
                 (a)                           (vsx, -1,  0)
        d uz = D (b) with direction matrix D = (vsy,  0, -1) ==>
                 (c)                           (vsz,  0,  0)
                 
        (a)    -1
        (b) = D  d uz
        (c)
        
        The screen coordinates of the projected star are (a, b)
        
        '''
        
        # Bail out if object in front of image plane
        
        if projectableVec3D [2] < supVecPlane [2]:
            return None   

        # Compute inverse of direction matrix D
        
        invDirMat = (dirVecLine * ns.array ((1, 0, 0)) .T + dirVec0Plane * ns.array ((-1, 0, 0)) .T  + dirVec1Plane * ns.array ((0, -1, 0)) .T) .I
        
        # Compute projected 3D vector
        
        projectedCelestialBodyVec = invDirMat @ projectableVec
                
        # rField in pixels / rScreen in m will map object with size of rScreen m exactly to rField pixels
        projectedVec2D = (
            (rField / (rScreen / 6d)) * projectedVec3D [1],
            (rField / (rScreen / 6d)) * projectedVec3D [2]
        )
        
        return true
            
        boolean map (double [] mappedVec2D, double [] mappableVec3D, double rField, double rScreen) {	
            double [] rotAngVec = new double [] {Math.PI / 180d * tilt, Math.PI/180d * course, 0d};
            
            double s, c;

            s = Math.sin (rotAngVec [1]);
            c = Math.cos (rotAngVec [1]);
                    
            double rotZCourseMat [][] = new double [][] {
                { c, -s, 0d},
                { s,  c, 0d},
                {0d, 0d, 1d}
            };

            s = Math.sin (rotAngVec [0]);
            c = Math.cos (rotAngVec [0]);
            
            double rotYTiltMat [][] = new double [][] {
                { c, 0d,  s},
                {0d, 1d, 0d},
                {-s, 0d,  c}
            };

            double rotationMat [][] = new double [3][3];
            double [] zoomedVec3D = new double [3];
            double [] rotatedVec = new double [3];
            
            LinAlg.mul (rotationMat, rotYTiltMat, rotZCourseMat);
            LinAlg.mul (zoomedVec3D, zoomFactor / 30d, mappableVec3D);
            LinAlg.mul (rotatedVec, rotationMat, zoomedVec3D);
            return project (mappedVec2D, rotatedVec, rField, rScreen);
        }
        
        boolean mapEyepiece (EyepieceImage eyepieceImage, Eyepiece eyepiece, double rField, double focLenObjective) {
            double magnif = focLenObjective / eyepiece.focLen;
            double angleUniverse = eyepiece.angle / magnif;
            eyepieceImage.rOnField = zoomFactor * rField * Math.sin ((Math.PI / 180d) * (angleUniverse / 2d));
            
            return eyepieceImage.rOnField < rField;
        }
    }
