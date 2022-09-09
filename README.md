# badobjlib
a bad obj library

Welcome to this repo, in it you will find a very basic library for reading and analyzing obj files. writing obj files is not supported yet, but obj files can be created from memory


Documentation:
*MORE SPECIFIC DETAILS TO COME in the future*
A Mesh object can be created from a file, Mesh(filename) or it can be created empty and filled in later, Mesh(" ", from_memory=True)

the mesh object is supposed to contain faces that are not just a group of three indices to vertices but contain the vertices themselves

A Face object, as stated above, will contain the three vertices themselves. many functions are available to this class.
it is possible to calculate the area of a face, know that a face shares vertices or a single vertex with another face and much more.

A vertex is a group of 3 floating point values. a vertex in this lib can be normalized and, amongst other things, it can determine its distance to a diferent vertex.

Use Cases
3d engines, 3d prototyping, 3d model analysis.
example:
 We can calculate the surface area of a prototype car if we have a 3d model in obj format of it. we just sum all the areas on the car with a for loop iterating through the mesh and summing up face.area().

