import nengo

import ccm
import ccm.lib.grid
import ccm.lib.continuous

mymap="""
################
#              #
#              #
#              #
######### ######
#     #        #
#     #     #  #
#           #  #
################
"""

class Cell(ccm.lib.grid.Cell):
    def color(self):
        return 'black' if self.wall else 'white'
    def load(self, char):
        if char == '#':
            self.wall = True

world = ccm.lib.grid.World(Cell, map=mymap, directions=4)

body = ccm.lib.continuous.Body()
world.add(body, x=3, y=3)


def environment(t, x):
    
    speed, rotation = x
    dt = 0.001
    max_speed = 30.0
    max_rate = 5.0
    body.turn(rotation*dt* max_rate)
    body.go_forward(speed*dt * max_speed)
    
    cells = []
    for i in range(world.width):
        for j in range(world.height):
            cells.append('<rect x=%d y=%d width=1 height=1 style="fill:%s"/>' %
                (i, j, world.get_cell(i, j).color()))


    direction = body.dir * 360.0 / world.directions
    agent = '<polygon points="0.25,0.25 -0.25,0.25 0,-0.5" style="fill:blue" transform=" translate(%f,%f) rotate(%f)"' % (body.x+0.5, body.y+0.5, direction)
    svg = '''<svg width="100%%" height="100%%" viewbox="0 0 %d %d">
        %s
        %s
        </svg>''' % (world.width, world.height, ''.join(cells), agent)
    
    
    environment._nengo_html_ = svg
    
    
    


model = nengo.Network()
with model:
    env = nengo.Node(environment, size_in=2)

    control = nengo.Node([0, 0])
    nengo.Connection(control, env)