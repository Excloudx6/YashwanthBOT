import discord
from yashparser import *
currency_abrv=""
currency_name=""
def set_currency(abrv, name):
    global currency_abrv, currency_name
    currency_abrv=abrv
    currency_name=name

    
    
def leader_board(ctx, player_stats, p1):
    tstr = ""
    embeded = discord.embeds.Embed()
    multi = 1 if p1 == "negrep" else -1

    method_type=None
    addition=""
    ending=p1
    print(p1, currency_abrv)

    if p1==currency_abrv:
        method_type=PlayerData.Coins.value
    elif p1 == "counts":
        method_type = PlayerData.Counts.value
    else:
        method_type = PlayerData.RepPoints.value
        ending="reputation points"

    for i, item in enumerate(sorted(player_stats.items(), key=lambda p: multi*p[1][method_type])):
        user = item[1][0]
        amt = item[1][method_type]
        if method_type==PlayerData.Coins.value:
            addition = lb_addition_parse(amt)
        tstr += "{}: <@!{}>, {:,.0f} {} {}\n".format(i + 1, item[0], amt, ending, addition) if "!" in item[
            0] else "{}: <@{}>, {:,.0f} {} {}\n".format(i + 1, item[0], amt, ending, addition)
        if i > 8:
            break
    embeded.add_field(name="Top 10", value=tstr)
    pos = 0
    for i, item in enumerate(sorted(player_stats.items(), key=lambda p: multi*p[1][method_type])):
        id = item[0]
        if id == ctx.message.author.id:
            pos = i + 1
    embeded.add_field(name="Your rank", value="Rank {}. You have {:,.0f} {}".format(pos, player_stats[
        ctx.message.author.id][method_type], ending), inline=False)
    return embeded



def return_parsed_floated_list(the_list):
    for i in range(len(the_list)):
        try:
            the_list[i] = float(the_list[i])
        except:
            pass
    for i in range(len(the_list)):
        try:
            the_list[i] = parse_config_params(the_list[i])
        except:
            pass
    return the_list
