import enum
import random

class PlayerData(
    enum.Enum):  # in stats, data is stored as a sort of jumbled array. this enumeration help makes sense of that. each item corresponds to the list index
    Name = 0
    Coins = 1
    Counts = 2
    RepPoints = 3
    Gen = 4
    Bank = 5
    Loan = 6


class ShopItem(enum.Enum):  # its helpful
    Role = 0
    Function = 1


class Jobs(enum.Enum):  # its helpful. contains a class method that gives a random job
    Counting = 0
    Trivia = 1
    Anagram = 2

    @classmethod
    def get_job(cls):
        return random.choice([Jobs.Counting, Jobs.Trivia, Jobs.Anagram])


class BotConfigParser(enum.Enum):
    Token="token"
    BotID="bot_id"
    OwnerID="owner_id"
    Description="desc"
    Prefix="prefix"


class IdParser(enum.Enum):
    MainBotChannel = "main_bot_channel_id"
    CountingChannel = "counting_channel_id"
    CountingMilestones = "counting_milestones_id"
    Server = "server_id"
    FoodBank = "food_bank_id"
    PurchaseLog = "purchase_log_id"
    DisabledChannels = "disabled_channels"


class EconomyParser(enum.Enum):
    CurrencyName = "currency_name"
    CurrencyAbbreviation = "currency_abrv"
    Guess = "guess"
    Trivia = "trivia"
    Anagram = "anagram"
    SmallMilestone = "small_milestone"
    MediumMilestone = "medium_milestone"
    LargeMilestone = "large_milestone"
    CountsMilestone = "counts_milestone"
    CompoundInterest = "compound_interest"
    LoanInterest = "loan_interest"
    BankValue = "bank_value"
    DailyRange = "daily_range"
    WorkRange = "work_range"
    Roles = "add_roles"
    Tax = "tax"
    GambleTax = "gamble_tax"
    CoinRange="random_coin_range"
    CoinTime="random_coin_time"

class JobParser(enum.Enum):
    JobCooldown = "new_job_cooldown"
    RoleMultiplier = "role_multiplier"
    BaseMultiplier = "base_multiplier"
    Tiers = "tiers"


def parse_config_params(inp):
    if inp == "counting":
        return Jobs.Counting
    elif inp == "trivia":
        return Jobs.Trivia
    elif inp == "anagram":
        return Jobs.Anagram
    elif inp == "role":
        return ShopItem.Role
    elif inp == "func":
        return ShopItem.Function
    return inp


def ship_parse(s):
    if s <= 10:
        addition = ":poop:"
    elif s <= 25:
        addition = ":nauseated_face:"
    elif s <= 40:
        addition = ":neutral_face:"
    elif s < 69:
        addition = ":slight_smile:"
    elif s == 69:
        addition = ":eggplant::peach::stuck_out_tongue_closed_eyes:"
    elif s < 90:
        addition = ":smile:"
    elif s >= 90:
        addition = ":heart_eyes:"
    elif s == 100:
        addition = ":heart_eyes_cat:"
    else:
        addition=""
    return addition

def lb_addition_parse(amt):
    if amt < 100:
        addition = ":neutral_face:"
    elif amt < 250:
        addition = ":sunglasses:"
    elif amt < 500:
        addition = ":money_mouth:"
    elif amt < 1000:
        addition = ":credit_card:"
    elif amt < 2500:
        addition = ":money_with_wings:"
    elif amt < 10000:
        addition = ":moneybag:"
    elif amt < 25000:
        addition = ":gem:"
    elif amt < 50000:
        addition = ":dvd:"
    else:
        addition = ":flag_eg:"
    return addition