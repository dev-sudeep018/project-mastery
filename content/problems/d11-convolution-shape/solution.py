import numpy as np


def _integer(value, minimum=1):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < minimum:
        raise ValueError("Expected an integer in the allowed range")
    return int(value)


def conv_output_shape(shape, kernel, stride, padding, dilation):
    values = []
    for index, pair in enumerate((shape,kernel,stride,padding,dilation)):
        if not isinstance(pair, (tuple,list)) or len(pair) != 2:
            raise ValueError("Every parameter needs two axes")
        values.append([_integer(v, 0 if index == 3 else 1) for v in pair])
    shape,kernel,stride,padding,dilation = values
    output = []
    for n,k,s,p,d in zip(shape,kernel,stride,padding,dilation):
        span = n+2*p-d*(k-1)-1
        if span < 0:
            raise ValueError("Effective kernel does not fit")
        output.append(span//s+1)
    return tuple(output)
