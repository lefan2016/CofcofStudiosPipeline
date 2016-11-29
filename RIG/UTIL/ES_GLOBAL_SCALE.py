#GLOBAL SCALE
import maya.cmds
sel=cmds.ls(sl=1)
jnts=sel

sel=cmds.ls(sl=1)
cnt=sel
def globalScale():
    global tfScalaGlobal,tfControl,tfJoints
    for j in jnts:
        #Create Node MultipleDivide
        nmd=cmds.createNode('multiplyDivide',n=str(j[:-3])+'NMD')
        #Primer control
        cmds.connectAttr('C_SNAIL_ROOT_TRF.Global_Scale',str(nmd)+'.input1X')
        cmds.connectAttr('C_SNAIL_ROOT_TRF.Global_Scale',str(nmd)+'.input1Y')
        cmds.connectAttr('C_SNAIL_ROOT_TRF.Global_Scale',str(nmd)+'.input1Z')
        #Segundo control
        cmds.connectAttr(str(cnt[0])+'.scale',str(nmd)+'.input2')
        #Resultado al joint
        cmds.connectAttr(str(nmd)+'.output',str(j)+'.scale')
def selJoints():
    jnts=cmds.ls(sl=True, type='joint')
    if jnts:
        cmds.textField(tfJoints, q=True,e=True,insertText=str(jnts))

def refreshAll():
    try:
        selObj = cmds.ls(sl=1)
        selAttrs = cmds.channelBox("mainChannelBox", q=1, sma=1)
    except:
        if not selObjs:
            print "no object and attribute is selected!"
        elif not selAttrs:
            print "no attribute is selected!"
    if selObj and selAttrs:
        return selObj,selAttrs
    
def UI():
    w='ES_GLOBAL_SCALE_'
    global tfScalaGlobal,tfControl,tfJoints
    if cmds.window(w,ex=1):
        cmds.deleteUI(w)
    w=cmds.window(w,title=w,resizeToFitChildren=True)
    rcl=cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 100)] )
    
    b1=cmds.button(label = "GLOBAL", command = 'setGlobal()', bgc = (1.0, 0.9, 0.1))
    tfScalaGlobal=cmds.textField(w + 'global', ann='Adiere el nombre del atributo exacto.',width=50,textChangedCommand="globalScale()",receiveFocusCommand='refreshAll()')
    
    b2=cmds.button(label = "CNTROL", command = 'setControl()', bgc = (0.5, 0.8, 0.1))
    tfControl=cmds.textField(w + 'control', ann='global.',width=300,textChangedCommand="refreshAll()",receiveFocusCommand='refreshAll()')
    
    b3=cmds.button(label = "JOINT", command = 'selJoints()', bgc = (1.0, 0.5, 0.1))
    tfJoints=cmds.textField(w + 'joint', ann='control.',width=300)
    
    b4=cmds.button(label = "CREATE", command = 'createNode()', bgc = (1.0, 0.1, 0.1),align='rigth')
    
    refreshAll()
    cmds.showWindow(w)
UI()