import json
import datetime
import matplotlib.pyplot as plt

def load_covid_data(filepath):
    # Determine which fields need to exist in the Json file and store them in these lists
    top_dict_keys = ['metadata','region','evolution']
    metadata_keys = ['time-range', 'age_binning']
    metadata_time_range_keys = ['start_date', 'stop_date']
    metadata_age_binning_keys = ['hospitalizations', 'population']
    
    region_keys = ['name', 'key', 'latitude', 'longitude', 'elevation', 'area', 'population', 'open_street_maps', 'noaa_station', 'noaa_distance']
    region_area_keys = ['total', 'rural', 'urban']
    region_population_keys = ['total', 'male', 'female', 'age', 'rural', 'urban']
    
    evolution_values_keys = ['hospitalizations', 'epidemiology', 'weather', 'government_response']
    evolution_values_hospitalizations_keys = ['hospitalized','intensive_care','ventilator']
    evolution_values_hospitalized_keys = ['new','total','current']
    evolution_values_new_total_current_keys=['all','male','female','age']
    evolution_values_epidemiology_keys = ['confirmed','deceased','recovered','tested']
    evolution_values_epidemiology_conf_dec_rec_test_keys = ['new','total']
    evolution_values_weather_keys = ['temperature','rainfall','snowfall','dew_point','relative_humidity']
    evolution_values_weather_temperature_keys = ['average','min','max']
    
    # Open file from filepath
    with open(filepath) as load_json:
            all_covid_data = json.load(load_json)
    if all_covid_data == {}:
        raise Exception("This is an Empty Json file.")
    else:
        for top_key in all_covid_data.keys():
            if len(all_covid_data.keys())!=len(top_dict_keys):
                raise Exception("Data Error: Lose value -- 'metadata', 'region' or 'evolution'")
            else:
                if top_key not in top_dict_keys:
                    raise Exception("Data Error: Should match the 'metadata', 'region', and 'evolution'")
    
        for metadata_key in all_covid_data['metadata'].keys():
            if len(all_covid_data['metadata'].keys())!=len(metadata_keys):
                raise Exception("Data Error: Lose value -- 'time-range' or 'age_binning'")
            else:
                if metadata_key not in metadata_keys:
                    raise Exception("Data Error: Not match")
        for metadata_time_range_key in all_covid_data['metadata']['time-range'].keys():
            if len(all_covid_data['metadata']['time-range'].keys())!=len(metadata_time_range_keys):
                raise Exception("Data Error: Lose value -- 'start_date' or 'stop_date')")
            else:
                if metadata_time_range_key not in metadata_time_range_keys:
                    raise Exception("metadata/time-range Data Error: Not match")
        for metadata_age_binning_key in all_covid_data['metadata']['age_binning'].keys():
            if len(all_covid_data['metadata']['age_binning'].keys())!=len(metadata_age_binning_keys):
                raise Exception("Data Error: Lose value -- 'hospitalizations' or 'population'")
            else:
                if metadata_age_binning_key not in metadata_age_binning_keys:
                    raise Exception("metadata/age_binning Data Error: Not match")    
                else:
                    len_hosp_age_bining = len(all_covid_data['metadata']['age_binning']['hospitalizations'])
                    len_pop_age_bining = len(all_covid_data['metadata']['age_binning']['population'])
        for region_key in all_covid_data['region'].keys():
            if len(all_covid_data['region'].keys())!=len(region_keys):
                raise Exception("Data Error: Lose value -- 'name', 'key',..., 'noaa_distance'")
            else:
                if region_key not in region_keys:
                    raise Exception("Data Error: Not match")
        for region_area_key in all_covid_data['region']['area'].keys():
            if len(all_covid_data['region']['area'].keys())!=len(region_area_keys):
                raise Exception("Data Error: Lose value -- 'total', 'rural' or 'urban'")
            else:
                if region_area_key not in region_area_keys:
                    raise Exception("region/area Data Error: Not match")
        for region_population_key in all_covid_data['region']['population'].keys():
            if len(all_covid_data['region']['population'].keys())!=len(region_population_keys):
                raise Exception("Data Error: Lose value -- 'total', 'male' ,..., 'urban'")
            else:
                if region_population_key not in region_population_keys:
                    raise Exception("region/population Data Error: Not match")
                elif len(all_covid_data['region']['population']["age"])!=len_pop_age_bining:
                    raise Exception("population age bin and population number do not match")
                

        for evolution_key in all_covid_data['evolution'].keys():
            try:
                datetime.datetime.strptime(evolution_key, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Incorrect data format, should be YYYY-MM-DD")
            else:
                for evolution_value in all_covid_data['evolution'].values():
                    for evolution_value_key in evolution_value.keys():
                        if len(evolution_value.keys())!=len(evolution_values_keys):
                            raise Exception("Data Error: Lose value -- 'hospitalizations', 'epidemiology', 'weather' or 'government_response'")
                        else:
                            if evolution_value_key not in evolution_values_keys:
                                raise Exception("evolution/value Data Error: Not match")
                            else:
                                for hos_key,hos_value in evolution_value['hospitalizations'].items():
                                    if len(evolution_value['hospitalizations'].keys())!=len(evolution_values_hospitalizations_keys):
                                        raise Exception("Data Error: Lose value -- 'hospitalized','intensive_care' or 'ventilator'")
                                    else:
                                        if hos_key not in evolution_values_hospitalizations_keys:
                                            raise Exception("evolution/value/hospitalizations Data Error: Not match")
                                        else:
                                            for hos_value_key, hos_value_value in hos_value.items():
                                                if len(hos_value.keys())!=len(evolution_values_hospitalized_keys):
                                                    raise Exception("Data Error: Lose value -- 'new','total' or 'current'")
                                                else:
                                                    if hos_value_key not in evolution_values_hospitalized_keys:
                                                        raise Exception("evolution/value/hospitalized_intensive_ventilator Data Error: Not match")
                                                    elif len(evolution_value['hospitalizations'][hos_key][hos_value_key]['age'])!=len_hosp_age_bining:
                                                        raise Exception("hospitalizations age bin and hospitalized number do not match")
                                                    else:
                                                        for hospitalized_key in hos_value_value.keys():
                                                            if len(hos_value_value.keys())!=len(evolution_values_new_total_current_keys):
                                                                raise Exception("Data Error: Lose value -- 'all','male','female' or 'age'")
                                                            else:
                                                                if hospitalized_key not in evolution_values_new_total_current_keys:
                                                                    raise Exception("evolution/value/new_total_current Data Error: Not match")
                                                               
                                for epi_key,epi_value in evolution_value['epidemiology'].items():
                                    if len(evolution_value['epidemiology'].keys())!=len(evolution_values_epidemiology_keys):
                                        raise Exception("Data Error: Lose value -- 'confirmed','deceased','recovered' or 'tested'")
                                    else:
                                        if epi_key not in evolution_values_epidemiology_keys:
                                            raise Exception("evolution/value/epidemiology Data Error: Not match")
                                        else:
                                            for epi_value_key, epi_value_value in epi_value.items():
                                                if len(epi_value.keys())!=len(evolution_values_epidemiology_conf_dec_rec_test_keys):
                                                    raise Exception("Data Error: Lose value -- 'new' or 'total'")
                                                else:
                                                    if epi_value_key not in evolution_values_epidemiology_conf_dec_rec_test_keys:
                                                        raise Exception("evolution/value/conf_dec_rec_test Data Error: Not match")
                                                    elif len(evolution_value['epidemiology'][epi_key][epi_value_key]['age'])!=len_hosp_age_bining:
                                                        raise Exception("hospitalizations age bin and epidemiology number do not match")
                                                    else:
                                                        for confirmed_key in epi_value_value.keys():
                                                            if len(epi_value_value.keys())!=len(evolution_values_new_total_current_keys):
                                                                raise Exception("Data Error: Lose value -- 'all','male','female' or 'age'")
                                                            else:
                                                                if confirmed_key not in evolution_values_new_total_current_keys:
                                                                    raise Exception("evolution/value/new_total_current Data Error: Not match")
                                for wea_key,wea_value in evolution_value['weather'].items():
                                    if len(evolution_value['weather'].keys())!=len(evolution_values_weather_keys):
                                        raise Exception("Data Error: Lose value -- 'temperature','rainfall','snowfall','dew_point' or 'relative_humidity'")
                                    else:
                                        if wea_key not in evolution_values_weather_keys:
                                            raise Exception("evolution/value/weather Data Error: Not match")
                                        else:
                                            if isinstance(wea_value,dict):
                                                for wea_value_key in wea_value.keys():
                                                    if len(wea_value.keys())!=len(evolution_values_weather_temperature_keys):
                                                        raise Exception("Data Error: Lose value -- 'average','min' or 'max'")
                                                    else:
                                                        if wea_value_key not in evolution_values_weather_temperature_keys:
                                                            raise Exception("evolution/value/weather/temperature Data Error: Not match")
                                if 'stringency_index' not in evolution_value['government_response'].keys():
                                    raise Exception("evolution/value/government_response Data Error: Not match")
    return all_covid_data


def cases_per_population_by_age(input_data):
    '''
    A = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-']
    B = ['0-19', '20-39', '40-']
    result = {'0-19': [('2020-05-23', 3.3), ('2020-05-24', 3.4), ...]
    '20-39': [(...)]

    If A and B cannot be matched.
    A = ['0-14', '15-29', '30-44', '45-']
    B = ['0-19', '20-39', '40-']
    throw an error
    '''
    # First get the hospitalizations age bin and the population age bin from the file, and split range edge to a 2D list.
    result_date_age_group_ratio={}
    a_ranges = []
    b_ranges = []
    for i in input_data["metadata"]["age_binning"]["hospitalizations"]:      
        a_ranges.append([i.split("-")[0],i.split("-")[1]])
    for j in input_data["metadata"]["age_binning"]["population"]:
        b_ranges.append([j.split("-")[0],j.split("-")[1]])
    # Throw an exception if there is a null value
    if len(a_ranges)==0:
        raise Exception("hospitalizations's age ranges are None.")
    if len(b_ranges)==0:    
        raise Exception("population's age ranges are None.")
    # For convenience, set a maximum age of 999
    for i in  range(len(a_ranges)):
        if a_ranges[i][1] == '':
            a_ranges[i][1] = '999'
        else:
            # Ensure that the arrays are disjoint. 0-24 and 25-39 instead of 0-24 and 24-39
            if int(a_ranges[i][1]) + 1 != int(a_ranges[i+1][0]) and i != len(a_ranges):
                raise Exception("hospitalizations's age ranges have some issue.")
    for j in  range(len(b_ranges)):
        if b_ranges[j][1] == '':
            b_ranges[j][1] = '999'
        else:
            if int(b_ranges[j][1]) + 1 != int(b_ranges[j+1][0]) and j != len(b_ranges):
                raise Exception("population's age ranges have some issue.")
    # In order to facilitate the subsequent steps, convert the values in the list into integers
    for i in  range(len(a_ranges)):
        a_ranges[i][0] = int(a_ranges[i][0])
        a_ranges[i][1] = int(a_ranges[i][1])
    for j in  range(len(b_ranges)):
        b_ranges[j][0] = int(b_ranges[j][0])
        b_ranges[j][1] = int(b_ranges[j][1])
    
    # Set the required parameters. 
    # index1 and index2 are used to traverse the two age range lists respectively

    index1=0
    index2=0
    overlap_ranges = []
    newconf_num_list = []
    population_num_list = []
    overlap_newconf_num = []
    overlap_total_num = []
    date_list = []
    
    evolution_data = input_data['evolution']

    for evo_key,epi in evolution_data.items():
        date_list.append(evo_key)
        for conf_key, conf_value in epi['epidemiology'].items():
            if conf_key =='confirmed':

                for i in range(len(conf_value['total']['age'])):
                    if conf_value['total']['age'][i] == None:
                        conf_value['total']['age'][i] = 0
                
                newconf_num_list.append(conf_value['total']['age'])       
    
    for i in range(len(input_data['region']['population']['age'])):
        if input_data['region']['population']['age'][i] == None:
            input_data['region']['population']['age'][i] = 0
    population_num_list.append(input_data['region']['population']['age'])
    # First find the position with the same first value in the two lists, and mark them with index1 and index2 respectively. Then determine which value of the second value of the position is greater, the smaller one starts to search in its own list, find the value that can be equal, and record the position with index. Then rebin. When rebining, their corresponding values are also rebined.
    while index1 < len(a_ranges) and index2 < len(b_ranges):
        if a_ranges[index1][0]==b_ranges[index2][0] and a_ranges[index1][1]==b_ranges[index2][1]:
            tmp = []
            tmp_num_newconf = []
            tmp_num_total = []
            tmp_num_newconf = [i[index1] for i in newconf_num_list]
            tmp_num_total = [i[index2] for i in population_num_list]
            tmp.append(min(a_ranges[index1][0], b_ranges[index2][0]))
            tmp.append(max(a_ranges[index1][1], b_ranges[index2][1]))
            index1 = index1 + 1
            index2 = index2 + 1
            overlap_newconf_num.append(tmp_num_newconf)
            overlap_total_num.append(tmp_num_total)                
            overlap_ranges.append(tmp)
            
        elif a_ranges[index1][0]==b_ranges[index2][0] and a_ranges[index1][1] < b_ranges[index2][1]:
                while index1<len(a_ranges):
                    tmp = []
                    tmp_num_newconf = []
                    tmp_num_newconf_add = []
                    tmp_num_newconf_result = []
                    tmp_num_total = []
                    tmp_num_total = [i[index2] for i in population_num_list]
                    tmp_num_newconf = [i[index1] for i in newconf_num_list]
                    index1 = index1 + 1
                    tmp_num_newconf_add = [i[index1] for i in newconf_num_list]
                    for  i in range(len(newconf_num_list)):
                        tmp_num_newconf_result.append(tmp_num_newconf[i] + tmp_num_newconf_add[i]) 
                    
                    if a_ranges[index1][1] == b_ranges[index2][1]:
                        tmp.append(min(a_ranges[index1][0], b_ranges[index2][0]))
                        tmp.append(max(a_ranges[index1][1], b_ranges[index2][1]))
                        overlap_ranges.append(tmp)
                        overlap_newconf_num.append(tmp_num_newconf_result) 
                        overlap_total_num.append(tmp_num_total)  
                        break
                    elif a_ranges[index1][1] > b_ranges[index2][1]:
                        raise Exception("Error: the age ranges provided cannot be rebined")
                index1 = index1 + 1
                index2 = index2 + 1
       
        elif a_ranges[index1][0]==b_ranges[index2][0] and a_ranges[index1][1] > b_ranges[index2][1]:   
                while index2<len(b_ranges):
                    tmp = []
                    tmp_num_newconf = []
                    tmp_num_total = []
                    tmp_num_total_add = []
                    tmp_num_total_result = []
                    tmp_num_total = [i[index2] for i in population_num_list]
                    tmp_num_newconf = [i[index1] for i in newconf_num_list]
                    
                    index2 = index2 + 1
                    tmp_num_total_add = [i[index2] for i in population_num_list]
                    for  i in range(len(population_num_list)):
                        tmp_num_total_result.append(tmp_num_total[i] + tmp_num_total_add[i])
                    if b_ranges[index2][1] == a_ranges[index1][1]:
                        tmp.append(min(a_ranges[index1][0], b_ranges[index2][0]))
                        tmp.append(max(a_ranges[index1][1], b_ranges[index2][1]))
                        overlap_ranges.append(tmp)
                        overlap_total_num.append(tmp_num_total_add) 
                        overlap_newconf_num.append(tmp_num_newconf)
                        break
                    elif b_ranges[index2][1] > a_ranges[index1][1]:
                        raise Exception("Error: the age ranges provided cannot be rebined")
                index1 = index1 + 1
                index2 = index2 + 1            
        else:
            index1 = index1 + 1
            index2 = index2 + 1
    if len(overlap_ranges)==0:
        raise Exception("Error: the age ranges provided cannot be rebined")
        
    date_conf_total_ratio_list = []
    for i in range(len(overlap_ranges)):
        date_conf_total_ratio_tuple = ()
        tmp_date_conf_total_ratio_list = []
        for date in range(len(date_list)):
            if overlap_total_num[i][0] == 0:
                break
            ratio = overlap_newconf_num[i][date] / overlap_total_num[i][0] * 100
            date_conf_total_ratio_tuple = (date_list[date],ratio)
            tmp_date_conf_total_ratio_list.append(date_conf_total_ratio_tuple)
        date_conf_total_ratio_list.append(tmp_date_conf_total_ratio_list)
    overlap_ranges_convert_strlist = []    
    
    for i in range(len(overlap_ranges)):
        if overlap_ranges[i][1] == 999:
            tmp_str = f'{overlap_ranges[i][0]}-'
        else:
            tmp_str = f'{overlap_ranges[i][0]}-{overlap_ranges[i][1]}'
        overlap_ranges_convert_strlist.append(tmp_str)
        
        age_group = overlap_ranges_convert_strlist[i]
        result_date_age_group_ratio[f"{age_group}"] = date_conf_total_ratio_list[i]
    return result_date_age_group_ratio

def hospital_vs_confirmed(input_data):
    evolution_data = input_data['evolution']
    conf_date = []
    hospital_data = []
    new_confirmed_data = []
    hosp_newconf_ratio = []
    result_date_hosp_newcon_ratio = []

    for key,info in evolution_data.items():
        hospital_num = info['hospitalizations']['hospitalized']['new']['all']
        new_confirmed_num = info['epidemiology']['confirmed']['new']['all']
        if hospital_num == None or new_confirmed_num == None:
            continue
        else:
            conf_date.append(key)
            hospital_data.append(hospital_num)
            new_confirmed_data.append(new_confirmed_num)
            hosp_newconf_ratio.append(hospital_num/new_confirmed_num)

    result_date_hosp_newcon_ratio.append(conf_date)
    result_date_hosp_newcon_ratio.append(hosp_newconf_ratio)
    result_date_hosp_newcon_ratio=tuple(result_date_hosp_newcon_ratio)
    return result_date_hosp_newcon_ratio 

def generate_data_plot_confirmed(input_data, sex, max_age, status):
    """
    At most one of sex or max_age allowed at a time.
    sex: only 'male' or 'female'
    max_age: sums all bins below this value, including the one it is in.
    status: 'new' or 'total' (default: 'total')
    """
    if sex and max_age:
        raise ValueError("At most one of sex or max_age allowed at a time.")
    else:
        if status == 'total':
            plot_linestyle='solid'
        elif status == 'new':
            plot_linestyle='dashed'
        elif status == '':
            status = 'total'
        else:
            raise ValueError("The entered status value does not meet the requirements")
            
        if sex:
            evolution_data = input_data['evolution']
            if sex =='male' or sex =='female':
                if sex == 'male':
                    plot_color ='green' 
                else:
                    plot_color = 'purple'
                    
                sex_conf_data = []
                conf_date = []
                result_sex_data_plot = {}
                
                for key,info in evolution_data.items():
                    sex_conf_num = info['epidemiology']['confirmed'][status][sex]
                    conf_date.append(key)
                    sex_conf_data.append(sex_conf_num)
        
                result_sex_data_plot['date'] = conf_date
                result_sex_data_plot['value'] = sex_conf_data
                result_sex_data_plot['label'] = f'{status} {sex}'
                result_sex_data_plot['linestyle'] = plot_linestyle
                result_sex_data_plot['color'] = plot_color
                return result_sex_data_plot
            else:
                raise ValueError("The entered sex value does not meet the requirements.")
                
        else:
            if isinstance(max_age,int):     
                age_conf_data = []
                conf_date = []
                result_age_data_plot = {}
                bin_count = 0
                age = 0
                age_ranges = []
                blew_maxage_conf_data = []
                evolution_data = input_data['evolution'] 
                
                for evo_key,epi in evolution_data.items():
                    conf_date.append(evo_key)
                    for conf_key, conf_value in epi['epidemiology'].items():
                        if conf_key =='confirmed':
                            for i in range(len(conf_value[status]['age'])):
                                if conf_value[status]['age'][i] == None:
                                    conf_value[status]['age'][i] = 0
                            age_conf_data.append(conf_value[status]['age']) 
                
                for i in input_data["metadata"]["age_binning"]["hospitalizations"]:      
                    age_ranges.append([i.split("-")[0],i.split("-")[1]])
                for i in  range(len(age_ranges)):
                    if age_ranges[i][1] == '':
                        age_ranges[i][1] = '999'
                    else:
                        if int(age_ranges[i][1]) + 1 != int(age_ranges[i+1][0]) and i != len(age_ranges):
                            raise Exception("hospitalizations's age ranges have some issue.")
                    age_ranges[i][0] = int(age_ranges[i][0])
                    age_ranges[i][1] = int(age_ranges[i][1])
                    if max_age >= age_ranges[i][0]:
                        bin_count = bin_count + 1
                        age = age_ranges[i][1]
                    if age <= 25:
                        plot_color ='green'
                    elif age <= 50:
                        plot_color ='orange'
                    elif age <= 75:
                        plot_color ='purple'
                    else:
                        plot_color ='pink'   
                        
                for i in range(len(age_conf_data)):
                    tmp_age_bin_num = 0
                    tmp_bin_count = bin_count
                    while tmp_bin_count > 0:
                        tmp_bin_count = tmp_bin_count - 1
                        tmp_age_bin_num = tmp_age_bin_num + age_conf_data[i][tmp_bin_count]           
                    blew_maxage_conf_data.append(tmp_age_bin_num)
        
                result_age_data_plot['label'] = f'{status} younger than {age}'
                           
                result_age_data_plot['date'] = conf_date
                result_age_data_plot['value'] = blew_maxage_conf_data
                result_age_data_plot['linestyle'] = plot_linestyle
                result_age_data_plot['color'] = plot_color
                return result_age_data_plot  
            else:
                raise ValueError("The entered max_age value does not meet the requirements.")
                                
def create_confirmed_plot(input_data, sex=False, max_ages=[], status ='total', save:bool = False):
    if isinstance(sex,bool):
        if isinstance(save, bool):
            if status =='total' or status == 'new': 
                # check that only sex or age is specified.
                if sex and max_ages:
                    raise ValueError("At most one of sex or max_age allowed at a time.")
                elif sex == False and (max_ages==[] or max_ages==None):  
                    raise ValueError("At least one sex or max_age is required.")
                else:
                    fig = plt.figure(figsize=(10, 10))
                    region_name = input_data['region']['name']
                    
                    # runs only when the sex plot is required
                    if sex:
                        type = 'sex' 
                        for sex in ['male', 'female']:                      
                            
                            sex_plot_data = generate_data_plot_confirmed(input_data,sex,max_ages,status)
                            plt.plot('date', 'value', data = generate_data_plot_confirmed(input_data,sex,max_ages,status), label = sex_plot_data['label'], color =sex_plot_data['color'], linestyle=sex_plot_data['linestyle'])             
                    
                    #  runs only when the age plot is required
                    if max_ages:
                        type = 'age' 
                        for age in max_ages: 
                            age_plot_data = generate_data_plot_confirmed(input_data, sex, age, status)
                            
                            plt.plot('date', 'value', data = generate_data_plot_confirmed(input_data,sex,age,status), label = age_plot_data['label'], color =age_plot_data['color'], linestyle=age_plot_data['linestyle'] )
                    
                    fig.autofmt_xdate()  # To show dates nicely
                    plt.title(f"Confirmed cases in {region_name}")
                    plt.xlabel("date")
                    plt.ylabel("number of cases")
                    plt.legend(loc='upper left') 
                    # where type may be sex or age
                    if save:           
                        save_path = f"{region_name}_evolution_cases_{type}.png"
                        plt.savefig(save_path)
                        plt.close()
                    else:
                        plt.show()
            else:
                raise ValueError("status is not 'total' or 'new'")
        else:
            raise ValueError("save is not bool")
    else:
        raise ValueError("sex is not bool")
def compute_running_average(data, window):
    # Judge odd or even
    if (window % 2) != 0:
        result_average = []
        # Find gap
        gap = int((window - 1) / 2)
        for i in range(len(data)):
            if i - gap < 0:
                result_average.append(None)
 
            elif i + gap >= len(data):
                result_average.append(None)
            else:
                # denominator
                tmp_denominator = window
                tmp_data = 0
                for tmp in range(i - gap , i + gap + 1):
                    # if value equle None, Skip it, but subtract 1 from the denominator
                    if data[tmp] == None:
                        tmp_denominator = tmp_denominator -1
                    else:
                        tmp_data = tmp_data + data[tmp]
                if tmp_denominator <= 0:
                    result_average.append(None)
                else:
                    result_average.append(tmp_data/tmp_denominator)   
        return result_average
    else:
        raise ValueError("Window must be odd.")

def simple_derivative(data):
    result_simple_derivative = []
    for i in range(len(data)):
        if i - 1 < 0:
            result_simple_derivative.append(None)
        elif data[i]==None or data[i-1]==None:
            result_simple_derivative.append(None)
        else:
            result_simple_derivative.append(data[i]-data[i-1])
    return result_simple_derivative

def count_high_rain_low_tests_days(input_data):
      days_rain_increased_total_number = 0
      days_rain_increased_test_decreased_total_number = 0 
      day_rain_list = []
      day_test_list = []
      smoothly_day_test_list = []
      derivatived_day_rain_list = []
      derivatived_day_test_list = []
      for data in input_data['evolution'].values():
          day_rain_list.append(data['weather']['rainfall'])
          day_test_list.append(data['epidemiology']['tested']['new']['all'])
          
      smoothly_day_test_list = compute_running_average(day_test_list,7)
     
      derivatived_day_rain_list = simple_derivative(day_rain_list)
      derivatived_day_test_list = simple_derivative(smoothly_day_test_list)
      
      for i in range(len(derivatived_day_rain_list)):
          if derivatived_day_rain_list[i] != None and derivatived_day_rain_list[i] > 0 :
              days_rain_increased_total_number = days_rain_increased_total_number + 1
              if derivatived_day_test_list[i] != None and derivatived_day_test_list[i] < 0 :
                  days_rain_increased_test_decreased_total_number = days_rain_increased_test_decreased_total_number + 1
      result_ratio = days_rain_increased_test_decreased_total_number/days_rain_increased_total_number
      return result_ratio
