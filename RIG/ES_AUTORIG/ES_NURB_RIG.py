# -*- encoding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
from PySide2 import QtCore, QtGui, QtUiTools
'''
import maya.cmds as cmds
import sys
path=r'P:\LOCAL\ES_SCRIPTS\RIG\ES_AUTORIG'
if not path in sys.path:
	sys.path.append(path)
try:
    import ES_NURB_RIG as AutoRig
    reload (ES_NURB_RIG)
except (RuntimeError, TypeError, NameError,IOError):
    print 'NO SE PUDO IMPORTAR EL MODULO'

ar=AutoRig.RigSpine('L_SNAIL_TENTACLE',#Nombre
            [0,1,0],#Direccion de nurb
            1,#subdiviciones de nurb en X
            20,#subdiviciones de nurb en Y
            0.5,#ancho de la nurb
            0.1,#Tamaño de nurb
            5)#Cantidad de joint y controles
a=ar.createSpine()#Crea La nurb seteada
ar.createDeformer('wave')#Crea deformadores y lo aplica en blendshape
'''
class RigSpine():#Creacion de una spina con nurbsPlane

    def __init__(self,name,directionAxi,splitU,splitV,width,lengthRatio,joint):
        self.name=name #Nombre de la espina y de su composicion ej:C_spine_spine_
        self.directionAxi=directionAxi #direccion del vector para crearlo ej:[0,1,0]
        self.splitU=splitU #Cantidad de subdiviciones en X del nurb
        self.splitV=splitV #Cantidad de subdiviciones en Y del nurb
        self.width=width #Ancho total del nurb
        self.lengthRatio=lengthRatio #Grosor del nurb
        self.joint=joint#Cantidad de huesos que blendeas para skiniar

    def JointInSpace(self,n='',pos=[],r=1.5,suff='_JNT'):#Made joints in space
        cmds.select(cl=1)#deselecciono
        self.jnt=cmds.joint(name=n+suff,p=pos,radius=r)
        return self.jnt

    def grupoDe(self,objs,name,inherits=True,shape=False,suff='_GRP',vis=True):#Made groups
        if not shape:
            self.grp=cmds.group(objs,n=str(name)+str(suff))
            cmds.setAttr(str(self.grp)+'.inheritsTransform', inherits)
        else:
            self.sp=cmds.circle(radius=2.0,nr=[0,0,1],n=str(name)+str('_CNT'))
            self.grp=cmds.group(self.sp,n=str(name)+str(suff))
            cmds.rename(cmds.listRelatives(self.sp,shapes=True),str(name)+str('_CNTSH'))
            cmds.parent(objs,self.sp)
            cmds.setAttr(str(self.grp)+'.inheritsTransform', inherits)
        if not vis:
            cmds.setAttr( str(self.grp) + '.visibility', False )
        return self.grp

    def createCnt( self, objs=[] ,dir=[0,0,1] ,rad=14 ,squad=False ,nameSuf='ZTR' ,nameTrf='TRF' ,nameCNT='CNT' ):
        #objs=cmds.ls(sl=1)
        grpYcnt=[]
        for obj in objs:
            if '|' in obj:
                obj=obj.split('|')[-1]
            if '_' in obj:
                newName=obj.split(obj.split('_')[-1:][0])[0]
            else:
                 newName=obj
            ztr=cmds.group(em=True,n=str(newName+nameSuf))
            matrix=cmds.xform(obj,q=1,matrix=1)
            if squad:
                diametro=rad
                trf=cmds.curve(n=str(newName+nameTrf),d=1,objectSpace=True,p=[(diametro,diametro,0),(-diametro,diametro,0),(-diametro,-diametro,0),(diametro,-diametro,0),(diametro,diametro,0)])
            else:
                trf=cmds.duplicate(ztr,n=str(newName+nameTrf))[0]
            cnt=cmds.circle(radius=rad/2.0,nr=dir,name=str(newName+nameCNT))[0]
            cmds.parent(cnt,trf)
            cmds.parent(trf,ztr)
            cmds.xform(ztr,matrix=matrix)
            pcns=cmds.parentConstraint(cnt,obj,n=newName+'PCNS')[0]
            scns=cmds.scaleConstraint(cnt,obj,n=newName+'SCNS')[0]
            grpYcnt.append(ztr)
        return grpYcnt

    def existNode(self,obj,type='skinCluster'):
        for x in cmds.listRelatives(obj):
            x=cmds.listConnections(x,t=type)
            if cmds.nodeType(x)=='skinCluster':
                return True
            else:
                return False

    def createAttr(self, objs=[], Attrs=[],niceName='',min=0, max=1.0, defa=0,ocultar=False,**kwargs ):
        for obj in [objs]:
            for nV in [Attrs]:
                if not cmds.attributeQuery( nV, n=obj ,exists=True ):
                    cmds.addAttr( obj, ln=str( nV ),nn=niceName, dv=defa, minValue=min, maxValue=max, k=1,**kwargs )
                if ocultar:
                    cmds.setAttr(obj+'.'+nV, lock=True)

    def createCopyAndBlendShape(self, obj, descrip= '_FORDEFORMER', suf= '_NBS' ):#crea el duplicado y luego lo adiere al original mediante un blendshape
        if not cmds.objExists( str(obj) + descrip ):
            if self.existNode(obj,'skinCluster'):#Solo si tiene un skin hace el bindPose
                #Coloco el objeto a copiar en el origen
                bindPose = cmds.dagPose( str(obj), q= True, bindPose= True )[0]
                cmds.dagPose( bindPose, restore= True )
            #Duplica el objeto para trabajarlo
            copy = cmds.duplicate( obj, n= obj + descrip )[0]
            nbs=str(obj)+suf
            #Crea blendshape si no existe lo agrega
            if cmds.objExists( str(obj) + suf ):
                try:
                    waithBsh=cmds.blendShape( obj + suf, q=True, wc=True)
                    nbs = cmds.blendShape (obj+suf, edit=True, target=[ obj, waithBsh+1, str(copy), 1.0 ])[0]
                except:
                    pass
            else:
                nbs = cmds.blendShape( [ copy, obj ], n=obj + suf )[0]
            return copy,nbs
        else:
            cmds.warning( 'Ya existe el deformador ' + obj + descrip )

    def createDeformsBlendShape(self,obj=None, control=None, tipoDeform='wave'):
        #objeto que duplicara para el deformador nuevo y el control donde iran los paramatro luego el nombre del deformador.
        if tipoDeform=='wave':
            descripcion='_FORWAVE'
            if not cmds.objExists(obj+'_FORWAVE'):
                #Crea blendshape si no existe lo agrega
                copy,nbs=self.createCopyAndBlendShape(obj,descripcion)
                #Creo el deformador con las siguientes propiedades
                deform = None
                dist=100.0
                deform = mel.eval("nonLinear -type wave -minRadius 0 -maxRadius "+ str(dist) +" -amplitude 0.5 -wavelength 1.0 -dropoff 0 -offset 0 "+ str(cmds.listRelatives(copy)[0]) +";")
                nnl = cmds.rename(deform[1],copy+'_NLW')
                ndf = cmds.rename(deform[0],copy+'_NWV')
                cmds.setAttr(str(nnl)+'.tz',-dist)
                cmds.setAttr(str(nnl)+'.visibility',False)
                #Creo los atributos en el control deseado
                if control!=None:
                    nVale=['waveOnOff','offset','amplitude','wavelength']
                    self.createAttr( control, tipoDeform ,'---------------',ocultar=True,at="enum",en=tipoDeform.upper())
                    self.createAttr( control, nVale[0] ,'<-waveOnOff',0 ,1.0 ,0)
                    self.createAttr( control, nVale[1] ,'<-offset',0 ,50.0 ,50.0 )
                    self.createAttr( control, nVale[2] ,'<-amplitude',0 ,100, 0.5 )
                    self.createAttr( control, nVale[3] ,'<-wavelength',0.1 ,10.0 ,1.4 )
                    #Conecto los atributos con el deformador
                    try:
                        cmds.connectAttr(control+'.'+nVale[0], nbs+'.'+copy,f=True)
                        cmds.expression(o=control,s=str(ndf)+"."+nVale[1]+"=time/"+str(control)+"."+ nVale[1] +";", n=obj+descripcion+'_EXP')
                        cmds.expression(o=control,s=str(ndf)+"."+nVale[2]+"="+str(control)+"."+ nVale[2] +";", n=obj+descripcion+'_EXP')
                        cmds.expression(o=control,s=str(ndf)+"."+nVale[3]+"="+str(control)+"."+ nVale[3] +";", n=obj+descripcion+'_EXP')
                    except RuntimeError:
                        pass
                return copy,nnl,ndf,nbs
            else:
                print 'FALTA ESPECIFICAR EL CONTROL DONDE IRAN SUS ATRIBUTOS'

        if tipoDeform=='squash':
            descripcion='_FORSQUASH'
            if not cmds.objExists(obj+'_FORSQUASH'):
                #Crea blendshape si no existe lo agrega
                copy,nbs=self.createCopyAndBlendShape(obj,descripcion)
                #Creo el deformador con las siguientes propiedades
                deform = None
                deform = mel.eval("nonLinear -type squash  -lowBound -1 -highBound 1 -startSmoothness 0 -endSmoothness 0 -maxExpandPos 0.5 -expand 1 -factor 0 "+ str(cmds.listRelatives(copy)[0]) +";")
                nnl = cmds.rename(deform[1],copy+'_NLW')
                ndf = cmds.rename(deform[0],copy+'_NWV')
                cmds.setAttr(str(nnl)+'.rx',-90)
                cmds.setAttr(str(nnl)+'.visibility',False)
                #Creo los atributos en el control deseado
                if control!=None:
                    nVale=['squashOnOff','factor','expand','maxExpandPos','startSmoothness','endSmoothness','lowBound','highBound']
                    self.createAttr( control, tipoDeform ,'---------------',ocultar=True,at="enum",en=tipoDeform.upper())
                    self.createAttr( control, nVale[0] ,'<-squashOnOff',0 ,1,0 )
                    self.createAttr( control, nVale[1] ,'<-factor',-10.0 ,10.0 ,0 )
                    self.createAttr( control, nVale[2] ,'<-expand',0 ,10 ,1 )
                    self.createAttr( control, nVale[3] ,'<-maxExpandPos',0.01 ,0.99, 0.01 )
                    self.createAttr( control, nVale[4] ,'<-startSmoothness',0 ,1 ,0 )
                    self.createAttr( control, nVale[5] ,'<-endSmoothness',0 ,1 ,1 )
                    self.createAttr( control, nVale[6]+tipoDeform ,'<-lowBound',-10 ,0 ,-2.5)
                    self.createAttr( control, nVale[7]+tipoDeform ,'<-highBound',0 ,10 ,0 )
                    #Conecto los atributos con el deformador
                    try:
                        cmds.connectAttr(control+'.'+nVale[0], nbs+'.'+copy,f=True)
                        cmds.expression(o=control,s=str(ndf) +"."+ nVale[1] +"="+str(control)+"."+ nVale[0] +";", n=obj+descripcion+'_EXP')
                        cmds.expression(o=control,s=str(ndf) +"."+ nVale[2] +"="+str(control)+"."+ nVale[1] +";", n=obj+descripcion+'_EXP')
                        cmds.expression(o=control,s=str(ndf) +"."+ nVale[3] +"="+str(control)+"."+ nVale[2] +";", n=obj+descripcion+'_EXP')
                        cmds.expression(o=control,s=str(ndf) +"."+ nVale[4] +"="+str(control)+"."+ nVale[3] +";", n=obj+descripcion+'_EXP')
                        cmds.expression(o=control,s=str(ndf) +"."+ nVale[5] +"="+str(control)+"."+ nVale[4] +";", n=obj+descripcion+'_EXP')
                        cmds.connectAttr(control+'.'+nVale[6]+tipoDeform, nbs+'.'+Vale[6],f=True)
                        cmds.connectAttr(control+'.'+nVale[7]+tipoDeform, nbs+'.'+nVale[7],f=True)
                    except RuntimeError:
                        pass
                return copy,nnl,ndf,nbs
            else:
                print 'FALTA ESPECIFICAR EL CONTROL DONDE IRAN SUS ATRIBUTOS'

        if tipoDeform=='bend':
            descripcion='_FORBEND'
            if not cmds.objExists(obj+'_FORBEND'):
                #Crea blendshape si no existe lo agrega
                copy,nbs=self.createCopyAndBlendShape(obj,descripcion)
                #Creo el deformador con las siguientes propiedades
                deform = None
                curvature=30.0
                deform = mel.eval("nonLinear -type bend -lowBound -5.0 -highBound 5.0 -curvature " + str(curvature) +" "+ str(cmds.listRelatives(copy)[0]) +";")
                nnl = cmds.rename(deform[1],copy+'_NLB')
                ndf = cmds.rename(deform[0],copy+'_NBD')
                cmds.setAttr(str(nnl)+'.tz',-5.0)
                cmds.setAttr(str(nnl)+'.rx',90)
                cmds.setAttr(str(nnl)+'.rz',90)
                cmds.setAttr(str(nnl)+'.sx',5)
                cmds.setAttr(str(nnl)+'.sy',5)
                cmds.setAttr(str(nnl)+'.sz',5)
                cmds.setAttr(str(nnl)+'.visibility',False)
                #Add atributos
                if control!=None:
                    nVale=['bendOnOff','curvature','lowBound','highBound']
                    self.createAttr( control, tipoDeform ,'---------------',ocultar=True,at="enum",en=tipoDeform.upper())
                    self.createAttr( control, nVale[0] ,'<-bendOnOff',0 ,1.0 ,0 )
                    self.createAttr( control, nVale[1] ,'<-curvature',-50.0 ,50.0 ,30.0 )
                    self.createAttr( control, nVale[2]+tipoDeform ,'<-lowBound',-5.0 ,5.0 ,-2.2 )
                    self.createAttr( control, nVale[3]+tipoDeform ,'<-highBound',-5.0 ,5.0 ,2.0 )
                    #Conecto los atributos con el deformador
                    try:
                        cmds.connectAttr(control+'.'+nVale[0], nbs+'.'+copy,f=True)
                        cmds.expression(o=control,s=str(ndf)+"."+nVale[1]+"="+str(control)+"."+ nVale[1] +";", n=obj+descripcion+'_EXP')
                        cmds.expression(o=control,s=str(ndf)+"."+nVale[2]+tipoDeform+"="+str(control)+"."+ nVale[2]+tipoDeform +";", n=obj+descripcion+'_EXP')
                        cmds.expression(o=control,s=str(ndf)+"."+nVale[3]+tipoDeform+"="+str(control)+"."+ nVale[3]+tipoDeform +";", n=obj+descripcion+'_EXP')
                    except RuntimeError:
                        pass
                return copy,nnl,ndf,nbs
            else:
                print 'FALTA ESPECIFICAR EL CONTROL DONDE IRAN SUS ATRIBUTOS'


    def nurbCreation(self,name,directionAxi=[0,1,0],splitU=1,splitV=5,width=0.1,lengthRatio=0.5,jnt=2):
        joints=[]
        #Positions and direction joints
        if directionAxi==[0,0,1]:
            print ('Aun no se desarrollo esta direccion de la nurbs, comuniquese con el desarrollador. Gracias.')#creo controles en los huesos del espacio con una direccion x
        elif directionAxi==[1,0,0]:
            print ('Aun no se desarrollo esta direccion de la nurbs, comuniquese con el desarrollador. Gracias.')#creo controles en los huesos del espacio con una direccion x
        elif directionAxi==[0,1,0]:
            x=int(splitV)#maximo de distancia de cada lado para el array
            lista=range(-x,x+1,jnt)
            for j in lista:
                pos=j/float((splitV/(splitV/2))/width)
                side= 'B' if j<0 else 'C' if j==0 else 'T'
                joints.append(self.JointInSpace(name+side+str(j),[0,0,pos],width+0.2/2))
        self.grpCtroles=[]
        self.grpCtroles.append(self.createCnt(joints,[0,0,1],width,True))#creo controles en los huesos del espacio con una direccion z
        #Create nurb with folicles
        self.nurb=cmds.nurbsPlane( ax=directionAxi,w=width, lr=splitV,u=splitU,v=splitV,n=name+'_NSK')
        self.nurbName=cmds.rebuildSurface (self.nurb,rpo=1, rt=0, end=1,kr=0,kcp=0,kc=1,su=splitU,du=1,sv=splitV,dv=3,tol=0.01,fr=0,dir=2)#reconstruyo la build
        cmds.setAttr(str(self.nurbName[0])+'.inheritsTransform', 0)
        mel.eval('createHair '+str(splitU)+' '+str(splitV)+' 5 0 0 0 0 '+str(splitU)+' 0 2 2 1')
        cmds.delete('hairSystem1','hairSystem1OutputCurves','nucleus1')
        self.grpFoll=cmds.rename('hairSystem1Follicles',(name+'_Follicles'+'_GRP'))
        cmds.setAttr(str(self.grpFoll)+'.inheritsTransform', False)
        cmds.setAttr(str(self.grpFoll)+'.visibility', False)
        self.follicles=cmds.listRelatives(self.grpFoll,children=True)
        self.jntsToSkin=[]
        for f in range(len(self.follicles)):
            self.foll=cmds.rename(self.follicles[f], name+str(f)+'_FLC')
            cmds.delete(cmds.listRelatives(self.foll,children=1)[1])
            self.jnt=cmds.joint(name=name+str(f)+'_JSK',absolute=1,radius=float(width)/2,rotationOrder='xyz')
            self.jntsToSkin.append(self.jnt)
            cmds.connectAttr( self.foll+'.outTranslate', self.jnt+'.translate',f=1)
            cmds.connectAttr( self.foll+'.outRotate', self.jnt+'.rotate',f=1)
        cmds.parent(self.jntsToSkin[1:], w=1)
        for j in self.jntsToSkin:#Fix bones rotation axis
            cmds.setAttr(j+'.jointOrientX',0)
            cmds.setAttr(j+'.jointOrientY',0)
            cmds.setAttr(j+'.jointOrientZ',0)
        #create skin #Prune weights #Remove unused influences
        self.scl=cmds.skinCluster(joints,self.nurbName[0],n=name+'_SCL',mi=3,dr=14.0)[0]
        cmds.select(self.nurbName[0])
        mel.eval('doPruneSkinClusterWeightsArgList 1 { "'+str(0.2)+'" }')
        mel.eval('removeUnusedInfluences')
        cmds.select(cl=1)
        #Creation Groups
        self.gJoints=self.grupoDe(self.jntsToSkin,name+'_jointsToSkin',inherits=False,vis=False)
        self.gJntsRig=self.grupoDe(joints,name+'_joint',inherits=False,vis=False)
        self.follicles=cmds.listRelatives(self.grpFoll,children=True)
        self.gCnts=self.grupoDe(self.grpCtroles[0], name+'_controls',inherits=True,shape=True)
        self.gNurb=self.grupoDe(self.nurbName, name=name+'_NURBS',inherits=False)
        self.gMaster=self.grupoDe([self.grpFoll,self.gJoints,self.gJntsRig,self.gCnts,self.gNurb],name)

        return [self.nurbName[0],self.follicles,self.jntsToSkin,joints,self.scl,self.gCnts]

    def createSpine(self):
        if not cmds.objExists(self.name+'_GRP'):
            self.datos=self.nurbCreation(self.name,self.directionAxi,self.splitU,self.splitV,self.width,self.lengthRatio,self.joint)
        else:
            cmds.warning('YA EXISTE '+ self.name +' CON ESE NOMBRE.')
            self.result =cmds.promptDialog(title='DESEA PONER OTRO NOMBRE?',message='Enter name:',
                        button=['Y','N'],defaultButton='Y', cancelButton='N',dismissString='N')
            if self.result  == 'Y':
                self.newName=cmds.promptDialog(query=True, text=True)
                self.datos=self.nurbCreation(str(self.newName),self.directionAxi,self.splitU,self.splitV,self.width,self.lengthRatio,self.joint)
            else:
                None
        return self.datos

    def createDeformer(self,tipo='wave'):
        #Creo los deformadores con su conexion y los deformadores
        self.deformers=self.createDeformsBlendShape(self.datos[0],cmds.listRelatives(self.datos[5])[0],tipo)
        #Creo un grupo para los deformadores
        if cmds.objExists(self.name+'_Deformers_GRP'):
            #Emparento el deformador al grupo existente
            cmds.parent(self.deformers[0:2],self.name+'_Deformers_GRP')
        else:
            self.gDef=self.grupoDe(self.deformers[0:2],self.name+'_Deformers',inherits=False,vis=False)
            #Meto el nuevo deformador al grupo master
            cmds.parent(self.gDef,self.gMaster)

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
