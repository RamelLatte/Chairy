
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


cpdef float FineAnimate(float Current, float Target, float Speed, float AO, float Threshold):
    
    if abs(Current - Target) < Threshold:
        return Target
    else:
        return Current + (Target - Current) * AO * Speed


cpdef float FineAnimateSpdUp(bint Negative, float Current, float Start, float Target, float Speed, float AO):

    if Current == Target:
        return Target

    if Negative: # -
        if Current < Target:
            return Target
        return Current - (abs(Current - Start) * AO * Speed)
    else: # +
        if Current > Target:
            return Target
        return Current + (abs(Current - Start) + 1 * AO * Speed)


# ChatGPT가 생성한 코드:

cdef float ease_in_out(float t):
    if t < 0.5:
        return 2 * t * t
    else:
        return -1 + (4 - 2 * t) * t


cpdef float SmoothEasedAnimate(float Current, float Start, float Target, float Speed, float AO):
    if Current == Target:
        return Target

    cdef float total_dist = abs(Target - Start)
    if total_dist == 0:
        return Target

    cdef float traveled = abs(Current - Start)
    cdef float progress = traveled / total_dist
    if progress > 1.0:
        progress = 1.0
    elif progress < 0.0:
        progress = 0.0

    cdef float eased = ease_in_out(progress)
    cdef float delta = (Target - Current) * eased * AO * Speed

    # overshoot 방지
    if Target > Current and Current + delta > Target:
        return Target
    elif Target < Current and Current + delta < Target:
        return Target
    return Current + delta