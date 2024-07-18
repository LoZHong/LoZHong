import PySimpleGUI as GUI
import math

def SolveQuadradic(a,b,c):
    x1 = ((-b) + math.sqrt((math.pow(b,2) - (4 * a * c))))/(2*a)
    x2 = ((-b) - math.sqrt((math.pow(b,2) - (4 * a * c))))/(2*a)
    return x1, x2

def CalculateData(RocDryWeight, RocWetWeight,RocBurnTime, RocAvForce, RocAngle):
    g = -9.81

    ### Stage 1 ###
    s1_u_acc_y = (RocAvForce *  math.sin(math.radians(RocAngle)))/((RocDryWeight + RocWetWeight)/2) - g
    s1_u_acc_x = (RocAvForce * math.cos(math.radians(RocAngle)))/((RocDryWeight + RocWetWeight)/2)

    s1_v_Vel_x = s1_u_acc_x * RocBurnTime
    s1_v_Vel_y = s1_u_acc_y * RocBurnTime

    s1_v_Dis_x = (s1_u_acc_x) * math.pow(RocBurnTime,2) / 2 #Distance Travel in Stage 1
    s1_v_Dis_y = (s1_u_acc_x) * math.pow(RocBurnTime,2) / 2


    ### Stage 2 ###
    #Calcualte Apogee
    s2_v_Vel_y = 0
    Apogee = - math.pow(s1_v_Vel_y, 2) / (2 * (g))

    #Calculate Time To Reach Apogee
    s2_t_ReachApogee_x = SolveQuadradic((g/2), s1_v_Vel_y, -Apogee)
    if(s2_t_ReachApogee_x[0] == s2_t_ReachApogee_x[1]):
        s2_t_ReachApogee = s2_t_ReachApogee_x[0]
    else:
        GUI.popup_error_with_traceback("[Error]: unable to Calculate time reach Apogee")
    
    #Calculate Time For Whole Stage 2
    s2_t_WholeS = s2_t_ReachApogee *2

    #Calculate Distance Travel For Stage 2
    s2_v_dis_x = s1_v_Vel_x * s2_t_WholeS

    ### Stage 3 ###
    # Notes:   I assume the angle exits the stage 2 is as same as it enters stage 2 
    #          also same as the initial angle. The Height which Stage 3 starts will 
    #          be as same as the height of stage 1 ends. The Velocity theortically
    #          will be same as the final v of s1
    
    #Calculate time to compact with Ground
    s3_t_GND_x = SolveQuadradic((-g/2) , s1_v_Vel_y, -s1_v_Dis_y)
    if(s3_t_GND_x[0] >= 0):
        s3_t_GND = s3_t_GND_x[0]
    else:
        s3_t_GND = s3_t_GND_x[1]

    #Calculate Final Velocity
    s3_v_vel_y = math.sqrt( (math.pow(s1_v_Vel_y,2) + ( 2 * -g * s1_v_Dis_y)))
    s3_v_vel_x = s1_v_Vel_x
    s3_v_vel = math.sqrt(math.pow(s3_v_vel_x,2) + math.pow(s3_v_vel_y,2))
    s3_v_vel_angle = math.acos(math.radians(s3_v_vel_y/s3_v_vel)) * 180 / math.pi


    flight_time = RocBurnTime + s2_t_ReachApogee + s3_t_GND

    HoriDistance = s1_v_Dis_x + s2_v_dis_x + (s3_v_vel_x * s3_t_GND)

    Velocity_Be4_Hitting_Ground = s3_v_vel
    Angle_Hit_Ground = s3_v_vel_angle

    print(    
            "asdasd  " + str(s1_v_Vel_x),
            s1_u_acc_y,
            s1_v_Dis_y,
            s1_v_Vel_y,
            Apogee
        )
    return Apogee, HoriDistance, Velocity_Be4_Hitting_Ground, flight_time,Angle_Hit_Ground
    


# All the stuff inside your window.
layout1 = [  [GUI.Text('Some text on Row 1')],
            [GUI.Text('Rocket Dry Weight (kg)'), GUI.InputText('1')],
            [GUI.Text('Weight Of Water Added (kg)'), GUI.InputText('0.5')],
            [GUI.Text('Rocket Burn Time (s)'), GUI.InputText('5')],
            [GUI.Text('Rocket Average Force Produced (N)'), GUI.InputText('10')],
            [GUI.Text('Rocket Angle Facing (Degree From Horizon)'), GUI.InputText('50')],
            [GUI.Button('Calculate'), GUI.Button('Cancel')],
            [GUI.Text('Apogee: '                , key='1' , visible= False)],
            [GUI.Text('Horizontal Distance: '   , key='2' , visible= False)],
            [GUI.Text('Final velocity: '        , key='3' , visible= False)],
            [GUI.Text('Angle hitting Ground: '  , key='4' , visible= False)],
            [GUI.Text('Flight Time'             , key='5' , visible= False)] ]

# Create the Window
window = GUI.Window('Window Title', layout1,element_justification='r')

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == 'Calculate':
        print('calculating!')
        Data = CalculateData(float(values[0]),float(values[1]) + float(values[0]),float(values[2]),float(values[3]),float(values[4]))
        if GUI.popup_yes_no('Apogee: ' + str(Data[0]) + '\nHorizontal Distance: ' + str(Data[1]) + '\nFinal velocity: ' + str(Data[2]) + '\nAngle hitting Ground: ' + str(Data[3]) + '\nFlight Time' + str(Data[4]) + '\nTemporaryly Save Data?') == 'Yes':
            window['1'].Update(visible=True)
            window['2'].Update(visible=True)
            window['3'].Update(visible=True)
            window['4'].Update(visible=True)
            window['5'].Update(visible=True)

            window['1'].Update('Apogee: '                + str(Data[0]))
            window['2'].Update('Horizontal Distance: '   + str(Data[1]))
            window['3'].Update('Final velocity: '        + str(Data[2]))
            window['4'].Update('Angle hitting Ground: '  + str(Data[3]))
            window['5'].Update('Flight Time'             + str(Data[4]))
        else:
            window['1'].Update(visible=False)
            window['2'].Update(visible=False)
            window['3'].Update(visible=False)
            window['4'].Update(visible=False)
            window['5'].Update(visible=False)

    if event == GUI.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break

window.close()