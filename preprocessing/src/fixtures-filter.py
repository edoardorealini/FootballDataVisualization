import json

data_path = "../data/"

fixtures_file = open(data_path + "serieA_fixtures.json",)
json_fixtures = json.load(fixtures_file)

fixtures = json_fixtures["api"]["fixtures"]
counter = 0

out_file = open(data_path + "next10_serieA_fixtures", "w")

good_fixtures = []

for fix in fixtures:
    if (fix["statusShort"] == "NS" or fix["statusShort"] == "TBD") and counter < 5:
        #out_file.write(json.dumps(fix))
        good_fixtures.append(fix)
        counter = counter + 1
        print(counter)
        print(fix)

out_file.write(good_fixtures)
print("Data filtered !")