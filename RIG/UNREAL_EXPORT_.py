import maya.cmds as cmds
import maya.mel as mel

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

def skeletalCopy(sources=[],rootName='',bake=False):
    if sources:
        jntsNews=[]
        cnsts=[]
        geos=[]
        if not cmds.objExists(rootName+'_GRP'):
            grp=cmds.group(n=rootName+'_GRP',empty=True)
        else:
            grp=rootName+'_GRP'
        if not cmds.objExists('C_'+rootName+'_ROOT_JNT'):
            root=cmds.joint(n='C_'+rootName+'_ROOT_JNT')
        else:
            root='C_'+rootName+'_ROOT_JNT'
        for source in sources:
            target=cmds.duplicate(source,n=str(source)[:-9]+'_MCPY')[0]
            cmds.parent(target,grp)
            influenceJoints = mc.skinCluster (source, query=True, influence=True)
            for jnt in influenceJoints:
                mtx=cmds.xform(jnt,q=True,m=True)
                cmds.select(cl=True)
                if not cmds.objExists(jnt+'_COPY'):
                    newJnt=cmds.joint(name=jnt+'_COPY',rad=0.5)
                else:
                    newJnt=jnt+'_COPY'

                cmds.select(cl=True)
                cmds.xform(newJnt,m=mtx)
                try:
                    cnsts.append(cmds.parentConstraint(jnt,newJnt,mo=True)[0])
                    cnsts.append(cmds.scaleConstraint(jnt,newJnt,mo=True)[0])
                except:
                    pass
                if not newJnt in jntsNews:
                    jntsNews.append(newJnt)
            try:
                cmds.parent(jntsNews,root)
            except:
                pass
            cmds.skinCluster( jntsNews, target, dr=4.5,n=str(target)[:-3]+'_SCL')
            cmds.select(source)
            cmds.select(target,tgl=True)
            cmds.copySkinWeights(noMirror=True,sa='closestPoint',ia='closestJoint')
            cmds.copySkinWeights(ss=source,ds=str(target),noMirror=True,sa='closestPoint',ia='closestJoint')
            mel.eval("copySkinWeights  -ss "+source+" -ds "+str(target)+" -noMirror -surfaceAssociation closestPoint -influenceAssociation closestJoint;")
            cmds.select(target)
            mel.eval('doPruneSkinClusterWeightsArgList 1 { "'+str(0.2)+'" }')
            mel.eval('removeUnusedInfluences')
            cmds.select(cl=True)
        if bake:
            bakernaitor(jntsNews)
            cmds.delete(cnsts)
    else:
        cmds.warning('Necesitas una geometria con skin')


selectGeo=[cmds.listRelatives(sel ,shapes=True,fullPath=True)[0] for sel in cmds.ls(sl=True)]#Elijo las geos
skeletalCopy(selectGeo,'SNAIL',False)
