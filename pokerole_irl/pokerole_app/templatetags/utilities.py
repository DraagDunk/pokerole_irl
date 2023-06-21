from django import template

register = template.Library()


@register.simple_tag
def stat_graphic(base_stat, max_stat):
    stat_str = ""
    stat_str += "🔴"*base_stat
    stat_str += "⚪"*(max_stat-base_stat)
    return stat_str


@register.simple_tag
def calc_accuracy(move, pokemon):
    return move.calc_accuracy(pokemon)


@register.simple_tag
def calc_damage(move, pokemon):
    return move.calc_damage(pokemon)
