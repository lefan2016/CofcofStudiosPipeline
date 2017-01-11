# USE : sets up spline IK to be able to stretch
# REQUIRES:
#    1. whichAxis(value)
#    2. editTxtGrpButtonArray
#    3. deleteWindow()
# NOTES : 
# 1. SELECT ALL THE JOINTS THAT MAKE UP THE IK JOINT CHAIN, IN ORDER, FROM START TO END
# 2. SELECT THE MAIN CTRL, THEN THE START CTRL, FINALLY THE END CTRL
# 3. SELECT OR TYPE IN HIERARCHICAL ORDER THE GROUP THAT THE DIMENSION NODE IS TO BE GROUPED UNDER
 
def setUpSplineIKstretch(jointArray,prefix,crve,aimAxis):
    splineNormaliseNode = prefix + 'spline_normalize_multiplyDivide'
    splineMultiplyNode = prefix + 'spline_multiplier_multiplyDivide'
    curveInfo = prefix + 'spline_curveInfo1'
 
    howManyJoints = len(jointArray)
    print ('howManyJoints = ' + str(howManyJoints))
    print ('howManyJoints / 3 = ' + str(float(howManyJoints) / float(3)))
    howManyNodes = int(math.ceil(float(howManyJoints) / float(3)))
    print ('howManyNodes = ' + str(howManyNodes))
    #START////////////////////////////////////////////////////////////////////////////////////CREATE CURVE INFO NODE FOR CHAR SPINE 
    #CREATE CURVE INFO AND MULTIPLYDIVIDE NODES
    curveInfoNode = maya.cmds.arclen(crve, ch=True)
    multiplierNode = maya.cmds.shadingNode('multiplyDivide',n=splineNormaliseNode + '1',au=True)
 
    splineNormalise = multiplierNode #ENSURE THAT THERE CONTINUITY THROUGH OUT THE SCRIPT
 
    #CONNECT ARCLENGTH TO INPUT1X 
    socket = multiplierNode + '.input1X'
    connector = curveInfoNode + '.arcLength'
    maya.cmds.connectAttr(connector, socket, force=True)
 
    #SET INPUT2X TO ARCLENGTH VALUE AND SET MULTIPLEDIVED NODES OPERATION TO DIVIDE
    socketAttribute = '.input2X'
 
    maya.cmds.setAttr(multiplierNode + '.operation',2)
    arcLength = maya.cmds.getAttr(connector)
 
    maya.cmds.setAttr(multiplierNode + '.input2X', arcLength)
 
    maya.cmds.rename(curveInfoNode, curveInfo)
    #print('splineMultiplyNode = ' + str(splineMultiplyNode))
    #END/////////////////////////////////////////////////////////////////////////////////////CREATE CURVE INFO NODE FOR CHAR SPINE 
 
    #START///////////////////////////////////////////////////////////////////////////////////CREATE MULTIPLYDIVIDE NODES TO BE CONNECTED TO THE INDIVIDUAL JOINTS TRANSLATEX 
        splineMultiply = []
        #CREATE MULTIPLYDIVIDE NODES 
        for i in range(0,howManyNodes,1):
        temp = maya.cmds.shadingNode('multiplyDivide', n=splineMultiplyNode + str(1), au=True)
        splineMultiply.append(temp)
         
    print ('splineMultiply = ' + str(splineMultiply))
 
    connectorAttribute1 = '.outputX' #change this variable
    socketAttribute1 = '.input' #change this variable
    connector1 = splineNormalise + connectorAttribute1
    connectorAttribute2 = '.output'
     
    whichJoint = 1
 
    whichAxis = [' ', 'X', 'Y', 'Z']
    brake = 0
 
    print ('jointArray 1 = ' + str(jointArray))
 
    #CONNECT THE NORMALISE NODE TO THE MULTIPLYDIVIDE NODES, COPY SPINE JOINT TRANSLATE-X TO MULTIPLYDIVIDE NODES INPUT 1XYZ ATTRIBUTES AND 
    #CONNECT MULTIPLYDIVIDE NODES OUTPUT XYZ TO SPINE JOINT TRANSLATEX
    for i in range(0, howManyNodes, 1):
         
        #multiply = i + 1
     
        for j in range(1, 4, 1):
            if(brake == 0):
                 
                #socket1 = splineMultiply + str(multiply) + (socketAttribute1 + '2' + whichAxis[j])
                socket1 = splineMultiply[i] + (socketAttribute1 + '2' + whichAxis[j])
                maya.cmds.connectAttr(connector1, socket1, force=True)
         
                getAttribute = maya.cmds.getAttr(jointArray[whichJoint] + '.t' + aimAxis.lower())
                #setAttr = maya.cmds.setAttr(splineMultiplyNode + str(multiply) + (socketAttribute1 + '1' + whichAxis[j]), getAttr)
                setAttr = maya.cmds.setAttr( splineMultiply[i] + (socketAttribute1 + '1' + whichAxis[j]), getAttribute)
         
                connector2 = splineMultiply[i] + (connectorAttribute2 + whichAxis[j])
                print ('connector2 = ' + str(connector2))
                socket2 = (jointArray[whichJoint] + '.t' + aimAxis.lower())
                print ('socket2 = ' + str(socket2))
                maya.cmds.connectAttr(connector2, socket2, force=True)
 
                whichJoint = whichJoint + 1
     
                print ('whichJoint = ' + str(whichJoint))
                print ('howManyJoints = ' + str(howManyJoints))
 
                #LOOP BREAK TO CATER FOR ODD NUMBER OF JOINTS
                if(whichJoint == howManyJoints):
                    brake = 1
                    print ('brake = ' + str(brake))
 
    #END/////////////////////////////////////////////////////////////////////////////////////CREATE MULTIPLYDIVIDE NODES TO BE CONNECTED TO THE INDIVIDUAL JOINTS TRANSLATEX 
     
###############################################################################################
#     GUI:    
###############################################################################################
 
def buildWindow(windowName,windowTitle, line1,line2,line3):
    questionButtonHeight=23
    maya.cmds.window( windowName, title= windowTitle, s=True, iconName='Short Name', widthHeight=(500, 300))
    maya.cmds.frameLayout(  windowName + '_frameLayout1', label=' ', borderStyle="in", lv=False, bv=False, mw=10, mh=10)
    maya.cmds.columnLayout(windowName + '_column1', adjustableColumn=True)
 
    maya.cmds.text( label= '   ' )
 
    maya.cmds.rowLayout(windowName + '_row1',numberOfColumns=3, columnWidth3=(80, 80, 80), adjustableColumn3=3, columnAlign3=('left','left','left'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
     
    maya.cmds.text( label= '   ' )
    maya.cmds.text( label= '   ' )
    maya.cmds.text( label= '   ' )
    maya.cmds.setParent('..')
 
    maya.cmds.text( label= '   ' )
 
    maya.cmds.frameLayout(windowName + '_formBase', label='Tabs', lv=False, labelAlign='top', borderStyle='in')
    #form = maya.cmds.formLayout(windowName + '_form1')
    #tabs = maya.cmds.tabLayout(windowName + '_tabs1', innerMarginWidth=5, innerMarginHeight=5)
    #maya.cmds.formLayout( form, edit=True, attachForm=[(tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)] )
     
    #maya.cmds.columnLayout('')
    #maya.cmds.scrollLayout('Global' , width=500, height=300, horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
 
    maya.cmds.rowLayout(windowName + '_row2',numberOfColumns=2, columnWidth2=(450, 20), adjustableColumn2=2, columnAlign2=('left','left'), columnAttach=[(1, 'both', 0), (2, 'both', 0)])
     
    maya.cmds.columnLayout(windowName + '_global1a', rs=3)
    maya.cmds.textFieldGrp( windowName + '_sidePrefix', label='Side Prefix:', text='L_', en=True )
    maya.cmds.textFieldGrp( windowName + '_jointType', label='joint type:', text='IK_', en=True )
    maya.cmds.textFieldGrp( windowName + '_limbTypeName', label='Limb Type Name:', text='leg_', en=True )
    maya.cmds.radioButtonGrp( windowName + '_jointAimAxis', label='Joint Aim Axis:', labelArray3=['X', 'Y', 'Z'], numberOfRadioButtons=3, en=True, sl=1 )
    maya.cmds.text( label= line1 )
    maya.cmds.textFieldButtonGrp( windowName + '_joints', label='Get Joints:', text='', buttonLabel='Select', en=True, bc='editTxtGrpButtonArray("' + windowName + '_joints' + '","textFieldButtonGrp")' )
    maya.cmds.text( label= line2 )
    maya.cmds.textFieldButtonGrp( windowName + '_curve', label='Get SplineIK Curve:', text='', buttonLabel='Select', en=True, bc='editTxtGrpButtonArray("' + windowName + '_curve' + '","textFieldButtonGrp")' )
    maya.cmds.text( label= line3 )
    maya.cmds.textFieldButtonGrp( windowName + '_grp', label='Get Group:', text='char_GRP  DO_NOT_ALTER_GRP   curves_GRP', buttonLabel='Select', en=True, bc='editTxtGrpButtonArray("' + windowName + '_grp' + '","textFieldButtonGrp")' )
    maya.cmds.text( label= '' )
    maya.cmds.setParent('..')
 
    maya.cmds.columnLayout(windowName + '_global1b', rs=3)
    maya.cmds.text( label= '   ' )
    maya.cmds.button(label='?', height = questionButtonHeight)
    maya.cmds.text( label= '   ' )
    maya.cmds.button(label='?', height = questionButtonHeight)
    maya.cmds.text( label= '   ' )
    maya.cmds.setParent('..')
     
    maya.cmds.setParent('..')
    #maya.cmds.setParent('..')
    #maya.cmds.setParent('..')
 
    maya.cmds.text( windowName + '_space1', label='' )
    maya.cmds.text( windowName + '_space2', label='' )
    maya.cmds.button(windowName + '_CreateSystem', label='Run Script', c='runWindow("' + windowName + '")' )
 
    maya.cmds.showWindow( windowName )
 
 
def runWindow(windowName):
    sidePrefix = maya.cmds.textFieldGrp( windowName + '_sidePrefix', q=True, text=True )
    jointType = maya.cmds.textFieldGrp( windowName + '_jointType', q=True, text=True )
    limbTypeName = maya.cmds.textFieldGrp( windowName + '_limbTypeName', q=True, text=True )
    jaa = maya.cmds.radioButtonGrp( windowName + '_jointAimAxis', q=True, sl=True )
    jointAimAxis = whichAxis(jaa)[1]
    getCurve = maya.cmds.textFieldButtonGrp( windowName + '_curve', q=True, text=True )
    splineIkCurve = getCurve.split()[0]
    getJoints = maya.cmds.textFieldButtonGrp( windowName + '_joints', q=True, text=True )
    joints = getJoints.split()
    getGroup = maya.cmds.textFieldButtonGrp( windowName + '_grp', q=True, text=True )
    groupCurve = getGroup.split()
 
    sidePrefix = 'L_'
    jointType = 'IK_'
    limbTypeName = 'leg_'
    prefix = sidePrefix + jointType + limbTypeName
 
 
    jointAimAxis = 'X'
 
    howManyNodes = int(math.ceil(len(joints) / 3)) #This divided by three because of X,Y,Z
 
    setUpGrp(groupCurve)
    print ('joints[0:(len(joints)-1)] = ' + str(joints[0:(len(joints)-1)]))
 
    splineIKstretchjoints = setUpSplineIKstretch(joints[0:(len(joints)-1)],prefix,splineIkCurve,jointAimAxis)
 
line1 = '    SELECT ALL THE JOINTS THAT MAKE UP THE IK JOINT CHAIN, IN ORDER, FROM START TO END:-'
line2 = '    SELECT THE MAIN CTRL, THEN THE START CTRL, FINALLY THE END CTRL:-'
line3 = '    SELECT OR TYPE IN HIERARCHICAL ORDER THE GROUP THAT THE DIMENSION NODE IS TO BE GROUPED UNDER'
ver = ' : ver 01.001 : '
windowTitle = 'Set Up Spline IK Stretch' + ver
rebuildCurveWindowName = 'SetUpSplineIKstretch'
deleteWindow(rebuildCurveWindowName)
buildWindow(rebuildCurveWindowName,windowTitle,line1,line2,line3)
