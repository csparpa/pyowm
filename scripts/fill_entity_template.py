#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__':

    import sys
    from jinja2 import Template

    param_1 = sys.argv[1]
    entity_name = param_1.title()

    try:
        param_2 = sys.argv[2]
        is_iterable = param_2 == '--iterable'
    except:
        is_iterable = False

    with open('new_entity.template.txt') as i:
        tpl = Template(i.read())
        rendered_text = tpl.render(entity_name=entity_name, is_iterable=is_iterable)
        with open('{}.py'.format(entity_name.lower()), 'w') as o:
            o.write(rendered_text)
