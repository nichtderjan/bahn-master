import pandas as pd
import xml.etree.ElementTree as ET
import logging
import copy

base = '/Users/jan/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Masterthesis/'


def load_ordnungsrahmen():

    # Parse the XML file
    tree = ET.parse(base + 'RB_Ost_KSS_ISS/Export_ISS/Ordnungsrahmen_ORBtrstB  21_ORBtrstYBLWG.xml')
    root = tree.getroot()

    # Define an empty list to store the data
    data = []

    # Extract the relevant information from each Betriebsstelle element
    for betriebsstelle in root.findall('.//Betriebsstelle'):
        ds100 = betriebsstelle.find('DS100').text.strip()
        name = betriebsstelle.find('Name').text.strip()
        x = float(betriebsstelle.find('Position/X').text)
        y = float(betriebsstelle.find('Position/Y').text)
        data.append([ds100, name, x, y])

    # Create the DataFrame
    df_Ordnungsrahmen = pd.DataFrame(data, columns=['DS100', 'Name', 'X', 'Y'])

    logging.debug(df_Ordnungsrahmen)
    return df_Ordnungsrahmen

def load_spurplanbetriebsstellen():
    tree = ET.parse(base + 'RB_Ost_KSS_ISS/Export_ISS/Spurplanbetriebsstellen_B  21_LMB.xml')
    root = tree.getroot()

    # Define a dictionary to store the data
    data = {'Betriebsstelle': [], 'Strecke': [], 'ID': [], 'Kilometrierung': [], 'X': [], 'Y': []}

    # Loop through the Spurplanbetriebsstelle elements and extract the data
    for sp in root.findall('.//Spurplanbetriebsstelle'):
        bs = sp.find('Betriebsstelle').text
        for sa in sp.findall('.//Spurplanabschnitt'):
            st = sa.find('Strecke').text
            for sk in sa.findall('.//Betriebsstellengrenze'):
                id_ = sk.find('ID').text
                km = sk.find('Kilometrierung').text
                x = sk.find('.//X').text
                y = sk.find('.//Y').text
                data['Betriebsstelle'].append(bs)
                data['Strecke'].append(st)
                data['ID'].append(id_)
                data['Kilometrierung'].append(km)
                data['X'].append(x)
                data['Y'].append(y)

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)
    logging.debug(df)
    return df

def load_kss():
    tree = ET.parse(base + 'RB_Ost_KSS_ISS/Export_KSS/KSS_88796-99953.xml')
    root = tree.getroot()
    idx = 0
    dict_for_pd = {}

    for child in root:
        if child.tag == 'railml':
            for child1 in child:
                if child1.tag == 'timetable':
                    for child2 in child1:
                        if child2.tag == 'train':
                            # here you can get trainID="1" trainNumber="26246/1" kind="RB-D (41.1)" timetablePeriodID="1"
                            # remarks="Geltungszeit: 13.11.2013 - 15.11.2013" in child__.attrib
                            train_attrib_dict = child2.attrib
                            for child3 in child2:
                                if child3.tag == 'timetableentries':
                                    for child4 in child3:
                                        if child4.tag == 'entry':
                                            dict_for_pd[idx] = copy.deepcopy(train_attrib_dict)
                                            dict_for_pd[idx].update(child4.attrib)
                                            for child5 in child4:
                                                if child5.tag == 'composition':
                                                    dict_for_pd[idx].update(child5.attrib)
                                                if child5.tag == 'section':
                                                    dict_for_pd[idx].update(child5.attrib)
                                                if child5.tag == 'additionalInformation':
                                                    for child6 in child5:
                                                            if child6.tag == 'basicCharacteristic':
                                                                for child7 in child6:
                                                                    if child7.tag == 'trainsetLength':
                                                                        dict_for_pd[idx]['trainsetLength'] = child7.text
                                                                    if child7.tag == 'trainsetWeight':
                                                                        dict_for_pd[idx]['trainsetWeight'] = child7.text
                                                                    if child7.tag == 'trainsetVelocity':
                                                                        dict_for_pd[idx]['trainsetVelocity'] = child7.text
                                                                    if child7.tag == 'maxVelocity':
                                                                        dict_for_pd[idx]['maxVelocity'] = child7.text
                                                                    if child7.tag == 'constructionVelocity':
                                                                        dict_for_pd[idx]['constructionVelocity'] = child7.text
                                                                    if child7.tag == 'lockingTrip':
                                                                        dict_for_pd[idx]['lockingTrip'] = child7.text
                                                                    if child7.tag == 'totalLength':
                                                                        dict_for_pd[idx]['totalLength'] = child7.text
                                                                    if child7.tag == 'totalWeight':
                                                                        dict_for_pd[idx]['totalWeight'] = child7.text


                                            idx += 1

    df = pd.DataFrame.from_dict(dict_for_pd)
    #transpose df_wild
    df = df.T
    logging.debug(df)
    return df
