import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import sys
path='..\UTILITYES'
if not path in sys.path:
    sys.path.append(path)
try:
    import UTILITYES
    reload(UTILITYES)
except ImportError:
    print 'porfavor fijate si tenes el modulo de utilidades'
def crearJointInSpace(n='',pos=[],r=1):#Made joints in space
    cmds.select(cl=1)
    jnt=cmds.joint(name=n+'_JNT',p=pos,radius=r)
    return jnt

def grupoDe(objetos,name):#Made groups
    grp=cmds.group(objetos,n=name+'_GRP')
    return grp

def NurbCreation(name,directionAxi=[0,0,1],splitU=1,splitV=5,width=5,lengthRatio=5):
    #Positions and direction joints
    if directionAxi==[0,0,1]:
        posJntT=[0,width/2,0]
        posJntM=[0,splitU/3,0]
        posJntB=[0,-width/2,0]
        dire=0

    elif directionAxi==[0,1,0]:
        posJntT=[width/2,0,0]
        posJntM=[splitV/3,0,0]
        posJntB=[-width/2,0,0]
        dire=1

    elif directionAxi==[1,0,0]:
        posJntT=[0,0,width/2]
        posJntM=[0,0,splitV/3]
        posJntB=[0,0,-width/2]
        dire=1
    #Create nurb with folicles
    nurb=cmds.nurbsPlane( ax=directionAxi,w=width, lr=lengthRatio,u=splitU,v=splitV,n=name+'_NSK' )
    nurbName=cmds.rebuildSurface (nurb,rpo=1, rt=0, end=1,kr=0,kcp=0,kc=1,su=splitU,du=1,sv=splitV,dv=3,tol=0.01,fr=0,dir=dire)#reconstruyo la build
    mel.eval('createHair '+str(splitU)+' '+str(splitV)+' 5 0 0 0 0 '+str(splitU)+' 0 2 2 1')
    cmds.delete('hairSystem1','hairSystem1OutputCurves','nucleus1')
    grpFoll=cmds.rename('hairSystem1Follicles',(name+'Follicles'+'_GRP'))
    follicles=cmds.listRelatives(grpFoll,children=1)
    jnts=[]
    jntsRig=[]
    for f in range(len(follicles)):
        foll=cmds.rename(follicles[f], name+'Flc'+str(f)+'_FLC')
        cmds.delete(cmds.listRelatives(foll,children=1)[1])
        jnt=cmds.joint(name=name+str(f)+'_JSK')
        jnts.append(jnt)
        cmds.connectAttr( foll+'.outTranslate', jnt+'.translate',f=1)
        cmds.connectAttr( foll+'.outRotate', jnt+'.rotate',f=1)
    cmds.parent(jnts[1:], w=1)

    #creation joint
    jntsRig.append(crearJointInSpace(name+'Top',posJntT,2))
    jntsRig.append(crearJointInSpace(name+'Mid',posJntM,2))
    jntsRig.append(crearJointInSpace(name+'Btm',posJntB,2))
    #create skin
    scl=cmds.skinCluster(jntsRig[0],jntsRig[1],jntsRig[2],nurbName[0],n=name+'_SCL')
    #Creation Groups
    gJoints=grupoDe(jnts,side+prefix+'_joints')
    gJntsRig=grupoDe(jntsRig,side+prefix+'_jointsRig')
    follicles=cmds.listRelatives(grpFoll,children=1)
    gJntsRig=grupoDe([grpFoll,gJoints,gJntsRig,nurbName[0]],name)

    return nurbName[0],follicles,jnts,jntsRig,scl



#PROPERTIES SPINE
side='C'#Letra de ubicacion en el espacio
prefix='_'+'spine'#Nombre del objeto
name='_'+'spine'#nombre de la parte

#Vertical
#splitU Numero en X
#splitV Numero en Y
#axis [1,0,0],[0,1,0],[0,0,1] Direccion en el espacio 
#Ratio del nurb

#Creo Rig spina vertical
rigNurb=NurbCreation(side+prefix+name,
                        directionAxi=[0,1,0],
                        splitU=5,
                        splitV=1,
                        width=5,
                        lengthRatio=0.2
                        )
