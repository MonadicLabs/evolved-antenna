import numpy as np
from eulerangles import *
from PyNEC import *
import StringIO

class AntennaState:

    def __init__(self):
        self.pos = np.array([0.0,0.0,0.0])
        # X, Y, Z orientation in radians
        self.orientation = np.array([0.0,0.0,0.0])

class Operator:
    def __init__(self):
        self.items_list = []

    def apply(self, state):
        print( "Base Operator apply()")
        return state

class NullOperator(Operator):
    def __init__(self):
        print( "NullOperator" )

    def apply(self, state):
        print( "Null Operator apply()")
        return state

class ForwardOperator(Operator):

    def __init__(self, length):
        self.length = length
        print( "ForwardOperator")

    def apply(self, state):
        print( "Forward apply()" )
        # Compute rotation matrix from current state
        rotMat = euler2mat( state.orientation[0], state.orientation[1], state.orientation[2] )
        # Create our length-vector (z-facing)
        lvec = np.array([0.0,0.0,self.length])
        # Rotate lvec by rotMat
        rvec = rotMat.dot( lvec )
        state.pos += rvec
        return state

class RotateXOperator(Operator):

    def __init__(self, value):
        self.value = value

    def apply(self, state):
        print("Rotate apply()")
        state.orientation[2]+= self.value
        return state

class RotateYOperator(Operator):

    def __init__(self, value):
        self.value = value

    def apply(self, state):
        print("Rotate apply()")
        state.orientation[1]+= self.value
        return state

class RotateZOperator(Operator):

    def __init__(self, value):
        self.value = value

    def apply(self, state):
        print("Rotate apply()")
        state.orientation[0]+= self.value
        return state

class AntennaEncoding:

    operators = []

    def __init__(self):
        self.operators = []

    def add_operator(self, op):
        self.operators.append(op)

    def toNEC(self, context):
        retStr = ""
        s = AntennaState()
        itg = 1
        i = 0
        geo = context.get_geometry()
        for op in self.operators:
            # Add new wire
            spos = s.pos
            gwStr = "GW " + str(itg)
            gwStr += " 50"
            gwStr += " " + str( s.pos[0] )
            gwStr += " " + str( s.pos[1] )
            gwStr += " " + str( s.pos[2] )
            s = op.apply(s)
            gwStr += " " + str( s.pos[0] )
            gwStr += " " + str( s.pos[1] )
            gwStr += " " + str( s.pos[2] )
            gwStr += " 0.00049999"
            npos = s.pos
            print( gwStr )
            geo.wire( itg, 1, spos[0], spos[1], spos[2], npos[0], npos[1], npos[2], 0.0001, 1, 1 )
            itg += 1