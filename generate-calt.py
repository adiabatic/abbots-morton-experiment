# coding: UTF-8
import yaml
import itertools

class Context(object): pass

class Predicates(object):
    
    @classmethod
    def _generic(self, pred, glyph):
        r = False
        try:
            cxns = itertools.chain.from_iterable(glyph['connection sets'])
            for cxn in cxns:
                if pred(cxn):
                    r = True
                    break
        except: pass
        return r

    @classmethod
    def can_s2(self, glyph):
        def f(cxn):
            return cxn.get('side') == 'left' and cxn.get('height') == 'short'
        return self._generic(f, glyph)
        
    @classmethod
    def can_2s(self, glyph):
        def f(cxn): return cxn.get('side') == 'right' and cxn.get('height') == 'short'
        return self._generic(f, glyph)
            
    @classmethod
    def can_b2(self, glyph):
        def f(cxn):
            return cxn.get('side') == 'left' and cxn.get('height') == 'baseline'
        return self._generic(f, glyph)
        
    @classmethod
    def can_2b(self, glyph):
        def f(cxn): return cxn.get('side') == 'right' and cxn.get('height') == 'baseline'
        return self._generic(f, glyph)
            

    
pred = Predicates()
CTX = Context()

TEMPLATE = """
lookup plain_to_2s {{
    {0.plain_to_2s}
}} plain_to_2s; 

lookup plain_to_s2 {{
    {0.plain_to_s2}
}} plain_to_s2; 

feature calt {{

    {0.can_2s}
    {0.can_s2}
    
    {0.does_2s}
    {0.does_s2}
    
    ###############################
    ## Pass 1: Connecting the Unconnected
    ##
    
    # at the baseline
    {0.calt_pass_1_baseline_1}

    {0.calt_pass_1_baseline_2}

    
    # at the Short height
    sub @can_2s @can_s2' lookup plain_to_s2;
    sub @can_2s' lookup plain_to_2s @can_s2;
    
    ###############################
    ## Pass 2: Upgrading the Half-Connected
    ##
    
    sub @does_2s @can_s2' lookup plain_to_s2;
    sub @can_2s' lookup plain_to_2s @does_s2;
    {0.calt_pass_2}
}} calt;
"""

y = None
with open('glyphinfo.yaml') as f:
    y = f.read()
glyphs = list(yaml.safe_load(y))

def classnameize(names):
    return ' '.join(itertools.chain(["["], names, ["]"]))




def new_can2b(glyph):
    r = False
    try:
        cxns = itertools.chain.from_iterable(glyph['connection sets'])
        for cxn in cxns:
            if cxn.get('side') == 'right' and cxn.get('height') == 'baseline':
                r = True
                break
    except: pass
    return r

####
## Baseline Height
# can/does start/end at baseline horizontally
can_b2  = [glyph['name'] for glyph in glyphs if pred.can_b2(glyph)]
does_b2 = [x + ".b2" for x in can_b2]
can_2b  = [glyph['name'] for glyph in glyphs if pred.can_2b(glyph)]
does_2b = [x + '.2b' for x in can_2b]


CTX.calt_pass_1_baseline_1 = \
    "\n    ".join("sub {} {}' by {};".format(classnameize(can_b2), can, does)
                  for can, does in zip(can_b2, does_b2))
CTX.calt_pass_1_baseline_2 = \
    '\n    '.join("sub {}' {} by {};".format(can, classnameize(can_2b), does)
                   for can, does in zip(can_2b, does_2b))

####
## Short Height



# can/does start/end at short height horizontally
can_s2  = [glyph['name'] for glyph in glyphs if pred.can_s2(glyph)]
does_s2 = [x + ".s2" for x in can_s2]
can_2s  = [glyph['name'] for glyph in glyphs if pred.can_2s(glyph)]
does_2s = [x + '.2s' for x in can_2s]

### lookups
CTX.plain_to_2s = \
    '\n    '.join("sub {} by {};".format(can, does) for can, does in zip(can_2s, does_2s))

CTX.plain_to_s2 = \
    '\n    '.join("sub {} by {};".format(can, does) for can, does in zip(can_s2, does_s2))

### classes
CTX.can_2s = "@can_2s = {};".format(classnameize(can_2s))
CTX.can_s2 = "@can_s2 = {};".format(classnameize(can_s2))
CTX.does_2s = "@does_2s = {};".format(classnameize(does_2s))
CTX.does_s2 = "@does_s2 = {};".format(classnameize(does_s2))


# don't bug me now
CTX.calt_pass_2 = ''

print TEMPLATE.format(CTX)
