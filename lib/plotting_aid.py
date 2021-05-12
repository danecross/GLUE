

# returns plottable points of axes from eigenvectors
def plot_axes_from_evecs_2D(evecs, length, origin=None):
        
    if origin is None:
        origin = [0]*len(evecs)
    
    try:
        length = list(length)
    except TypeError:
        length = [length]*len(evecs)
    
    return [line_from_vector(v, l, start=origin) for v,l in zip(evecs, length)]
    

# returns plottable start/end points of a line defined by a vector
def line_from_vector(v, length, start=None):
    
    if start is None: # start at origin
        start = [0]*len(v)

    v = normalize(v) 
    end = [v[i]*length+start[i] for i in range(len(v))]
    
    axes = [[start[i], end[i]] for i in range(len(v))]

    return axes

# normalizes the input vector
def normalize(v):

    V = sum([vi**2 for vi in v])**(1/2)
    return [vi/V for vi in v]




