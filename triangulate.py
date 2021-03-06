import numpy as np
import argparse
import sys
import math;

def triangulate_on_timestamps_2D(p1, p2, p3, k1=0.06, k2=1, bias=0.1):
    """
    given a list of three times representing time difference between
    i-th receiver receiving the signal and the signal origin time,
    determine the position of the origin
    args:
        p is the input signal in arbitrary units proportional to decibels
    kwargs:
        k1 is a proportionality constant for power falloff of the tone
        k2 is a proportionality constant for converting p -> dB
    """

    # for logarithmic 'dB' power inputs
    # parr = k2*np.array([p1, p2, p3])/10
    # v1, v2, v3 = np.power(10, parr)
    # r1, r2, r3 = k1/v1, k1/v2, k1/v3
    r1, r2, r3 = k1/(p1+bias), k1/(p2+bias), k1/(p3+bias)

    # Determine some coefficients to do basic linear algebra
    A = x3 - x2
    B = y3 - y2
    C = .5*(r2**2 - x2**2 - y2**2) - .5*(r3**2 - x3**2 - y3**2)
    D = x3 - x1
    E = y3 - y1
    F = .5*(r1**2 - x1**2 - y1**2) - .5*(r3**2 - x3**2 - y3**2)

    # solve the linear equation
    Q = np.array([[A, B],
                    [D, E]])
    P = np.array([[C], [F]])
    S = np.linalg.inv(Q).dot(P)
    x, y = S[0][0], S[1][0]

    return x,y


def dopler_on_timesignals(f1, f2, f3, x, y, f0=7000):
    """
    Passed frequency information from the three receivers as well as
    previously determined position of the source, compute the expected
    velocity of the source
    """
    cos_thetas = []
    for xi, yi in [(x1,y1), (x2,y2), (x3,y3)]:
        cos_theta = (x-xi)/np.sqrt((x-xi)**2 + (y-yi)**2)
        cos_thetas.append(cos_theta)

    cos_thetas = np.array(cos_thetas)
    sin_thetas = np.sin(np.arccos(cos_thetas))
    fvals = (np.array([f1, f2, f3])/f0 -1 )*V_S
    # for every combination of linear systems, see what the doppler algorithm
    # claims the velocity is
    for i, j in [(0,1), (1,2), (2,0)]:
        Mij = np.array([[cos_thetas[i], sin_thetas[i]],
                        [cos_thetas[j], sin_thetas[j]]])
        F = np.array([ [fvals[i]], [fvals[j]]])
        V = np.linalg.inv(Mij).dot(F)
        vx, vy = V[0][0], V[1][0]

# # # # main routine
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('powers', metavar='p', type=float, nargs=3,
                    help='an integer for the accumulator')
args = parser.parse_args()

# fixed positions of laptops
# POSITIONS OF RECIEVERS, in [m]
R1 = (7, 6)
R2 = (math.sqrt(85)*math.cos(math.atan(6/7) + 2*math.pi/3), math.sqrt(85)*math.sin(math.atan(6/7) + 2*math.pi/3))
R3 = (math.sqrt(85)*math.cos(math.atan(6/7) + 4*math.pi/3), math.sqrt(85)*math.sin(math.atan(6/7) + 4*math.pi/3))

x1, y1 = R1[0], R1[1]
x2, y2 = R2[0], R2[1]
x3, y3 = R3[0], R3[1]

V_S = 343 # m/s

coords = triangulate_on_timestamps_2D(*args.powers)
print(coords[0], coords[1])
sys.stdout.flush()
#velocities = dopler_on_timesignals(7010, 7001, 6990, 0.1, 0.1)
