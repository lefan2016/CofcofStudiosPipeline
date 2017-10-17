# -*- encoding: utf-8 -*-
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
        try:
            imgSeq.fileTextureName.set ( fPath )
        except:
            pass

def createFacePart ( filePath , pos , layerTex , createAt , projScale ):

    layer = filePath.split('\\')[-1]
    projector      = createNode ( 'projection' ,     n = layer + '_PRJ'    )
    projector.projType.set(3)
    imgSeq         = createNode ( 'file'       ,     n = layer + '_FILE'   )
    imgSeq.useFrameExtension.set(True)
    texturePlacer  = createNode ( 'place3dTexture' , n = layer + '_3DP')  # repr(texturePlacer) help(nt.Place3dTexture)
    texturePlacer.inheritsTransform.set(False)
    texturePlacer.translate.set ( createAt )
    connectAttr ( texturePlacer + '.worldInverseMatrix[0]' , projector + '.placementMatrix' , f = 1 )  # conecto matrices

    # asigno textura al file.
    asignText ( imgSeq , filePath )

    # conecto color y alfa de secuencia de imagen a projector
    connImg2ProjColor ( imgSeq , projector  )

    # conecto projection a un layer determinado o el siguiente disponible.
    inputNr = connProj2LayTexture( projector , layerTex , pos )
    return projector , imgSeq , texturePlacer , inputNr

def connImg2ProjColor ( imgSeq , projector  ):
    '''
    Conecta color de imgSeq a projector.
    '''
    connectAttr ( imgSeq + '.outColor'     , projector + '.image' )

def locChooser (layer,locs):
    '''
    Determina cuál locator se va a usar para crear los controles.
    '''
    if layer == 'l_ojo' or layer == 'l_pupila' or layer ==  'l_parpado':
        choosenLoc = locs[0]
    else:
        choosenLoc = locs[1]
    return choosenLoc

def parentControls ( networkDic ) :
    parent ( networkDic[11][3][1][0] , networkDic[12][3][0][0] )
    delete ( networkDic[11][3][3][0] )
    for n in range(13,15):
        parent ( networkDic[n][3][1][0] , networkDic[15][3][0][0]  )
        delete ( networkDic[n][3][3][0] )

def getLocation ( ): # del bBoxCentera
    sel = ls(sl=1)
    if len ( sel )== 1 and nodeType( sel[0].getShape() )== 'mesh' :
        if sel[0]  :
            bBoxCenter = sel[0].getBoundingBox().center()
            return bBoxCenter
    else:
        warning ( ' Selection is null or multiple. Positioning at (0,0,0) ' )
        return dt.Vector([0.0, 0.0, 0.0])

def createIfNeeded( node_Name , node_Type ):
    if not objExists ( node_Name ) :
        nodeRet  =   createNode ( node_Type , n = node_Name )
    else:
        nodeRet   = node_Name
    return nodeRet

def move2 ( parenting , child ):
    parentC = parentConstraint ( parenting , child  )
    delete ( parentC )

def createAimSystem ( layer , placer , loc , headBBoxCenter ):
    locAim   = spaceLocator( n=layer+'_LOC' )
    locAim.visibility.set(0)
    locAim.translate.set( headBBoxCenter[0] , headBBoxCenter[1] , headBBoxCenter[2]+1 )
    aimConst = aimConstraint(locAim, placer ,mo=1,n=locAim+'_AIMC')
    move2 ( loc , locAim )
    return locAim

def connectAlphas ( layeredTextureDic ):
    alphas = {10:10 , 11:12 , 12:12 , 13:13 , 14:15 , 15:15 } # que layer usa el layer. el 10 usa el 10, el 11 usa el 12, el 13 usa el 13, el 14 usa el 15,,,
    for pos in layeredTextureDic.keys():
        connImg2ProjAlpha ( layeredTextureDic[ alphas[pos] ][1] , layeredTextureDic[pos][0] )

def connImg2ProjAlpha ( imgSeq , projector  ):
    '''
    Conecta  alfa de imgSeq a projector.
    '''
    # conecto con el alfa q necesito que recorte.
    for channel in ('R','G','B'):
        connectAttr ( imgSeq.name()  + '.outAlpha' , projector + '.transparency' + channel )

def selValidation ( selObjects ):  # selObjects = ls(sl=1)
    counter = { 'locators': 0 , 'meshes': 0 , 'controls': 0 }
    if len (selObjects) == 3:
        for s in selObjects:
            if nodeType( s.getShape() ) == 'locator':
                counter['locators'] = counter['locators']+1
            elif nodeType( s.getShape() ) == 'mesh':
                counter['meshes'] = counter['meshes']+1
            elif nodeType( s.getShape() ) == 'nurbsCurve':
                counter['controls'] = counter['controls']+1
        return counter['locators']==1 and counter['meshes']==1 and counter['controls']==1
    else:
        return False

def placerControl(headSize,objs=[],placer3d='',nameSuf='ZTR',nameTrf='TRF',nameCNT='CNT',rad=2): #objs=texturePlacer
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
        cntl=cmds.circle(radius=rad,nr=(0,0,1),name=str(newName+nameCNT)) # creo cnt
        if 'l_ojo' in obj or 'boca' in obj:                               # tamaños para cada tipo
            ccLook (cntl,rad,3,5)
        elif 'l_pupila' in obj or 'lengua' in obj:
            ccLook (cntl,rad*0.6,1,1)
        elif 'l_parpado' in obj :
            ccLook (cntl,rad*1.2,1,1)
        cnt=cntl[0]
        mCircle=cntl[1]
        pcns=cmds.parentConstraint(trf,cnt) # constraints
        scns=cmds.scaleConstraint(trf,cnt)
        cmds.delete(pcns,scns)              # borro constraints
        cmds.parent(cnt,trf)
        cntsRet.append(cnt)
        ztrs.append (ztr)
        makeCircles.append ( renameMakeNurbCircle( mCircle ) )
        cmds.parent( obj , cnt )
        mulDivNode = createNode ('multiplyDivide',name=newName+'_MULT' )
        mulDivNode.input2X.set(headSize)
        mulDivNode.input2Y.set(headSize)
        mulDivNode.input2Z.set(headSize)
        connectAttr ( cnt + '.scale' , mulDivNode+'.input1' )
        connectAttr ( mulDivNode + '.output' , placer3d + '.scale')
        root = cmds.group(em=True,n=str(newName+'ROT'))
        roots.append (root)
        cmds.parent( ztr , root )
    return cntsRet,ztrs,makeCircles,roots



def ccLook ( circ , controlSize , degree , sections ):
    ccShape = listRelatives ( circ )[0]
    ccTrf   = ccShape.getTransform()
    ccTrf.getShape().inputs()[0].radius.set( controlSize )
    ccTrf.getShape().inputs()[0].degree.set(degree)
    ccTrf.getShape().inputs()[0].sections.set(sections)

def getLocation ( meshS ): # del bBoxCentera
    bBoxCenter = meshS.getBoundingBox().center()  # repr (ls(sl=1)[0].getBoundingBox() ) help( dt.BoundingBox ) help( nt.Transform )
    return bBoxCenter

def createInitialLocators(sel): # del location, initialLocators, loc
    '''
    Crea locators para posicion inicial de projectores.
    '''
    location = getLocation ( sel )
    locationOffsetX = sel.getBoundingBox().width() / 4 # help (nt.Transform)   help (dt.BoundingBox)   ls(sl=1)[0].translate.set ( 1,1,1)
    locationOffsetY = sel.getBoundingBox().height()/ 4
    locationOffsetZ = sel.getBoundingBox().depth() / 2
    select(cl=1)
    posX = location[0] + locationOffsetX
    posY = location[1] - locationOffsetY
    posZ = location[2] + locationOffsetZ
    pEyeX , pEyeY , pEyeZ , pMouthX , pMouthY , pMouthZ = (0,)*6
    if not objExists( 'L_Eye_LOC' ):
        loc1 = spaceLocator( n='L_Eye_LOC')
        loc1.translate.set ( posX , location[1] , posZ )
        pEyeX = posX
        pEyeY = location[1]
        pEyeZ = posZ
    else:
        pEyeX = getAttr('L_Eye_LOC.translateX')
        pEyeY = getAttr('L_Eye_LOC.translateY')
        pEyeZ = getAttr('L_Eye_LOC.translateZ')
    if not objExists( 'Mouth_LOC' ):
        loc2 = spaceLocator( n='Mouth_LOC')
        loc2.translate.set ( location[0] , posY , posZ )
    else:
        pMouthX = getAttr('Mouth_LOC.translateX')
        pMouthY = getAttr('Mouth_LOC.translateY')
        pMouthZ = getAttr('Mouth_LOC.translateZ')
    return { 'L_Eye_LOC': [pEyeX , pEyeY , pEyeZ ]  , 'Mouth_LOC': [ pMouthX , pMouthY , pMouthZ ]  }

def deleteHelpLocators ():
    for o in ('L_Eye_LOC', 'Mouth_LOC' , 'scaleReference_LOC'):
        delete (o)


####### ####### ####### ####### ####### ####### ####### #######

def create2DFacialRig (  ):
    selection = ls(sl=1)
    if selValidation ( selection ) :
        for s in selection:
            if nodeType( s.getShape() ) == 'locator':
                locSize = s.scale.get()[0]
            elif nodeType( s.getShape() ) == 'mesh':
                sel = s
                headSize = s.getBoundingBox().depth() / 2
            elif nodeType( s.getShape() ) == 'nurbsCurve':
                headControl = s
        location_locators = createInitialLocators(sel)
        mypath       = 'O:\EMPRESAS\RIG_FACE2D\PERSONAJES\MILO\FACES'
        ordenLayers  = { 'l_ojo': 15 , 'l_pupila' : 14 , 'l_parpado' : 13 , 'boca' : 12 , 'lengua' : 11 , 'extras' : 10 }
        dirsFiles    = dirs_files_dic( mypath ,'png')
        layeredTextureDic = {}
        layerTex     =   createIfNeeded ( 'Face_LTX' , 'layeredTexture' )
        pjShader     = listConnections( listHistory( sel  ,f=1),type='aiStandard')[0]  # por ahora asumo q tiene aiStandard Shader.
        faceShader   = createIfNeeded ( 'Face_SHD' , 'aiStandard' )
        headPivot    = sel.getBoundingBox().center()
        try:
            connectAttr ( layerTex + '.outColor'  , faceShader+ '.color' )
        except:
            pass
        for k in dirsFiles.keys(): # k='O:\EMPRESAS\RIG_FACE2D\PERSONAJES\MILO\FACES\l_ojo'
            layer = k.split('\\')[-1]
            if 'r_' != layer[0:2] and dirsFiles[k]!=[]:
                # determina cuál locator se va a usar para crear los controles.
                loc = locChooser ( layer , location_locators.keys() )
                # path de secuencia
                filePath = k + '\\' + dirsFiles[k][0]
                # crea projector,file y placer conectados al canal especificado
                projectorImagePlacerInput = createFacePart ( filePath , ordenLayers[ layer ] , layerTex  , headPivot  , headSize )
                # guardo parte en dic
                layeredTextureDic [ projectorImagePlacerInput[3]  ] = projectorImagePlacerInput [ : -1 ]
                # creo sistema Aim. Argumentos: layer, nombreDelPlacer , locatorParaUbicar.translate
                locAim = createAimSystem ( layer , projectorImagePlacerInput[2] , loc , headPivot )
                # creo control para el Aim
                ccCnt = placerControl ( headSize,objs=locAim , rad = locSize , placer3d = projectorImagePlacerInput[2]  )
                # guardo control
                layeredTextureDic [ projectorImagePlacerInput[3]  ] = layeredTextureDic [ projectorImagePlacerInput[3]  ] + tuple( [ ccCnt ] )
        connectAlphas  ( layeredTextureDic )
        parentControls ( layeredTextureDic )
        deleteHelpLocators ()
    else:
        warning ( '  Selection is null or multiple. Select head mesh ' )



if cmds.window ('win2dFacialRig',exists=1):
    cmds.deleteUI ( 'win2dFacialRig' )
win = cmds.window('win2dFacialRig', title="2D Facial Rig! v1.0" , menuBar=0 , w=100 , s=1 , height= 100, bgc=(0.1,0.1,0.1) , resizeToFitChildren=1 )
#location_locators = createInitialLocators(sel)
col1 = cmds.columnLayout( columnAttach=('left', 5), rowSpacing=10, columnWidth=550 , p=win , bgc=(0.3,0.3,0.3) )
cmds.button('1 ) Select the head mesh and click me. \n',p=col1,c="createInitialLocators(ls(sl=1)[0])" )
cmds.text('Place locators where eyes and mouth\nshould be. Rotations are considered.',p=col1)
c1 = cmds.columnLayout( columnAttach=('left', 5), rowSpacing=10, columnWidth=550, p=win , bgc=(0.3,0.3,0.3) )
cmds.text('\n2 ) Shift-Select:',p=c1)
r0 = cmds.rowLayout( numberOfColumns=1, adjustableColumn=1, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0)] ,p=c1)
#cmds.text('-  Locator with scale you want controllers to have. \nIf you don\'t have one, click me for creating one.',al="left",p=r0)
cmds.button( label = '-  A LOCATOR with scale you want controllers to have. \nIf you don\'t have one, click me for creating one.' , command = 'cmds.spaceLocator(n="scaleReference_LOC")' , p = r0 )
cmds.text('-  Head mesh.',p=c1)
cmds.text('-  Head controller.',p=c1)
c2 = cmds.columnLayout( columnAttach=('left', 5), rowSpacing=10, columnWidth=550 , p=win , bgc=(0.3,0.3,0.3) )
r1 = cmds.rowLayout( numberOfColumns=2, columnWidth3=(80, 75, 150), adjustableColumn=1, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0)] )
cmds.text('and press:  ' , p = r1 )
cmds.button( label = 'Rig head' , command = 'location_locators=create2DFacialRig ()' , p = r1 )
cmds.showWindow (win)