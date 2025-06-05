
cpdef float Animate(float Current, float Target, float Speed, float AO):
    
    if abs(Current - Target) < 0.5:
        return Target
    else:
        return Current + (Target - Current) * AO * Speed
        

cpdef float AnimateSpdUp(bint Negative, float Current, float Start, float Target, float Speed, float AO):

    if Current == Target:
        return Target

    if Negative: # -
        if Current < Target:
            return Target
        return Current - ((abs(Current - Start) + 1) * AO * Speed)
    else: # +
        if Current > Target:
            return Target
        return Current + ((abs(Current - Start) + 1) * AO * Speed)