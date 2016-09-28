import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import sys
from PySide2 import QtCore, QtGui, QtUiTools

class RigSpine():
    '''
    #Funciones pensadas para creacion de una spina con nurbsPlane
    '''
    def __init__(self,name,directionAxi,splitU,splitV,width,lengthRatio,jntskin):
        self.name=name #Nombre de la espina y de su composicion ej:C_spine_spine_
        self.directionAxi=directionAxi #direccion del vector para crearlo ej:[0,1,0]
        self.splitU=splitU #Cantidad de subdiviciones en X del nurb
        self.splitV=splitV #Cantidad de subdiviciones en Y del nurb
        self.width=width #Ancho total del nurb
        self.lengthRatio=lengthRatio #Grosor del nurb
        self.jntToskin=jntskin#Cantidad de huesos que blendeas para skiniar

    def JointInSpace(self,n='',pos=[],suff='_JNT',r=1.5):#Made joints in space
        cmds.select(cl=1)#deselecciono
        self.jnt=cmds.joint(name=n+suff,p=pos,radius=r)
        return self.jnt

    def grupoDe(self,objs,name,suff='_GRP'):#Made groups
        self.grp=cmds.group(objs,n=name+suff)
        return self.grp

    def createCnt(self,objs=[],dir=[0,0,1],rad=14,nameSuf='ZTR',nameTrf='TRF',nameCNT='CNT'):
        #objs=cmds.ls(sl=1)
            grpYcnt=[]
            for obj in objs:
                print obj
                if '|' in obj:
                    obj=obj.split('|')[-1]
                if '_' in obj:
                    newName=obj.split(obj.split('_')[-1:][0])[0]
                else:
                    newName=obj
                #currentParent=cmds.listRelatives(obj,parent=1)
                ztr=cmds.group(em=True,n=str(newName+nameSuf))
                pcns=cmds.parentConstraint(obj,ztr)[0]
                scns=cmds.scaleConstraint(obj,ztr)[0]
                cmds.delete(pcns,scns)
                trf=cmds.duplicate(ztr,n=str(newName+nameTrf))[0]
                cmds.parent(trf,ztr)
                cnt=cmds.circle(radius=rad,nr=dir,name=str(newName+nameCNT))[0]
                pcns=cmds.parentConstraint(trf,cnt)
                scns=cmds.scaleConstraint(trf,cnt)
                cmds.delete(pcns,scns)
                cmds.parent(cnt,trf)
                pcns=cmds.parentConstraint(cnt,obj)
                scns=cmds.scaleConstraint(cnt,obj)
                grpYcnt.append(ztr)
            return grpYcnt

    def nurbCreation(self,name,directionAxi=[0,1,0],splitU=1,splitV=5,width=5,lengthRatio=5,jntskin=5):

        self.jntsRigSkin=[]
        self.grpCtroles=[]
        #Positions and direction joints
        if directionAxi==[0,0,1]:
            for j in range(jntskin+1):
                if not j == jntskin+1:
                    self.jntsRigSkin.append(self.JointInSpace(name+str(j),[jntskin-j,0,0])
            self.grpCtroles.append(self.createCnt(self.jntsRigSkin,[1,0,0],width)[0])#creo controles en los huesos del espacio con una direccion x
        elif directionAxi==[1,0,0]:
            for j in range(jntskin+1):
                if not j == jntskin+1:
                    self.jntsRigSkin.append(self.JointInSpace(name+str(j),[0,jntskin-j,0]))
            self.grpCtroles.append(self.createCnt(self.jntsRigSkin,[0,1,0],width)[0])#creo controles en los huesos del espacio con una direccion y
        elif directionAxi==[0,1,0]:
            for j in range(-jntskin,jntskin):
                if not j > 40:
                    self.jntsRigSkin.append(self.JointInSpace(name+str(j),[0,0,jntskin]))
            self.grpCtroles.append(self.createCnt(self.jntsRigSkin,[0,0,1],width)[0])#creo controles en los huesos del espacio con una direccion z

        #Create nurb with folicles
        self.nurb=cmds.nurbsPlane( ax=directionAxi,w=width, lr=lengthRatio,u=splitU,v=splitV,n=name+'_NSK')
        self.nurbName=cmds.rebuildSurface (self.nurb,rpo=1, rt=0, end=1,kr=0,kcp=0,kc=1,su=splitU,du=1,sv=splitV,dv=3,tol=0.01,fr=0,dir=2)#reconstruyo la build
        mel.eval('createHair '+str(splitU)+' '+str(splitV)+' 5 0 0 0 0 '+str(splitU)+' 0 2 2 1')
        cmds.delete('hairSystem1','hairSystem1OutputCurves','nucleus1')
        self.grpFoll=cmds.rename('hairSystem1Follicles',(name+'Follicles'+'_GRP'))
        self.follicles=cmds.listRelatives(self.grpFoll,children=1)
        self.jnts=[]
        for f in range(len(self.follicles)):
            self.foll=cmds.rename(self.follicles[f], name+'Flc'+str(f)+'_FLC')
            cmds.delete(cmds.listRelatives(self.foll,children=1)[1])
            self.jnt=cmds.joint(name=name+str(f)+'_JSK',absolute=1)
            self.jnts.append(self.jnt)
            cmds.connectAttr( self.foll+'.outTranslate', self.jnt+'.translate',f=1)
            cmds.connectAttr( self.foll+'.outRotate', self.jnt+'.rotate',f=1)
        cmds.parent(self.jnts[1:], w=1)

        #create skin
        self.scl=cmds.skinCluster(self.jntsRigSkin,self.nurbName[0],n=name+'_SCL')

        #Creation Groups
        self.gJoints=self.grupoDe(self.jnts,name+'_joints')
        self.gJntsRig=self.grupoDe(self.jntsRigSkin,name+'_jointsRig')
        self.follicles=cmds.listRelatives(self.grpFoll,children=1)
        self.gCnts=self.grupoDe(self.grpCtroles,name+'_CNTS')

        self.gJntsRig=self.grupoDe([self.grpFoll,self.gJoints,self.gJntsRig,self.gCnts,self.nurbName[0]])

        return self.nurbName[0],self.follicles,self.jnts,self.jntsRigSkin,self.scl,self.gCnts

    def createSpine(self):
        if not cmds.objExists(self.name+'_GRP'):

            self.nurbCreation(self.name,self.directionAxi,self.splitU,self.splitV,self.width,self.lengthRatio,self.jntToskin)
        else:
            cmds.warning('YA EXISTE '+ self.name +' CON ESE NOMBRE.')
            newName=cmds.promptDialog(title='DESEA PONER OTRO NOMBRE?',message='Enter name:',
                        button=['Y','N'],defaultButton='Y', cancelButton='N',dismissString='N')
            if newName == 'Y':
                self.nurbCreation(str(self.name+'_DUPLICATE'),self.directionAxi,self.splitU,self.splitV,self.width,self.lengthRatio,self.jntToskin)
            else:
                None

class winAR(RigSpine):
    def __init__():

        self.dir=r'P:/LOCAL/ES_SCRIPTS/RIG/ES_AUTORIG/'
        self.fileui='autoRigUI.ui'
        #utl.compilarPySideUI(dir,fire)
        self.uiFile=self.dir+self.fileui

        loader = QtUiTools.QUiLoader()
        loader.registerCustomWidget(RigSpine)
        rwin = loader.load(uiFile)
        rwin.show()
