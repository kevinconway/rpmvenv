############### External Macros ################
{% for macro_name, macro_value in macros.items() %}# {{ macro_name }}: {{ macro_value }}
{% endfor %}
################################################

############### Local Macros ###################
{% for define_name, define_value in defines.items() %}%define {{ define_name }} {{ define_value }}
{% endfor %}
################################################

############### Globals ########################
{% for global_name, global_value in globals.items() %}%global {{ global_name }} {{ global_value }}
{% endfor %}
################################################

############### Tags ###########################
{% for tag_name, tag_value in tags.items() %}{{ tag_name}}: {{ tag_value }}
{% endfor %}
################################################

############### Sections #######################
{% for block_name, block_lines in blocks.items() %}%{{ block_name }}
{% for block_line in block_lines %}{{ block_line }}
{% endfor %}
{% endfor %}
################################################
