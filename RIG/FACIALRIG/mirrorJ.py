# @Date:   2018-08-15T03:04:27-03:00
# @Last modified time: 2018-08-18T04:33:43-03:00
import maya.cmds as cmds
import os, sys

import re
mirroriables=[]
jnts=cmds.ls(sl=True,type='joint')
#filtro left
for jnt in jnts:
    pattern1=re.compile('L_')
    if pattern.match(str(jnt.upper())):
        mirroriables.append(jnt)

for j in mirroriables:
    grp=cmds.group(n='mirrorTempGrp',empty=True,w=1)
    if cmds.listRelatives(j,children=True):
        jPrincipal=cmds.duplicate(j,rr=True)
        newname=j.split('L_') or j.split('l_')
        newJ=mc.rename(j,newname[0:]+'R_')
        cmds.parent(newJ,grp,r=True)
        cmds.setAttr(grp+'.scaleX', -1)
        cmds.makeIdentity(grp,t=1,r=1,s=1)

        cmds.delete(grp)
