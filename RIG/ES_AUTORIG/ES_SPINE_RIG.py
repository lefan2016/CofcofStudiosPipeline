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

dir=r'P:/LOCAL/ES_SCRIPTS/RIG/ES_AUTORIG/'
fileui='autoRigUI.ui'
#utl.compilarPySideUI(dir,fire)
uiFile=dir+fileui

loader = QUiLoader()
loader.registerCustomWidget(autoRig)
aRig = loader.load(uiFile)
aRig.show()

class autoRig(object):

    def __init__(self):
        print('hola')

    def crearJointInSpace(self,n='',pos=[],r=1):#Made joints in space
        cmds.select(cl=1)
        self.jnt=cmds.joint(name=n+'_JNT',p=pos,radius=r)
        return self.jnt

    def grupoDe(self,objetos,name):#Made groups
        self.grp=cmds.group(objetos,n=name+'_GRP')
        return self.grp

    def NurbCreation(self,name,directionAxi=[0,0,1],splitU=1,splitV=5,width=5,lengthRatio=5):
        if not cmds.objExists(name+'_GRP'):
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
        else:
            cmds.warning('YA EXISTE '+ name +' CON ESE NOMBRE.')



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
aR.NurbCreation(variableNombre,
                        [0,1,0],
                        5,
                        1,
                        5,
                        0.2
                        )



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
