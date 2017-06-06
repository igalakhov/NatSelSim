import math as m
import mpmath as np
def doRepSucc(): #this funciton give us a new, updated reproductive success
    reprSuccess = 2
    food = 500
    curPopulation = 1000
    succChange = 1
    ratio = food/curPopulation

    if(ratio < 1):
        output = reprSuccess * m.tan(((ratio - 1)*m.pi)/4)
        print("HIT")
        return reprSuccess + output*succChange
    else:
        slop = reprSuccess * m.pow(np.sec(m.pi/-4), 2) * (m.pi/4)
        output = slop * (ratio - 2) + reprSuccess
        return reprSuccess + output*succChange

print(doRepSucc())
