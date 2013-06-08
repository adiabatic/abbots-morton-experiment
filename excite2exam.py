FROM = 'excite-Qs'
TO   = 'exam-Qs'

from_layer = Font.glyphs[FROM].layers[0]
XHEIGHT = Font.masters[0].xHeight
WIDTH = Font.masters[0].widthValue
WIDTH = 550

to_layer = Font.glyphs[TO].layers[0] = from_layer.copyDecomposedLayer()


for path in to_layer.paths:
    for node in path.nodes:
        # mess with node.x and node.y
        node.y = XHEIGHT - node.y
        node.x = WIDTH   - node.x

