from antencoding import AntennaEncoding
from antencoding import *
from PyNEC import *

def main():

    context=nec_context()

    x = AntennaEncoding()
    x.add_operator( ForwardOperator(0.010) )
    x.add_operator( RotateXOperator(1.5) )
    x.add_operator( ForwardOperator(0.010) )
    x.add_operator( RotateXOperator(-1.5) )
    x.add_operator( ForwardOperator(0.010) )
    x.add_operator( RotateXOperator(-1.5) )
    x.add_operator( ForwardOperator(0.010) )
    x.toNEC(context)

if __name__ == "__main__":
    main()
