import nestdictutils

d = \
    {\
     "Aurelia Silgar" : \
        {"class" : "Cleric",
         "race" : "Dwarf",
         "alignmnent" : "Chaotic Good",
         "equipment" : \
            {"Bedroll" : \
                {"number" : 1,
                 "cost" : 1,
                 "weight" : 7}}},
     "Martinus Olsenir" : \
        {"class" : "Fighter",
         "race" : "Dwarf",
         "alignment" : "Lawful Good"},
     "Non-playing characters" : \
        {"Loton Burmingson" : \
            {"class" : "Bard",
             "race" : "Human",
             "alignment" : "Lawful Good"},
        },
    }

#keypaths = utils.recursive_iter_key_paths(d)

#print(utils.recursive_get_key_paths(d, "Lawful Good"))

#newdict = utils.recursive_remove(d, (("Aurelia Silgar", "class"), "Cleric"))
#print(newdict)

#newdict = utils.recursive_pop(d, ["class"])
#print(newdict)

d = {1: 2, 3: {4:5}, 6: {3: {7: 8}, 7: [10]}, 7: 2}

f = lambda x: x > 4

key_paths = (((1,2),3), ((4,),5), ((4,),6))
d2 = {14: {15: 16}, 3: {17: 18}}
d3 = {6 : {3 : {9:10}}}
new_d = nestdictutils.recursive_filter_dict(d, f, in_place = False)
print(new_d)