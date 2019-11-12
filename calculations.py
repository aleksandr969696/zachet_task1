import numpy as np
from scipy.integrate import odeint
import math
import copy
from classes import Particle, Emitter
G = 6.6743015*math.pow(10,-11)


def f_x(y0, t, masses):
    a_array = []
    points = []
    for i, m in enumerate(masses):
        points.append([y0[i*4], y0[i*4+1], m])
    for i, p in enumerate(points):
        a_array.append(calculate_a([point for j, point in enumerate(points) if j !=i], points[i]))
    ret = []

    for i, a in enumerate(a_array):
        ret.extend([y0[i * 4 + 2], y0[i * 4 + 3], a[0], a[1]])
    return ret


def calculate_odeint(particles, t_, delta_t):
    t = np.linspace(0, t_, t_ / delta_t + 1)
    y0 = []
    for p in particles:
        y0.extend(p.to_array_coords())
    # print([p.m for p in particles])
    lk = odeint(f_x, y0, t,
                args=([p.m for p in particles],))
    return [[{'x': lk[z][i*4],'y': lk[z][i*4+1],'u': lk[z][i*4+2],'v': lk[z][i*4+3]}
            for i in range(int(len(lk[z])/4))] for z in range(len(lk))]


def calculate_a(points_j, point_i):
    summ_x = 0
    summ_y = 0
    for j, p in enumerate(points_j):
        r_3 = math.pow(
            math.pow(math.fabs(p[0] - point_i[0]), 2) + math.pow(math.fabs(p[1] - point_i[1]),
                                                                                 2), 3 / 2)
        summ_x += G*p[2] * (p[0] - point_i[0]) / r_3
        summ_y += G*p[2] * (p[1] - point_i[1]) / r_3
    return ([summ_x, summ_y])


def my_verle_for_xy(z, delta_t, a_prev):
    a = a_prev
    x_next = z[0] + z[2] * delta_t + 1 / 2 * a[0]
    y_next = z[1] + z[3] * delta_t + 1 / 2 * a[1]
    return (x_next, y_next)


def my_verle_for_uv(uv_prev, delta_t, a_prev, a_next):
    u_next = uv_prev[0] + 1 / 2 * (a_next[0] + a_prev[0]) * delta_t
    v_next = uv_prev[1] + 1 / 2 * (a_next[1] + a_prev[1]) * delta_t
    return (u_next, v_next)


def calculate_verle(particles, t_, delta_t):
    t = np.linspace(0, t_, t_ / delta_t + 1)
    all_coords = []
    coords = []
    for p in particles:
        coords.append([p.x, p.y, p.u, p.v])
    all_coords.append(coords)

    a = np.zeros((len(particles), 2))
    a_next = np.zeros((len(particles), 2))
    for k, tk in enumerate(t):
        if k !=0:
            coords = []
            for i, p in enumerate(particles):
                if tk == t[0]:
                    a[i, 0], a[i, 1] = calculate_a([[all_coords[k-1][j][0], all_coords[k-1][j][1],
                                                     pa.m] for j, pa in enumerate(particles) if j != i],
                                                   [all_coords[k-1][i][0], all_coords[k-1][i][1], p.m])
                lk = my_verle_for_xy([all_coords[k-1][i][0], all_coords[k-1][i][1],all_coords[k-1][i][2],all_coords[k-1][i][3]],
                                     delta_t, a[i])
                coords.append([lk[0], lk[1],0,0])
            for i, p in enumerate(coords):
                a_next[i, 0], a_next[i, 1] = calculate_a([[pa[0], pa[1], particles[j].m]
                                                          for j, pa in enumerate(coords) if j != i],
                                                         [p[0], p[1], particles[i].m])
                lk = my_verle_for_uv([all_coords[k-1][i][2], all_coords[k-1][i][3]], delta_t, a[i], a_next[i])
                coords[i][2], coords[i][3] = lk[0], lk[1]
            all_coords.append(coords)
            a = copy.deepcopy(a_next)

    return [[{'x': p[0], 'y': p[1], 'u': p[2], 'v': p[3]} for p in c] for c in all_coords]
