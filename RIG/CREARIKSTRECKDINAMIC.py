import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
'''
USO: Selecciona o especifica el ultimo tramo de la cadena de huesos.
VERSION: maya 2017
EXAMPLE:
import maya.cmds as cmds
import sys
path=r'P:\LOCAL\ES_SCRIPTS\RIG'
if not path in sys.path:
	sys.path.append(path)
try:
    import CREARIKSTRECKDINAMIC as spl
    reload (spl)
except (RuntimeError, TypeError, NameError,IOError):
    print 'NO SE PUDO IMPORTAR EL MODULO'
a=[]
a=spl.crearIkStreckDinamic(nameRig='L_CABLE_RIG1')

'''

def Aliniar(object=None,offsetGrp=None):
    # match object transform
    if cmds.nodeType(object)=='transform':
        if cmds.nodeType(offsetGrp)=='transform':
            cmds.delete( cmds.parentConstraint( object, offsetGrp ) )
            cmds.delete( cmds.scaleConstraint( object, offsetGrp ) )
        else:
            cmds.warning('Falta el target.')
    else:
        cmds.warning('No hay que alinear.')

def controlSphera(name='_CNT',scale=1,toObj=None):
    ctrlObject = cmds.circle( n = name, ch = False, normal = [1, 0, 0], radius = scale )
    addShape = cmds.circle( n =name, ch = False, normal = [0, 0, 1], radius = scale )[0]
    addShape2 = cmds.circle( n =name, ch = False, normal = [0, 1, 0], radius = scale )[0]
    cmds.parent( cmds.listRelatives( addShape, s = 1 ), ctrlObject[0], r = 1, s = 1 )
    cmds.parent( cmds.listRelatives( addShape2, s = 1 ), ctrlObject[0], r = 1, s = 1 )
    cmds.delete( addShape,addShape2 )
    if toObj:
        Aliniar(ctrlObject,toObj)
    return ctrlObject
def makeOffsetGrp( object, prefix = '' ,control=False,radio=1):

    try:
        objectParents = cmds.listRelatives( object, p = 1 )
    except:
        objectParents=None
    offsetGrp = cmds.group( n = prefix + '_TRF', em = 1 )
    if objectParents!=None:
        Aliniar(object,offsetGrp)
        cmds.parent( offsetGrp, objectParents[0] )
    if control:
        cnt=controlSphera(prefix+'_CNT',radio)
        #cnt=cmds.circle(n=prefix+'_CNT',normal=[1,0,0],r=radio)
        Aliniar(object,offsetGrp)
        Aliniar(object,cnt)
        # parent object under offset cnt
        cmds.parent(object,object)
        cmds.parent(cnt, offsetGrp )
    else:
        #Alinia al objeto
        Aliniar(object,offsetGrp)
        # parent object under offset group
        cmds.parent( object, offsetGrp )
    return offsetGrp

def crearIkStreckDinamic(jntEnd=None,nameRig=None ):
    if jntEnd == None:
        #Busco las conexiones de joints
        try:
            jntEnd=cmds.ls(sl=1,type='joint')[0]
            joints=cmds.listRelatives(jntEnd,ap=True,type='joint',f=True)[0].split('|')
            cant=len(joints)
            jntStart=joints[1]
        except:
            cmds.warning('Selecciona el ultimo joint de una cadena')
    if jntEnd:
        if nameRig==None:
            nameRig='L_BODYPART_WIRE1'
        #Enlista los joints y busca el rootJoint
        joints=cmds.listRelatives(jntEnd,ap=True,type='joint',f=True)[0].split('|')
        jointList = [p for p in joints if p and cmds.nodeType(p) == 'joint']
        rootJoint = jointList[0] if jointList else None
        #Creacion de Ik Handle
        ikh=cmds.ikHandle( sj=jntStart, ee=jntEnd,sol='ikSplineSolver',roc=False, p=2, pcv=False,ns=3,n=nameRig+'_IKH')
        crv=cmds.rename(ikh[2],nameRig+'_CRV')
        #seteo en inherits la curva asi puedo mirroriar
        cmds.setAttr(crv+'.inheritsTransform',False)
        #Creacion de los cluster y sus controles
        c1=cmds.cluster(crv+'.cv[4:5]')#top cluster
        c2=cmds.cluster(crv+'.cv[2:3]')#mid cluster
        c3=cmds.cluster(crv+'.cv[0:1]')#btn cluster
        #Creo offsets
        cg1=makeOffsetGrp(c1[1],nameRig+'top',True)
        cg2=makeOffsetGrp(c2[1],nameRig+'mid',True)
        cg3=makeOffsetGrp(c3[1],nameRig+'btn',True)
        #rename cluster
        cn1=cmds.rename(c1[1],nameRig+'top_CLR')
        cn2=cmds.rename(c2[1],nameRig+'mid_CLR')
        cn3=cmds.rename(c3[1],nameRig+'btn_CLR')
        #cmds.parentConstraint(c3,joints[0],mo=True)#parent primer joint
        #Creamos nodos para el streching
        CVI=cmds.createNode('curveInfo',n=nameRig+'_CVI')
        NMD=cmds.createNode('multiplyDivide',n=nameRig+'_NMD')
        NCD=cmds.createNode('condition',n=nameRig+'_NCD')
        #Conectamos la informacion del largo de la curva
        crvShape=cmds.listRelatives(crv)[0]
        cmds.connectAttr(crvShape+'.worldSpace[0]',CVI+'.inputCurve',f=True)
        cmds.connectAttr(CVI+'.arcLength',NMD+'.input1.input1X',f=True)
        cmds.connectAttr(CVI+'.arcLength',NCD+'.firstTerm',f=True)
        cmds.connectAttr(NMD+'.output.outputX',NCD+'.colorIfTrue.colorIfTrueR',f=True)
        #Configuaramos los nodos
        distInicial=cmds.getAttr(CVI+'.arcLength')
        cmds.setAttr(NMD+'.input2X',distInicial)
        cmds.setAttr(NMD+'.operation',2)
        cmds.setAttr(NCD+'.operation',2)
        #Conectamos a todos los joints a la salida en escala de X y duplicamos la cadena para bake
        extrajntList=[]
        for j in jointList:
            cmds.connectAttr(NCD+'.outColor.outColorR',j+'.scale.scaleX.',f=True)
            #Duplicado
            matrix=cmds.xform(j,q=1,ws=1,m=1)
            jntExtra=cmds.joint(name=str(j)+'_JSK')
            extrajntList.append(jntExtra)
            cmds.xform(jntExtra,m=matrix)
            cmds.parentConstraint(j,jntExtra)
            cmds.scaleConstraint(j,jntExtra)

        #Ordenamos todo en grupos
        g1=cmds.group([cg1,cg2,cg3],n=nameRig+'CONTROLS_GRP')
        g2=cmds.group([jntStart,ikh[0],crv],n=nameRig+'RIG_GRP')
        g3=cmds.group(extrajntList,n=nameRig+'JOINTSKIN_GRP')
        grp=cmds.group(empty=True,n=nameRig+'_GRP')
        cmds.parent([g1,g2,g3],grp)
        #Escondo los grupos
        off=[g3,g2,cn1,cn2,cn3]
        for g in off:
            cmds.setAttr(str(g)+'.v',False)

    return [c1,c2,c3,jointList,jntExtra]

#mel.eval('makeCurvesDynamicHairs %d %d %d' % (attach, snap, match))
