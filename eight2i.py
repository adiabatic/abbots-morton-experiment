eight_layer = Font.glyphs["eight-Qs"].layers[0]
i_layer = Font.glyphs['i-Qs'].layers[0] = eight_layer.copyDecomposedLayer()

XHEIGHT = 500
WIDTH = 600

for path in i_layer.paths:
    for node in path.nodes:
        # mess with node.x and node.y
        node.x = WIDTH - node.x
