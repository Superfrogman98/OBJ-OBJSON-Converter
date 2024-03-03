import objson_converter_functions as cm

def main():
    continueInput=True
    while(continueInput):
        inputDir = input("Input File Location: ")
        outputDir = input("Output File Location: ")
        inputFileName = input("Input File Name: ")
        type = inputFileName.split(".")
        inputName = type[0]
        if(len(type) == 2):
            type = type[1]
        if(type == "obj"):
            cm.obj_to_objson(inputName,inputDir,outputDir)
        elif(type == "objson"):
            cm.objson_to_obj(inputName,inputDir,outputDir)
        else:
            print("File format not supported, not(obj or objson")
  
        if(input("Continue(Y/N):").lower() != "y"):
            continueInput=False   
            
if __name__ == "__main__":
    main()