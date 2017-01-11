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


nameRig = 'L_PISTON1'
loc1, loc2 = crearHelpersLocators( nameRig )

pistonIkRig(loc1,loc2,nameRig)
