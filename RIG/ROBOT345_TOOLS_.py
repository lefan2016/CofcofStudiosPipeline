import maya.cmds as cmds

cnts=cmds.ls('ROBOT345__Ctrl_*Effector')
for cnt in cnts:
    cmds.setAttr(str(cnt)+'.reachTranslation',k=1)
    cmds.setAttr(str(cnt)+'.reachRotation',k=1)


import maya.cmds
import maya.mel
import sys
path='P:\LOCAL\ES_SCRIPTS\EXOCORTEX\ExocortexCrate\Maya\MEL\ExocortexAlembic'
if not path in sys.path:
    sys.path.append(path)

import ExocortexAlembic as EA

help(EA._import)
help(EA._export)
help(EA._attach)
help(EA._import.IJobInfo)


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

#ere.nonlinearDeformer([lowCRV[0]],'twist',rotate=(0,0,90))
#ere.nonlinearDeformer([lowCRV[0]],'sine',rotate=(0,0,90))


setAttr "pCylinder1_19_LOC_ACNS.worldUpVectorX" 1;
setAttr "pCylinder1_19_LOC_ACNS.worldUpVectorY" 0;
