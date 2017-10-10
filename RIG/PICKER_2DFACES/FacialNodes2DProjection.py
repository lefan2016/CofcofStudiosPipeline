from pymel.core import *
from os import listdir
from os.path import isfile, join

def dirs_files_dic ( mypath , filterExtension ):
    '''
    Returns a dic { Dir : files in Dir }. A dictonary with subdirectories and files inside them from a directory input.
    Example:
        dirs_files_dic('O:\EMPRESAS\RIG_FACE2D\ScriptingGuideRig\Maps','png')
    '''
    from os import listdir
    from os.path import isfile, join
    returnDic = {}
    dirs= [f for f in os.listdir(mypath) if not isfile(join(mypath, f))]
    for subdir in dirs:
        subdir = mypath+'\\'+subdir
        onlyfiles = [f for f in listdir(subdir) if ( isfile(join(subdir, f)) and os.path.splitext(f)[1]=='.'+filterExtension)]
        returnDic[subdir]= onlyfiles
    return returnDic

mypath     = 'O:\EMPRESAS\RIG_FACE2D\ScriptingGuideRig\Maps'
dirsFiles  = dirs_files_dic( mypath ,'png')
layerTex   = createNode ( 'layeredTexture' , n = 'Face_LTX' )
#projectors = []      projectors.append ( projector )
for k in dirsFiles.keys():
    layer = k.split('\\')[-1]
    projector  = createNode ( 'projection' , n = layer + '_PRJ'   )
    imgSeq     = createNode ( 'file'       , n = layer + 'FILE'   )
    #img -> projection
    connectAttr ( imgSeq + '.outColor'     , projector + '.image' )
    for channel in ('R','G','B'):
        connectAttr ( imgSeq + '.outAlpha' , projector + '.transparency' + channel )  # conecto imagen al projection
    # projection -> layeredTexture
    connectAttr ( projector + '.outColor'  , layerTex + 'inputs[7]' )
