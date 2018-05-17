import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 20
    polygons = []
    edges = []

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
        print commands

        for line in commands:
            if line[0] == 'push':
                stack.append( [ x[:] for x in stack[-1] ] )
                
            elif line[0] == 'pop':
                stack.pop()

            elif line[0] == 'move':
                trans = make_translate(float(line[1]), float(line[2]), float(line[3]))
                matrix_mult( stack[-1], trans )
                stack[-1] = [ x[:] for x in trans]

            elif line[0] == 'rotate':
                theta = float(line[2]) * (math.pi / 180)
                
                if line[1] == 'x':
                    trans = make_rotX(theta)
                elif line[1] == 'y':
                    trans = make_rotY(theta)
                else:
                    trans = make_rotZ(theta)
                    
                matrix_mult( stack[-1], trans )
                stack[-1] = [ x[:] for x in trans ] 

            elif line[0] == 'scale':
                trans = make_scale(float(line[1]), float(line[2]), float(line[3]))
                matrix_mult( stack[-1], trans )
                stack[-1] = [ x[:] for x in trans ]

            elif line[0] == 'box':
                add_box(polygons,
                        float(line[1]), float(line[2]), float(line[3]),
                        float(line[4]), float(line[5]), float(line[6]))
                matrix_mult( stack[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []

            elif line[0] == 'sphere':
                add_sphere(polygons,
                           float(line[1]), float(line[2]), float(line[3]),
                           float(line[4]), step_3d)
                matrix_mult( stack[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []

            elif line[0] == 'torus':
                add_torus(polygons,
                          float(line[1]), float(line[2]), float(line[3]),
                          float(line[4]), float(line[5]), step_3d)
                matrix_mult( stack[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []

            elif line[0] == 'line':
                add_edge( edges,
                          float(line[1]), float(line[2]), float(line[3]),
                          float(line[4]), float(line[5]), float(line[6]) )
                matrix_mult( stack[-1], edges )
                draw_lines(eges, screen, zbuffer, color)
                edges = []

            elif line[0] == 'save':
                save_extension(screen, line[1]+line[2])

            elif line[0] == 'display':
                display(screen)
            
            else:
                print "Parsing failed."
                return
            
