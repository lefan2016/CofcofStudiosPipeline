import maya.cmds as cmds
import maya.mel as mel
#UNREAL EXPORTER GENERIC
def bakernaitor(objets=[],min=None,max=None, nameAnimLayer='NEW_BAKE'):
    if not min:
        min = cmds.playbackOptions(q=True, min=True)
    if not max:
        max = cmds.playbackOptions(q=True, max=True)
    cmds.refresh(su=True)#Disable refresh
    cmds.bakeResults(objets, simulation=True,
                     sampleBy=1,
                     time=(min, max),
                     oversamplingRate=4,#Sampleo
                     disableImplicitControl=True,
                     bakeOnOverrideLayer=False,#Se agrega una capa Override
                     destinationLayer=nameAnimLayer,#Si existe la capa se agrega en ella
                     preserveOutsideKeys=True,
                     sparseAnimCurveBake=True,
                     removeBakedAttributeFromLayer=False,
                     controlPoints=False,
                     shape=False)
    cmds.refresh(su=False)#Enable refresh

def searchSCL(obj):
    node=None
    for n in cmds.listHistory(obj):
        if str(cmds.nodeType(n))=='skinCluster':
            node=n
    return node

def createLayer(objs=[],layerName=''):
    if layerName:
        if cmds.objExists(layerName) and cmds.nodeType(layerName)=='displayLayer':
            ly=cmds.editDisplayLayerMembers( layerName, objs ) # store my selection into the display layer
        else:
            cmds.createDisplayLayer(name=layerName,number=1, empty=True)
            ly=cmds.editDisplayLayerMembers( layerName, objs )
        return ly

def createLayerAnim(objs=[],layerName=''):
        if layerName:
            if cmds.objExists(layerName) and cmds.nodeType(layerName)=='AnimLayer':
                cmds.select(objs,r=True)
                ly=cmds.animLayer( e=True addSelectedObjects=layerName ) # store my selection into the display layer
            else:
                cmds.animLayer( name=layerName, override=True )
                cmds.select(objs,r=True)
                ly=cmds.animLayer( e=True addSelectedObjects=layerName )
            return ly

def skeletalCopy(sources=[], rootName='', bake=False,deleteCnts=False):

    if sources:
        jntsNews = []
        cnsts = []
        geos = []
        nTarget=''

        if not cmds.objExists(rootName + '_GRP'):
            grp = cmds.group(n=rootName + '_GRP', empty=True)
        else:
            grp = rootName + '_GRP'
        if not cmds.objExists('C_' + rootName + '_ROOT_JNT'):
            root = cmds.joint(n='C_' + rootName + '_ROOT_JNT')
        else:
            root = 'C_' + rootName + '_ROOT_JNT'

        for source in sources:

            if '|' in source:
                nTarget=source.split('|')[-1]
            elif ':' in source or nTarget:
                nTarget=source.split(':')[-1]
            else:
                nTarget=source
            if cmds.objExists(str(nTarget)+'_MCPY'):
                target=str(nTarget)+'_MCPY'
                cmds.warning('Ya existe '+ target)
            else:
                target = cmds.duplicate(source, n=str(nTarget)+'_MCPY')[0]

            if str(cmds.listRelatives(target, parent=True)[0]) != grp:
                cmds.parent(target, grp)

            influenceJoints = cmds.skinCluster(source, query=True, influence=True)

            for jnt in influenceJoints:
                mtx = cmds.xform(jnt, q=True, ws=True,m=True)
                cmds.select(cl=True)
                if cmds.objExists(jnt + '_COPY'):
                    newJnt = jnt + '_COPY'
                else:
                    newJnt = cmds.joint(name=jnt + '_COPY',p=(mtx[:3]), rad=0.5)

                cmds.select(cl=True)
                cmds.xform(newJnt, m=mtx)

                try:
                    cnsts.append(cmds.parentConstraint(jnt, newJnt, mo=True,n=jnt+'_HCNS')[0])
                    cnsts.append(cmds.scaleConstraint(jnt, newJnt, mo=True,n=jnt+'_SCNS')[0])
                except:
                    pass

                if not newJnt in jntsNews:
                    jntsNews.append(newJnt)
                if root in jntsNews:
                    jntsNews.remove(root)

            for j in jntsNews:#Me aseguro que estan todos en el root
                padre=cmds.listRelatives(j, parent=True)
                if not padre:
                    cmds.parent(j, root)


            if not searchSCL(target):
                cmds.skinCluster(jntsNews, target, dr=4.5, n=str(target)[:-3] + '_SCL')
            cmds.copySkinWeights(ss=str(searchSCL(source)), ds=str(searchSCL(target)), noMirror=True, sa='closestPoint', ia='closestJoint')
            #cmds.select(target)
            #mel.eval( 'doPruneSkinClusterWeightsArgList 1 { "' + str(0.2) + '" }')
            #mel.eval('removeUnusedInfluences')
            #cmds.select(cl=True)

            #Ordeno todo en un layer
            createLayer(objs=[target], layerName=rootName+'_LAY')
            createLayer(objs=jntsNews, layerName=rootName+'_LAY')

        if bake:
            createLayerAnim(jntsNews, rootName+'_LAN')
            bakernaitor(jntsNews,nameAnimLayer=rootName+'_LAN')
        if deleteCnts:
            cmds.delete(cnsts)
    else:
        cmds.warning(str(source) + ' Necesita una geometria con skin' )
'''
#Seleccionar un grupo de geometrias para reconocer todos los mesh
sel=cmds.ls(sl=1)
selectGeo=[]
selectGeo=cmds.listRelatives(sel ,children=True,fullPath=True)
skeletalCopy(selectGeo,'SNAIL',False)
'''
