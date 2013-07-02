FROM = 'low-qs'
TO   = 'llan-qs'

XHEIGHT = 500
WIDTH = 685

from_layer = Font.glyphs[FROM].layers[0]
to_layer = Font.glyphs[TO].layers[0] = from_layer.copyDecomposedLayer()


for path in to_layer.paths:
    for node in path.nodes:
        # mess with node.x and node.y
        node.x = WIDTH - node.x
