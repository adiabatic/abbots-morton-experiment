FROM = 'braceleft'
TO   = 'braceright'


from_layer = Font.glyphs[FROM].layers[0]
XHEIGHT = Font.masters[0].xHeight
WIDTH = Font.masters[0].widthValue
WIDTH = 531

to_layer = Font.glyphs[TO].layers[0] = from_layer.copyDecomposedLayer()

print "width: {0}\nheight: {1}".format(WIDTH, XHEIGHT)


for path in to_layer.paths:
    for node in path.nodes:
        # mess with node.x and node.y
        node.x = WIDTH - node.x

