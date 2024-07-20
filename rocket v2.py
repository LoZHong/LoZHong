import PySimpleGUI as GUI
import math
import matplotlib.pyplot as plt

g = -9.81

class DataStruct:
    def __init__(self, i_time, i_data):
        self.c_time = i_time
        self.c_data = i_data

    def get_data(self, target_time):
        for a in self.c_time:
            if a == target_time:
                _index = self.c_time.index(a)
                result_data = self.c_data[_index]
                break
        else:
            a = 0
            b = 0
            for a in self.c_time:
                if target_time < a and target_time > b:
                    result_data = (self.c_data[self.c_time.index(a)] + self.c_data[self.c_time.index(b)]) /2
                elif target_time < self.c_time[-1]:
                    b = a
                else:
                    result_data = 0

        return result_data

def LoadFile(FileName):

    time = []
    data = []

    if(FileName == None):
        filename = "RocketForce.txt"
    else:
        filename = FileName

    #Open and Read File
    raw_data = open(filename, "r")
    str_data = str(raw_data.read())
    raw_data.close()

    data_list = str_data.split("\n")
    #print(data_list)
    for i in data_list:
        o = i.split("\t")
        #print(o)
        if(o[0] != ""):
            try:
                time.append(float(o[0]))
                data.append(float(o[1]))
            except:
                print(str(o) + " has no data value")

    return time, data
    
def SaveFile(FileName, data):

    file = open(FileName, "w")
    file.write(str(data))

    print(file.name)
    file.close()


    return "Done"

def CalculateData(time_interval,max_stimulate_time, Rocket_Force_Graph , RocDryWeight, RocWetWeight,RocBurnTime, RocAvForce, RocAngle):
    Sample_time = 0

    F_Gph = Rocket_Force_Graph

    time = []

    F_x_l = []
    F_y_l = []

    A_x_l = []
    A_y_l = []

    V_x_l = []
    V_y_l = []

    D_x_l = []
    D_y_l = []

    c_f_l = []
    while Sample_time <= max_stimulate_time:
        time.append(Sample_time)
        #Current Force of the Rocket
        C_force = F_Gph.get_data(Sample_time)
        c_f_l.append(C_force)
        print(C_force)

        F_x = C_force * math.cos(math.radians(RocAngle))
        F_y = C_force * math.sin(math.radians(RocAngle)) + (g * RocDryWeight)
        F_x_l.append(F_x)
        F_y_l.append(F_y)

        A_x = F_x / RocDryWeight
        A_y = F_y / RocDryWeight
        A_x_l.append(A_x)
        A_y_l.append(A_y)

        try:
            V_x = V_x_l[-1] + (A_x * (time_interval))
            V_y = V_y_l[-1] + (A_y * (time_interval))
        except:
            V_x = 0
            V_y = 0
        
        if(V_y <= 0):
            V_y = 0

        try:
            D_x = (V_x_l[-1] * time_interval) + (A_x * math.pow(time_interval,2) / 2)
            D_y = (V_y_l[-1] * time_interval) + (A_y * math.pow(time_interval,2) / 2)
        except:
            D_x = 0
            D_y = 0

        if(D_y <= 0):
            D_y = 0

        V_x_l.append(V_x)
        V_y_l.append(V_y)

        D_x_l.append(D_x)
        D_y_l.append(D_y)

        #print(D_y)

        Sample_time += time_interval  

    return time, D_x_l, D_y_l , F_x_l, F_y_l, A_x_l, A_y_l, V_x_l, V_y_l , c_f_l


# All the stuff inside your window.
layout1 = [  [GUI.Text('Some text on Row 1')],
            [GUI.Text('Rocket Dry Weight (kg)'), GUI.InputText('0.1')],
            [GUI.Text('Weight Of Water Added (kg)'), GUI.InputText('0.05')],
            [GUI.Text('Rocket Burn Time (s)'), GUI.InputText('5')],
            [GUI.Text('Rocket Average Force Produced (N)'), GUI.InputText('10')],
            [GUI.Text('Rocket Angle Facing (Degree From Horizon)'), GUI.InputText('80')],
            [GUI.Button('Calculate'), GUI.Button('Cancel')],
            [GUI.Button('Import File')]
            #[GUI.Text('Apogee: '                , key='1' , visible= False)],
            #[GUI.Text('Horizontal Distance: '   , key='2' , visible= False)],
            #[GUI.Text('Final velocity: '        , key='3' , visible= False)],
            #[GUI.Text('Angle hitting Ground: '  , key='4' , visible= False)],
            #[GUI.Text('Flight Time'             , key='5' , visible= False)] 
            ]

# Create the Window
window = GUI.Window('Window Title', layout1,element_justification='r')

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    Force_Gph = None

    if event == 'Import File':
        filename = GUI.popup_get_file('Import File')
        x,y = LoadFile(filename)
        Force_Gph = DataStruct(x,y)

        #print(Force_Gph.get_data(0.3))


    if event == 'Calculate':
        print('calculating!')

        if(Force_Gph == None):
            x,y = LoadFile(None)
            Force_Gph = DataStruct(x,y)

        Data =  CalculateData(0.02, 100, Force_Gph, float(values[0]),float(values[1]) + float(values[0]),float(values[2]),float(values[3]),float(values[4]))
        if GUI.popup_yes_no("Finish Calculate! \n Save Data?") == 'Yes':
            GUI.popup_auto_close(SaveFile("Data.txt", Data[2]))
            plt.plot(Data[0], Data[1], 'r--', Data[0], Data[2], 'rs',Data[0], Data[3], 'g--', Data[0], Data[4], 'gs',Data[0], Data[5], 'b--', Data[0], Data[6], 'bs',Data[0], Data[7], 'bo', Data[0], Data[8], 'k')
            plt.show()
        #    window['1'].Update(visible=True)
        #    window['2'].Update(visible=True)
        #    window['3'].Update(visible=True)
        #    window['4'].Update(visible=True)
        #    window['5'].Update(visible=True)
        #
        #    window['1'].Update('Apogee: '                + str(Data[0]))
        #    window['2'].Update('Horizontal Distance: '   + str(Data[1]))
        #    window['3'].Update('Final velocity: '        + str(Data[2]))
        #    window['4'].Update('Angle hitting Ground: '  + str(Data[3]))
        #    window['5'].Update('Flight Time'             + str(Data[4]))
        #else:
        #    window['1'].Update(visible=False)
        #    window['2'].Update(visible=False)
        #    window['3'].Update(visible=False)
        #    window['4'].Update(visible=False)
        #    window['5'].Update(visible=False)

    if event == GUI.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break

window.close()