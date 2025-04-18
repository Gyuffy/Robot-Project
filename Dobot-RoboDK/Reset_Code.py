from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

from robodk import *      # RoboDK API
from robolink import *    # Robot toolbox

RB = RDK.Item("RB", 2)
CON = RDK.Item("Conv", 2)
Box1 = RDK.Item("Box1", 5)
Box2 = RDK.Item("Box2", 5)
Obj_Frame = RDK.Item("Obj_Frame", 3)

def parse_matrix(matrix_str):
    lines = matrix_str.strip().split('\n')
    matrix = []
    for line in lines:
        line = line.strip().strip(';').strip('[]')  # [, ], ; 제거
        values = line.split(',')
        row = [float(val.strip()) for val in values]
        matrix.append(row)
    return matrix

def set_frame(Obj, Frame):
    Obj.setParent(Frame)

def reset():
    set_frame(Box1, Obj_Frame)
    set_frame(Box2, Obj_Frame)

    pos1 = parse_matrix("""[     1.000000,     0.000000,     0.000000,     0.000000 ;
      0.000000,     1.000000,     0.000000,     0.000000 ;
      0.000000,     0.000000,     1.000000,     125.000000 ;
      0.000000,     0.000000,     0.000000,     1.000000 ];""")
    
    pos2 = parse_matrix("""[     1.000000,     0.000000,     0.000000,     0.000000 ;
      0.000000,     1.000000,     0.000000,     0.000000 ;
      0.000000,     0.000000,     1.000000,     0.000000 ;
      0.000000,     0.000000,     0.000000,     1.000000 ];""")
    

    Box1.setPose(Mat(pos1))
    Box2.setPose(Mat(pos2))

    RB.MoveJ([0.000000, 0.000000, 90.000000, 0.000000, 90.000000, 0.000000])

    CON.MoveJ([0])

reset()