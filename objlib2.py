#Created by Ignacio Alfredo Savi Gualco, not responsable for misuse, no guarantee of proper functioning. Use at your own risk, no fees or credits required to use this lib.
import math,struct
class Mesh: 
 def __init__(self, filename, from_memory = False): 
  self.vertices = []
  self.faces = []
  self.from_memory = from_memory
  self.empty = False
  if not self.from_memory:
   with open(filename) as f:
    for line in f:
     if line.startswith('v '):
      self.vertices.append(Vertex(*map(float, line.split()[1:4]))) 
     elif line.startswith('f '):
      self.faces.append(Face(*map(int, line.split()[1:4])))
  else:
   self.empty = True

 def fill_mesh_faces_only(self,faces):
  for face in faces:
   self.vertices.append(face.v1)
   self.vertices.append(face.v2)
   self.vertices.append(face.v3) 
   self.faces.append(face)
   if len(faces)>0:
    self.empty = False
 def fill_mesh_faces_and_verts(self,faces,vertices):


  self.faces = faces
  self.vertices = vertices
  if len(faces) * len(vertices)>0:
   self.empty = False
class Vertex: 
 def __init__(self, x, y, z):
  self.x = x 
  self.y = y 
  self.z = z
 def __repr__(self):
  return "Vertex({}, {}, {})".format(self.x, self.y, self.z)
 def distance3d(self,vertex):
  return math.sqrt((self.x-vertex.x)**2+(self.y-vertex.y)**2+(self.z-vertex.z)**2)
 def distance3dsq(self,vertex):
  return ((self.x-vertex.x)**2+(self.y-vertex.y)**2+(self.z-vertex.z)**2)
 def angle_relative(self,vertex):
  return math.acos((self.x*vertex.x+self.y*vertex.y+self.z*vertex.z)/(math.sqrt(self.x**2+self.y**2+self.z**2)*math.sqrt(vertex.x**2+vertex.y**2+vertex.z**2)))
 def angle_relative_degrees(self,vertex):
  return math.degrees(math.acos((self.x*vertex.x+self.y*vertex.y+self.z*vertex.z)/(math.sqrt(self.x**2+self.y**2+self.z**2)*math.sqrt(vertex.x**2+vertex.y**2+vertex.z**2))))
 def dotproduct(self,vertex):
  return self.x*vertex.x+self.y*vertex.y+self.z*vertex.z
  
 def crossproduct(self,vertex):
  return Vertex(self.y*vertex.z-self.z*vertex.y,self.z*vertex.x-self.x*vertex.z,self.x*vertex.y-self.y*vertex.x)
 def normalize(self):
  return Vertex(self.x/math.sqrt(self.x**2+self.y**2+self.z**2),self.y/math.sqrt(self.x**2+self.y**2+self.z**2),self.z/math.sqrt(self.x**2+self.y**2+self.z**2))
 def add(self,vertex):
  return Vertex(self.x+vertex.x, self.y+vertex.y, self.z+vertex.z)
 def subtract(self,vertex):
  return Vertex(self.x-vertex.x, self.y-vertex.y, self.z-vertex.z)
 def multiply(self,scalar):
  return Vertex(scalar*self.x, scalar*self.y, scalar*self.z)
 def divide_inverted(self,scalar):
  if(self.x * self.y * self.z != 0):

   return Vertex(scalar/self.x, scalar/self.y, scalar/self.z)
  else:
   print("Warning, division by 0 avoided")  
   return "impossible"
 def divide(self,scalar):
  if scalar == 0:
   print("Warning, division by 0 avoided")  
   return "impossible"
  return Vertex(self.x/scalar, self.y/scalar, self.z/scalar)
 def Q_rsqrt(self,number):
  threehalfs = 1.5
  x2 = number * 0.5
  y = number
    
  packed_y = struct.pack('f', y)       
  i = struct.unpack('i', packed_y)[0]  # treat float's bytes as int 
  i = 0x5f3759df - (i >> 1)            # arithmetic with magic number
  packed_i = struct.pack('i', i)
  y = struct.unpack('f', packed_i)[0]  # treat int's bytes as float
    
  y = y * (threehalfs - (x2 * y * y))  # Newton's method
  return y
 def fast_approx_normalize(self):
  return Vertex(self.x*self.Q_rsqrt(self.x**2+self.y**2+self.z**2),self.y*self.Q_rsqrt(self.x**2+self.y**2+self.z**2),self.z*self.Q_rsqrt(self.x**2+self.y**2+self.z**2))
class Face:
 def __init__(self, v1, v2, v3):
  self.v1 = v1 
  self.v2 = v2 
  self.v3 = v3 
 def __repr__(self): 
  return "Face({}, {}, {})".format(self.v1, self.v2, self.v3)
 def area(self):
  v1 = self.v1
  v2 = self.v2
  v3 = self.v3
  return 0.5*math.sqrt(((v2.x-v1.x)*(v3.y-v1.y)-(v2.y-v1.y)*(v3.x-v1.x))**2+((v2.x-v1.x)*(v3.z-v1.z)-(v2.z-v1.z)*(v3.x-v1.x))**2+((v2.y-v1.y)*(v3.z-v1.z)-(v2.z-v1.z)*(v3.y-v1.y))**2)
 def Q_rsqrt(self,number):
  threehalfs = 1.5
  x2 = number * 0.5
  y = number
    
  packed_y = struct.pack('f', y)       
  i = struct.unpack('i', packed_y)[0]  # treat float's bytes as int 
  i = 0x5f3759df - (i >> 1)            # arithmetic with magic number
  packed_i = struct.pack('i', i)
  y = struct.unpack('f', packed_i)[0]  # treat int's bytes as float
    
  y = y * (threehalfs - (x2 * y * y))  # Newton's method
  return y
  
 def fast_aproximate_area(self):
  try:
   v1 = self.v1
   v2 = self.v2
   v3 = self.v3
   return 0.5/self.Q_rsqrt(((v2.x-v1.x)*(v3.y-v1.y)-(v2.y-v1.y)*(v3.x-v1.x))**2+((v2.x-v1.x)*(v3.z-v1.z)-(v2.z-v1.z)*(v3.x-v1.x))**2+((v2.y-v1.y)*(v3.z-v1.z)-(v2.z-v1.z)*(v3.y-v1.y))**2)   
  except:
   print("Warning using slow method and exact area")
   return self.area()
 def centroid(self):
  v1 = self.v1
  v2 = self.v2
  v3 = self.v3
  return Vertex(((self.area()/3)*(((self.area()/3)+((self.area()/3)+((self.area()/3)+0))))), ((self.area()/3)*(((self.area()/3)+((self.area()/3)+((self.area()/3)+0))))), ((self.area()/3)*(((self.area()/3)+((self.area()/3)+((self.area()/3)+0))))))
 def bigger_than(self,face):
  v1 = self.v1
  v2 = self.v2
  v3 = self.v3
  vf1 = face.v1
  vf2 = face.v2
  vf3 = face.v3
  return (((v2.x-v1.x)*(v3.y-v1.y)-(v2.y-v1.y)*(v3.x-v1.x))**2+((v2.x-v1.x)*(v3.z-v1.z)-(v2.z-v1.z)*(v3.x-v1.x))**2+((v2.y-v1.y)*(v3.z-v1.z)-(v2.z-v1.z)*(v3.y-v1.y))**2) > (((vf2.x-vf1.x)*(vf3.y-vf1.y)-(vf2.y-vf1.y)*(vf3.x-vf1.x))**2+((vf2.x-vf1.x)*(vf3.z-vf1.z)-(vf2.z-vf1.z)*(vf3.x-vf1.x))**2+((vf2.y-vf1.y)*(vf3.z-vf1.z)-(vf2.z-vf1.z)*(vf3.y-vf1.y))**2)
 def normal_vector(self):
  
  v1 = self.v1

  v2 = self.v2
  v3 = self.v3
  return Vertex(((v2.y-v1.y)*(v3.z-v1.z)-(v2.z-v1.z)*(v3.y-v1.y)), ((v2.z-v1.z)*(v3.x-v1.x)-(v2.x-v1.x)*(v3.z-v1.z)), ((v2.x-v1.x)*(v3.y-v1.y)-(v2.y-v1.y)*(v3.x-v1.x)))

 def angle_relative(self,face):
  
  return math.acos((self.normal_vector().x*face.normal_vector().x+self.normal_vector().y*face.normal_vector().y+self.normal_vector().z*face.normal_vector().z)/(math.sqrt(self.normal_vector().x**2+self.normal_vector().y**2+self.normal_vector().z**2)*math.sqrt(face.normal_vector().x**2+face.normal_vector().y**2+face.normal_vector().z**2)))
 def angle_relative_degrees(self,face):
  return math.degrees(self.angle_relative(face))
 def shared_vertices_amount(self,face):
  amount = 0
  v1 = self.v1
  v2 = self.v2
  v3 = self.v3
  vf1 = face.v1
  vf2 = face.v2
  vf3 = face.v3
  if(v1.x == vf1.x and v1.y == vf1.y and v1.z == vf1.z):
   amount +=1
  if(v2.x == vf2.x and v2.y == vf2.y and v2.z == vf2.z):
   amount +=1
  if(v3.x == vf3.x and v3.y == vf3.y and v3.z == vf3.z):
   amount +=1
  return amount
 def shares_vertices(self,face):
  amount = 0
  v1 = self.v1
  v2 = self.v2
  v3 = self.v3
  vf1 = face.v1
  vf2 = face.v2
  vf3 = face.v3
  if(v1.x == vf1.x and v1.y == vf1.y and v1.z == vf1.z):
   return True
  if(v2.x == vf2.x and v2.y == vf2.y and v2.z == vf2.z):
   return True
  if(v3.x == vf3.x and v3.y == vf3.y and v3.z == vf3.z):
   return True
  return False

