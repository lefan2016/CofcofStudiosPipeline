from pymel.core import *
from os import listdir
from os.path import isfile, join
import pymel.core.datatypes
path=r'P:\LOCAL\ES_SCRIPTS\RIG'
if not path in sys.path:
	sys.path.append(path)

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

def placerControl(objs=[],placer3d='',nameSuf='ZTR',nameTrf='TRF',nameCNT='CNT',rad=2): #objs=texturePlacer
    '''
    Crea controles para objectos.
    Returns [ [Controls 's name] , [ZTRs 's name]  ]
    '''
    select(cl=1)
    select( objs )
    objs = cmds.ls(sl=1)

    cntsRet     = []
    ztrs        = []
    makeCircles = []
    roots       = []
    for obj in objs: # obj = 'r_pupila_3DP'
        if '|' in obj:
            obj=obj.split('|')[-1]
        if '_' in obj:
            newName=obj.split(obj.split('_')[-1:][0])[0]
        else:
            newName=obj
        ztr=cmds.group(em=True,n=str(newName+nameSuf))
        pcns=cmds.parentConstraint(obj,ztr)[0]
        scns=cmds.scaleConstraint(obj,ztr)[0]
        cmds.delete(pcns,scns)
        trf=cmds.duplicate(ztr,n=str(newName+nameTrf))[0]
        cmds.parent(trf,ztr)
        cntl=cmds.circle(radius=rad,nr=(0,0,1),name=str(newName+nameCNT))
        cnt=cntl[0]
        mCircle=cntl[1]
        pcns=cmds.parentConstraint(trf,cnt)
        scns=cmds.scaleConstraint(trf,cnt)
        cmds.delete(pcns,scns)
        cmds.parent(cnt,trf)
        cntsRet.append(cnt)
        ztrs.append (ztr)
        makeCircles.append ( renameMakeNurbCircle( mCircle ) )
        cmds.parent( obj , cnt )
        connectAttr ( cnt + '.scale' , placer3d + '.scale')
        root = cmds.group(em=True,n=str(newName+'ROT'))
        roots.append (root)
        cmds.parent( ztr , root )
    return cntsRet,ztrs,makeCircles,roots


def constraintObj2Cnt (sel,cnts):
    for o in sel:
        for cnt in cnts[0]:
            if o.split('JNT')[0] == cnt.split('CNT')[0]:
                cmds.parentConstraint(cnt,o,mo=True,n=cnt.split('CNT')[0]+'_HCNT')

def renameMakeNurbCircle( makeNode ):
    oCurve = listConnections( makeNode , sh=1)[0]
    newNameMakeCircle = oCurve.split('Shape')[0] + '_makeNCircle'
    return rename ( makeNode , newNameMakeCircle )



def connProj2LayTexture( projector , layerTex , chNumber ):
    '''
    Conecta el projector al layeredTexture al canal X. si no esta disponible, lo conecta al proximo disponible.
    '''
    counter = chNumber
    attrConnected = False
    while not attrConnected : # voy probando hasta dar con el proximo input[X].color disponible
        try :
            connectAttr ( projector + '.outColor'  , layerTex + '.inputs['+ str(counter)+'].color' )
            connectAttr ( projector + '.outAlpha'  , layerTex + '.inputs['+ str(counter)+'].alpha' )
            attrConnected = True
        except:
            counter = counter + 1
            pass
    return counter

def asignText ( imgSeq , fPath ) :
    '''
    asigna textura al nodo file.
    '''
    if isfile ( fPath ):
        print '           Archivo existe'
        try:
            imgSeq.fileTextureName.set ( fPath ) #filePath fPath
        except:
            pass


def move2 ( parenting , child ):
    parentC = parentConstraint ( parenting , child  )
    delete ( parentC )


def createAimSystem ( layer , placer , loc ):
    locAim   = spaceLocator( n=layer+'_LOC' )
    locAim.translateZ.set(1)
    aimConst = aimConstraint(locAim, placer ,mo=1,n=locAim+'_AIMC')
    move2 ( loc , locAim )
    return locAim

def createFacePart ( filePath , pos , layerTex ):

    layer = filePath.split('\\')[-1]
    print layer + '\n    creando proj'
    projector      = createNode ( 'projection' ,     n = layer + '_PRJ'    )
    projector.projType.set(3)
    print '    creando file'
    imgSeq         = createNode ( 'file'       ,     n = layer + '_FILE'   )
    imgSeq.useFrameExtension.set(True)
    print '    creando placer'
    texturePlacer  = createNode ( 'place3dTexture' , n = layer + '_3DP')  # repr(texturePlacer) help(nt.Place3dTexture)
    texturePlacer.inheritsTransform.set(False)
    connectAttr ( texturePlacer + '.worldInverseMatrix[0]' , projector + '.placementMatrix' , f = 1 )  # conecto matrices

    # asigno textura al file.
    print '    asigno tex \n \n'
    asignText ( imgSeq , filePath )

    # conecto color y alfa de secuencia de imagen a projector
    connImg2ProjColor ( imgSeq , projector  )

    # conecto projection a un layer determinado o el siguiente disponible.
    inputNr = connProj2LayTexture( projector , layerTex , pos )
    return projector , imgSeq , texturePlacer , inputNr

def createIfNeeded( node_Name , node_Type ):
    if not objExists ( node_Name ) :
        nodeRet  =   createNode ( node_Type , n = node_Name )
    else:
        nodeRet   = node_Name
    return nodeRet

def connImg2ProjColor ( imgSeq , projector  ):
    '''
    Conecta color de imgSeq a projector.
    '''
    connectAttr ( imgSeq + '.outColor'     , projector + '.image' )


def connImg2ProjAlpha ( imgSeq , projector  ): #imgSeq=layeredTextureDic[pos][1] projector=layeredTextureDic[pos][0]  del imgSeq,projector
    '''
    Conecta  alfa de imgSeq a projector.
    '''
    # conecto con el alfa q necesito que recorte.
    alphas = { 'r_ojo_000_png_FILE': 'r_ojo_000_png_FILE' , 'r_pupila_000_png_FILE' : 'r_ojo_000_png_FILE' , 'r_parpado_000_png_FILE' : 'r_parpado_000_png_FILE' , 'extras_000_png_FILE' : 'r_ojo_000_png_FILE' , 'boca_000_png_FILE' : 'boca_000_png_FILE'  , 'lengua_000_png_FILE' : 'boca_000_png_FILE'  }
    for channel in ('R','G','B'):
        connectAttr ( alphas[ imgSeq.name() ] + '.outAlpha' , projector + '.transparency' + channel )

def locChooser (layer,locs): # del locs
    '''
    Determina cuál locator se va a usar para crear los controles.
    '''
    if layer == 'r_ojo' or layer == 'r_pupila' or layer ==  'r_parpado':
        choosenLoc = locs[0]
    else:
        choosenLoc = locs[1]
    return choosenLoc

def connectAlphas ( layeredTextureDic ):
    for pos in layeredTextureDic.keys():
        print layeredTextureDic[pos][1] , layeredTextureDic[pos][0]
        connImg2ProjAlpha ( layeredTextureDic[pos][1] , layeredTextureDic[pos][0] )

def parentControls ( networkDic ) :
    parent ( networkDic[11][3][1][0] , networkDic[12][3][0][0] )
    delete ( networkDic[11][3][3][0] )
    for n in range(13,15):
        parent ( networkDic[n][3][1][0] , networkDic[15][3][0][0]  )
        delete ( networkDic[n][3][3][0] )

def getLocation ( ): # del bBoxCenter
    sel = ls(sl=1)
    if len ( sel )== 1 and nodeType( sel[0].getShape() )== 'mesh' :
        if sel[0]  :
            bBoxCenter = sel[0].getBoundingBox().center()  # repr (ls(sl=1)[0].getBoundingBox() ) help( dt.BoundingBox ) help( nt.Transform )
            return bBoxCenter
    else:
        warning ( ' Selection is null or multiple. Positioning at (0,0,0) ' )
        return dt.Vector([0.0, 0.0, 0.0])

def createInitialLocators(): # del location, initialLocators, loc
    '''
    Crea locators para posicion inicial de projectores.
    '''
    location = getLocation ( )
    select(cl=1)
    initialLocators = ('L_Eye_LOC' , 'Mouth_LOC')
    for l in initialLocators :
        if not objExists( l ):
            loc = spaceLocator( n=l)
            loc.translate.set ( location )

    return initialLocators

####### ####### ####### ####### ####### ####### ####### #######

def create2DFacialRig ( locations ):
    # del sel,locations,mypath,ordenLayers ,dirsFiles ,layeredTextureDic ,layerTex ,pjShader,faceShader,k
    # del locations
    # del mypath
    # del ordenLayers
    # del dirsFiles
    # del layeredTextureDic
    # del layerTex
    # del pjShader
    # del faceShader
    # del k
    #locations=('L_Eye_LOC', 'Mouth_LOC')
    # k= 'O:\\EMPRESAS\\RIG_FACE2D\\PERSONAJES\\MILO\\FACES\\a_diente'
    sel = ls(sl=1)
    if len ( sel )== 1 and nodeType( sel[0].getShape() )== 'mesh' :
        if ls(sl=1) :
            sel = ls(sl=1)[0]
            mypath     = 'O:\EMPRESAS\RIG_FACE2D\PERSONAJES\MILO\FACES'
            ordenLayers = { 'r_ojo': 15 , 'r_pupila' : 14 , 'r_parpado' : 13 , 'boca' : 12 , 'lengua' : 11 , 'extras' : 10 }
            dirsFiles  = dirs_files_dic( mypath ,'png')
            layeredTextureDic = {}
            layerTex   =   createIfNeeded ( 'Face_LTX' , 'layeredTexture' )
            pjShader   = listConnections( listHistory( sel  ,f=1),type='aiStandard')[0]  # por ahora asumo q tiene aiStandard Shader.
            faceShader   =   createIfNeeded ( 'Face_SHD' , 'aiStandard' )
            try:
                connectAttr ( layerTex + '.outColor'  , faceShader+ '.color' )
            except:
                pass
            for k in dirsFiles.keys():
                layer = k.split('\\')[-1]
                if 'l_' != layer[0:2] and dirsFiles[k]:
                    # determina cuál locator se va a usar para crear los controles.
                    loc = locChooser ( layer , locations )
                    # path de secuencia
                    filePath = k + '\\' + dirsFiles[k][0]
                    # crea projector,file y placer conectados al canal especificado
                    projectorImagePlacerInput = createFacePart ( filePath , ordenLayers[ layer ] , layerTex )
                    # guardo parte en dic
                    layeredTextureDic [ projectorImagePlacerInput[3]  ] = projectorImagePlacerInput [ : -1 ]
                    # creo sistema Aim
                    locAim = createAimSystem ( layer , projectorImagePlacerInput[2] , loc )
                    # creo control para el Aim
                    ccCnt = placerControl ( objs=locAim , rad = 1 , placer3d = projectorImagePlacerInput[2] )
                    # guardo control
                    layeredTextureDic [ projectorImagePlacerInput[3]  ] = layeredTextureDic [ projectorImagePlacerInput[3]  ] + tuple( [ ccCnt ] )
            # conecto alfas
            connectAlphas  ( layeredTextureDic )
            #emparentando controles
            parentControls ( layeredTextureDic )
        else:
            warning ( '  Selection is null or multiple. Select head mesh ' )
    else:
        warning('select mesh head')

locs = createInitialLocators()
create2DFacialRig (locs)
