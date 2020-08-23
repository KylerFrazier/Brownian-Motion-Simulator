def anticlockwise(p1,p2,q1):

    return (q1[1]-p1[1]) * (p2[0]-p1[0]) > (p2[1]-p1[1]) * (q1[0]-p1[0])

def line_collision(p1,p2,q1,q2):

    return  anticlockwise(p1,q1,q2) != anticlockwise(p2,q1,q2) and \
            anticlockwise(p1,p2,q1) != anticlockwise(p1,p2,q2)