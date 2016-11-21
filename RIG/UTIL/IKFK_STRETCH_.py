import maya.cmds as cmds
def createRamdomRotationInSpace( CNT=None,targets=None,nameNode='L_TENTACLE_' ):

    if not cmds.attributeQuery( nameNode+'AMPLITUDE', n=CNT ,exists=True ):
        cmds.addAttr(CNT , shortName=nameNode+'AMPLITUDE', longName=nameNode+'AMPLITUDE', defaultValue=0, k=True)
    if not cmds.attributeQuery( nameNode+'FRECUENCY_X', n=CNT ,exists=True ):
        cmds.addAttr(CNT , shortName=nameNode+'FRECUENCY_X', longName=nameNode+'FRECUENCY_X', defaultValue=0.6, k=True)
    if not cmds.attributeQuery( nameNode+'FRECUENCY_Y', n=CNT ,exists=True ):
        cmds.addAttr(CNT , shortName=nameNode+'FRECUENCY_Y', longName=nameNode+'FRECUENCY_Y', defaultValue=0.8, k=True)
    if not cmds.attributeQuery( nameNode+'FRECUENCY_Z', n=CNT ,exists=True ):
        cmds.addAttr(CNT , shortName=nameNode+'FRECUENCY_Z', longName=nameNode+'FRECUENCY_Z', defaultValue=-0.5, k=True)

    cmds.expression( s= str(targets)+".rx = sin( time*"+str(CNT)+'.'+nameNode+'FRECUENCY_X'+" )*"+str(CNT)+'.'+nameNode+'AMPLITUDE'+";\n"+
                        str(targets)+".ry = sin( time*"+str(CNT)+'.'+nameNode+'FRECUENCY_Y'+" )*"+str(CNT)+'.'+nameNode+'AMPLITUDE'+";\n"
                        +str(targets)+".rz = sin( time*"+str(CNT)+'.'+nameNode+'FRECUENCY_Z'+" )*"+str(CNT)+'.'+nameNode+'AMPLITUDE'+";",n=nameNode+'RAMDOM_EXP')

createRamdomRotationInSpace('L_SNAIL_TENTACLE_controls_CNT','L_SNAIL_TENTACLE_controls_TRF2','L_TENTACLE_')
def createJointIkInOrderOne(sufJoint='JIK'):
    sel=cmds.ls(sl=1)
    if len(sel)>=3:
        JNTS=[]
        pos,ori=cmds.xform(sel[0],q=True,ws=True,t=True),cmds.xform(sel[0],q=True,ws=True,ro=True)
        cmds.select(cl=1)
        JNTS.append(cmds.joint(n=str(sel[0].split(str(sel[0].split('_')[-1:][0]))[0])+sufJoint,a=True,p=pos,o=ori))

        for obj in sel[1:]:
            pos,ori=cmds.xform(obj,q=True,ws=True,t=True),cmds.xform(sel[0],q=True,ws=True,ro=True)
            JNTS.append(cmds.joint(n=str(obj.split(str(obj.split('_')[-1:][0]))[0])+sufJoint,a=True,p=pos))
        cmds.select(sel)
        return JNTS
    else:
        print 'Necesitas 3 o mas puntos para crar un ik'

def createLocatorsInOrder(sufLoc='LIK'):
    sel=cmds.ls(sl=1)
    if len(sel):
        LOCS=[]
        for obj in sel:
            pos,ori=cmds.xform(obj,q=True,ws=True,t=True),cmds.xform(sel[0],q=True,ws=True,ro=True)
            loc=cmds.spaceLocator(n=str(obj.split(str(obj.split('_')[-1:][0]))[0])+sufLoc)[0]
            cmds.xform(loc,ws=True,t=pos,ro=ori)
            LOCS.append(loc)
        return LOCS
    else:
        print 'Necesitas seleccionar puntos en el espacio'

def ikfkStretch(JNTS=[],LOCS=[]):

    IKH=cmds.ikHandle(n= "HAND_IKH", sj= JNTS[0], ee= JNTS[2], sol = 'ikRPsolver')

    PVC=cmds.poleVectorConstraint(LOCS[1], IKH[0],n='HAND_PVC' )

    cmds.parent(PVC,LOCS[2])
    cmds.parent(JNTS[0],LOCS[0])

    hipPos = cmds.xform(JNTS[0], q=True, ws=True, t=True)
    anklePos = cmds.xform(IKH[0], q=True, ws=True, t=True)
    pelvisPos = cmds.xform(LOCS[0], q=True, ws=True, t=True)

    cmds.addAttr(LOCS[2] , shortName='Twist', longName='Twist', defaultValue=0, k=True)

    PMA=str(cmds.shadingNode("plusMinusAverage", asUtility=True, n='HAND_TWIST_PMA'))
    NMD=str(cmds.shadingNode("multiplyDivide", asUtility=True, n='HAND_TWIST_NMD'))

    cmds.connectAttr(str(LOCS[2])+'.Twist', NMD+'.input1X')
    cmds.connectAttr(str(LOCS[2])+'.ry', NMD+'.input1Y')
    cmds.connectAttr(str(LOCS[0])+'.ry', NMD+'.input1Z')
    cmds.setAttr( NMD+'.input2X', -1)
    cmds.setAttr( NMD+'.input2Y', -1)
    cmds.setAttr( NMD+'.input2Z', -1)
    cmds.connectAttr( NMD+'.input1X', PMA+'.input1D[0]')
    cmds.connectAttr( NMD+'.input1Y', PMA+'.input1D[1]')
    cmds.connectAttr( PMA+'.output1D', IKH[0]+'.twist')

    ADL=str(cmds.shadingNode("addDoubleLinear", asUtility=True, n='HAND_STRETCH_ADL'))
    CMP=str(cmds.shadingNode("clamp", asUtility=True, n='HAND_STRETCH_CMP'))
    NMD_HAND_CNT=str(cmds.shadingNode("multiplyDivide", asUtility=True, n='HAND_STRETCHCNT_NMD'))
    NMD_RODILLA=str(cmds.shadingNode("multiplyDivide", asUtility=True, n='HAND_STRETCHRODILLA_NMD'))
    NMD_MUNIECA=str(cmds.shadingNode("multiplyDivide", asUtility=True, n='HAND_STRETCHMUNIECA_NMD'))

    cmds.addAttr(LOCS[2], shortName='Stretch', longName='Stretch', defaultValue=0, k=True)

    hipPos = cmds.xform(JNTS[0], q=True, ws=True, t=True)
    anklePos = cmds.xform(IKH[0], q=True, ws=True, t=True)
    disDim = cmds.distanceDimension(sp=(hipPos), ep=(anklePos))
    disDim = cmds.rename(disDim, 'HAND_STRETCH_DDN')

    kneeLen = cmds.getAttr(str(LOCS[0])+'.tx')
    ankleLen = cmds.getAttr(str(LOCS[2])+'.tx')
    legLen = (kneeLen + ankleLen)

    cmds.setAttr(ADL+'.input2', legLen)
    cmds.setAttr(NMD_HAND_CNT+'.input2X', legLen)
    cmds.setAttr(NMD_RODILLA+'.input2X', kneeLen)
    cmds.setAttr(NMD_MUNIECA+'.input2X', ankleLen)

    cmds.connectAttr(str(LOCS[2])+'.Stretch', ADL+'.input1')
    cmds.setAttr (CMP+".minR", 12.800084)
    cmds.setAttr (NMD_HAND_CNT+".operation",  2)

    cmds.connectAttr(disDim+'.distance', CMP+'.inputR')
    cmds.connectAttr( ADL+'.output', CMP+'.maxR')

    cmds.connectAttr(CMP+'.outputR', NMD_HAND_CNT+'.input1X')
    cmds.connectAttr(NMD_HAND_CNT+'.outputX', NMD_RODILLA+'.input1X')
    cmds.connectAttr(NMD_HAND_CNT+'.outputX', NMD_MUNIECA+'.input1X')

    cmds.connectAttr(NMD_RODILLA+'.outputX', str(JNTS[1])+'.tx')
    cmds.connectAttr(NMD_MUNIECA+'.outputX', str(JNTS[2])+'.tx')

    CDN=str(cmds.shadingNode("condition", asUtility=True, n='HAND_STRETCH_CDN'))
    cmds.connectAttr(disDim+'.distance', CDN+'.firstTerm')

JNTS=createJointIkInOrderOne()
LOCS=createLocatorsInOrder()

JNTS2=createJointIkInOrderOne()
LOCS2=createLocatorsInOrder()

ikfkStretch(JNTS,LOCS)
ikfkStretch(JNTS2,LOCS2)
