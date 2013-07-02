FROM = 'vie-qs'
TO   = 'fee-qs'

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
    # doesn't seem to work
    del(path.nodes[-1]) # get rid of tail

