#Gabo Salinas
#26/06/18
#this tool animates channelBox selected attributes with input values. keyframes are
#separated by the "keys separation" value.
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel



        

def testAnimation():
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
    for at in ( attsShape , attsMain , attsHistory , attsOut ):
        if at:
            atts.extend ( at   )

    if sel and keysValues and keysSeparation and atts:


        for s in sel:
            for at in range( len(atts) ) :
                for k in range(len(keysValues)):
                    currFrame = pm.currentTime( query=True )
                    pm.setAttr ( s + '.' + atts[at] , int ( keysValues[k] ) )
                    pm.setKeyframe ( s + '.' + atts[at] )
                    pm.currentTime( currFrame+ int(keysSeparation) , edit=True )

    else:
        pm.warning ('Be sure you have selected objects and attributes to animate.')



def UI():
    if cmds.window('TestAnimation',ex=1):
        cmds.deleteUI('TestAnimation')
    w=cmds.window('TestAnimation',title='Test animation',resizeToFitChildren=True)
    rcl=cmds.columnLayout(  )
    r1l=cmds.rowLayout (nc=2 , p=rcl)
    b1=cmds.text(label = "Values", w=150, p=r1l )
    cmds.textField('keyValues',width=300, p=r1l)
    r1l=cmds.rowLayout (nc=2 , p=rcl)
    b1=cmds.text(label = "Keys separation", w=150, p=r1l )
    cmds.textField('keysSeparation',width=300, p=r1l)

    r2l=cmds.rowLayout (nc=6 , p=rcl)
    b2=cmds.button(label = "Animate", w=450 , command = 'testAnimation()', bgc = (0.5, 0.8, 0.1) , p=r2l )


    cmds.showWindow(w)
UI()
