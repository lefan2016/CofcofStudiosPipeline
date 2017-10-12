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
    dirs= [f for f in listdir(mypath) if not isfile(join(mypath, f))]
    for subdir in dirs:
        subdir = mypath+'\\'+subdir
        onlyfiles = [f for f in listdir(subdir) if ( isfile(join(subdir, f)) and os.path.splitext(f)[1]=='.'+filterExtension)]
        returnDic[subdir]= onlyfiles
    return returnDic

def folders2Rig (mypath):
    '''
    Create a network for 2D facial rig system from a folder input by user.
    '''
    #mypath     = 'O:\EMPRESAS\RIG_FACE2D\ScriptingGuideRig\Maps'
    dirsFiles  = dirs_files_dic( mypath ,'png')
    layerTex   = createNode ( 'layeredTexture' , n = 'Face_LTX' )
    layerTexShader = createNode ( 'layeredTexture' , n = 'FaceBody_LTX' )
    pjShader   = createNode ( 'aiStandard' , n = 'Character_SHD' )
    connectAttr ( layerTex + '.outColor'  , layerTexShader + '.inputs[0].color' )
    connectAttr ( layerTex + '.outAlpha'  , layerTexShader + '.inputs[0].alpha' )
    connectAttr ( layerTexShader + '.outColor'  , pjShader + '.color' )
    for k in dirsFiles.keys():
        layer = k.split('\\')[-1]
        projector  = createNode ( 'projection' , n = layer + '_PRJ'   )
        imgSeq     = createNode ( 'file'       , n = layer + '_FILE'   )
        setAttr ( imgSeq + '.useFrameExtension' , 1)
        try:
            setAttr ( imgSeq + '.fileTextureName' , k + '\\' + dirsFiles[k][0] )
        except:
            pass
        #img -> projection
        connectAttr ( imgSeq + '.outColor'     , projector + '.image' )
        for channel in ('R','G','B'):
            connectAttr ( imgSeq + '.outAlpha' , projector + '.transparency' + channel )  # conecto imagen al projection
        # projection -> layeredTexture
        counter=0
        attrConnected=False
        while not attrConnected:
            try:
                connectAttr ( projector + '.outColor'  , layerTex + '.inputs['+ str(counter)+'].color' )
                connectAttr ( projector + '.outAlpha'  , layerTex + '.inputs['+ str(counter)+'].alpha' )
                attrConnected = True
            except:
                counter = counter + 1
                pass
