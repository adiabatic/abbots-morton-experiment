FROM = 'they-qs'
TO   = 'she-qs'

from_layer = Font.glyphs[FROM].layers[0]
XHEIGHT = Font.masters[0].xHeight
WIDTH = Font.masters[0].widthValue

to_layer = Font.glyphs[TO].layers[0] = from_layer.copyDecomposedLayer()


for path in to_layer.paths:
    for node in path.nodes:
        # mess with node.x and node.y
        node.y += 400 # this is where the bottom ends

TO   = 'thaw-qs'

from_layer = Font.glyphs[FROM].layers[0]
XHEIGHT = Font.masters[0].xHeight
WIDTH = Font.masters[0].widthValue

to_layer = Font.glyphs[TO].layers[0] = from_layer.copyDecomposedLayer()


for path in to_layer.paths:
    for node in path.nodes:
        # mess with node.x and node.y
        node.y = XHEIGHT - node.y
        node.x = WIDTH   - node.x
        node.x += 4*WIDTH
