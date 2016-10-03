import maya.cmds as cmds
import maya.mel as mel
from PySide2 import QtCore, QtGui, QtUiTools
'''
ejecucion:
import maya.cmds as cmds
import sys
path=r'\\NAS-ESPIRAL\Volume_1\PIPELINE\LOCAL\ES_SCRIPTS'
if not path in sys.path:
	sys.path.append(path)
import ES_SPINE_RIG
reload (ES_SPINE_RIG)

ar=RigSpine('L_SNAIL_EYE',#Nombre
            [0,1,0],#Direccion de nurb
            1,#subdiviciones de nurb en X
            6,#subdiviciones de nurb en Y
            6,#ancho de la nurb
            2,#Tamaño de nurb
            1)#Cantidad de joint y controles
a=ar.createSpine()#Crea La nurb seteada
'''
class RigSpine():#Creacion de una spina con nurbsPlane

    def __init__(self,name,directionAxi,splitU,splitV,width,lengthRatio,jnts):
        self.name=name #Nombre de la espina y de su composicion ej:C_spine_spine_
        self.directionAxi=directionAxi #direccion del vector para crearlo ej:[0,1,0]
        self.splitU=splitU #Cantidad de subdiviciones en X del nurb
        self.splitV=splitV #Cantidad de subdiviciones en Y del nurb
        self.width=width #Ancho total del nurb
        self.lengthRatio=lengthRatio #Grosor del nurb
        self.jnts=jnts#Cantidad de huesos que blendeas para skiniar

    def JointInSpace(self,n='',pos=[],r=1.5,suff='_JNT'):#Made joints in space
        cmds.select(cl=1)#deselecciono
        self.jnt=cmds.joint(name=n+suff,p=pos,radius=r)
        return self.jnt

    def grupoDe(self,objs,name,suff='_GRP'):#Made groups
        self.grp=cmds.group(objs,n=str(name)+suff)
        return self.grp

    def createCnt(self,objs=[],dir=[0,0,1],rad=14,nameSuf='ZTR',nameTrf='TRF',nameCNT='CNT'):
        #objs=cmds.ls(sl=1)
            grpYcnt=[]
            for obj in objs:
                if '|' in obj:
                    obj=obj.split('|')[-1]
                if '_' in obj:
                    newName=obj.split(obj.split('_')[-1:][0])[0]
                else:
                     newName=obj
                #currentParent=cmds.listRelatives(obj,parent=1)
                ztr=cmds.group(em=True,n=str(newName+nameSuf))
                matrix=cmds.xform(obj,q=1,matrix=1)
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
                pcns=cmds.parentConstraint(cnt,obj,n=newName+'PCNS')
                scns=cmds.scaleConstraint(cnt,obj,n=newName+'SCNS')
                cmds.xform(ztr,matrix=matrix)
                grpYcnt.append(ztr)
            return grpYcnt

    def nurbCreation(self,name,directionAxi=[0,1,0],splitU=1,splitV=5,width=5,lengthRatio=5,jnts=5):
        self.jnts=[]
        self.grpCtroles=[]
        #Positions and direction joints
        if directionAxi==[0,0,1]:
            print ('Aun no se desarrollo esta direccion de la nurbs, comuniquese con el desarrollador. Gracias.')#creo controles en los huesos del espacio con una direccion x
        elif directionAxi==[1,0,0]:
            print ('Aun no se desarrollo esta direccion de la nurbs, comuniquese con el desarrollador. Gracias.')#creo controles en los huesos del espacio con una direccion x
        elif directionAxi==[0,1,0]:
            for j in range(-jnts,jnts+1):
                if j == 0:
                    self.jnts.append(self.JointInSpace(name+'C'+str(j),[0,0,j],width/2))
                if j < 0:
                    self.jnts.append(self.JointInSpace(name+'T'+str(j),[0,0,j],width/2))
                if j > 0:
                    self.jnts.append(self.JointInSpace(name+'B'+str(j),[0,0,j],width/2))
        self.grpCtroles.append(self.createCnt(self.jnts,[0,0,1],width))#creo controles en los huesos del espacio con una direccion z

        #Create nurb with folicles
        self.nurb=cmds.nurbsPlane( ax=directionAxi,w=width, lr=lengthRatio,u=splitU,v=splitV,n=name+'_NSK')
        self.nurbName=cmds.rebuildSurface (self.nurb,rpo=1, rt=0, end=1,kr=0,kcp=0,kc=1,su=splitU,du=1,sv=splitV,dv=3,tol=0.01,fr=0,dir=2)#reconstruyo la build
        mel.eval('createHair '+str(splitU)+' '+str(splitV)+' 5 0 0 0 0 '+str(splitU)+' 0 2 2 1')
        cmds.delete('hairSystem1','hairSystem1OutputCurves','nucleus1')
        self.grpFoll=cmds.rename('hairSystem1Follicles',(name+'_Follicles'+'_GRP'))
        self.follicles=cmds.listRelatives(self.grpFoll,children=1)
        self.jntsToSkin=[]
        for f in range(len(self.follicles)):
            self.foll=cmds.rename(self.follicles[f], name+str(f)+'_FLC')
            cmds.delete(cmds.listRelatives(self.foll,children=1)[1])
            self.jnt=cmds.joint(name=name+str(f)+'_JSK',absolute=1,radius=width/2,rotationOrder='xyz')
            self.jntsToSkin.append(self.jnt)
            cmds.connectAttr( self.foll+'.outTranslate', self.jnt+'.translate',f=1)
            cmds.connectAttr( self.foll+'.outRotate', self.jnt+'.rotate',f=1)
        cmds.parent(self.jntsToSkin[1:], w=1)
        for j in jntsToSkin:#Fix bones rotation axis
            cmds.setAttr(j+'.jointOrientX',0)
            cmds.setAttr(j+'.jointOrientY',0)
            cmds.setAttr(j+'.jointOrientZ',0)

        #create skin #Prune weights #Remove unused influences
        self.scl=cmds.skinCluster(self.jnts,self.nurbName[0],n=name+'_SCL',mi=3,dr=14.0)[0]
        cmds.select(self.nurbName[0])
        mel.eval('doPruneSkinClusterWeightsArgList 1 { "'+str(0.2)+'" }')
        mel.eval('removeUnusedInfluences')
        cmds.select(cl=1)

        try:
            #Creation Groups
            self.gJoints=self.grupoDe(self.jntsToSkin,name+'_jointsToSkin')
            self.gJntsRig=self.grupoDe(self.jnts,name+'_joint')
            self.follicles=cmds.listRelatives(self.grpFoll,children=1)
            self.gCnts=self.grupoDe(self.grpCtroles[0], name+'_controls')
            self.gNurb=self.grupoDe(self.nurbName, name+'_Nurbs')
            self.gJntsRig=self.grupoDe([self.grpFoll,self.gJoints,self.gJntsRig,self.gCnts,self.gNurb],name)
        except:
            cmds.delete(self.jntsToSkin)

        return self.nurbName[0],self.follicles,self.jntsToSkin,self.jnts,self.scl,self.gCnts

    def createSpine(self):
        if not cmds.objExists(self.name+'_GRP'):

            self.nurbCreation(self.name,self.directionAxi,self.splitU,self.splitV,self.width,self.lengthRatio,self.jnts)
        else:
            cmds.warning('YA EXISTE '+ self.name +' CON ESE NOMBRE.')
            self.result =cmds.promptDialog(title='DESEA PONER OTRO NOMBRE?',message='Enter name:',
                        button=['Y','N'],defaultButton='Y', cancelButton='N',dismissString='N')
            if self.result  == 'Y':
                self.newName=cmds.promptDialog(query=True, text=True)
                self.nurbCreation(str(self.newName),self.directionAxi,self.splitU,self.splitV,self.width,self.lengthRatio,self.jnts)
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
