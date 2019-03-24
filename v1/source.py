"""
The MIT License (MIT)
Copyright (c) 2019 bebe morse#9433
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

######### SERVER BOT TEMPLATE (THIS IS A YASHWANTH BOT) #########
##  CODE WRITTEN BY bebe morse#9433 , 2019. PLEASE GIVE CREDIT IF USING THIS CODE IN YOUR OWN PROJECT ##
## CODE OVERVIEW ##
# 1. If you have not already run setup.py, do so (you must only do so once)
# 2. Configure the config.ini to suit your server (you can get ids by right clicking on something in discord developer mode).
# 3. This bot was not designed for multi-server usage, please customize it for your own server, however you may adapt it to make it multiserver.


### IMPORTS ###
import discord, json, asyncio, math, datetime, time, configparser
from yashparser import *
from methods import *
from discord.ext import commands
from discord.utils import get


################
### ENUMERATIONS ARE CONTAINED WITHIN YASHPARSER
###################


### load config variables
cfg = configparser.ConfigParser()
cfg.read("config.ini")

def map_sections(section, parse_num):
    options, options_dict = cfg.options(section), {}
    for option in options:
        try:
            # special cases
            if option == "desc":
                options_dict[option] = cfg.get(section, option)
            else:
                b1 = cfg.get(section, option).split("!")
                for b in range(len(b1)):
                    b1[b] = b1[b].split("|")
                ndict = {}
                if len(b1) > 1:
                    for ele in b1:
                        splitted_ele = return_parsed_floated_list(ele[1].split(","))
                        ndict[parse_config_params(ele[0])] = splitted_ele
                if len(ndict) == 0:
                    obj = cfg.get(section, option).split(",")
                    if parse_num:
                        obj = return_parsed_floated_list(obj)
                    options_dict[option] = obj if len(obj) > 1 else obj[0]
                else:
                    options_dict[option] = ndict
        except:
            options_dict[option] = None
    return options_dict


config_ids = map_sections(section="config_ids", parse_num=False)
bot_config = map_sections(section="config", parse_num=False)
economy_map = map_sections(section="economy", parse_num=True)
job_map = map_sections(section="jobs", parse_num=True)
shop_map = map_sections(section="shop", parse_num=True)

###  CONFIGURATION VARIABLES ###

main_channel_id = config_ids[IdParser.MainBotChannel.value]
counting_id = config_ids[IdParser.CountingChannel.value]
counting_milestones_id = config_ids[IdParser.CountingMilestones.value]
disabled_channels = config_ids[IdParser.DisabledChannels.value]
serverid = config_ids[IdParser.Server.value]
food_bank_id = config_ids[IdParser.FoodBank.value]
purchase_log_id = config_ids[IdParser.PurchaseLog.value]

token = bot_config[BotConfigParser.Token.value]
bot_id = bot_config[BotConfigParser.BotID.value]
owner_id = bot_config[BotConfigParser.OwnerID.value]
bot_description = bot_config[BotConfigParser.Description.value]
command_prefix = bot_config[BotConfigParser.Prefix.value]

### CONFIGURE SHOP ###
shop_items = shop_map["items"]

## CONFIGURE JOBS ##
tiers = job_map[JobParser.Tiers.value]
job_cooldown = job_map[JobParser.JobCooldown.value]
role_multiplier = job_map[JobParser.RoleMultiplier.value]
base_multiplier = job_map[JobParser.BaseMultiplier.value]

### VARIABLE DECLARATIONS ###
bot = commands.Bot(command_prefix=command_prefix, description=bot_description, owner_id=int(owner_id))
done = False  # for counting buffer
OT = datetime.datetime.now()
milestone_dict = {}
##############################


#### CURRENCY VARIABLES ####
currency_abrv = economy_map[EconomyParser.CurrencyAbbreviation.value]
currency_name = economy_map[EconomyParser.CurrencyName.value]
set_currency(currency_abrv, currency_name)
guess_reward = int(economy_map[EconomyParser.Guess.value])
trivia_reward = int(economy_map[EconomyParser.Trivia.value])
small_milestone = int(economy_map[EconomyParser.SmallMilestone.value])
medium_milestone = int(economy_map[EconomyParser.MediumMilestone.value])
large_milestone = int(economy_map[EconomyParser.LargeMilestone.value])
counts_milestone = int(economy_map[EconomyParser.CountsMilestone.value])
anagram_reward = int(economy_map[EconomyParser.Anagram.value])
compound_interest = economy_map[EconomyParser.CompoundInterest.value]
loan_dpr = economy_map[EconomyParser.LoanInterest.value]
bank_value = int(economy_map[EconomyParser.BankValue.value])
daily_range = economy_map[EconomyParser.DailyRange.value]
work_range = economy_map[EconomyParser.WorkRange.value]
roles = economy_map[EconomyParser.Roles.value]
tax = economy_map[EconomyParser.Tax.value]
gamble_tax = economy_map[EconomyParser.GambleTax.value]
rcoin_range=economy_map[EconomyParser.CoinRange.value]
rcoin_time=economy_map[EconomyParser.CoinTime.value]
#######################


### FILES OPENING AND CLOSING

# open the current number file stored within dat, which loads the last number said in #counting
with open("dat/currentnumber.txt", "r") as f:
    currentnumber = int(f.read())

# the anagram word list.
with open("dat/wordlist.txt", "r") as f:
    wordlist = f.read().split("\n")
    wordlist = [v if len(v) >= 3 and len(v) <= 7 else None for v in wordlist]
    wordlist = list(filter(None, wordlist))  ## makes the anagram bit a bit easier

#facts that yashwanth says
with open("dat/facts.txt", "r") as f:
    rows = f.readlines()

# swears list that yashwanths uses with -dirtytalk
with open("dat/swears.txt", "r") as f:
    swears = f.readlines()

# trivia list for -trivia. aiken system
with open("dat/trivia.txt", "r") as f:
    triviaL = f.readlines()

# food image list. some are broken. find a better one if you can
with open("dat/foodIU.txt", "r") as f:
    foods = f.readlines()

# daily stuff. i should store this all in one dictionary this is not a good way of doing it you can change it if you want
with open("dat/claimedusers.txt", "r") as f:
    claimedusers = f.read().split(",")
with open("dat/dailyreps.txt", "r") as f:
    dreps = f.read().split(",")
with open("dat/dailynegreps.txt", "r") as f:
    dnreps = f.read().split(",")

# load stats and job informations
with open("dat/stats.txt", "r") as f:
    player_stats = json.loads(f.read())
with open("dat/jobs.txt", "r") as f:
    player_jobs = json.loads(f.read())


## PLAYER DATA ##
def write_data(stat):
    with open("dat/stats.txt", "w") as f:
        f.write(json.dumps(stat))


async def check_for_player_data(id, name):
    try:
        player_stats[id]
    except:
        if name != "":
            player_stats[id] = [name, 0, 0, 0, 0, 0, 0]
        else:
            get_name = await bot.get_user_info(id)
            player_stats[id] = [get_name.name, 0, 0, 0, 0, 0, 0]


async def add_data(amt, id, user_name, data_type):
    await check_for_player_data(id, user_name)
    player_stats[id][data_type] += int(amt)
    if user_name != "":
        player_stats[id][PlayerData.Name.value] = user_name
    write_data(player_stats)


###############

bot.remove_command("help")


### ASYNCRHOONOUS METHODS ###

## random interval free yashcoin
## every so often (as perscribed in config) yashwanth will say 'next person gets this much yashcoin'
async def random_getyash():
    await bot.wait_until_ready()
    try:
        lobby = bot.get_channel(id=main_channel_id)

        while not bot.is_closed:
            await asyncio.sleep(random.randint(rcoin_time[0], rcoin_time[1]))
            amt = random.randint(rcoin_range[0], rcoin_range[1])
            await bot.send_message(destination=lobby,
                                   content="The next person to talk in this channel gets {} {}".format(amt,
                                                                                                       currency_name))
            next = await bot.wait_for_message(channel=lobby)
            await add_data(amt, next.author.id, next.author.name, PlayerData.Coins.value)
            await bot.send_message(destination=lobby,
                                   content="{} has been awarded {} {}".format(next.author.name, amt, currency_name))
    except:
        pass


async def minutely():
    await bot.wait_until_ready()
    while not bot.is_closed:
        for uid, info in player_stats.items():
            await add_data(info[PlayerData.Gen.value], uid, "", PlayerData.Coins.value)
        with open("dat/statsbackup.txt", "w") as f:
            f.write(json.dumps(player_stats))
        await asyncio.sleep(60)


async def daily_reset():
    global claimedusers, dnreps, dreps, OT
    await bot.wait_until_ready()
    while not bot.is_closed:
        if datetime.datetime.now().day != OT.day:
            claimedusers = []
            dreps = []
            dnreps = []
            with open("dat/claimedusers.txt", "w") as f:
                f.write("")
            with open("dat/dailyreps.txt", "w") as f:
                f.write("")
            with open("dat/dailynegreps.txt", "w") as f:
                f.write("")
            for uid, items in player_stats.items():
                player_stats[uid][PlayerData.Bank.value] = math.ceil(
                    (1 + compound_interest) * player_stats[uid][PlayerData.Bank.value])
                player_stats[uid][PlayerData.Loan.value] = math.ceil(
                    (1 + loan_dpr) * player_stats[uid][PlayerData.Loan.value])

            write_data(player_stats)
        OT = datetime.datetime.now()
        await asyncio.sleep(60)


async def check_rep():
    global player_stats
    await bot.wait_until_ready()
    this_server = bot.get_server(serverid)
    role = get(bot.get_server(serverid).roles, name="negative rep")
    while not bot.is_closed:
        for userss in this_server.members:
            if "negative rep" in [u.name.lower() for u in userss.roles]:
                try:
                    b = player_stats[userss.id][PlayerData.RepPoints.value]
                    if b >= 0:
                        await bot.remove_roles(userss, role)
                except:
                    pass
            else:
                try:
                    b = player_stats[userss.id][PlayerData.RepPoints.value]
                    if b < 0:
                        await bot.add_roles(userss, role)
                except:
                    pass
        await asyncio.sleep(15)


####################


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    server = bot.get_server(serverid)

    bot.loop.create_task(daily_reset())
    bot.loop.create_task(check_rep())
    bot.loop.create_task(minutely())
    bot.loop.create_task(random_getyash())

    await bot.edit_channel(channel=bot.get_channel(counting_id), topic=str(currentnumber))

    await bot.change_presence(game=discord.Game(name="with a rubix cube"))


@bot.event
async def on_message(message):
    global currentnumber
    global done
    global milestone_dict

    print(message.author.name, message.content)

    if message.channel.id == counting_id:
        if message.author.id != bot_id:
            if not done:
                if random.randint(1, 100) != 1:
                    if message.content == str(currentnumber):
                        done = True
                        onetosend = currentnumber
                        currentnumber += 1
                        if currentnumber > 10000:
                            await bot.send_message(destination=bot.get_channel(counting_milestones_id),
                                                   content="Counting has reset to 1!")
                            currentnumber = 1
                        if onetosend % 100 == 0:
                            sorted_chances = sorted(milestone_dict.items(), key=lambda p: -p[1])
                            length = sum(x[1] for x in sorted_chances)
                            chance = random.randint(1, length)
                            concur = 0
                            for it in sorted_chances:
                                concur += it[1]
                                if concur >= chance:
                                    winnerid = it[0]
                                    percent = round((100 * it[1]) / (length), 2)
                                    break

                            if onetosend % 1000 == 0:
                                if onetosend % 10000 == 0:
                                    await add_data(large_milestone, winnerid, "", PlayerData.Coins.value)
                                    await bot.send_message(destination=bot.get_channel(counting_milestones_id),
                                                           content="<@{}> has reached a large milestone of {}! :tada: They had a {}% chance of getting this milestone"
                                                                   ":tada: They have been awarded {} {}".format(winnerid, onetosend, percent, large_milestone, currency_name))

                                else:
                                    await add_data(medium_milestone, winnerid, "", PlayerData.Coins.value)
                                    await bot.send_message(destination=bot.get_channel(counting_milestones_id),
                                                           content="<@{}> has reached a medium milestone of {}! :tada: They had a {}% chance of getting this milestone"
                                                                   ":tada: They have been awarded {} {}".format(winnerid, onetosend, percent, medium_milestone, currency_name))
                            else:
                                await add_data(small_milestone, winnerid, "", PlayerData.Coins.value)
                                await bot.send_message(destination=bot.get_channel(counting_milestones_id),
                                                       content="<@{}> has reached a small milestone of {}! :tada: They had a {}% chance of getting this milestone"
                                                                   ":tada: They have been awarded {} {}".format(winnerid, onetosend, percent, small_milestone, currency_name))
                            milestone_dict = {}

                        await bot.edit_channel(channel=message.channel, topic=str(currentnumber))
                        await add_data(1, message.author.id, message.author.name, PlayerData.Counts.value)
                        await progress_job("Count", message.author.id, message.author.name)

                        done = False
                        id = message.author.id
                        try:
                            milestone_dict[message.author.id] += 1
                        except:
                            milestone_dict[message.author.id] = 0
                        if player_stats[message.author.id][PlayerData.Counts.value] % 500 == 0:
                            await bot.send_message(destination=bot.get_channel("556394197284945931"),
                                                   content="<@{}> has reached {} counts! :tada: They have been awarded {} {}".format(message.author.id, player_stats[message.author.id][
                                                           PlayerData.Counts.value], counts_milestone, currency_name))
                            await add_data(counts_milestone, message.author.id, "", PlayerData.Coins.value)
                        with open("dat/currentnumber.txt", "w") as f:
                            f.write(str(currentnumber))
                    else:
                        await bot.delete_message(message)
                else:
                    await bot.delete_message(message)
            else:
                await bot.delete_message(message)
    if message.channel.id not in disabled_channels:
        await bot.process_commands(message)


async def progress_job(job_type, uid, name):
    global player_jobs
    try:
        if job_type == player_jobs[uid][3]:
            player_jobs[uid][1] += 1
            with open("dat/jobs.txt", "w") as f:
                f.write(json.dumps(player_jobs))
        if player_jobs[uid][1] >= player_jobs[uid][2]:
            print("why")
            await bot.send_message(destination=bot.get_channel(main_channel_id),
                                   content="Well done <@" + uid + ">. You've completed your job and earned " + str(
                                       player_jobs[uid][4]) + " " + currency_name + "!")
            await add_data(player_jobs[uid][4], uid, name,
                           PlayerData.Coins.value)
            del player_jobs[uid]
            with open("dat/jobs.txt", "w") as f:
                f.write(json.dumps(player_jobs))
    except:
        pass


@bot.command(pass_context=True)
async def fact(ctx, *args):
    await bot.say(random.choice(rows))


@bot.command(pass_context=True)
async def ship(ctx, *args):
    a1, a2 = "", ""
    try:
        a1 = args[0]
        a2 = args[1]
    except:
        pass

    s = 0
    for i, l in enumerate(a1):
        s += ord(l) * (i + 1)
    for i, l in enumerate(a2):
        s += ord(l) * (i + 1)

    s += 23 * (len(a1) + len(a2))
    s = s % 101
    embeded = discord.embeds.Embed()
    addition = ship_parse(s)
    embeded.add_field(name="Shipping " + a1 + " and " + a2, value=str(s) + "% " + addition, inline=False)
    await bot.say(embed=embeded)


@bot.command(pass_context=True)
async def dirtytalk(ctx, *args):
    totalStr = ""
    for x in range(5):
        totalStr += random.choice(swears) + " "
    await bot.say(totalStr)


@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def guess(ctx, *args):
    await bot.say('i have chosen a number between 1 and 10, it is your job to find it!')

    def is_correct(m):
        return m.author == m.author and m.content.isdigit()

    answer = random.randint(1, 10)
    try:
        guess = await bot.wait_for_message(timeout=5.0, check=is_correct, author=ctx.message.author)
    except asyncio.TimeoutError:
        return await bot.say('you took too long.. the answer is {}.'.format(answer))
    if int(guess.content) == answer:
        await bot.say(':tada: you got it! +' + str(guess_reward) + " " + currency_name + "! :tada:")
        await add_data(guess_reward, ctx.message.author.id, ctx.message.author.name, PlayerData.Coins.value)
    else:
        await bot.say('wrong! it is actually {}.'.format(answer))


@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def trivia(ctx, *args):
    choice = random.choice(triviaL)
    ctl = []
    cType = None
    try:
        cType = choice.split(":")[0]
    except:
        pass
    if cType != None:
        for x in triviaL:
            try:
                if x.split(":")[0] == cType:
                    ctl.append(x)
            except:
                pass

    ABCD = ["A", "B", "C", "D"]
    answer = choice.split("*")[1].capitalize()
    cores = random.choice(ABCD)
    ABCD.remove(cores)
    adict = {cores: answer}

    chosen_list = triviaL if len(ctl) < 10 else ctl

    for x in ABCD:
        adict[x] = random.choice(chosen_list).split("*")[1].capitalize()

    sortedkeys = sorted(adict.keys(), key=lambda x: x.lower())

    displayStr = ""
    for i in sortedkeys:
        displayStr += (i + ": " + adict[i] + "\n")

    embeded = discord.embeds.Embed()
    embeded.title = choice.split("*")[0]
    embeded.description = displayStr
    await bot.say(embed=embeded)
    try:
        guess = await bot.wait_for_message(timeout=10.0, author=ctx.message.author)
    except asyncio.TimeoutError:
        return await bot.say('you took too long.. the answer is {}.'.format(answer))

    if guess == None:
        await bot.say("times up! the answer is {}".format(answer))
    else:
        if guess.content.lower().strip() == cores.lower().strip():
            await bot.say(":tada: you got it right! +{} {}! :tada:".format(trivia_reward, currency_name))
            await progress_job("Trivia", ctx.message.author.id, ctx.message.author.name)
            await add_data(trivia_reward, ctx.message.author.id, ctx.message.author.name, PlayerData.Coins.value)
        else:
            await bot.say("wrong! the answer is {}".format(answer))


@bot.command(pass_context=True)
async def bal(ctx, user: discord.Member = None):
    try:
        if user == None:
            user = ctx.message.author
        uid = user.id
        await check_for_player_data(ctx.message.author.id, uid)
        c = player_stats[uid][PlayerData.Coins.value]
        await bot.say("{} has {} {}".format(user.name, c, currency_name))
    except:
        await bot.say("Please enter a valid user")

## leaderboards

@bot.command(pass_context=True)
async def lb(ctx):
    await check_for_player_data(ctx.message.author.id, ctx.message.author.name)
    embeded = leader_board(ctx, player_stats, currency_abrv)
    await bot.say(embed=embeded)

@bot.command(pass_context=True)
async def countinglb(ctx, *args):
    await check_for_player_data(ctx.message.author.id, ctx.message.author.name)
    embeded = leader_board(ctx, player_stats, "counts")
    await bot.say(embed=embeded)

@bot.command(pass_context=True)
async def replb(ctx, *args):
    await check_for_player_data(ctx.message.author.id, ctx.message.author.name)
    embeded = leader_board(ctx, player_stats, "rep")
    await bot.say(embed=embeded)

@bot.command(pass_context=True)
async def negreplb(ctx, *args):
    await check_for_player_data(ctx.message.author.id, ctx.message.author.name)
    embeded = leader_board(ctx, player_stats, "negrep")
    await bot.say(embed=embeded)


@bot.command(pass_context=True)
async def daily(ctx, *args):
    global roles
    dl = random.randint(daily_range[0], daily_range[1])
    if ctx.message.author.id in claimedusers:
        await bot.say("You have already claimed today's {}! Come back tommorow!".format(currency_name))
    else:
        await add_data(dl, ctx.message.author.id, ctx.message.author.name, PlayerData.Coins.value)
        await bot.say("You have claimed your daily reward of {} {}!".format(dl, currency_name))
        claimedusers.append(ctx.message.author.id)
        with open("dat/claimedusers.txt", "w") as f:
            endstr = ""
            for id in claimedusers:
                endstr += "{},".format(id)
            endstr = endstr[:-1]
            f.write(endstr)


@bot.command(pass_context=True)
@commands.cooldown(1, 600, commands.BucketType.user)
async def work(ctx, *args):
    global roles
    dl = random.randint(work_range[0], work_range[1])
    mult = 1
    for role in roles:
        if role.lower() in [y.name.lower() for y in ctx.message.author.roles]:
            mult += 1
    dl *= mult
    await add_data(dl, ctx.message.author.id, ctx.message.author.name, PlayerData.Coins.value)
    await bot.say("You worked and gained {} {}!".format(dl, currency_name))


@bot.command(pass_context=True)
@commands.cooldown(1, 4, commands.BucketType.user)
async def anagram(ctx, *args):
    ans = random.choice(wordlist)
    anslist = list(ans)
    random.shuffle(anslist)
    ruffled = ''.join(anslist)
    await bot.say("Unscramble {}".format(ruffled))

    try:
        response = await bot.wait_for_message(timeout=10.0, author=ctx.message.author)
    except asyncio.TimeoutError:
        await bot.say("Time's up! The answer was {}".format(ans))
    try:
        if response.content.lower().strip() == ans:
            await bot.say(":tada: You got it right! +{} {} :tada:".format(anagram_reward, currency_name))
            await progress_job("Anagram", ctx.message.author.id, ctx.message.author.name)
            await add_data(anagram_reward, ctx.message.author.id, ctx.message.author.name, PlayerData.Coins.value)
        else:
            await bot.say("Wrong, the word was {}".format(ans))
    except AttributeError:
        await bot.say("Time's up! The answer was {}".format(ans))


@bot.command(pass_context=True)
async def gamble(ctx, *args):
    try:
        if args[0] == "all":
            amt = player_stats[ctx.message.author.id][PlayerData.Coins.value]
        else:
            amt = int(args[0])
        try:
            multiplier = float(args[1])
        except:
            multiplier = 2
        if multiplier > 1:
            await check_for_player_data(ctx.message.author.id, ctx.message.author.name)
            pamt = player_stats[ctx.message.author.id][PlayerData.Coins.value]
            if amt <= pamt and amt > 0:
                perc = round((100 * amt / pamt), 2)
                chance = round(((100 * (1 - gamble_tax)) / multiplier), 5)
                await bot.say("Please confirm that you want to gamble "
                              "{} {}. ({}% of your total balance) for a chance to win {} {} at a {} % chance (Y/N)".format(
                    amt, currency_name, perc, int(math.floor(multiplier * amt)), currency_name, chance))
                try:
                    guess = await bot.wait_for_message(timeout=10.0, author=ctx.message.author)
                except asyncio.TimeoutError:
                    await bot.say("Response timed out")

                if guess.content.lower().strip() == "y":
                    decision = random.random()
                    if decision < (chance / 100):
                        await add_data(int(math.floor(amt * (multiplier - 1))), ctx.message.author.id,
                                       ctx.message.author.name, PlayerData.Coins.value)
                        await bot.say("Congratulations! You won {} {} ({})".format(int(math.floor(amt * multiplier)),
                                                                                   currency_name, decision))
                    else:
                        await add_data(-amt, ctx.message.author.id,
                                       ctx.message.author.name, PlayerData.Coins.value)
                        await bot.say("Sorry, you lost! ({})".format(decision))

                else:
                    await bot.say("Gamble aborted")
            else:
                await bot.say("You cannot afford to gamble this much")
        else:
            await bot.say("Incorrect multiplier")

    except:
        await bot.say("Please enter a valid amount to gamble")


@bot.command(pass_context=True)
async def dieroll(ctx, *args):
    try:
        if args[0] == "all":
            amt = player_stats[ctx.message.author.id][PlayerData.Coins.value]
        else:
            amt = int(args[0])
        await check_for_player_data(ctx.message.author.id, ctx.message.author.name)
        pamt = player_stats[ctx.message.author.id][PlayerData.Coins.value]
        if amt <= pamt and amt > 0:
            perc = round((100 * amt / pamt), 2)
            await bot.say("Please confirm that you want to die roll "
                          "" + str(amt) + " " + currency_name + ". (" + str(perc) + "% of your total balance) (Y/N)")
            try:
                guess = await bot.wait_for_message(timeout=10.0, author=ctx.message.author)
            except asyncio.TimeoutError:
                await bot.say("Response timed out")

            if guess.content.lower().strip() == "y":
                decision = random.randint(1, 6)

                await bot.say("Rolling die...")
                await asyncio.sleep(0.5)
                if decision == 1:
                    result = "lost all of your bet"
                    aloss = -amt

                elif decision == 2:
                    result = "lost two thirds of your bet"
                    aloss = -int(math.ceil(2 * amt / 3))
                elif decision == 3:
                    result = "lost a half of your bet"
                    aloss = -int(math.ceil(amt / 2))
                elif decision == 4:
                    result = "kept your bet"
                    aloss = 0
                elif decision == 5:
                    result = "doubled your bet"
                    aloss = amt
                elif decision == 6:
                    result = "doubled your bet"
                    aloss = amt
                await add_data(aloss, ctx.message.author.id, ctx.message.author.name, PlayerData.Coins.value)
                pref = "+" if aloss >= 0 else ""
                await bot.say("You rolled a " + str(decision) + " and " + result + " (" + pref + str(
                    aloss) + " " + currency_abrv + ")")

            else:
                await bot.say("Die roll aborted")
        else:
            await bot.say("You cannot afford to Die roll this much")
    except:
        await bot.say("Error! Please try again")


@bot.command(pass_context=True)
async def set(ctx, user: discord.Member = None, amt: int = 0):
    await check_for_player_data(ctx.message.author.id, ctx.message.author.name)
    try:
        try:
            pamt = player_stats[ctx.message.author.id][PlayerData.Coins.value]
            if pamt < amt or amt <= 0:
                await bot.say("You cannot give this!")
            else:
                try:
                    print(user)
                    uid = user.id
                    await check_for_player_data(uid, ctx.message.author.name)
                    namt = int(math.floor((1 - tax) * amt))
                    if namt < 1:
                        namt = 1

                    await bot.say(
                        "Are you sure you want to give {} {} to <@{}> (4% TAX) (Y/N)".format(namt, currency_name, uid,
                                                                                             100 * tax))

                    try:
                        response = await bot.wait_for_message(timeout=10.0, author=ctx.message.author)
                    except asyncio.TimeoutError:
                        await bot.say("Response timed out")

                    if response.content.lower().strip() == "y":
                        await add_data(namt, uid, "", PlayerData.Coins.value)
                        await add_data(-amt, ctx.message.author.id, ctx.message.author.name, PlayerData.Coins.value)
                        await bot.say(str(namt) + " " + currency_name + " successfully given to <@" + user.id + ">")
                    else:
                        await bot.say("Donation aborted")
                except:
                    await bot.say("Invalid arguments or time out")
        except:
            await bot.say("Error")
    except:
        await bot.say("Invalid arguments")


async def shop_functions(param):
    if param == "Food":
        pass


@bot.command(pass_context=True)
async def shop(ctx, *args):
    global generatorusers

    embeded = discord.embeds.Embed()
    embeded.title = "Shop"
    embeded.add_field(name="Description", value="Type the number of the product you would like to purchase")

    tstr = ""

    sorted_shop_items = sorted(shop_items.items(), key=lambda p: p[1][0])

    for i, item in enumerate(sorted_shop_items):
        tstr += str(i + 1) + ". " + item[0] + " - " + "**{:,.0f}".format(int(item[1][0])) + currency_abrv + "**\n"

    embeded.add_field(name="Products", value=tstr)

    uid = ctx.message.author.id
    uname = ctx.message.author.name

    await check_for_player_data(uid, uname)

    embeded.add_field(name="Your Balance", value=str(player_stats[uid][PlayerData.Coins.value]) + " " + currency_name,
                      inline=False)

    await bot.say(embed=embeded)

    try:
        while True:
            try:
                response = await bot.wait_for_message(timeout=10.0, author=ctx.message.author)
            except asyncio.TimeoutError:
                await bot.say("Shop timed out")
                break
            try:
                choice = sorted_shop_items[int(response.content) - 1]
                price = int(choice[1][0])
                f_type = choice[1][1]
                param = choice[1][2]
                if player_stats[uid][PlayerData.Coins.value] > price:
                    if f_type == ShopItem.Role:
                        if param in [y.name.lower() for y in ctx.message.author.roles]:
                            await bot.say("You already have the role " + param)
                        else:
                            role = get(ctx.message.author.server.roles, name=param)
                            await bot.add_roles(ctx.message.author, role)
                            await add_data(-price, ctx.message.author.id, ctx.message.author.name,
                                           PlayerData.Coins.value)
                            await bot.say(
                                "You have received the " + param + " role and " + str(
                                    price) + " " + currency_name + " has been deducted from your balance!")

                    elif f_type == ShopItem.Function:
                        print(param)
                        if param == "food":
                            embedede = discord.embeds.Embed()
                            embedede.description = "<@" + uid + "> has purchased food for the food-bank!"
                            embedede.set_image(url=random.choice(foods).split(",")[1])

                            await bot.send_message(destination=bot.get_channel(food_bank_id), embed=embedede)
                            await add_data(-price, ctx.message.author.id, ctx.message.author.name,
                                           PlayerData.Coins.value)
                            await bot.say(
                                "You have received " + param + " and " + str(
                                    price) + " " + currency_name + " has been deducted from your balance! Food has been added to <#" + food_bank_id + ">")


                        elif param == "gen":
                            if player_stats[uid][PlayerData.Gen.value] > 0:
                                await bot.say("You already own a Yashcoin Generator")
                            else:
                                await add_data(-price, ctx.message.author.id, ctx.message.author.name,
                                               PlayerData.Coins.value)
                                await add_data(1, ctx.message.author.id, ctx.message.author.name,
                                               PlayerData.Gen.value)
                                generatorusers.append(uid)
                                await bot.say("You have bought a Yashcoin Generator!")

                    try:
                        await bot.send_message(destination=bot.get_channel(purchase_log_id),
                                               content="<@{}> has bought {} for {} {}".format(ctx.message.author.id,
                                                                                              choice[0], price,
                                                                                              currency_abrv))
                    except:
                        pass

                else:
                    await bot.say("You cannot afford " + choice[0])
                break
            except:
                pass
    except:
        await bot.say("Shop timed out")


@bot.command(pass_context=True)
async def gen(ctx):
    uid = ctx.message.author.id
    await check_for_player_data(uid, ctx.message.author.name)
    if player_stats[uid][PlayerData.Gen.value] == 0:
        await bot.say("You do not have a generator to upgrade, please buy one from the shop")
    else:
        price = shop_items["Yashcoin Generator"][0]
        scale = 1.15 ** player_stats[uid][PlayerData.Gen.value]
        new_price = int(price * scale)
        embede = discord.embeds.Embed()
        embede.add_field(name="Your Generator", value="Your generator currently generates {} {} a minute".format(
            player_stats[uid][PlayerData.Gen.value], currency_name))
        embede.add_field(name="Upgrade",
                         value="Would you like to spend {} {} to upgrade your generator to give an extra 1 {} per minute? (Y/N)".format(
                             new_price, currency_name, currency_name))
        await bot.say(embed=embede)

        try:
            response = await bot.wait_for_message(timeout=10.0, author=ctx.message.author)
        except asyncio.TimeoutError:
            await bot.say("Response timed out")

        if response.content.lower().strip() == "y":
            if player_stats[uid][PlayerData.Coins.value] >= new_price:
                await add_data(1, uid, ctx.message.author.name, PlayerData.Gen.value)
                await add_data(-1 * new_price, uid, ctx.message.author.name, PlayerData.Coins.value)
                await bot.say("You have successfully upgraded your bot!")
            else:
                await bot.say("You cannot afford to upgrade this")
        else:
            await bot.say("Upgrade aborted")


@bot.command(pass_context=True)
async def bank(ctx, *args):
    embede = discord.embeds.Embed()
    embede.add_field(name="Bank Value", value="{:,.0f} ".format(bank_value) + currency_abrv)
    embede.add_field(name="Your Balance", value="{:,.0f}".format(
        player_stats[ctx.message.author.id][PlayerData.Bank.value]) + " " + currency_abrv)
    embede.add_field(name="Daily Compound Interest", value=str(round(compound_interest * 100, 2)) + "%")
    embede.add_field(name="Loaned Money", value="{:,.0f}".format(
        player_stats[ctx.message.author.id][PlayerData.Loan.value]) + " " + currency_abrv)
    embede.add_field(name="Loan Daily Percentage Rate", value=str(round(loan_dpr * 100, 2)) + "%")
    await bot.say(embed=embede)


@bot.command(pass_context=True)
async def dep(ctx, *args):
    uid = ctx.message.author.id
    try:
        if args[0] == "all":
            amt = player_stats[uid][PlayerData.Coins.value]
        else:
            amt = int(args[0])

        if amt > 0 and amt <= player_stats[uid][PlayerData.Coins.value]:
            await add_data(amt, uid, ctx.message.author.name, PlayerData.Bank.value)
            await add_data(-amt, uid, ctx.message.author.name, PlayerData.Coins.value)

            await bot.say("You have deposited " + str(amt) + " " + currency_name + " into the bank of yash!")
        else:
            await bot.say("You cannot deposit this!")
    except:
        await bot.say("Please enter a valid amount to deposit")


@bot.command(pass_context=True)
async def withdraw(ctx, *args):
    uid = ctx.message.author.id
    try:
        if args[0] == "all":
            amt = player_stats[uid][PlayerData.Bank.value]
        else:
            amt = int(args[0])

        if amt > 0 and amt <= player_stats[uid][PlayerData.Bank.value]:
            await add_data(amt, uid, ctx.message.author.name, PlayerData.Coins.value)
            await add_data(-amt, uid, ctx.message.author.name, PlayerData.Bank.value)

            await bot.say("You have withdrew " + str(amt) + " " + currency_name)
        else:
            await bot.say("You cannot withdraw this!")
    except:
        await bot.say("Please enter a valid amount to deposit")


@bot.command(pass_context=True)
async def loan(ctx, *args):
    uid = ctx.message.author.id
    try:
        amt = int(args[0])
        if player_stats[uid][PlayerData.Loan.value] >= 0:
            if amt > 0 and amt <= player_stats[uid][PlayerData.Bank.value]:
                await add_data(-amt, uid, ctx.message.author.name, PlayerData.Loan.value)
                await add_data(amt, uid, ctx.message.author.name, PlayerData.Bank.value)
                await bot.say("You have taken out a loan of " + str(amt) + " " + currency_name)
            else:
                await bot.say("You cannot take a loan worth more than your current balance!")
        else:
            await bot.say("You already have a loan out! Pay that one back first")
    except:
        await bot.say("Please enter a valid amount to loan")


@bot.command(pass_context=True)
async def payloan(ctx, *args):
    uid = ctx.message.author.id
    try:
        loaned = player_stats[uid][PlayerData.Loan.value]
        if player_stats[uid][PlayerData.Bank.value] > 0:
            if player_stats[uid][PlayerData.Bank.value] + loaned >= 0:
                await add_data(-loaned, uid, ctx.message.author.name, PlayerData.Loan.value)
                await add_data(loaned, uid, ctx.message.author.name, PlayerData.Bank.value)
                await bot.say(
                    "You have paid off all of your loan! ({:,.0f}".format(-loaned) + " " + currency_abrv + ")")
            else:
                perc = round(100 * (-player_stats[uid][PlayerData.Bank.value]) / loaned, 2)
                bal = player_stats[uid][PlayerData.Bank.value]
                await add_data(bal, uid, ctx.message.author.name, PlayerData.Loan.value)
                await add_data(-bal, uid, ctx.message.author.name, PlayerData.Bank.value)
                await bot.say("You have paid off " + str(perc) + "% of your loan! ({:,.0f}".format(
                    bal) + " " + currency_abrv + ")")
        else:
            await bot.say("You have no money in your bank account to pay a loan")

    except:
        await bot.say("You cant do this!")


@bot.command(pass_context=True)
async def loanlb(ctx, *args):
    tstr = ""
    await check_for_player_data(ctx.message.author.id, ctx.message.author.name)
    embeded = discord.embeds.Embed()
    for i, item in enumerate(sorted(player_stats.items(), key=lambda p: p[1][PlayerData.Loan.value])):
        user = item[1][PlayerData.Name.value]
        amt = item[1][PlayerData.Loan.value]
        addition = ""
        if "!" in item[0]:
            tstr += str(i + 1) + ": <@!" + item[0] + ">, {:,.0f}".format(amt) + " " + currency_abrv + " in debt\n"
        else:
            tstr += str(i + 1) + ": <@" + item[0] + ">, {:,.0f} ".format(amt) + "  " + currency_abrv + " in debt\n"
        if i > 8:
            break

    embeded.add_field(name="Top 10 reputation points", value=tstr)
    pos = 0
    for i, item in enumerate(sorted(player_stats.items(), key=lambda p: p[1][PlayerData.Loan.value])):
        id = item[0]
        if id == ctx.message.author.id:
            pos = i + 1
    embeded.add_field(name="Your rank", value="Rank " + str(pos) + ". You are {:,.0f} ".format(
        player_stats[ctx.message.author.id][PlayerData.Loan.value]) + " " + currency_abrv + " in debt", inline=False)
    await bot.say(embed=embeded)

async def reject_job(ctx):
    global player_jobs
    player_jobs[ctx.message.author.id] = [False, time.time()]
    with open("dat/jobs.txt", "w") as f:
        f.write(json.dumps(player_jobs))
    await bot.say("You cancelled or rejected this job. Wait 30 seconds to get a new one")

##JOBCOMMAND##
@bot.command(pass_context=True)
async def job(ctx, *args):
    on_cd = False
    checking_progress = False
    try:
        if not player_jobs[ctx.message.author.id][0]:
            if time.time() - job_cooldown > player_jobs[ctx.message.author.id][1]:
                on_cd = False
            else:
                on_cd = True
        else:
            on_cd = True
            checking_progress = True
            try:
                if args[0] == "cancel":
                    await bot.say("Are you sure you want to cancel your job? (Y/N)")
                    try:
                        response = await bot.wait_for_message(timeout=10.0, author=ctx.message.author)
                    except asyncio.TimeoutError:
                        await bot.say("Timed Out")
                    if response.content.lower().strip() == "y":
                        await reject_job(ctx)
                    else:
                        await bot.say("Cancellation aborted")
                else:
                    int("hello")
            except:
                await bot.say(str(player_jobs[ctx.message.author.id][3]) + " " + str(
                    player_jobs[ctx.message.author.id][1]) + "/" + str(
                    player_jobs[ctx.message.author.id][2]) + ". Reward: " + str(
                    player_jobs[ctx.message.author.id][4]) + " " + currency_name)
    except:
        pass
    if not on_cd:
        jobType = Jobs.get_job()

        jobTier = random.randint(0, 4)

        if jobTier == 0:
            difficulty = "Very Easy"
        elif jobTier == 1:
            difficulty = "Easy"
        elif jobTier == 2:
            difficulty = "Medium"
        elif jobTier == 3:
            difficulty = "Hard"
        elif jobTier == 4:
            difficulty = "Very Hard"

        times_do=int(tiers[jobType][jobTier])
        if jobType == Jobs.Counting:
            jobName = "Count {} times".format(times_do)
            jobTag = "Count"
        elif jobType == Jobs.Trivia:
            jobName = "Get trivia correct {} times".format(times_do)
            jobTag = "Trivia"
        elif jobType == Jobs.Anagram:
            jobName = "Get anagram correct {} times".format(times_do)
            jobTag = "Anagram"

        reward = int((20 + 45 * jobTier) * base_multiplier + random.randint(-5, 5))
        rewardStr = "Reward:\n{} {}\n".format(reward, currency_abrv)
        for i, role in enumerate(roles):
            if role.lower() in [u.name.lower() for u in ctx.message.author.roles]:
                reward += int(5 * (jobTier + 1) * (i + 1) * role_multiplier)
                rewardStr += "+{} {} (from {})\n".format(int(5 * (jobTier + 1) * (i + 1) * role_multiplier), currency_abrv, role)

        rewardStr += "Total Reward: " + str(reward) + " " + currency_abrv

        embede = discord.embeds.Embed()
        embede.add_field(name="Job", value=jobName + "\n" + difficulty, inline=False)
        embede.add_field(name="Reward", value=rewardStr, inline=False)
        embede.add_field(name="Accept Job?", value="Y/N")
        await bot.say(embed=embede)

        try:
            guess = await bot.wait_for_message(timeout=15.0, author=ctx.message.author)
        except asyncio.TimeoutError:
            return await bot.say('Job request timed out, check back in 30 seconds')
        try:
            if guess.content.lower().strip() == "y":
                player_jobs[ctx.message.author.id] = [True, 0, times_do, jobTag, reward]
                with open("dat/jobs.txt", "w") as f:
                    f.write(json.dumps(player_jobs))
                await bot.say("Job accepted! Type -job to check your progress")
            else:
                await reject_job(ctx)
        except:
            await reject_job(ctx)
    else:
        if not checking_progress:
            await bot.say("Please wait {}s before requesting a new job".format(round(job_cooldown - (time.time() - player_jobs[ctx.message.author.id][1]),2)))


@bot.command(pass_context=True)
async def circ(ctx, *args):
    total = 0
    for item, key in player_stats.items():
        total += key[PlayerData.Coins.value]
        total += key[PlayerData.Bank.value]
    relative = bank_value / total
    embede = discord.embeds.Embed()
    embede.add_field(name="YC in Circulation", value="YC {:,.0f}".format(total), inline=True)
    embede.add_field(name="Relative Value", value="{:,.4f}".format(relative), inline=True)
    await bot.say(embed=embede)


@bot.command(pass_context=True)
@commands.has_role("Yashcoin Baller")
async def whip(ctx, *args):
    user = ""
    for arg in args:
        user += arg + " "
    if user == "":
        user = "nothing"
    await bot.say("You whipped " + user)


@bot.command(pass_context=True)
@commands.has_role("Ultimate Yashcoin Baller")
async def slap(ctx, *args):
    user = ""
    for arg in args:
        user += arg + " "
    if user == "":
        user = "nothing"
    await bot.say("You slapped " + user)


@bot.command(pass_context=True)
@commands.has_role("Supreme Yashcoin Baller")
async def nut(ctx, *args):
    user = ""
    for arg in args:
        user += arg + " "
    if user == "":
        user = "nothing"
    await bot.say("You nutted on " + user)


@bot.command(pass_context=True)
@commands.has_role("Godly Yashcoin Baller")
async def lick(ctx, *args):
    user = ""
    for arg in args:
        user += arg + " "
    if user == "":
        user = "nothing"
    await bot.say("You licked " + user)



@bot.command(pass_context=True)
async def rep(ctx, user: discord.Member = None):
    global dreps
    try:
        if ctx.message.author.id != user.id:
            if ctx.message.author.id not in dreps:
                dreps.append(ctx.message.author.id)
                with open("dat/dailyreps.txt", "w") as f:
                    tstr = ""
                    for uid in dreps:
                        tstr += uid + ","
                    f.write(tstr)
                    await add_data(1, user.id, user.name, PlayerData.RepPoints.value)
                await bot.say("You have given a reputation point to <@{}>".format(user.id))
            else:
                await bot.say("You have already given rep today")
        else:
            await bot.say("You cant give or take reputation points from yourself!")
    except:
        await bot.say("Please provide a valid user!")


@bot.command(pass_context=True)
async def negrep(ctx, user: discord.Member = None):
    global dnreps
    try:
        if ctx.message.author.id != user.id:
            if ctx.message.author.id not in dnreps:
                dnreps.append(ctx.message.author.id)
                with open("dat/dailynegreps.txt", "w") as f:
                    tstr = ""
                    for uid in dnreps:
                        tstr += uid + ","
                    f.write(tstr)
                    await add_data(-1, user.id, user.name, PlayerData.RepPoints.value)
                await bot.say("You have given a negative reputation point to <@{}>".format(user.id))
            else:
                await bot.say("You have already given negative rep today")
        else:
            await bot.say("You cant give or take reputation points from yourself!")
    except:
        await bot.say("Please provide a valid user!")


@bot.command(pass_context=True)
async def rp(ctx, user: discord.Member = None):
    try:
        if user == None:
            user = ctx.message.author
        await check_for_player_data(user.id, user.name)
        reppoint = player_stats[user.id][PlayerData.RepPoints.value]
        await bot.say("<@{}> has {} reputation points".format(user.id, reppoint))
    except:
        await bot.say("Please give a valid user argument")


@bot.command(pass_context=True)
async def stats(ctx, user: discord.Member = None):
    if user == None:
        uid = ctx.message.author.id
    else:
        uid = user.id

    await check_for_player_data(uid, ctx.message.author.name)

    coin = player_stats[uid][PlayerData.Coins.value]
    count = player_stats[uid][PlayerData.Counts.value]
    reppoints = player_stats[uid][PlayerData.RepPoints.value]
    uname = player_stats[uid][PlayerData.Name.value]

    sendstr = "{}: {}\nCounts: {}\nReputation Points: {}".format(currency_name, coin, count, reppoints)

    embeded = discord.embeds.Embed()
    embeded.add_field(name="{}'s Stats".format(uname), value=sendstr, inline=False)

    await bot.say(embed=embeded)


@bot.command(pass_context=True)
async def splat(ctx):
    embede = discord.embeds.Embed()
    embede.set_image(url="http://www.sclance.com/pngs/white-paint-splatter-png/white_paint_splatter_png_1513201.png")
    await bot.say(embed=embede)


## don't remove these commands
@bot.command(pass_context=True)
async def help(ctx):
    embede = discord.embeds.Embed()
    embede.add_field(name="Help",
                     value="Click [here](https://github.com/bebe-morse/YashwanthBOT/blob/master/documentation.md) to get help on the bot's commands")
    await bot.say(embed=embede)


@bot.command(pass_context=True)
async def credit(ctx):
    embede = discord.embeds.Embed()
    embede.add_field(name="Credits", value="Thanks to bebe morse#9433 for creating the framework for this bot.\n"
                                           "You can support him **[here](https://paypal.me/bebemorse?locale.x=en_GB)**.\n"
                                           "If you have queries for the bot, join his server **[here](https://discord.gg/GrMbpX)**.\n"
                                           "This bot is open source. You can get it **[here](https://github.com/bebe-morse/YashwanthBOT)**")
    await bot.say(embed=embede)

##### ERRORS #####
@work.error
@trivia.error
@anagram.error
@guess.error
async def cooldown_error(error, ctx):
    await bot.say(error)

@slap.error
@whip.error
@nut.error
@lick.error
async def check_error(error, ctx):
    role_type = "yashcoin ballers" if ctx.command.name == "whip" else "ultimate yashcoin ballers" if ctx.command.name == "slap" else "supreme yashcoin ballers" if ctx.command.name == "nut" else "godly yashcoin ballers"
    role_type = role_type.capitalize()
    if isinstance(error, commands.CheckFailure):
        await bot.say("Hey! Only {} can {}".format(role_type, ctx.command))
###########################

# run the bot lol
bot.run(token, bot=True, reconnect=True)
