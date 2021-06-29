'''Encapsulation of HTML5 canvas, WebGL context and shaders
'''

class Shader:
    '''Encapsulates vertex or fragment shader and compiles its code
    
    Convenience functions setAttributes, setIndices and setUniform enable
    easy manipulation of named shader variables.
    '''

    shaderTypesGl = {'vertex': gl.GL_VERTEX_SHADER, 'fragment': gl.GL_FRAGMENT_SHADER}
    
	def __init__ (self, aType, code):
        ''' Create and compile encapsulated WebGL shader
        '''
		self.shaderGl = gl.glCreateShader (self.shaderTypesGl [aType])
		gl.glShaderSource (self.shaderGl, code)
		gl.glCompileShader (self.shaderGl)
		
class Canvas:
    '''Encapsulates canvas and context, accepting and linking encapsulated shaders
    '''

    def __init__ (self, parentId, *shaders):
        '''Creates ready to go canvas, context and shaders
        
        After that, altering c.q. manipulating the image is a matter of calling 
        setAttributes, setIndices and setUniform.
        '''
        
        parent = document.getElementById (self.parentId)
        self.createCanvas ()
        self.prepareContext ()
        self.linkShaders ()
    
    def _createCanvas (self):
        '''Create HTML5 canvas and attach it to parent
        
        The canvas will fully cover the parent.
        '''
    
        self.canvas = document.createElement ('canvas')
        self.parent.appendChild (self.canvas)
        
        self.canvas.style.width = '100%'                # Make canvas fit parent
        self.canvas.style.height = '100%'
        
        self.canvas.width  = self.canvas.offsetWidth    # Adapt internal width in pixels
        self.canvas.height = self.canvas.offsetHeight
        
    def _prepareContext (self):
        '''Get WebGL2 context from canvas, and set its background color and viewport
        
        The context is cleared to the background color.
        '''
    
        self.context = self.canvas.getContext ('webgl2')
        self.context.clearColor (0, 0, 0, 1)
        self.context.viewport (0, 0, self.canvas.width, self.canvas.height)
        self.context.js_clear (self.context.COLOR_BUFFER_BIT | self.context.DEPTH_BUFFER_BIT)
        
    def _linkShaders (self):
        '''Link precompiled shaders into WebGL program.
        
        Attach, link and then release the shaders.
        '''
    
		programGl = self.context.glCreateProgram ()
		for shader in shaders:				
			self.context.glAttachShader (programGl, shader.shaderGl)	
		self.context.glLinkProgram (programGl)
		for shader in shaders:
			self.context.glDetachShader (programGl, shader.shaderGl)
		self.context.glUseProgram (programGl)    
        
	def setAttributes (self, attributeDict):
        '''Sets shader attributes
        
        attributeDict can e.g. be:
        
            # Numscrypt arrays                  # Having type and shape:
            
        {   'starPosition': starPositions,      # typesNs [typesGen ['coordinate']], (3, 100)
            'starMagnitude: starMagnitudes,     # typesNs [typesGen ['coordinate']], (1, 100)
            'starColor': starColors,            # typesNs [typesGen ['colorComponent']], (4, 100)
            
            'planetPosition': planetPositions,  # typesNs [typesGen ['coordinate']], (3, 8)
            'planetRadius': planetRadii,        # typesNs [typesGen ['coordinate']], (1, 8)
            'planetColor': planetColors         # typesNs [typesGen ['colorComponent']], (4, 8)
        }
        '''
    
		attributeBuffer = gl.glGenBuffers (1)	                                # Get unused identifier
		gl.glBindBuffer (gl.GL_ARRAY_BUFFER, attributeBuffer)	                # Allocate GPU buffer
               
        attributeArrays = attributeDict.values ()                               # Same order as keys
		gl.glBufferData (                                                       # Copy data to GPU buffer 
            gl.GL_ARRAY_BUFFER,
            sum ([                                                              # Total size
                attributeArray.nbytes for attributeArray in attributeArrays
            ]),
            ns.concatenate (attributeArrays),                                   # Same order as keys
            gl.GL_STATIC_DRAW
        )
		
		for attributeName, attributeArray in attributeDict.items ():                                                              
			gl.glEnableVertexAttribArray (                                      # Set reference to attribute array in shader program
                gl.glGetAttribLocation (self.programGl, attributeName)
            )	                            
			gl.glVertexAttribPointer (                                          # Connect vertex attribute array to the right places the in already filled buffer
                gl.glGetAttribLocation (self.programGl, attributeName),         # Place in program to store reference to attribute
                attributeArray.shape [0],                                       # Nr. of components per vertex 
                # TYPE
                False,
                stride
                pointer
            )
			offset += attributeArray.nbytes
	
	def setIndices (self, indices):
		indexBuffer = gl.glGenBuffers (1)	                                    # Get empty buffer
		gl.glBindBuffer (gl.GL_ELEMENT_ARRAY_BUFFER, indexBuffer)	            # Make buffer current
		gl.glBufferData (                                                       # Copy data to buffer
            gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, gl.GL_STATIC_DRAW
        )
		
	def setUniform (self, name, value):
		location = gl.glGetUniformLocation (self.programGl, name)               # Reference to named field in program
		if isinstance (value, numpy.matrix):
			if value.shape == (4, 4):
				gl.glUniformMatrix4fv (location, 1, gl.GL_FALSE, value.T.tolist ())
			elif value.shape == (4, 1):
				gl.glUniform4fv (location, 1, value.tolist ())
			else:
				raise Exception ('Invalid uniform shape')
		elif isinstance (value, float):
			gl.glUniform1f (location, value)
		elif isinstance (value, int):
				gl.glUniform1i (location, value)
		else:
			raise Exception ('Invalid uniform type')



        