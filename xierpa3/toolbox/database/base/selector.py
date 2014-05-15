# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    selector.py
#
from xierpa3.toolbox.transformer import TX

class Rule:

    # Operators
    LT                     = '<'
    LE                     = '<='
    GT                     = '>'
    GE                     = '>='
    EQ                     = '='
    EQCASE                 = 'case insensitive equals' #this will be faked with ILIKE
    NE                     = '!='
    HAS                     = '~*'
    IN                     = 'in'
    IS                     = 'is'
    ISNOT                 = 'is not'
    LIKE                 = 'like'
    ILIKE                 = 'ilike' #case insensitive
    OPERATORS             = (LT, LE, GT, GE, EQ, NE, HAS, IN, IS, ISNOT, LIKE, ILIKE)

    # Values
    NULL                 = 'NULL'
    TRUE                 = 'TRUE'
    FALSE                 = 'FALSE'
    VALUES                 = (NULL, TRUE, FALSE)
    YEAR_T                 = "date_part('year', %s)"
    MONTH_T                 = "date_part('month', %s)"
    
    def __init__(self, field, operator=None, value=None):
        self.field = field
        self.operator = operator
        
        if isinstance(value,bool):
            self.value = value and self.TRUE or self.FALSE
        elif value is None:
            self.value = self.NULL
        else:
            self.value = value

        if operator == Rule.IN and not isinstance(self.value,(list,tuple,set)):
            self.value = [self.value]

    def __repr__(self):
        return "Rule(" + self.getClause().encode('utf-8') + ")"

    def getClause(self):
        u"""
        <doc>
        The <code>getClause</code> answers the where clause of the rule. If the result of the clause is
        empty, then answer <code>None</code>.
        </doc>
        """
        clause = []
        if self.field and self.operator:
            if self.operator == self.IN:
                clause.append(self.field)
                clause.append(self.operator)
                
                safevalues = []
                for v in self.value:
                    if isinstance(v,(int,float,long)):
                        v = str(v)
                    safevalues.append(TX.escapeSqlQuotes(v))
                    
                clause.append("('" + "','".join(safevalues) + "')")
            else:
                clause.append(self.field)
                if self.operator == self.EQCASE:
                    clause.append(self.ILIKE)
                else:
                    clause.append(self.operator)
                if self.value in self.VALUES or isinstance(self.value, (int, long, float)):
                    clause.append('%s' % self.value)
                elif not isinstance(self.value, basestring):
                    clause.append(u"'%s'" % TX.escapeSqlQuotes(`self.value`))
                else:
                    safe = TX.escapeSqlQuotes(self.value)
                    if self.operator == self.EQCASE:
                        #arbitrarily choose # as the escape char
                        safe = safe.replace('#','##').replace('%','#%').replace('_','#_')
                    clause.append(u"'%s'" % safe)
                    if self.operator == self.EQCASE:
                        clause.append(" ESCAPE '#'")
        
        return ' '.join(clause)

class Selector:

    def __init__(self, ruleset=None, andor='AND'):
        self.andor = andor
        self.ruleset = []
        if ruleset:
            if isinstance(ruleset, dict):
                # If there is an (args) dictionary defined, then use that to build the rules.
                for field, value in ruleset.items():
                    if value is None:
                        self.ruleset.append(Rule(field, Rule.IS, value))
                    else:
                        self.ruleset.append(Rule(field, Rule.EQ, value))
            else:
                if not isinstance(ruleset, (tuple, list)):
                    ruleset = [ruleset]
                for rule in ruleset:
                    self.append(rule)

    def __repr__(self):
        s = []
        for rule in self.getRuleSet():
            s.append(str(rule))
        return 'Selector(' + ' '.join(s) + ')'

    def getClause(self):
        u"""
        <doc>
        The <code>getClause</code> answers the where clause of the selector. If the result of the clause is
        empty, then answer <code>None</code>.
        </doc>
        """
        clause = []
        for rule in self.getRuleSet():
            clause.append(rule.getClause())
        return ' {0} '.format(self.andor).join(clause) or None

    def getRuleSet(self):
        u"""
        <doc>
        The <code>getRuleSet</code> answers the <code>self.ruleset</code> of the selector.
        </doc>
        """
        return self.ruleset

    def append(self, rule):
        if not isinstance(rule, Rule):
            rule = Rule(rule)
        self.ruleset.append(rule)
