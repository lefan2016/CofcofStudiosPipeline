# @Date:   2018-08-20T14:57:26-03:00
# @Last modified time: 2018-08-20T20:56:50-03:00



# -*- encoding: utf-8 -*-
#Gabo Salinas
#26/06/18
#this tool animates channelBox selected attributes with input values. keyframes are
#separated by the "keys separation" value.
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
'''
import sys
path=r'F:\Repositores\GitHub\CofcofStudiosPipeline\RIG\testAnim'
if not path in sys.path:
    sys.path.append(path)
import testAnim
reload(testAnim)
sys.path.remove(path)
'''
def testAnimation(arg):
    sel=pm.ls(sl=1)
    keysValues     = cmds.textField ( 'keyValues' , q=1,text=1).split(',')
    keysSeparation = cmds.textField ( 'keysSeparation' , q=1,text=1)
    initialFrame = pm.currentTime( query=True )
    cBox = mel.eval ('global string $gChannelBoxName; $temp=$gChannelBoxName; ')
    attsShape   = pm.channelBox ( cBox , q=1,ssa=1 )
    attsMain    = pm.channelBox ( cBox , q=1,sma=1 )
    attsHistory = pm.channelBox ( cBox , q=1,sha=1 )
    attsOut     = pm.channelBox ( cBox , q=1,soa=1 )
    atts = []
    relativeAnimation = cmds.checkBox ('cb_relativeAnim',q=1,value=1)
    for at in ( attsShape , attsMain , attsHistory , attsOut ):
        if at:
            atts.extend ( at   )

    if sel and keysValues and keysSeparation and atts:
        cmds.refresh(su=True)#Disable refresh
        for s in sel:
            for at in range( len(atts) ) :
                actualAttValue = (0,pm.getAttr ( s + '.' + atts[at] ))[relativeAnimation==True ]
                for k in range(len(keysValues)):
                    print 'valor:' + keysValues[k]
                    currFrame = pm.currentTime( query=True )
                    attValue =   actualAttValue + int ( keysValues[k] )
                    pm.setAttr ( s + '.' + atts[at] , attValue )
                    pm.setKeyframe ( s + '.' + atts[at] )
                    pm.currentTime( currFrame+ int(keysSeparation) , edit=True )
        cmds.refresh(su=False)#Enable refresh

    else:
        pm.warning ('Be sure you have selected objects and attributes to animate.')
        cmds.refresh(su=False)#Enable refresh



def UI():
    if cmds.window('TestAnimation',ex=1):
        cmds.deleteUI('TestAnimation')
    w=cmds.window('TestAnimation',title='Test animation',resizeToFitChildren=True)
    rcl=cmds.columnLayout(  )
    r1l=cmds.rowLayout (nc=2 , p=rcl)
    b1=cmds.text(label = "Values", w=150, p=r1l )
    cmds.textField('keyValues',width=300, p=r1l,text='0,2,-2,0')
    r1l=cmds.rowLayout (nc=2 , p=rcl)
    b1=cmds.text(label = "Keys separation", w=150, p=r1l )
    cmds.textField('keysSeparation',width=300, p=r1l,text='10')

    r2l=cmds.rowLayout (nc=6 , p=rcl)
    cmds.checkBox ('cb_relativeAnim',label='relative')
    b2=cmds.button(label = "Animate", w=450 , command = testAnimation, bgc = (0.5, 0.8, 0.1) , p=r2l )


    cmds.showWindow(w)
UI()
