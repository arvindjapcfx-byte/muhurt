import requests
import json
import time
from datetime import datetime, timedelta
import DivineAPI_generateHTML

# ===========================
# HELPERS
# ===========================
def get_planets_in_house(response_data, house_no):
    return [p for p in response_data["data"]["planets"] if p.get("house") == house_no and p.get("name", "").lower() != "ascendant"]

def get_house_lord_details(response_data, house_no, asc_sign_no):
    planets = response_data["data"]["planets"]
    sign_lords = {
        1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon", 5: "Sun", 6: "Mercury",
        7: "Venus", 8: "Mars", 9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter"
    }
    house_sign_no = (asc_sign_no + house_no - 1) % 12 or 12
    lord_name = sign_lords.get(house_sign_no)
    lord_details = next((p for p in planets if p.get('name') == lord_name), None)
    return {
        "house_no": house_no,
        "house_sign_no": house_sign_no,
        "lord_name": lord_name,
        "lord_details": lord_details
    }

def get_palnet_details(response_data, planet_name):
    planets = response_data["data"]["planets"]
    planet_details = next((p for p in planets if p.get('name') == planet_name), None)
    return {
        "planet_details": planet_details
    }

# ===========================
# CONFIG
# ===========================
url = "https://astroapi-3.divineapi.com/indian-api/v2/planetary-positions"
headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2RpdmluZWFwaS5jb20vcmVnZW5lcmF0ZS1hcGkta2V5cyIsImlhdCI6MTc1ODcyMTg3MywibmJmIjoxNzU4NzIxODczLCJqdGkiOiI4N0tsR3RvQ2dkZWo1a3NpIiwic3ViIjoiNDI5OSIsInBydiI6ImU2ZTY0YmIwYjYxMjZkNzNjNmI5N2FmYzNiNDY0ZDk4NWY0NmM5ZDcifQ.mDBrMvra3gi2HK6WNZE15UPcKM4ln8p4ABCmTzjlG4E'
}
base_payload = {
    'api_key': 'be13a815e2ef75b832e3eb452c216ab8',
    'full_name': 'Kocharam',
    'gender': 'male',
    'place': 'Erode',
    'lat': '11.1956',
    'lon': '77.4300',
    'tzone': '5.5',
    'lan': 'en'
}

# ===========================
# MAIN RUNNER
# ===========================
def run_for_date(input_date,start_time, end_time):
    """
    Run API requests every 2 minutes from 09:15 to 15:30 for given date (dd/mm/YYYY).
    For each response, run the condition checks and print results.
    """
    start_dt = datetime.strptime(input_date + " "+start_time, "%d/%m/%Y %H:%M")
    end_dt = datetime.strptime(input_date + " "+end_time, "%d/%m/%Y %H:%M")
    current_time = start_dt

    try:
        file_name = f"{current_time.day}_{current_time.month}_{current_time.year}.txt"
        with open(file_name, "x") as f:
            f.write(file_name + "\n\n")
        print("File ",file_name," created successfully.")
    except FileExistsError:
        raise Exception(f"File {file_name} already exists.")

    current_address = ""
    previus_address = ""

    selected_address_set = []
    unselected_address_set = []
    _11th_exclusive_address_array = []
    _3_11_address_array = []
    _2_11_address_array = []
    _4_11_address_array = []
    _5_9_address_array = []
    _2_11_10_address_array = []
    _2_9_10_address_array = []
    _2_5_11_address_array = []

    all_muhurt_dictionary = {}

    while current_time <= end_dt:
        '''print(f"\n=== Processing for time: {current_time.strftime('%H:%M')} ===")
        '''
        failure_reason_array = []
        payload = base_payload.copy()
        payload.update({
            'day': str(current_time.day),
            'month': str(current_time.month),
            'year': str(current_time.year),
            'hour': str(current_time.hour),
            'min': str(current_time.minute),
            'sec': '00'
        })

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code != 200:
                print("HTTP error:", response.status_code, response.text)
                current_time += timedelta(minutes=2)
                continue

            data = response.json()
            if data.get("success") != 1 or "data" not in data or "planets" not in data["data"]:
                print("API returned no valid data:", data)
                current_time += timedelta(minutes=2)
                continue

            planets = data["data"]["planets"]
            ascendant = next((p for p in planets if p.get("name") == "Ascendant"), None)
            if not ascendant:
                print("Ascendant not found in response!")
                current_time += timedelta(minutes=2)
                continue

            asc_sign_no = ascendant.get("sign_no")
            # get house lords
            _11th = get_house_lord_details(data, 11, asc_sign_no)
            _8th = get_house_lord_details(data, 8, asc_sign_no)
            _12th = get_house_lord_details(data, 12, asc_sign_no)

            _11th_name = _11th.get("lord_name")
            _8th_name = _8th.get("lord_name")
            _12th_name = _12th.get("lord_name")

            '''print(f"Ascendant sign_no: {asc_sign_no}")
            print("11th Lord:", _11th_name)
            print("8th Lord:", _8th_name)
            print("12th Lord:", _12th_name)
            print("11th Lord Nakshatra Lord:", _11th.get("lord_details", {}).get("nakshatra_lord"))
            '''
            # ===========================
            # Your condition checks (integrated, but safe)
            # ===========================
            condtions_met = None
            '''print("===============================")
            '''

            asc_rashi_lord = ascendant.get("rashi_lord")
            asc_nakshatra_lord = ascendant.get("nakshatra_lord")
            asc_sub_lord = ascendant.get("sub_lord")
            eleventh_lord_details = _11th.get("lord_details") or {}
            eleventh_nakshatra_lord = eleventh_lord_details.get("nakshatra_lord")

            asc_rashi_lord_details = get_palnet_details(data, asc_rashi_lord)
            asc_sub_lord_details = get_palnet_details(data, asc_sub_lord)
            asc_nakshatra_lord_details = get_palnet_details(data, asc_nakshatra_lord)

            asc_rashi_lord_significator_NL =  asc_rashi_lord_details["planet_details"].get("nakshatra_lord") if asc_rashi_lord_details["planet_details"] else None
            asc_nakshatra_lord_significator_NL =  asc_sub_lord_details["planet_details"].get("nakshatra_lord") if asc_nakshatra_lord_details["planet_details"] else None           
            asc_sub_lord_significator_NL =  asc_sub_lord_details["planet_details"].get("nakshatra_lord") if asc_sub_lord_details["planet_details"] else None

            asc_rashi_lord_Planet_house =  asc_rashi_lord_details["planet_details"].get("house") if asc_rashi_lord_details["planet_details"] else None
            asc_nakshatra_lord_Planet_house =  asc_nakshatra_lord_details["planet_details"].get("house") if asc_nakshatra_lord_details["planet_details"] else None  
            asc_sub_lord_Planet_house =  asc_sub_lord_details["planet_details"].get("house") if asc_sub_lord_details["planet_details"] else None    


            current_address = ascendant.get("rashi_lord")+ " / "+ ascendant.get("nakshatra_lord")+ " / "+ ascendant.get("sub_lord")
            current_address_short_form = ascendant.get("rashi_lord")[0:2]+ " / "+ ascendant.get("nakshatra_lord")[0:2]+ " / "+ ascendant.get("sub_lord")[0:2]
                        
            if current_address == previus_address:
                current_time += timedelta(minutes=2)
                continue
            else:
                previus_address = current_address
            
            address_set = {"Mars / Ketu / Saturn"
                          , "Mars / Venus / Saturn"
                          , "Venus / Sun / Jupiter"
                          , "Venus / Moon / Jupiter"
                          , "Mercury / Mars / Mercury"
                          , "Mercury / Rahu / Mars"
                          , "Moon / Saturn / Venus"
                          , "Moon / Mars / Venus"
                          , "Sun / Ketu / Mercury"
                          , "Sun / Venus / Mercury"
                          , "Mercury / Moon / Moon"
                          , "Mercury / Moon / Mercury"
                          , "Venus / Mars / Sun"
                          , "Venus / Rahu / Sun"
                          , "Venus / Jupiter / Sun"
                          , "Mars / Saturn / Mercury"
                          , "Mars / Mercury / Mercury"
                          , "Jupiter / Ketu / Venus"
                          , "Jupiter / Venus / Venus"
                          , "Saturn / Moon / Mars"
                          , "Saturn / Rahu / Jupiter"
                          , "Saturn / Jupiter / Jupiter"
                          , "Jupiter / Saturn / Saturn"
                          , "Jupiter / Mercury / Mercury"} 

            _11th_exclusive_address_set = {"Mercury / Moon / Mercury"
                                     , "Mercury / Mars / Mercury"
                                     , "Jupiter / Mercury / Mercury"
                                     , "Mars / Mercury / Mercury"}
            

            _3_11_array_set = {"Venus / Moon / Jupiter"
                              , "Mercury / Mars / Sun"
                              , "Moon / Mercury / Venus"
                              , "Sun / Venus / Mercury"
                              , "Sun / Sun / Sun"
                              , "Mercury / Moon / Mars"
                              , "Mars / Saturn / Mercury"
                              , "Mars / Mercury / Saturn"
                              , "Jupiter / Venus / Saturn"
                              , "Saturn / Mars / Jupiter"
                              , "Jupiter / Saturn / Venus"}
            
            _2_11_array_set = {"Mars / Ketu / Rahu"
                               ,"Venus / Moon / Venus"
                               ,"Sun / Ketu / Jupiter"
                               ,"Mercury / Sun / Mercury"
                               ,"Mercury / Moon / Ketu"
                               ,"Jupiter / Ketu / Rahu"
                               ,"Saturn / Moon / Rahu"
                               ,"Saturn / Mars / Moon"
                               ,"Saturn / Jupiter / Moon"}
            
            _4_11_array_set = {"Mars / Venus / Rahu"
                               ,"Venus / Moon / Jupiter"
                               ,"Sun / Sun / Rahu"
                               ,"Venus / Jupiter / Saturn"
                               ,"Mars / Saturn / Rahu"
                               ,"Jupiter / Ketu / Mars"
                               ,"Saturn / Sun / Venus"
                               ,"Saturn / Rahu / Mercury"
                               ,"Jupiter / Saturn / Rahu"}
            
            _5_9_address_set = {"Mercury / Rahu / Moon"
                                ,"Venus / Rahu / Sun"
                                ,"Jupiter / Venus / Sun"
                                ,"Saturn / Rahu / Sun"}

            _2_11_10_address_set = {"Sun / Ketu / Jupiter"}

            _2_9_10_adress_set = {"Saturn / Rahu / Moon"}


            _2_5_11_address_set = {"Mars / Ketu / Ketu"
                                   ,"Saturn / Rahu / Jupiter"
                                   ,"Saturn / Rahu / Sun"
                                   ,"Sun / Venus / Mercury"}


            if (current_address == "Mars/ Ketu / Ketu") :{ 
                print("Mars / Ketu / Ketu time"+ ":"+ current_time.strftime('%H:%M'))
            }

            if (current_address in address_set or 
                current_address in _11th_exclusive_address_set or
                current_address in _3_11_array_set or
                current_address in _2_11_array_set or
                current_address in _4_11_array_set or
                current_address in _5_9_address_set or
                current_address in _2_11_10_address_set or
                current_address in _2_9_10_adress_set or
                current_address in _2_5_11_address_set):

                condtions_met = True

                not_allowed_pairs = {
                    (1, 6), (6, 1),
                    (2, 7), (7, 2),
                    (3, 8), (8, 3),
                    (4, 9), (9, 4),
                    (5, 10), (10, 5),
                    (6, 11), (11, 6),
                    (7, 12), (12, 7),
                    (8, 1), (1, 8),
                    (9, 2), (2, 9),
                    (10, 3), (3, 10),
                    (11, 4), (4, 11),
                    (12, 5), (5, 12)
                }

                '''print(asc_rashi_lord_Planet_house, asc_nakshatra_lord_Planet_house, asc_sub_lord_Planet_house)
                '''
                if (asc_rashi_lord_Planet_house, asc_nakshatra_lord_Planet_house) in not_allowed_pairs:
                    '''print("*** FAILED Rashi lord and Nakshatra lord are in not allowed pair of houses")
                    '''
                    failure_reason_array.append("68_AB")
                    condtions_met = False
                
                if (asc_rashi_lord_Planet_house, asc_sub_lord_Planet_house) in not_allowed_pairs:   
                    '''print("*** FAILED Rashi lord and Sub lord are in not allowed pair of houses")
                    '''
                    failure_reason_array.append("68_AC")
                    condtions_met = False

                if (asc_nakshatra_lord_Planet_house, asc_sub_lord_Planet_house) in not_allowed_pairs:
                    '''print("*** FAILED Nakshatra lord and Sub lord are in not allowed pair of houses")
                    '''
                    failure_reason_array.append("68_BC")
                    condtions_met = False

                '''print (asc_rashi_lord_significator_NL, asc_nakshatra_lord_significator_NL, asc_sub_lord_significator_NL)
                print(_8th_name)
                print (asc_sub_lord_details.get("house"), asc_nakshatra_lord_details.get("house"))  
                '''
                
                if asc_rashi_lord_significator_NL == _8th_name:
                    '''print("*** FAILED Rashi lord significator NL is matching with 8th lord")
                    '''
                    failure_reason_array.append("A_8th")
                    condtions_met = False

                if asc_nakshatra_lord_significator_NL and asc_nakshatra_lord_significator_NL == _8th_name:
                    '''print("*** FAILED Nakshatra lord significator NL is matching with 8th lord")
                    '''
                    failure_reason_array.append("B_8th")
                    condtions_met = False


                #check sub lord  and nakshatra lord significator NL is not 8th House
                if asc_sub_lord_significator_NL and asc_sub_lord_significator_NL == _8th_name:
                    '''print("*** FAILED Sub lord significator NL is matching with 8th lord")
                    '''
                    failure_reason_array.append("C_8th")
                    condtions_met = False
                else:
                    '''print("TICK Sub lord significator NL is NOT matching with 8th lord")
                    '''

                if asc_sub_lord_details.get("house") == 8 or asc_nakshatra_lord_details.get("house") == 8:
                    '''print("*** FAILED Sub lord or nakshatra lord is in 8th house")
                    '''
                    failure_reason_array.append("8house")
                    condtions_met = False

                # check if 11th lord is in 8th or 12th house
                lord_house = eleventh_lord_details.get("house")
                if lord_house in [8, 12]:
                    '''print("*** FAILED 11th lord is in 8th or 12th house")
                    '''
                    failure_reason_array.append(2)
                    condtions_met = False
                else:
                    '''print("TICK 11th lord is NOT in 8th or 12th house")
                    '''

                # check if 11th lord's nakshatra_lord matches 8th lord
                if eleventh_nakshatra_lord and eleventh_nakshatra_lord == _8th_name:
                    '''print("*** FAILED 11th lord nakshatra_lord is matching with 8th lord")
                    '''
                    failure_reason_array.append(3)
                    condtions_met = False
                else:
                    '''print("TICK 11th lord nakshatra_lord is NOT matching with 8th lord")
                    '''

                # check if 11th lord's nakshatra_lord matches 12th lord
                if eleventh_nakshatra_lord and eleventh_nakshatra_lord == _12th_name:
                    '''print("*** FAILED 11th lord nakshatra_lord is matching with 12th lord")
                    '''
                    failure_reason_array.append(3)
                    condtions_met = False
                else:
                    '''print("TICK 11th lord nakshatra_lord is NOT matching with 12th lord")
                    '''

                # Check planets actually present in 8th and 12th houses
                planets_8th = get_planets_in_house(data, 8)
                planets_12th = get_planets_in_house(data, 12)
                planets_11th = get_planets_in_house(data, 11)


                for p in planets_8th:
                    if eleventh_nakshatra_lord and eleventh_nakshatra_lord == p.get("name"):
                        '''print("*** FAILED 11th lord nakshatra_lord is matching with planet in 8th house -", p.get("name"))
                        '''
                        failure_reason_array.append(4)
                        condtions_met = False

                for p in planets_12th:
                    if eleventh_nakshatra_lord and eleventh_nakshatra_lord == p.get("name"):
                        '''print("*** FAILED 11th lord nakshatra_lord is matching with planet in 12th house -", p.get("name"))
                        '''
                        failure_reason_array.append(5)
                        condtions_met = False

                for p in planets_11th:
                    if (p.get("name") == "Ketu" or p.get("name") == "Rahu"):
                        continue
                    print("11th house planet:", p.get("name"))
                    planet_Details = get_palnet_details(data, p.get("name"))
                    planet_nakshatra_lord = planet_Details["planet_details"].get("nakshatra_lord") if planet_Details["planet_details"] else None
                    
                    if planet_nakshatra_lord and planet_nakshatra_lord == _8th_name:
                        print("*** FAILED Planet in 11th house nakshatra_lord is matching with 8th lord -", p.get("name"))
                        failure_reason_array.append(6)
                        condtions_met = False

                    if planet_nakshatra_lord and planet_nakshatra_lord == _12th_name:
                        print("*** FAILED Planet in 11th house nakshatra_lord is matching with 12th lord -", p.get("name"))
                        failure_reason_array.append(7)
                        condtions_met = False


                    for p8 in planets_8th:
                        if planet_nakshatra_lord and planet_nakshatra_lord == p8.get("name"):
                            print("*** FAILED Planet in 11th house nakshatra_lord is matching with planet in 8th house -", p8.get("name"))
                            failure_reason_array.append(8)
                            condtions_met = False
                            break

                    for p12 in planets_12th:
                        if planet_nakshatra_lord and planet_nakshatra_lord == p12.get("name"):
                            print("*** FAILED Planet in 11th house nakshatra_lord is matching with planet in 12th house -", p12.get("name"))
                            
                            failure_reason_array.append(9)
                            condtions_met = False
                            break


                if _11th_exclusive_address_set.__contains__(current_address):
                    print(current_address, "|", current_time.strftime('%H:%M') , "|", failure_reason_array)
                    _11th_exclusive_address_string = current_address_short_form + "|"+ current_time.strftime('%H:%M') + (" - " + str(failure_reason_array) if failure_reason_array else "") + " *11"
                    unselected_address_set.append(_11th_exclusive_address_string) if(failure_reason_array) else selected_address_set.append(_11th_exclusive_address_string)
                    continue
                    

                if _3_11_array_set.__contains__(current_address):
                    print(current_address, "|", current_time.strftime('%H:%M') , "|", failure_reason_array)
                    _3_11_address_string = current_address_short_form + "|"+ current_time.strftime('%H:%M') + (" - " + str(failure_reason_array) if failure_reason_array else "") + " *3_11"
                    unselected_address_set.append(_3_11_address_string) if(failure_reason_array) else selected_address_set.append(_3_11_address_string)
                    continue
                    
                
                if _2_11_array_set.__contains__(current_address):
                    print(current_address, "|", current_time.strftime('%H:%M') , "|", failure_reason_array)
                    _2_11_address_string = current_address_short_form + "|"+ current_time.strftime('%H:%M') + (" - " + str(failure_reason_array) if failure_reason_array else "") + " *2_11"
                    unselected_address_set.append(_2_11_address_string) if(failure_reason_array) else selected_address_set.append(_2_11_address_string)
                    continue
                    

                if _4_11_array_set.__contains__(current_address):
                    print(current_address, "|", current_time.strftime('%H:%M') , "|", failure_reason_array)
                    _4_11_address_string = current_address_short_form + "|"+ current_time.strftime('%H:%M') + (" - " + str(failure_reason_array) if failure_reason_array else "") + " *4_11"
                    unselected_address_set.append(_4_11_address_string) if(failure_reason_array) else selected_address_set.append(_4_11_address_string)
                    continue                    

                if _5_9_address_set.__contains__(current_address):
                    print(current_address, "|", current_time.strftime('%H:%M') , "|", failure_reason_array)
                    _5_9_address_string = current_address_short_form + "|"+ current_time.strftime('%H:%M') + (" - " + str(failure_reason_array) if failure_reason_array else "") + " *5_9"
                    unselected_address_set.append(_5_9_address_string) if(failure_reason_array) else selected_address_set.append(_5_9_address_string)
                    continue
                    

                if _2_11_10_address_set.__contains__(current_address):
                    print(current_address, "|", current_time.strftime('%H:%M') , "|", failure_reason_array)
                    _2_11_10_address_string = current_address_short_form + "|"+ current_time.strftime('%H:%M') + (" - " + str(failure_reason_array) if failure_reason_array else "") +  " *2_11_10"
                    unselected_address_set.append(_2_11_10_address_string) if(failure_reason_array) else selected_address_set.append(_2_11_10_address_string)
                    continue
                    

                if _2_9_10_adress_set.__contains__(current_address):
                    print(current_address, "|", current_time.strftime('%H:%M') , "|", failure_reason_array)
                    _2_9_10_address_string = current_address_short_form + "|"+ current_time.strftime('%H:%M') + (" - " + str(failure_reason_array) if failure_reason_array else "") + " *2_9_10"
                    unselected_address_set.append(_2_9_10_address_string) if(failure_reason_array) else selected_address_set.append(_2_9_10_address_string)
                    continue
                    

                if _2_5_11_address_set.__contains__(current_address):
                    print(current_address, "|", current_time.strftime('%H:%M') , "|", failure_reason_array)
                    _2_5_11_address_string = current_address_short_form + "|"+ current_time.strftime('%H:%M') + (" - " + str(failure_reason_array) if failure_reason_array else "") + " *2_5_11"
                    unselected_address_set.append(_2_5_11_address_string) if(failure_reason_array) else selected_address_set.append(_2_5_11_address_string)
                    continue
                    
                print("Final Conditions met for this timeslot:", condtions_met)
                if condtions_met == False:
                    print(current_address, "|", current_time.strftime('%H:%M') , "|", failure_reason_array)
                    unselected_address_string = current_address_short_form + "|"+ current_time.strftime('%H:%M') + (" - " + str(failure_reason_array) if failure_reason_array else "") + " *"
                    unselected_address_set.append(unselected_address_string)
                else:
                    print("ELSE")
                    print(current_address, "|", current_time.strftime('%H:%M') , ":(✓)")
                    selected_address_string = current_address_short_form+ "|"+ current_time.strftime('%H:%M') + " *"
                    selected_address_set.append(selected_address_string)

            else:
                '''print("Ascendant sub_lord does NOT match 11th lord; skipping those specific checks.")'''

            '''print("Conditions met for this timeslot:", condtions_met)
            '''

        except Exception as e:
            print("Exception while processing:", repr(e))

        # Move to next time slot (every 2 minutes)
        current_time += timedelta(minutes=2)
        time.sleep(1)  # Pauses execution for 1 second

    file_name = f"{end_dt.day}_{end_dt.month}_{end_dt.year}.txt"
            
    with open(file_name, "a") as f:
        f.write("Selected Muhurt"+"\n")     
        f.write("==================="+"\n")   
        for item in selected_address_set:
            f.write(item + "\n")    
        f.write("\nUnselected Muhurt"+"\n")
        f.write("==================="+"\n")
        for item in unselected_address_set:
            f.write(item + "\n")    
        f.write("\n11th Exclusive Muhurt"+"\n")
        f.write("==================="+"\n")
        for item in _11th_exclusive_address_array:
            f.write(item + "\n")
        f.write("\n3rd and 11th Lord Muhurt"+"\n")
        f.write("==================="+"\n")
        for item in _3_11_address_array:
            f.write(item + "\n")
        f.write("\n2nd and 11th Lord Muhurt"+"\n")
        f.write("==================="+"\n")
        for item in _2_11_address_array:
            f.write(item + "\n")
        f.write("\n4th and 11th Lord Muhurt"+"\n")
        f.write("==================="+"\n")
        for item in _4_11_address_array:
            f.write(item + "\n")
        f.write("\n5th and 9th Lord Muhurt"+"\n")
        f.write("==================="+"\n")
        for item in _5_9_address_array:
            f.write(item + "\n")
        f.write("\n2nd, 11th and 10th Lord Muhurt"+"\n")
        f.write("==================="+"\n")
        for item in _2_11_10_address_array:
            f.write(item + "\n")
        f.write("\n2nd, 9th and 10th Lord Muhurt"+"\n")
        f.write("==================="+"\n")
        for item in _2_9_10_address_array:
            f.write(item + "\n")
        f.write("\n2nd, 5th and 11th Lord Muhurt"+"\n")
        f.write("==================="+"\n")
        for item in _2_5_11_address_array:
            f.write(item + "\n")

    file_name = f"{end_dt.day}_{end_dt.month}_{end_dt.year}_script.html"

    html_content = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Muhurt Results - {input_date}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f8f9fa;
            }}
            header {{
                color: rgb(0, 0, 0);
                text-align: center;
                padding: 20px 10px;
            }}
            h1 {{
                text-align: center;
                color: #1f2937;
                border-bottom: 3px solid #2563eb;
                padding-bottom: 10px;
                margin-bottom: 30px;
            }}
            h2 {{
                color: #2563eb;
                margin-top: 40px;
                margin-bottom: 20px;
                font-size: 22px;
                border-left: 6px solid #2563eb;
                padding-left: 10px;
            }}
            .container {{
                display: flex;
                flex-direction: column; /* Vertical stack */
                gap: 40px;
                align-items: left;
            }}
            .list {{
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                padding: 20px;
                width: 100%;
            }}
            .item {{
                background: #f9fafb;
                border-left: 5px solid #3b82f6;
                margin-bottom: 15px;
                border-radius: 8px;
                padding: 15px 20px;
                transition: 0.3s;
                font-weight: bold;
                color: #374151;
                font-size: 30px;                
            }}
            .uitem {{
                background: #f9fafb;
                border-left: 5px solid #ea1919;
                margin-bottom: 15px;
                border-radius: 8px;
                padding: 15px 20px;
                transition: 0.3s;
                font-weight: bold;
                color: #374151;
                font-size: 30px;
            }}            
            .highlight {{
                background-color: #9af0ab !important;
                font-weight: bold;
            }}
            .time {{
                color: #555;
                float: right;
            }}
            #clock {{
            position: absolute;
            top: 20px;
            right: 30px;
            font-size: 40px;
            color: #374151;
            }}       
     /* Astrology chart styles */
            .chart {{
                display: grid;
                grid-template-columns: repeat(4, 1fr); /* Four equal-width columns */
                grid-template-rows: repeat(4, 1fr);
                width: 100%; /* Fill available width */
                aspect-ratio: 2 / 1; /* Keep it square */
                border: 3px solid #000;
                background-color: white;
                border-radius: 20px; /* <-- rounded corners */
                overflow: hidden; /* hides cell borders at the corners */                
                box-shadow: 0 0 10px rgba(0,0,0,0.2);
                margin-top: 40px;
            }}

            .cell {{
                border: 1px solid #000;
                display: flex;
                justify-content: center;
                align-items: center;
                font-weight: bold;
                font-size: 1.2vw; /* Scales with width */
                color: #1f2937;
                position: relative;
            }}

            .cell span {{
                position: centered;
                top: 5px;
                left: 5px;
                font-size: 2.8vw;
                font-weight: bold;
                color: #555;
            }}

            .merged {{
                grid-column: 2 / span 2;
                grid-row: 2 / span 2;
                background-color: #f3f4f6;
                border: 2px solid #000;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 2.5vw;
                font-weight: bold;
            }}


            .chart-container {{
                text-align: center;
            }}
            .chart-container h2 {{
                border-left: none;
                margin-bottom: 10px;
            }}            
            


        </style>
    </head>
    <body>
        <header>
            <p id="toggleHide" 
            style="position: absolute; top: 20px; left: 30px; font-size: 24px; color: #2563eb; cursor: pointer; font-weight: bold;">
            Full
            </p>

            <h1>Muhurt {input_date} <p id="clock" style="font-size: 40px; color: #374151; margin-top: 10px;"></p></h1>
        </header>
        <!--
        <div class="chart-container">
            <h2>Astrology Chart</h2>
            <div class="chart">
            <div id="12" class="cell"><span>12</span></div>
            <div id="1" class="cell"><span>1</span></div>
            <div id="2" class="cell"><span>2</span></div>
            <div id="3" class="cell"><span>3</span></div>
            <div id="11" class="cell"><span>11</span></div>
            <div class="merged" id="chartcenter">Kocharam</div>
            <div id="4" class="cell"><span>4</span></div>
            <div id="10" class="cell"><span>10</span></div>
            <div id="5" class="cell"><span>5</span></div>
            <div id="9" class="cell"><span>9</span></div>
            <div id="8" class="cell"><span>8</span></div>
            <div id="7" class="cell"><span>7</span></div>
            <div id="6" class="cell"><span>6</span></div>
        </div>
        -->
              
        <div class="container">
            <div class="list" id="selected">
                <h2>Selected Muhurt</h2>
                {''.join(f'<div class="{ "uitem" if "-" in item else "item" }" data-time="{item.split("|")[1].split()[0]}">{item.split("*")[0].strip().replace("|","&nbsp&nbsp|&nbsp&nbsp")}<span style="float: right; color: blue;">{item.split("*")[1].strip()}</span></div>' for item in selected_address_set)}
            </div>
            <div class="list" id="unselected">
                <h2>Unselected Muhurt</h2>
                {''.join(f'<div class="uitem" data-time="{item.split("|")[1].split()[0]}">{item.split("*")[0].strip()}<span style="float: right; color: blue;">{item.split("*")[1].strip()}</span></div>' for item in unselected_address_set)}
            </div>
                                    

        </div>
        <!-- Astrology Box 
        <div class="chart-container">
            <h2>Astrology Chart</h2>
            <div class="chart">
            <div id="12" class="cell"><span>12</span></div>
            <div id="1" class="cell"><span>1</span></div>
            <div id="2" class="cell"><span>2</span></div>
            <div id="3" class="cell"><span>3</span></div>
            <div id="11" class="cell"><span>11</span></div>
            <div class="merged">CENTER</div>
            <div id="4" class="cell"><span>4</span></div>
            <div id="10" class="cell"><span>10</span></div>
            <div id="5" class="cell"><span>5</span></div>
            <div id="9" class="cell"><span>9</span></div>
            <div id="8" class="cell"><span>8</span></div>
            <div id="7" class="cell"><span>7</span></div>
            <div id="6" class="cell"><span>6</span></div>
        </div>
        -->

        <script>
            let hideMode = true; // start in hide mode (only future items shown)

            
            function hidePastItems() {{
                const nowUTC = new Date();
                const istOffset = 5.5 * 60 * 60 * 1000; // IST = UTC + 5:30
                const istTime = new Date(nowUTC.getTime() + istOffset);
                const currentMinutes = istTime.getUTCHours() * 60 + istTime.getUTCMinutes();

                document.querySelectorAll(".item, .uitem").forEach(div => {{
                    const timeText = div.dataset.time;
                    if (!timeText) return;
                    const [hours, minutes] = timeText.split(":").map(Number);
                    const divMinutes = hours * 60 + minutes;

                    if (hideMode && currentMinutes > divMinutes + 15) {{
                        div.style.display = "none"; // hide past + 15 min
                    }} else {{
                        div.style.display = ""; // show all
                    }}
                }});
            }}
            
            function toggleHideMode() {{
                hideMode = !hideMode;
                const toggleBtn = document.getElementById("toggleHide");
                toggleBtn.textContent = hideMode ? "Full" : "Live";
                hidePastItems();
            }}

        
            function updateISTClock() {{
                const nowUTC = new Date();
                const istOffset = 5.5 * 60 * 60 * 1000; // IST = UTC + 5:30
                const istTime = new Date(nowUTC.getTime() + istOffset);
        
                const hours = String(istTime.getUTCHours()).padStart(2, '0');
                const minutes = String(istTime.getUTCMinutes()).padStart(2, '0');
                const seconds = String(istTime.getUTCSeconds()).padStart(2, '0');
        
                document.getElementById("clock").textContent =
                    `${{hours}}:${{minutes}}:${{seconds}}`;
            }}

            function highlightNextInSection(sectionId) {{
                const now = new Date();
                const currentMinutes = now.getHours() * 60 + now.getMinutes();
                let nextItem = null;
                let smallestDiff = Infinity;

                
                //const items = document.querySelectorAll(`#${{sectionId}} .item`);
                const items = document.querySelectorAll(`.item`);

                items.forEach(el => {{
                    const timeMatch = el.dataset.time?.split(':');
                    if (!timeMatch || timeMatch.length < 2) return;
                    const hrs = parseInt(timeMatch[0]);
                    const mins = parseInt(timeMatch[1]);
                    const totalMins = hrs * 60 + mins;
                    const diff = totalMins - currentMinutes;
                    if (diff > 0 && diff < smallestDiff) {{
                        smallestDiff = diff;
                        nextItem = el;
                    }}
                }});

                items.forEach(el => el.classList.remove('highlight'));
                if (nextItem) {{
                    nextItem.classList.add('highlight');
                }}
            }}

            function highlightNextMuhurt() {{
                highlightNextInSection('selected');
                //highlightNextInSection('unselected');
            }}

            window.onload = function() {{
                document.getElementById("toggleHide").addEventListener("click", toggleHideMode);

                hidePastItems();          
                highlightNextMuhurt();    
                updateISTClock();

                setInterval(updateISTClock, 1000);
                setInterval(highlightNextMuhurt, 60000);
                setInterval(hidePastItems, 60000); // auto-refresh every minute
            }};

        </script>        

    </body>
    </html>"""

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML file '{file_name}' created successfully.")    
    
    return "Completed all time slots."

# ===========================
# RUN
# ===========================
'''
if __name__ == "__main__":
    start_date = datetime.strptime("14/11/2025", "%d/%m/%Y")
    end_date = datetime.strptime("14/11/2025", "%d/%m/%Y")

    current_date = start_date
    while current_date <= end_date:
        run_for_date(current_date.strftime("%d/%m/%Y"), "00:00", "23:59")
        current_date += timedelta(days=1)    
'''

if __name__ == "__main__":
    tomorrow = datetime.today() '''+ timedelta(days=1)'''

    start_date = tomorrow
    end_date = tomorrow

    current_date = start_date
    while current_date <= end_date:
        run_for_date(current_date.strftime("%d/%m/%Y"), "00:00", "23:59")
        current_date += timedelta(days=1)        
