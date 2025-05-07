from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

from robodk import *      # RoboDK API
from robolink import *    # Robot toolbox

RB = RDK.Item("RB", 2)
RB_Tool = RDK.Item("Tool1", 4)
CON = RDK.Item("Conv", 2)
CON_F = RDK.Item("Conv_F", 3)
Box1 = RDK.Item("Box1", 5)
Box2 = RDK.Item("Box2", 5)
Obj_Frame = RDK.Item("Obj_Frame", 3)
Moving_Frame = RDK.Item("Moving_Frame", 3)

def parse_matrix(matrix_str):
    lines = matrix_str.strip().split('\n')
    matrix = []
    for line in lines:
        line = line.strip().strip(';').strip('[]')  # [, ], ; 제거
        values = line.split(',')
        row = [float(val.strip()) for val in values]
        matrix.append(row)
    return matrix

def pick_place():
    RB.MoveJ(Mat([59.034098, 2.386412, 87.559600, 0.053988, 90.000000, -59.034098]))    # Rotate to pick
    RB.MoveJ(Mat([59.034098, 8.015065, 108.636930, -26.651995, 90.000000, -59.034098]))    # Down
    RB.MoveJ(Mat([59.034098, 11.664608, 112.688852, -34.353460, 90.000000, -59.034098]))    # Pick
    RB_Tool.AttachClosest("Box1", 1000.0)   # Attach
    time.sleep(2)
    RB.MoveJ(Mat([59.034098, 8.015065, 108.636930, -26.651995, 90.000000, -59.034098])) 
    RB.MoveJ(Mat([60.538508, 2.481046, 87.460600, 0.058354, 90.000000, -60.538508]))
    RB.MoveJ(Mat([-4.600065, 0.067137, 89.932820, 0.000043, 90.000000, 4.600065]))
    RB.MoveJ(Mat([-4.424332, 19.644088, 117.039993, -46.684081, 90.000000, 4.424332]))  # Ready to place
    RB.MoveJ(Mat([-4.424332, 25.521266, 118.805356, -54.326622, 90.000000, 4.424332]))  # Place
    # RB_Tool.DetachClosest()
    # RB_Tool.DetachAll(CON)
    RB_Tool.DetachAll(CON_F)
    CON.MoveJ([500])
    time.sleep(2)


    RB.MoveJ(Mat([60.538508, 2.481046, 87.460600, 0.058354, 90.000000, -60.538508]))    # Rotate to pick
    RB.MoveJ(Mat([60.538508, 19.471923, 117.303513, -46.775436, 90.000000, -60.538508]))    # Down
    RB.MoveJ(Mat([60.538508, 25.372577, 119.073245, -54.445822, 90.000000, -60.538508]))    # Pick
    RB_Tool.AttachClosest("Box2", 1000.0)   # Attach
    time.sleep(2)
    RB.MoveJ(Mat([60.538508, 25.372577, 119.073245, -54.445822, 90.000000, -60.538508]))
    RB.MoveJ(Mat([60.538508, 2.481046, 87.460600, 0.058354, 90.000000, -60.538508]))
    RB.MoveJ(Mat([-4.600065, 0.067137, 89.932820, 0.000043, 90.000000, 4.600065]))
    RB.MoveJ(Mat([-4.424332, 19.644088, 117.039993, -46.684081, 90.000000, 4.424332]))  # Ready to place
    RB.MoveJ(Mat([-4.424332, 25.521266, 118.805356, -54.326622, 90.000000, 4.424332]))  # Place
    # RB_Tool.DetachClosest()
    # RB_Tool.DetachAll(CON)
    RB_Tool.DetachAll(CON_F)
    RB.MoveJ(Mat([-4.600065, 0.067137, 89.932820, 0.000043, 90.000000, 4.600065]))
#     Box2.setPose(Mat(parse_matrix("""[     1.000000,     0.000000,     0.000000,    -550.000000 ;
#       0.000000,     1.000000,     0.000000,    60.000000 ;
#       0.000000,     0.000000,     1.000000,     0.000000 ;
#       0.000000,     0.000000,     0.000000,     1.000000 ];
# """)))
    CON.MoveJ([1000])
    
    # Box1.setParent(Moving_Frame)
    # time.sleep(2)
    # RB.MoveJ(Mat([-4.600065, 0.067137, 89.932820, 0.000043, 90.000000, 4.600065]))  # Return
    
    # for i in range(100):
    #     pos = [[1, 0, 0, 140+i*10], [0, 1, 0, 210], [0, 0, 1, 0], [0, 0, 0, 1]]
    #     Moving_Frame.setPose(Mat(pos))




RDK.RunProgram("Reset_Code")
time.sleep(2)
pick_place()
