# coding: UTF-8
import yaml
import itertools

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
            

    
pred = Predicates()
CTX = Context()

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
{0.can_2s}
{0.can_s2}

{0.does_2s}
{0.does_s2}

{0.can_s2s}
{0.does_s2s}


## Connects at baseline
{0.can_2b}
{0.can_b2}

{0.does_2b}
{0.does_b2}

{0.can_b2b}
{0.does_b2b}


##############################################################
## Single-Glyph Substitutions
##

lookup plain_to_2s {{
    {0.plain_to_2s}
}} plain_to_2s; 

lookup plain_to_s2 {{
    {0.plain_to_s2}
}} plain_to_s2; 

lookup s2_to_s2s {{
    {0.s2_to_s2s}
}} s2_to_s2s;

lookup _2s_to_s2s {{
    {0._2s_to_s2s}
}} _2s_to_s2s;


## at baseline

lookup plain_to_2b {{
    {0.plain_to_2b}
}} plain_to_2b; 

lookup plain_to_b2 {{
    {0.plain_to_b2}
}} plain_to_b2; 

lookup b2_to_b2b {{
    {0.b2_to_b2b}
}} b2_to_b2b;

lookup _2b_to_b2b {{
    {0._2b_to_b2b}
}} _2b_to_b2b;


##############################################################
## 'calt' Passes
##

### Connects the unconnected.
lookup calt_pass_1 {{
    
    # at the Short height
    sub @can_2s' lookup plain_to_2s
        @can_s2' lookup plain_to_s2;

    # at the baseline
    sub @can_2b' lookup plain_to_2b
        @can_b2' lookup plain_to_b2;
}} calt_pass_1;


### Connects what's connected on one side already.
lookup calt_pass_2 {{
    
    # Short height
    sub @does_2s' lookup _2s_to_s2s
        @does_s2' lookup  s2_to_s2s;

    
    # at the baseline
    sub @does_2b' lookup _2b_to_b2b
        @does_b2' lookup  b2_to_b2b;
    
}} calt_pass_2;

lookup calt_pass_3 {{
    sub @does_s2s
        @can_s2'   lookup plain_to_s2;
    sub @does_b2b
        @can_b2'   lookup plain_to_b2;
}} calt_pass_3;


##############################################################
## Features
##

feature calt {{    
    lookup calt_pass_1;
    lookup calt_pass_2;
    lookup calt_pass_3;
}} calt;
"""

y = None
with open('glyphinfo.yaml') as f:
    y = f.read()
glyphs = list(yaml.safe_load(y))

def classnameize(names):
    return ' '.join(itertools.chain(["["], names, ["]"]))


####
## Baseline Height
# can/does start/end at baseline horizontally
can_b2  = [glyph['name'] for glyph in glyphs if pred.can_b2(glyph)]
does_b2 = [x + ".b2" for x in can_b2]
can_2b  = [glyph['name'] for glyph in glyphs if pred.can_2b(glyph)]
does_2b = [x + '.2b' for x in can_2b]

can_b2b  = [glyph['name'] for glyph in glyphs if pred.can_b2b(glyph)]
does_b2b = [x + ".b2b" for x in can_b2b]

can_b2b  = [glyph['name'] for glyph in glyphs if pred.can_b2b(glyph)]
does_b2b = [x + ".b2b" for x in can_b2b]


CTX.calt_pass_1_baseline_1 = \
    "\n    ".join("sub {} {}' by {};".format(classnameize(can_b2), can, does)
                  for can, does in zip(can_b2, does_b2))
CTX.calt_pass_1_baseline_2 = \
    '\n    '.join("sub {}' {} by {};".format(can, classnameize(can_2b), does)
                   for can, does in zip(can_2b, does_2b))

####
## Short Height



# can/does start/end at short height horizontally on one side only
can_s2  = [glyph['name'] for glyph in glyphs if pred.can_s2(glyph)]
does_s2 = [x + ".s2" for x in can_s2]
can_2s  = [glyph['name'] for glyph in glyphs if pred.can_2s(glyph)]
does_2s = [x + '.2s' for x in can_2s]

# can/does start/end at short height horizontally on both sides
can_s2s  = [glyph['name'] for glyph in glyphs if pred.can_s2s(glyph)]
does_s2s = [x + ".s2s" for x in can_s2s]



### lookups


CTX.plain_to_2s = \
    '\n    '.join("sub {} by {};".format(can, does) for can, does in zip(can_2s, does_2s))

CTX.plain_to_s2 = \
    '\n    '.join("sub {} by {};".format(can, does) for can, does in zip(can_s2, does_s2))

CTX.s2_to_s2s = \
    '\n    '.join("sub {}.s2 by {};".format(can, does) for can, does in zip(can_s2s, does_s2s))

CTX._2s_to_s2s = \
    '\n    '.join("sub {}.2s by {};".format(can, does) for can, does in zip(can_s2s, does_s2s))

## at baseline

CTX.plain_to_2b = \
    '\n    '.join("sub {} by {};".format(can, does) for can, does in zip(can_2b, does_2b))

CTX.plain_to_b2 = \
    '\n    '.join("sub {} by {};".format(can, does) for can, does in zip(can_b2, does_b2))

CTX.b2_to_b2b = \
    '\n    '.join("sub {}.b2 by {};".format(can, does) for can, does in zip(can_b2b, does_b2b))

CTX._2b_to_b2b = \
    '\n    '.join("sub {}.2b by {};".format(can, does) for can, does in zip(can_b2b, does_b2b))



### classes


CTX.can_2b =   "@can_2b = {};".format(classnameize(can_2b))
CTX.can_b2 =   "@can_b2 = {};".format(classnameize(can_b2))

CTX.does_2b =  "@does_2b = {};".format(classnameize(does_2b))
CTX.does_b2 =  "@does_b2 = {};".format(classnameize(does_b2))

CTX.can_b2b  = "@can_b2b = {};".format(classnameize(can_b2b))

CTX.does_b2b = "@does_b2b = {};".format(classnameize(does_b2b))




CTX.can_2s =   "@can_2s = {};".format(classnameize(can_2s))
CTX.can_s2 =   "@can_s2 = {};".format(classnameize(can_s2))

CTX.does_2s =  "@does_2s = {};".format(classnameize(does_2s))
CTX.does_s2 =  "@does_s2 = {};".format(classnameize(does_s2))

CTX.can_s2s  = "@can_s2s = {};".format(classnameize(can_s2s))

CTX.does_s2s = "@does_s2s = {};".format(classnameize(does_s2s))



print TEMPLATE.format(CTX)
