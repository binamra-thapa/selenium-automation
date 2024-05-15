from functions.paymode import test_paymode
from functions.paymode import paymode
def main():
    print("Executing")
    #CallingPaymodeFunction
    '''
    1. Browse to pmx-ENV-cs.saas-<n or p>.com/px/login
    '''
    # paymode("qa6")
    test_paymode()



if __name__ == "__main__":
    main()
