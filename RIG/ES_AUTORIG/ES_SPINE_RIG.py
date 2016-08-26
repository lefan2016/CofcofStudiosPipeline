import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import sys
from PySide import QtCore, QtGui, QtUiTools
path='P:/LOCAL/PH_SCRIPTS/_SCRIPTS'
if not path in sys.path:
    sys.path.append(path)
try:
    import UTILITIES as utl
    reload(utl)
except ImportError:
    print 'porfavor fijate si tenes el modulo de utilidades'


class RigSpine():

    def __init__(self,name,directionAxi,splitU,splitV,width,lengthRatio):
        self.name=name
        self.directionAxi=directionAxi
        self.splitU=splitU
        self.splitV=splitV
        self.width=width
        self.lengthRatio=lengthRatio

    def JointInSpace(self,n='',pos=[],r=1):#Made joints in space
        cmds.select(cl=1)
        self.jnt=cmds.joint(name=n+'_JNT',p=pos,radius=r)
        return self.jnt

    def grupoDe(self,objs,name):#Made groups
        self.grp=cmds.group(objs,n=name+'_GRP')
        return self.grp

    def NurbCreation(self,name,directionAxi=[0,0,1],splitU=1,splitV=5,width=5,lengthRatio=5):
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
        self.nurb=cmds.nurbsPlane( ax=directionAxi,w=width, lr=lengthRatio,u=splitU,v=splitV,n=name+'_NSK' )
        self.nurbName=cmds.rebuildSurface (self.nurb,rpo=1, rt=0, end=1,kr=0,kcp=0,kc=1,su=splitU,du=1,sv=splitV,dv=3,tol=0.01,fr=0,dir=dire)#reconstruyo la build
        mel.eval('createHair '+str(splitU)+' '+str(splitV)+' 5 0 0 0 0 '+str(splitU)+' 0 2 2 1')
        cmds.delete('hairSystem1','hairSystem1OutputCurves','nucleus1')
        self.grpFoll=cmds.rename('hairSystem1Follicles',(name+'Follicles'+'_GRP'))
        self.follicles=cmds.listRelatives(self.grpFoll,children=1)
        self.jnts=[]
        self.jntsRig=[]
        for f in range(len(self.follicles)):
            self.foll=cmds.rename(self.follicles[f], name+'Flc'+str(f)+'_FLC')
            cmds.delete(cmds.listRelatives(self.foll,children=1)[1])
            self.jnt=cmds.joint(name=name+str(f)+'_JSK',absolute=1)
            self.jnts.append(self.jnt)
            cmds.connectAttr( self.foll+'.outTranslate', self.jnt+'.translate',f=1)
            cmds.connectAttr( self.foll+'.outRotate', self.jnt+'.rotate',f=1)
        cmds.parent(self.jnts[1:], w=1)
        #creation joint
        self.jntsRig.append(self.JointInSpace(name+'Top',posJntT,2))
        self.jntsRig.append(self.JointInSpace(name+'Mid',posJntM,2))
        self.jntsRig.append(self.JointInSpace(name+'Btm',posJntB,2))
        #create skin
        self.scl=cmds.skinCluster(self.jntsRig[0],self.jntsRig[1],self.jntsRig[2],self.nurbName[0],n=name+'_SCL')
        #Creation Groups
        self.gJoints=self.grupoDe(self.jnts,name+'_joints')
        self.gJntsRig=self.grupoDe(self.jntsRig,name+'_jointsRig')
        self.follicles=cmds.listRelatives(self.grpFoll,children=1)
        self.gJntsRig=self.grupoDe([self.grpFoll,self.gJoints,self.gJntsRig,self.nurbName[0]],name)

        return self.nurbName[0],self.follicles,self.jnts,self.jntsRig,self.scl

        def createSpine(self):
            if not cmds.objExists(name+'_GRP'):
                
        else:
            cmds.warning('YA EXISTE '+ name +' CON ESE NOMBRE.')
            newName=cmds.raw_input('Quiere agregar otro nombre?')
            if newName:
                NurbCreation(name,)


class winAR(autoRig):
    def __init__():

        self.dir=r'P:/LOCAL/ES_SCRIPTS/RIG/ES_AUTORIG/'
        self.fileui='autoRigUI.ui'
        #utl.compilarPySideUI(dir,fire)
        self.uiFile=self.dir+self.fileui

        loader = QtUiTools.QUiLoader()
        loader.registerCustomWidget(autoRig)
        rwin = loader.load(uiFile)
        rwin.show()


#PROPERTIES SPINE
side='C'#Letra de ubicacion en el espacio
prefix='_'+'spine'#Nombre del objeto
name='_'+'spine'#nombre de la parte
variableNombre=side+prefix+name
#Vertical
#splitU Numero en X
#splitV Numero en Y
#axis [1,0,0],[0,1,0],[0,0,1] Direccion en el espacio
#Ratio del nurb
aR=autoRig()
w=winAR
aR.NurbCreation(variableNombre,[0,1,0],5,1,5,.2)

'''
class createMyLayoutCls(object):
    def show(self):
        self.createMyLayout()
    def createMyLayout(self):
        #check to see if our window exists
        if cmds.window('utility', exists = True):
            cmds.deleteUI('utility')
        # create our window
        self.window = cmds.window('utility', widthHeight = (200, 200), title = 'Distribute', resizeToFitChildren=1, sizeable = False)
        cmds.setParent(menu=True)
        # create a main layout
        mainLayout = cmds.columnLayout(w = 200, h = 200, cw = 15, rs = 12, co = ['both',5])
        # X Control
        self.xAxis = cmds.checkBox('X')
        # Distribute Button
        btnDistribute = cmds.button(label = 'Distribute', width = 180, height = 40, c = self.GetSelectedNodes)
        # show window
        cmds.showWindow(self.window)

    def GetSelectedNodes(self,*args):
        cal = cmds.checkBox(self.xAxis,q = True, v = True)
        print cal

b_cls = createMyLayoutCls()
b_cls.show()


win=' AUTORIG - ESPIRAL STUDIOS v(0.1)'
if cmds.window(win,q=1,ex=1):
    cmds.deleteUI(win)
cmds.window(w, title=w,widthHeight=(350, 150))
cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 250), (2, 100), (3, 100)] )
cmds.frameLayout( label='Spine',ann='Agrega la cantidad de huesos necesarios.')
cmds.separator( style='none' )
cmds.intSliderGrp(columnAttach=[2, 'left', 3],cl3=['right','left','left'], field=True, label='Joints', minValue=3, maxValue=50, fieldMinValue=-100, fieldMaxValue=100, value=3 )
cmds.showWindow()

'''
