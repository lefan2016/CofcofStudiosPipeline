import maya.cmds as cmds
import maya.mel as mel
#UNREAL EXPORTER GENERIC
def bakernaitor(objets=[],min=None,max=None):
    if not min:
        min = cmds.playbackOptions(q=True, min=True)
    if not max:
        max = cmds.playbackOptions(q=True, max=True)
    cmds.refresh(su=True)#Disable refresh
    cmds.bakeResults(objets, simulation=True,
                     sampleBy=1,
                     time=(min, max),
                     disableImplicitControl=True,
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

def skeletalCopy(sources=[], rootName='', bake=False):

    if sources:
        jntsNews = []
        cnsts = []
        geos = []

        if not cmds.objExists(rootName + '_GRP'):
            grp = cmds.group(n=rootName + '_GRP', empty=True)
        else:
            grp = rootName + '_GRP'
        if not cmds.objExists('C_' + rootName + '_ROOT_JNT'):
            root = cmds.joint(n='C_' + rootName + '_ROOT_JNT')
        else:
            root = 'C_' + rootName + '_ROOT_JNT'

        for source in sources:

            nTarget=''
            if '|' in source:
                nTarget=source.split('|')[-1]
            if ':' in source or nTarget:
                nTarget=source.split(':')[-1]
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
                if not cmds.objExists(jnt + '_COPY'):
                    newJnt = cmds.joint(name=jnt + '_COPY',p=(mtx[:3]), rad=0.5)
                else:
                    newJnt = jnt + '_COPY'

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
                
            for j in jntsNews:
                padre=cmds.listRelatives(j, parent=True)
                if not padre:
                    cmds.parent(j, root)

            '''
            target = cmds.listRelatives(target, shapes=True, fullPath=True)
            for t in target:
                if searchSCL(t):
                    targetSCL=t'''
            if not searchSCL(target):
                cmds.skinCluster(jntsNews, target, dr=4.5, n=str(target)[:-3] + '_SCL')
            #cmds.select(source)
            #cmds.select(target, tgl=True)
            #cmds.copySkinWeights(sa='closestPoint', ia='closestJoint', noMirror=True)
            cmds.copySkinWeights(ss=str(searchSCL(source)), ds=str(searchSCL(target)), noMirror=True, sa='closestPoint', ia='closestJoint')
            #mel.eval("copySkinWeights  -ss "+source+" -ds "+str(target)+" -noMirror -surfaceAssociation closestPoint -influenceAssociation closestJoint;")
            cmds.select(target)
            mel.eval( 'doPruneSkinClusterWeightsArgList 1 { "' + str(0.2) + '" }')
            mel.eval('removeUnusedInfluences')
            cmds.select(cl=True)

        if bake:
            bakernaitor(jntsNews)
            #cmds.delete(cnsts)
    else:
        cmds.warning(str(source) + ' Necesita una geometria con skin' ) 
'''
#Seleccionar un grupo de geometrias para reconocer todos los mesh
sel=cmds.ls(sl=1)
selectGeo=[]
selectGeo=cmds.listRelatives(sel ,children=True,fullPath=True)
skeletalCopy(selectGeo,'SNAIL',False)
'''
