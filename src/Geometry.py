import math


def dot(vec1, vec2):
	dot_sum = 0
	for i in range(len(vec1)):
		dot_sum += vec1[i] * vec2[i]
	return dot_sum


def vector_diff(vec1, vec2):
	vec3 = []
	for i in range(len(vec1)):
		vec3.append(vec2[i] - vec1[i])
	return vec3


def point_in_rectangle(point, pa, pb, pc, pd):
	return (0 <= dot(vector_diff(pa, point), vector_diff(pa, pb)) <= dot(vector_diff(pa, pb), vector_diff(pa, pb))) and \
		   (0 <= dot(vector_diff(pa, point), vector_diff(pa, pd)) <= dot(vector_diff(pa, pd), vector_diff(pa, pd)))


def point_distance_line(point, pa, pb):
	a = pa[1] - pb[1]
	b = pb[0] - pa[0]
	c = (pa[0] - pb[0])*pa[1] + (pb[1] - pa[1])*pa[0]
	return abs(a*point[0] + b*point[1] + c) / math.sqrt(a**2 + b**2)


def perpendicular_intersection_point(pa, pb, point):
	if pb[0] - pa[0] == 0:
		return pa[0], point[1]
	slope = (pb[1] - pa[1]) / (pb[0] - pa[0])
	b = pa[1] - slope*pa[0]
	if slope == 0:
		return point[0], pa[1]
	perp_slope = -1 / slope
	perp_b = point[1] - perp_slope*point[0]
	x_int = (perp_b - b) / (slope - perp_slope)
	y_int = perp_slope*x_int + perp_b
	return x_int, y_int


def point_distance_point(pa, pb):
	return math.sqrt((pb[0] - pa[0])**2 + (pb[1] - pa[1])**2)

def circle_intersect_lineseg(center, radius, pa, pb):
	point = perpendicular_intersection_point(pa, pb, center)
	if max(pa[0], pb[0]) >= point[0] >= min(pa[0], pb[0]) and max(pa[1], pb[1]) >= point[1] >= min(pa[1], pb[1]):
		return point_distance_point(point, center) < radius


def circle_intersect_line(center, radius, pa, pb):
	return point_distance_line(center, pa, pb) < radius


def circle_intersect_rectangle(pcirc, radius, pa, pb, pc, pd):
	return (point_in_rectangle(pcirc, pa, pb, pc, pd) or
			circle_intersect_lineseg(pcirc, radius, pa, pb) or
			circle_intersect_lineseg(pcirc, radius, pb, pc) or
			circle_intersect_lineseg(pcirc, radius, pc, pd) or
			circle_intersect_lineseg(pcirc, radius, pd, pa))