import os
import json
import ast
cwd = os.getcwd();

#default to 0 indent, less readable, but much smaller
jsonIndent = 0
defaultbounds = [-0.5, -0.5, -0.5, 0.5, 0.5, 0.5]
defaultboxes = [[-0.5, -0.5, -0.5, 0.5, 0.5, 0.5]]
debugOutput = False

def objson_to_obj(modelName,inputLocation="input/",outputLocation="output/"):
    bounds = defaultbounds
    boxes = defaultboxes
    
    outputOBJ = ""
    vertexes = {}
    #(x,y,z):obj index
    uniqueVertexes = {}

    #(x,y,z,face):(objson index, obj index)
    normals = {}
    #(x,y,z):obj index
    uniqueNormals= {}

    #(u,v,face):(objson index, obj index)
    uv = {}
    #(x,y,z):obj index
    uniqueUV = {}

    #(objson-point1,objson-point2,objson-point3,face):(obj-point1,obj-point2,obj-point3)
    faces = {}
    faceTextures = {}
    #(face,localIndex),remappedIndex
    faceVertexMap = {}
    faceUVMap = {}
    faceNormalMap = {}
    groupTextures = {-1:0}
    
    file = inputLocation+modelName+".objson"
    print(file)
    try: 
        inputFile = open(file, "r");
        modelData = json.load(inputFile);
        outputOBJ += "# bounds "+ str(modelData['bounds']) +"\n"
        if 'boxes' in modelData:
            outputOBJ += "# boxes "+ str(modelData['boxes']) +"\n"
        else:
            outputOBJ += "# boxes "+ str([]) +"\n"
        outputOBJ = outputOBJ + "mtllib " + modelName + ".mtl\n"
        outputOBJ = outputOBJ + "o " + modelName + "\n"
        faceIndex = 0
        #faces are just groups in the objson file,not necessarily adjacent triangles
        for f in modelData['faces']:
            objsonVIndex = 0
            objsonNIndex = 0
            objsonUIndex = 0
            for v in f['vertices']:
                #(x,y,z,face): (objsonIndex:objsonIndex)
                addedVValue = vertexes.setdefault((v[0],v[1],v[2],faceIndex), (objsonVIndex,objsonVIndex))
                if(addedVValue == (objsonVIndex,objsonVIndex)):
                    objsonVIndex +=1
                uniqueVertexes.update({(v[0],v[1],v[2]):""})
                
                addedNValue = normals.setdefault((v[3],v[4],v[5],faceIndex,objsonNIndex), (objsonNIndex,objsonNIndex))
                if(addedNValue == (objsonNIndex,objsonNIndex)):
                    objsonNIndex +=1
                uniqueNormals.update({(v[3],v[4],v[5]): ""})
    
                addedUValue = uv.setdefault((v[6],v[7],faceIndex,objsonUIndex), (objsonUIndex,objsonUIndex))
                if(addedUValue == (objsonUIndex,objsonUIndex)):
                    objsonUIndex +=1
                uniqueUV.update({(v[6],v[7]): ""})
                
            for t in f['triangles']:
                faces.update({(t[0],t[1],t[2],faceIndex):(t[0],t[1],t[2])})
            faceTextures.update({faceIndex:f['texture']})
            faceIndex+=1
        
        #index uniqueVertexes and put them in the output file
        i = 1
        for v in uniqueVertexes:
            uniqueVertexes.update({v:i})
            outputOBJ += "v "+ str(v[0]) + " " + str(v[1]) + " "+ str(v[2]) + "\n"
            i+=1
            
        #index uniqueUVs and put them in the output file
        i = 1
        for u in uniqueUV:
            uniqueUV.update({u:i})
            outputOBJ += "vt "+ str(u[0]) + " " + str(u[1]) + "\n"
            i+=1
          
        #index uniqueNormals and put them in the output file
        i = 1
        for n in uniqueNormals:
            uniqueNormals.update({n:i})
            outputOBJ += "vn "+ str(n[0]) + " " + str(n[1]) + " "+ str(n[2]) + "\n"
            i+=1
                
        #matches objson vertices to the obj unique vertices index
        #print("vertexes")#v
        for v in vertexes:
            #get vertex, update the OBJ index to match the index from unique vertices
            objsonIndex = vertexes[v][0]
            objIndex = uniqueVertexes[(v[0],v[1],v[2])]
            vertexes.update({v: (objsonIndex,objIndex)})
            faceVertexMap.update({(v[3],vertexes[v][0]):vertexes[v][1]})
            #print(v," | ", vertexes[v])
        
        #matches objson uvs to the obj unique uv indexs
        #print("\nuv")
        for u in uv:
            uv.update({u: (uv[u][0],uniqueUV[(u[0],u[1])])})
            faceUVMap.update({(u[2],uv[u][0]):uv[u][1]})
            #print(u," | ", uv[u]) 
            
        #matches objson normals to the obj unique normal indexs    
        #print("\nnormals")#
        for n in normals:
            normals.update({n: (normals[n][0],uniqueNormals[(n[0],n[1],n[2])])})
            faceNormalMap.update({(n[3],normals[n][0]):normals[n][1]})
            #print(n," | ", normals[n])    
        
        #set material to none, and smooth shading to false
        outputOBJ += "usemtl None\ns off\n"
            
        #print(str(normals) + "\n") #vn
        #print(str(uv) + "\n") #vt
        #print(str(faces) + "\n") #f
        #print(faceNormalMap)
        
        #add the faces to the obj file, adding in groups based on the objson groups and pairing the texted used
        faceGroup = -1
           
        for f in faces:
            #faces.update({f:(faceVertexMap[(f[3],faces[f][0])],faceVertexMap[(f[3],faces[f][1])],faceVertexMap[(f[3],faces[f][2])])})
            x = str(faceVertexMap[(f[3],faces[f][0])]) + "/" + str(faceUVMap[(f[3],f[0])]) + "/" + str(faceNormalMap[(f[3],f[0])])
            y = str(faceVertexMap[(f[3],faces[f][1])]) + "/" + str(faceUVMap[(f[3],f[1])]) + "/" + str(faceNormalMap[(f[3],f[1])])
            z = str(faceVertexMap[(f[3],faces[f][2])]) + "/" + str(faceUVMap[(f[3],f[2])]) + "/" + str(faceNormalMap[(f[3],f[2])])
            if(faceGroup != f[3]): 
                faceGroup = f[3]
                outputOBJ += "g face"+str(faceGroup)+"-texture:"+str(faceTextures[f[3]])+"\n"
            #x = str(faceVertexMap[(f[3],f[0])]+1) + "//" + str(faceNormalMap[(f[3],f[0])]+1)
            #y = str(faceVertexMap[(f[3],f[1])]+1) + "//" + str(faceNormalMap[(f[3],f[1])]+1)
            #z = str(faceVertexMap[(f[3],f[2])]+1) + "//" + str(faceNormalMap[(f[3],f[2])]+1)
            outputOBJ += "f " + x + " " + y + " " + z +"\n"
        #print(outputOBJ)
        output = open(outputLocation+modelName+".obj","w")
        output.write(outputOBJ)
        output.close()
        
        
        inputFile.close()
    except IOError:
        print("File not accessible");  
        
def obj_to_objson(modelName,inputLocation="input/",outputLocation="output/"):
    outputOBJSON = {}
    bounds = defaultbounds
    boxes = defaultboxes
    #(x,y,z,face):(objson index, obj index)
    vertexes = {}
    #(x,y,z):obj index
    uniqueVertexes = {}

    #(x,y,z,face):(objson index, obj index)
    normals = {}
    #(x,y,z):obj index
    uniqueNormals= {}

    #(u,v,face):(objson index, obj index)
    uv = {}
    #(x,y,z):obj index
    uniqueUV = {}

    #(objson-point1,objson-point2,objson-point3,face):(obj-point1,obj-point2,obj-point3)
    faces = {}
    faceTextures = {}
    #(face,localIndex),remappedIndex
    faceVertexMap = {}
    faceUVMap = {}
    faceNormalMap = {}
    groupTextures = {-1:0}    
    group=-1    
    file = inputLocation+modelName+".obj"
    print(file)
    try:  
        inputFile = open(file, "r");
        inputLines = inputFile.readlines();
        v=1
        n=1
        u=1
        f=0
        for line in inputLines:
            tokens = line.split(' ')
            if(tokens[0]=='#'):
                if(tokens[1].lower() == 'bounds'):
                    bounds = ast.literal_eval(line.split(' ',2)[2].replace('\n',''))
                elif(tokens[1].lower() == 'boxes'):
                    boxes = ast.literal_eval(line.split(' ',2)[2].replace('\n',''))
            elif(tokens[0]=='mtllib'):
                #print("Materials")
                continue
            elif(tokens[0]=='o'):
                #print("Object Name")
                continue
            elif(tokens[0]=='v'):
                #print("Vertex")
                vertexes.update({v:[tokens[1],tokens[2],tokens[3].replace('\n','')]})
                v += 1
            elif(tokens[0]=='vt'):
                #print("UV map vertex")
                uv.update({u:[tokens[1],tokens[2].replace('\n','')]})
                u += 1
            elif(tokens[0]=='vn'):
                #print("Normal")
                normals.update({n:[tokens[1],tokens[2],tokens[3].replace('\n','')]})
                n += 1
            elif(tokens[0]=='usemtl'):
                #print("Material to use")
                continue
            elif(tokens[0]=='s'):
                #print("Smooth Shading")
                continue
            elif(tokens[0]=='f'):
                #print("Face")
                x = tokens[1].split('/')
                y = tokens[2].split('/')
                z = tokens[3].replace('\n','').split('/')
                faces.update({f:(group,[x,y,z])})
                f += 1
            elif(tokens[0]=='g'):
                #print("Group")
                texture = tokens[1].split('_')
                for t in texture:
                    if("face" in t and "texture" in t):
                        texture = t.replace('face','').replace('texture:','').replace('\n','').split('-')
                        break
                groupTextures.update({int(texture[0]):int(texture[1])})
                group += 1
            #print(tokens)
        inputFile.close()
        if(debugOutput):
            print("Vertexes")
            print(vertexes)

            print("\nNormals")
            print(normals)

            print("\nUVs")
            print(uv)

            print("\nFaces")
            print(faces)

            print("\n Group textures")
            print(groupTextures)
        
        outputOBJSON.update({"bounds":bounds})
        
        
        faceTriangles = [[]]
        lastGroup = faces[0][0]
        faceList = []
        i = 0
        localFaceMap = {}
        currentGroup = -1
        lenG = len(groupTextures)
        for g in groupTextures:
            currentGroup = g
            for f in faces:
                if(faces[f][0]==currentGroup):
                    faceTriangles[-1].append(faces[f][1])
            faceTriangles.append([])  
        faceTriangles.pop()#remove extra last empty array
        i = 0
        group = -1
        lenUV = len(uv)
        for f in faceTriangles:
            faceVertices=[]
            localFaceMap = {}
                            #x,y,z, nz,ny,nz, ux,uv
            expandedVertex = [0,0,0,0,0,0,0,0]
            singleFaceTriangles = [] 
            for tri in f:
                localTri = []
                for v in tri:
                    expandedVertex[0] = float(vertexes[int(v[0])][0])
                    expandedVertex[1] = float(vertexes[int(v[0])][1])
                    expandedVertex[2] = float(vertexes[int(v[0])][2])
                    expandedVertex[3] = float(normals[int(v[2])][0])
                    expandedVertex[4] = float(normals[int(v[2])][1])
                    expandedVertex[5] = float(normals[int(v[2])][2])
                    if(lenUV>0):
                        expandedVertex[6] = float(uv[int(v[1])][0])
                        expandedVertex[7] = float(uv[int(v[1])][1])
                    else:
                        expandedVertex[6] = 0.0
                        expandedVertex[7] = 1.0
                    addedValue = localFaceMap.setdefault(tuple(expandedVertex),i)
                    localTri.append(addedValue)
                    if(addedValue == i):
                        i+=1 
                singleFaceTriangles.append(localTri)
            for f in localFaceMap:
                faceVertices.append(list(f))
            if(len(faceVertices)>0):
                currentFace = {"texture":groupTextures[group], "vertices":faceVertices, "triangles": singleFaceTriangles}
                faceList.append(currentFace)
            group += 1
            i = 0
        outputOBJSON.update({"faces":faceList})
        outputOBJSON.update({"boxes":boxes})
        
        #write with unix line ends to save some extra space
        output = open(outputLocation+modelName+".objson","w", newline='\n')
        output.write(json.dumps(outputOBJSON,indent=jsonIndent))
        output.close()
        
       
    except IOError:
        print("File not accessible");  
        
def convert_model(modelName,mode="OBJ",inputLocation="input/",outputLocation="output/"):
    if(mode == "OBJ"):
        objson_to_obj(modelName,inputLocation,outputLocation)
    else:
        obj_to_objson(modelName,inputLocation,outputLocation)


