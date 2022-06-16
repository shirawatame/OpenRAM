# See LICENSE for licensing information.
#
# Copyright (c) 2016-2021 Regents of the University of California
# Santa Cruz
# All rights reserved.
#
import re


class baseSection:
    """
    This is the base section class for other section classes to inherit.
    It is also used as the top most section.
    """

    children = []

    def expand(self, dict, fd):
        for c in self.children:
            c.expand(dict, fd)


class loopSection(baseSection):
    """
    This section is for looping elements. It will repeat the children
    sections based on the key list.
    """
    def __init__(self, var, key):
        self.var = var
        self.key = key

    def expand(self, dict, fd):
        for ind in dict[self.key]:
            dict[self.var] = ind
            for c in self.children:
                c.expand(dict, fd)
        if self.var in dict:
            del dict[self.var]


class conditionalSection(baseSection):
    """
    This class will conditionally print it's children based on the 'cond'
    element.
    """
    def __init__(self, cond):
        self.cond = cond

    def expand(self, dict, fd):
        run = eval(self.cond, dict)
        if run:
            for c in self.children:
                c.expand(dict, fd)


class textSection(baseSection):
    """
    This is plain text section. It can contain parameters that can be
    replaced based on the dictionary.
    """

    def __init__(self, text):
        self.text = text

    def expand(self, dict, fd):
        varRE = re.compile('\{\{ (\S*) \}\}')
        vars = varRE.finditer(self.text)
        newText = self.text
        for var in vars:
            newText = newText.replace('{{ ' + var.group(1) + ' }}', str(dict[var.group(1)]))
        print(newText, end='', file=fd)


class template:
    """
    The template class will read a template and generate an output file
    based on the template and the given dictionary.
    """

    def __init__(self, template, dict):
        self.template = template
        self.dict = dict

    def readTemplate(self):
        lines = []
        with open(self.template, 'r') as f:
            lines = f.readlines()

        self.baseSectionSection = baseSection()
        sections = []
        context = [self.baseSectionSection]
        forRE = re.compile('\{% for (\S*) in (\S*) %\}')
        endforRE = re.compile('\{% endfor %\}')
        ifRE = re.compile('\{% if (.*) %\}')
        endifRE = re.compile('\{% endif %\}')
        for line in lines:
            m = forRE.match(line)
            if m:
                section = loopSection(m.group(1), m.group(2))
                sections.append(section)
                context[-1].children.append(section)
                context.append(section)
                continue
            m = ifRE.match(line)
            if m:
                section = conditionalSection(m.group(1))
                section.append(section)
                context[-1].children.append(section)
                context.append(section)
                continue
            if endforRE.match(line) or endifRE.match(line):
                context.pop()
            else:
                context[-1].children.append(textSection(line))

    def write(self, filename):
        fd = open(filename, 'w')
        self.readTemplate()
        self.baseSectionSection.expand(self.dict, fd)
        fd.close()
