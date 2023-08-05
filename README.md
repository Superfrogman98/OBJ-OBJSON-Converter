# OBJ-SMEG-Converter
Python script to convert between OBJ and Smeg model files

-Bounds can be set up in the OBJ by adding comments like
# bounds [x1, y1, z1, x2, y2, z2]
# boxes [[x1, y1, z1, x2, y2, z2],[x3, y3, z3, x4, y4, z4]]

when exporting the obj model check:
  Include:
    Selection Only
    Objects as OBJ Groups
  Geometry:
    Apply Modifiers
    Write Normals
    Include UVs
    Write Materials

by seperating faces into multiple objects in blender, and naming them, they can be used to allow cladding/different textures
from the given block(though most don't seem to be implemented in a functional manner)
  the faceID should start at 0 and increase by 1 for each groups
  the name of the object should be formatted like <identifier>_face<faceID>-texture:<0/1 for no cladding, 2+ for cladding> 