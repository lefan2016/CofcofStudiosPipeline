import maya.cmds
import sys
path='P:\LOCAL\ES_SCRIPTS\RIG'
if not path in sys.path:
	sys.path.append(path)
import ES_RIG_CURVE as ere
reload(ere)

seleccion=cmds.ls(sl=1,o=True)
seleccionEdge=cmds.ls(sl=1)
cosas={}
crv=ere.edgeLoopCrv(seleccionEdge)
cosas[0]=ere.creaLocWithJointsInPositionVertexOfCurve([crv],step=2)
ere.aimConsecutiveList(cosas[0][0])
lowCRV=ere.crearLowCrvControl([crv])
aimConstraint
#ere.nonlinearDeformer([lowCRV[0]],'twist',rotate=(0,0,90))
#ere.nonlinearDeformer([lowCRV[0]],'sine',rotate=(0,0,90))


cnts=cmds.ls('ROBOT345__Ctrl_*Effector')
for cnt in cnts:
    cmds.setAttr(str(cnt)+'.reachTranslation',k=1)
    cmds.setAttr(str(cnt)+'.reachRotation',k=1)


import maya.cmds as mc
SLCS=mc.ls('*_SLC',type='transform')
for slc in SLCS:
    jointName=slc.split('_SLC')[0]
    #si es un joint sigo
    if mc.objExists(jointName) and mc.nodeType(jointName)=='joint':
        attrs=mc.listAttr (slc, keyable=1)
        for attr in attrs:
            mc.setAttr (slc+"."+attr, lock=0)
    #si no estaba emparentado sigo
        if not mc.objExists(str(jointName)+'__PCNS'):
            #emparento
            mc.parentConstraint(jointName,slc,name=str(jointName)+'__PCNS',maintainOffset=True)
        if not mc.objExists(str(jointName)+'__SCNS'):
            #emparento
            mc.scaleConstraint(jointName,slc,name=str(jointName)+'__SCNS',maintainOffset=True)
    print str(jointName)
    print str(slc)
'''
objs=cmds.ls(sl=1)
adel=[]
for obj in objs:
    a=cmds.listRelatives(obj,children=True,type=['parentConstraint','scaleConstraint'])
    if a:
        adel.append(a[0])
        adel.append(a[1])
cmds.delete(adel)
'''
#Creador de piston
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

def crearHelpersLocators(name=''):
    startLocator=cmds.spaceLocator(n=str(name)+"_START"+'_LOC')[0]
    cmds.move(0,0,0,startLocator)
    endLocator=cmds.spaceLocator(n=str(name)+"_END"+'_LOC')[0]
    cmds.move(0,7,0,endLocator)
    return startLocator,endLocator

def pistonIkRig(startLocator=None,endLocator=None,nameRig=''):
    #startLocator,endLocator=loc1,loc2
    # Start/End points
    startPoint = cmds.xform(startLocator, q=True, ws=True, rp=True)
    endPoint = cmds.xform(endLocator, q=True, ws=True, rp=True)
    # Use maya API vector class
    mVectorStart = OpenMaya.MVector(startPoint[0], startPoint[1], startPoint[2])
    mVectorEnd = OpenMaya.MVector(endPoint[0], endPoint[1], endPoint[2])
    mVectorResult = mVectorEnd - mVectorStart

    # Create a locator per joint number
    newPoint = mVectorResult * 0.5
    finalPointStart = mVectorStart + newPoint
    finalPointEnd = mVectorEnd + -newPoint

    cmds.select(cl=True)
    jStart1=cmds.joint(name=nameRig+'_LOWER1_JSK',p=mVectorStart)
    jStart2=cmds.joint(name=nameRig+'_LOWER2_JSK',p=finalPointStart)
    ikH1=cmds.ikHandle( sj=jStart1, ee=jStart2, p=2, w=.5 ,name=str(nameRig)+'_LOWER_IKH')[0]
    cmds.pointConstraint(endLocator,ikH1,offset=[0,0,0],maintainOffset=False,name=str(nameRig)+'_LOEWR_PCNS')
    cmds.parent(jStart1,startLocator)
    cmds.setAttr(ikH1+'.v',False)

    jEnd1=cmds.joint(name=nameRig+'_UPPER1_JSK',p=mVectorEnd)
    jEnd2=cmds.joint(name=nameRig+'_UPPER2_JSK',p=finalPointEnd)
    ikH2=cmds.ikHandle( sj=jEnd1, ee=jEnd2, p=2, w=.5 ,name=str(nameRig)+'_UPPER_IKH')[0]
    cmds.pointConstraint(startLocator,ikH2,offset=[0,0,0],maintainOffset=False,name=str(nameRig)+'_UPPER_PCNS')
    cmds.parent(jEnd1,endLocator)
    cmds.setAttr(ikH2+'.v',False)

    cmds.group([startLocator,endLocator,ikH1,ikH2],name=nameRig+'_RIG_GRP')


nameRig = 'L_PISTON7'
loc1, loc2 = crearHelpersLocators( nameRig )

pistonIkRig(loc1,loc2,nameRig)
