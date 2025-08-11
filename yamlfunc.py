import yaml
import os

async def GetRaceJockeys(race_id):
    file_path = os.path.join(os.path.dirname(__file__), "races/{}.yaml".format(race_id))
    race_file = open(file_path, "r")
    yaml_content = yaml.safe_load_all(race_file)

    yaml_race_info = next(yaml_content)
    jockey_list = []

    jockey_number = yaml_race_info["partecipants number"]

    for n in range(jockey_number):
        jockey_list.append((yaml_race_info["partecipants"][n]["player {}".format(n+1)][0]["name"], yaml_race_info["partecipants"][n]["player {}".format(n+1)][1]["horse"]))

    race_file.close()
    return jockey_number, jockey_list

async def GetRaceBetRates(race_id):
    file_path = os.path.join(os.path.dirname(__file__), "races/{}.yaml".format(race_id))
    race_file = open(file_path, "r")
    yaml_content = yaml.safe_load_all(race_file)
    yaml_race_info = next(yaml_content)
    yaml_bet_info = next(yaml_content)
    rates_list = []

    jockey_number = yaml_race_info["partecipants number"]

    for n in range(jockey_number):
        rates_list.append(yaml_bet_info["rates"][n]["player {}".format(n+1)])

    race_file.close()
    return rates_list

async def GetUsersBets(race_id):
    file_path = os.path.join(os.path.dirname(__file__), "races/{}.yaml".format(race_id))
    race_file = open(file_path, "r")
    yaml_content = yaml.safe_load_all(race_file)
    yaml_race_info = next(yaml_content)
    yaml_bet_info = next(yaml_content)
    bet_list = []
    temp_list = []

    jockey_number = yaml_race_info["partecipants number"]

    for n in range(jockey_number):
        for x in range(yaml_bet_info["p{} bets".format(n+1)][0]["bet num"]):
            temp_list.append((yaml_bet_info["p{} bets".format(n+1)][x+1]["bettor {}".format(x+1)][0]["name"], yaml_bet_info["p{} bets".format(n+1)][x+1]["bettor {}".format(x+1)][1]["amount"]))
        
        bet_list.append(temp_list.copy())
        temp_list.clear()

    race_file.close()
    return bet_list


async def add_bet(race_id, username, amount, jockey_number):
    file_path = os.path.join(os.path.dirname(__file__), "races/{}.yaml".format(race_id))
    race_file = open(file_path, "r")
    yaml_content = yaml.safe_load_all(race_file)
    yaml_race_info = next(yaml_content)
    yaml_bet_info = next(yaml_content)
    
    amount_of_bets = yaml_bet_info["p{} bets".format(jockey_number)][0]["bet num"]
    yaml_bet_info["p{} bets".format(jockey_number)].append({"bettor {}".format(amount_of_bets + 1) : [{"name" : username}, {"amount" : amount}]})
    yaml_bet_info["p{} bets".format(jockey_number)][0]["bet num"] = amount_of_bets + 1
    new_document = [yaml_race_info, yaml_bet_info]
    to_add = yaml.safe_dump_all(new_document)
    race_file.close()
    race_file_w = open(file_path, "w")
    race_file_w.write(to_add)
    race_file_w.close()



async def test():
    jockeys = await GetRaceJockeys(100000)
    rates = await GetRaceBetRates(100000)
    bets = await GetUsersBets(100000)
    print(jockeys)
    print(rates)
    print(bets)
    print("adding bet of 1000 on first player")
    await add_bet(100000, "testname", 1500, 1)


#asyncio.run(test())