# OBJ-OBJSON-Converter
Python script to convert between OBJ and OBJSON(Smeg) model files for ArchitectureCraft

-Bounds can be set up in the OBJ by adding comments like<br>
>\# bounds [x1, y1, z1, x2, y2, z2]<br>
>\# boxes [[x1, y1, z1, x2, y2, z2],[x3, y3, z3, x4, y4, z4]]<br>

when exporting the obj model check:<br>
Include:<br>
>Selection Only<br>
>Objects as OBJ Groups<br>

Geometry:<br>
>Apply Modifiers<br>
>Write Normals<br>
>Include UVs<br>
>Write Materials<br>

by seperating faces into multiple objects in blender, and naming them, they can be used to allow cladding/different textures
from the given block(though most don't seem to be implemented in a functional manner)<br>
  >the faceID should start at 0 and increase by 1 for each group<br>
  >the name of the object should be formatted like <identifier>_face<faceID>-texture:<0/1 for no cladding, 2+ for cladding> 
  
when importing to blenderselect Split by Group
