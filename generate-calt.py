# coding: UTF-8
import yaml
import itertools

TEMPLATE = """
# Glyph names and lookup names must be:
# - up to 31 characters
# - be comprised of A-Z a-z 0-9 . _
# - must not start with a digit or period (underscores OK)

# glyph names and lookup names can be 31 characters;
# glyph class names (lists) max out at 30.

##############################################################
## Glyph Classes
##

## Connects at Short
{0[can_2s]}
{0[can_s2]}

{0[does_2s]}
{0[does_s2]}

{0[can_s2s]}
{0[does_s2s]}


## Connects at baseline
{0[can_2b]}
{0[can_b2]}

{0[does_2b]}
{0[does_b2]}

{0[can_b2b]}
{0[does_b2b]}


## Diagonal Connections
{0[can_s2b]}
{0[can_b2s]}



##############################################################
## 'calt' Passes
##

# figure out when we should use:
# - no vs. upside-down-no
# - utter vs. alternate-utter
# - fee that starts at the top left and ends at Short vs. starts at Short and doesn't end
# - etc.
lookup determine_variants {{
    sub no-qs it-qs no-qs'      by no-qs.alt;
    sub she-qs      no-qs'      by no-qs.alt;
    sub no-qs.alt   no-qs'      by no-qs.alt;
    sub it-qs it-qs no-qs'      by no-qs.alt;
}} determine_variants;



### Connects the unconnected.
lookup calt_pass_1 {{

    {0[calt_pass_1]}
        
}} calt_pass_1;



#lookup calt_pass_2 {{
    

#}} calt_pass_2;


##############################################################
## Features
##

feature calt {{
    lookup determine_variants;
    lookup calt_pass_1;
#    lookup calt_pass_2;
}} calt;
"""

class Context(object): pass

class Predicates(object):
    
    @classmethod
    def _any_cxn(self, pred, glyph):
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
    def _has_given_connection(self, glyph, left_height, right_height):
        for cset in glyph['connection sets']:
            have_lhs = False
            have_rhs = False
            for cxn in cset:
                try:
                    if cxn['side'] == 'left'  and cxn['height'] == left_height: have_lhs = True
                    if cxn['side'] == 'right' and cxn['height'] == right_height: have_rhs = True
                except: pass
                if have_lhs and have_rhs: return True
        return False
            

    @classmethod
    def can(self, glyph, s):
        """Return True if glyph can connect like s. (s might be things like "b2s".)"""
        return getattr(self, 'can_'+s)(glyph)
    
    @classmethod
    def can_s2(self, glyph):
        def f(cxn):
            return cxn.get('side') == 'left' and cxn.get('height') == 'short'
        return self._any_cxn(f, glyph)
        
    @classmethod
    def can_2s(self, glyph):
        def f(cxn): return cxn.get('side') == 'right' and cxn.get('height') == 'short'
        return self._any_cxn(f, glyph)
            
    @classmethod
    def can_s2s(self, glyph):
        return self._has_given_connection(glyph, 'short', 'short')
            
    @classmethod
    def can_s2b(self, glyph):
        return self._has_given_connection(glyph, 'short', 'baseline')
            
    @classmethod
    def can_b2(self, glyph):
        def f(cxn):
            return cxn.get('side') == 'left' and cxn.get('height') == 'baseline'
        return self._any_cxn(f, glyph)
        
    @classmethod
    def can_2b(self, glyph):
        def f(cxn): return cxn.get('side') == 'right' and cxn.get('height') == 'baseline'
        return self._any_cxn(f, glyph)
            
    @classmethod
    def can_b2b(self, glyph):        
        return self._has_given_connection(glyph, 'baseline', 'baseline')            

    @classmethod
    def can_b2s(self, glyph):
        return self._has_given_connection(glyph, 'baseline', 'short')
            
            
def flatten_once(lol):
    return itertools.chain.from_iterable(lol)


def stringize(connection):
    if not connection: return ''
    
    angle = connection['angle']
    height = connection['height']
    side = connection['side']
    
    if angle != 'horizontal':
        raise NotImplementedError
    if height == 'short':
        if side == 'left':
            return 's2'
        elif side == 'right':
            return '2s'
        else:
            raise ValueError('side neither left nor right')
    elif height == 'baseline':
        if side == 'left':
            return 'b2'
        elif side == 'right':
            return '2b'
        else:
            raise ValueError('side neither left nor right')
    else:
        raise ValueError('height neither short nor baseline')


def can_connect(lhs, rhs):
    """Return True if the lhs string (say, "2b") can connect to the rhs (say, "b2")."""
    if lhs.endswith('2b') and rhs.startswith('b2'): return True
    if lhs.endswith('2s') and rhs.startswith('s2'): return True
    return False

def could_connect_rhs(lhs, glyph, rhs):
    """Return a string like "b2s" or "s2b" that would connect to lhs when placed on rhs.
    
    lhs should be a string like "2b"; rhs should be a string like no-qs or no-qs.2b.
    
    Return '' if lhs and rhs can't connect."""
    
    for cset in glyph['connection sets']:
        if len(cset) <= 1: continue
        
    

pred = Predicates()
CTX = {}



y = None
with open('glyphinfo.yaml') as f:
    y = f.read()
glyphs = list(yaml.safe_load(y))

def classnameize(names):
    return ' '.join(itertools.chain(["["], names, ["]"]))


GLYPHS = {}
connection_types = "2b b2 b2b 2s s2 s2s b2s s2b".split()

for cxn in connection_types:
    GLYPHS['can_'+cxn] = \
        [glyph['name'] for glyph in glyphs if pred.can(glyph, cxn)]
    GLYPHS['does_'+cxn] = [x + '.' + cxn for x in GLYPHS['can_'+cxn]]
        



### classes

for style in connection_types:
    CTX['can_'+style]  = "@can_{} = {};".format(style, classnameize(GLYPHS['can_'+style]))
    CTX["does_"+style] = "@does_{} = {};".format(style, classnameize(GLYPHS['does_'+style]))



### calt pass 1

subs = []

for glyph, cxn in itertools.product(glyphs, "2s 2b".split()):
    if pred.can(glyph, cxn):
        name = glyph['name']
        name_to = name.replace('.alt.', '')
        subs.append("sub {0:<12} @can_{1} by {2}.{1};".format(name+"'", cxn, name_to))

CTX['calt_pass_1'] =  '\n    '.join(subs)



### calt pass 2

subs = []
for glyph, previous_attr in itertools.product(glyphs, ['', '2s', '2b']):
    name = glyph['name']
    if not previous_attr:
        print
        print "    #", name
        continue
    cxns = flatten_once(glyph['connection sets'])
    cxns = [k for k, v in itertools.groupby(sorted(cxns))]
    cxns.insert(0, {})
    for cxn in cxns:
        if can_connect(previous_attr, stringize(cxn)): continue
        cxn_s = stringize(cxn)
        if cxn_s: cxn_s = "." + cxn_s
        from_name = "{}{}'".format(name, cxn_s)
        print "    sub @can_{:<12} {:<14} by ...;".format(previous_attr, from_name, stringize(cxn))

    


#print TEMPLATE.format(CTX)






        
    

def connection_types_for(g, h):
    """
    g and h are glyph objects.
    Return a list of 2-tuples that describe the left and right connection types that 
    the pair can use, like:
    
    [
        (
            dict(side=left,  height=short, angle=horizontal),
            dict(side=right, height=short, angle=horizontal)
        )
    ]
    
    Returns an empty list if nothing matches (say, for "roe it").
    BUG: needs a way to specify partially connecting glyphs for a second pass.
    """
    cxns = []
    for gset, hset in itertools.product(g['connection sets'], h['connection sets']):
        for gcxn, hcxn in zip(gset, hset):
            if gcxn['height'] == hcxn['height'] and \
               gcxn['angle']  == hcxn['angle']  and \
               gcxn['side'] == 'left' and hcxn['side'] == 'right':
                cxns.append((gcxn, hcxn))
    return cxns
