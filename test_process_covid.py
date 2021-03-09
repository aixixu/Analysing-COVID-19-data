from pathlib import Path
from process_covid import (load_covid_data,
                  hospital_vs_confirmed,
                  cases_per_population_by_age,
                  generate_data_plot_confirmed,
                  create_confirmed_plot,
                  count_high_rain_low_tests_days,
                  simple_derivative,
                  compute_running_average
                  )
import pytest


# The example in the assignment description is converted to test
# 2.2 example
def test_example_1_can_rebin():
    '''
    A = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-']
    B = ['0-19', '20-39', '40-']
    them can be rebined.
    the expected result = ['0-19', '20-39', '40-']
    '''
    data_directory = Path("test_data")
    data_file = "Exactly_match_scheme_test_can_rebin.json"
    expected_result = ['0-19', '20-39', '40-']
    assert list(cases_per_population_by_age(load_covid_data(data_directory / data_file)).keys()) == expected_result

def test_example_1_cannot_rebin():
    '''
    A = ['0-14', '15-29', '30-44', '45-']
    B = ['0-19', '20-39', '40-']
    them cannot be rebined.
    so throw an error
    '''
    data_directory = Path("test_data")
    data_file = "Exactly_match_scheme_test_cannot_rebin.json"
    with pytest.raises(Exception) as e:
        cases_per_population_by_age(load_covid_data(data_directory / data_file))  
    assert e.match("Error: the age ranges provided cannot be rebined")
    
def test_example_1_not_broken_down_into_age_groups():
    '''
    this area the confirmed cases not broken down into age groups
    so them cannot be rebined.
    throw an error
    '''
    data_directory = Path("test_data")
    data_file = "Exactly_match_scheme_test_rebin_not_broken_down.json"
    with pytest.raises(Exception) as e:
        cases_per_population_by_age(load_covid_data(data_directory / data_file))  
    assert e.match("hospitalizations's age ranges are None.")

# 2.4 example
def test_example_2_not_correct_correct_save_argument():
    '''
    If the save parameter is not a boolean value, an error will be thrown
    '''
    data_directory = Path("test_data")
    data_file = "Exactly_match_scheme.json"
    with pytest.raises(Exception) as e:
        create_confirmed_plot(load_covid_data(data_directory / data_file),False,[10,34,55],'total','True')  
    assert e.match("save is not bool")

# 2.5 example
def test_example_3_compute_running_average_1():    
    '''
    input_data = [0, 1, 5, 2, 2, 5]
    window = 3 
    the expected result = [None, 2.0, 2.666, 3.0, 3.0, None]
    '''
    input_data = [0, 1, 5, 2, 2, 5]
    expected_result = [None, 2.0, 2.6666666666666665 , 3.0, 3.0, None]
    assert compute_running_average(input_data,3) == expected_result
    
def test_example_3_compute_running_average_2():    
    '''
    input_data = [2, None, 4]
    window = 3 
    the expected result = [None, 3.0, None]
    '''
    input_data = [2, None, 4]
    expected_result = [None, 3.0, None]
    assert compute_running_average(input_data,3) == expected_result
    
def test_example_3_simple_derivative():    
    '''
    input_data = [None, 1, 2, None, 4]
    the expected result = [None, None, 1, None, None]
    '''
    input_data = [None, 1, 2, None, 4]
    expected_result = [None, None, 1, None, None]
    assert simple_derivative(input_data) == expected_result



#Test load_covid_data
def test_load_covid_data_agebin_no_match_age_number():
    '''
    "age_binning": "hospitalizations" in this file:
          ["0-24",
          "25-49",
          "50-"]
    it is an array of length 3
    But the length of the following age data is 4 for example:
    "2020-03-16": {
       "hospitalizations": {
         "hospitalized": {
           "new": {
              ...
             "age": [
              15,
              23,
              21,
              13
             ]}}}}
    So an exception is thrown
    '''
    data_directory = Path("test_data")
    data_file = "Exactly_match_scheme_agebin_no_match_age_number.json"
    with pytest.raises(Exception) as e:
        load_covid_data(data_directory / data_file)  
    assert e.match("hospitalizations age bin and hospitalized number do not match")

def test_load_covid_data_no_match_case_empty_Json_file():
    '''
    Load an empty Json file
    '''
    data_directory = Path("test_data")
    data_file = "Empty_Json_file.json"
    with pytest.raises(Exception) as e:
        load_covid_data(data_directory / data_file)  
    assert e.match('This is an Empty Json file.')

def test_load_covid_data_no_match_case_no_region():
    '''
    Remove all region data
    '''
    data_directory = Path("test_data")
    data_file = "Not_Exactly_match_scheme_no_region.json"
    with pytest.raises(Exception) as e:
        load_covid_data(data_directory / data_file)  
    assert e.match("Data Error: Lose value -- 'metadata', 'region' or 'evolution'")
    
def test_load_covid_data_no_match_case_no_metadata_time_range():
    '''
    Remove all metadata:age_binning:hospitalizations
    '''
    data_directory = Path("test_data")
    data_file = "Not_Exactly_match_scheme_no_metadata_time_range.json"
    with pytest.raises(Exception) as e:
        load_covid_data(data_directory / data_file)  
    assert e.match("Data Error: Lose value -- 'time-range' or 'age_binning'")
    
def test_load_covid_data_no_match_case_no_metadata_age_binning_hospitalizations():
    '''
    Remove metadata:age_binning:hospitalizations
    '''
    data_directory = Path("test_data")
    data_file = "Not_Exactly_match_scheme_no_metadata_age_binning_hospitalizations.json"
    with pytest.raises(Exception) as e:
        load_covid_data(data_directory / data_file)  
    assert e.match("Data Error: Lose value -- 'hospitalizations' or 'population'")
    
def test_load_covid_data_no_match_case_no_female_data():
    '''
    Remove all female data
    '''
    data_directory = Path("test_data")
    data_file = "Not_Exactly_match_scheme_no_female_data.json"
    with pytest.raises(Exception) as e:
        load_covid_data(data_directory / data_file)  
    assert e.match("Data Error: Lose value -- 'total', 'male' ,..., 'urban'")

def test_load_covid_data_no_match_case_evolution_Incorrectly_formatted_date():
    '''
    Change the date data "2020-03-16" to "2020/03/16"
    '''
    data_directory = Path("test_data")
    data_file = "Not_Exactly_match_scheme_evolution_Incorrectly_formatted_date.json"
    with pytest.raises(ValueError) as e:
        load_covid_data(data_directory / data_file)  
    assert e.match("Incorrect data format, should be YYYY-MM-DD")
    
def test_load_covid_data_no_match_case_evolution_Incorrectly_date():
    '''
    Change the date data "2020-03-16" to "2020-03-32"
    '''
    data_directory = Path("test_data")
    data_file = "Not_Exactly_match_scheme_evolution_Incorrectly_date.json"
    with pytest.raises(ValueError) as e:
        load_covid_data(data_directory / data_file)  
    assert e.match("Incorrect data format, should be YYYY-MM-DD")
    
def test_load_covid_data_no_match_case_evolution_hospitalizations_changeto_hospital():
    '''
    Change the hospitalizations to hospital
    '''
    data_directory = Path("test_data")
    data_file = "Not_Exactly_match_scheme_evolution_hospitalizations_changeto_hospital.json"
    with pytest.raises(Exception) as e:
        load_covid_data(data_directory / data_file)  
    assert e.match("evolution/value Data Error: Not match")

def test_load_covid_data_no_match_case_evolution_government_response_no_stringency_index():
    '''
    Remove the stringency_index in evolution/government_response
    '''
    data_directory = Path("test_data")
    data_file = "Not_Exactly_match_scheme_evolution_government_response_no_stringency_index.json"
    with pytest.raises(Exception) as e:
        load_covid_data(data_directory / data_file)  
    assert e.match("evolution/value/government_response Data Error: Not match")



#Test hospital_vs_confirmed    
def test_hospital_vs_confirmed_missing_value():
    '''
    Test whether hospital_vs_confirmed can produce the expected output when some values are missing
    This Json file include 5 days data
    2020-3-16 and 2020-3-20 data are complete.
    2020-3-16:
    new admissions in hospitals: 72
    the new confirmed cases: 144
    2020-3-20:
    new admissions in hospitals: 188
    the new confirmed cases: 376
    3-17 Missing new admissions in hospitals data and the new confirmed cases data
    3-18 Missing new admissions in hospitals data
    3-19 missing the new confirmed cases data
    So they will not be returned
    '''
    data_directory = Path("test_data")
    data_file = "Not_Exactly_match_scheme_missing_hospital_confirm_value.json"
    
    expected_result = (['2020-03-16', '2020-03-20'], [0.5, 0.5])
    assert hospital_vs_confirmed(load_covid_data(data_directory / data_file) ) == expected_result



#Test generate_data_plot_confirmed    
def test_generate_data_plot_confirmed_not_correct_sex_argument():
    '''
    Use incorrect sex value as input, other values ​​are correct \
    use 4 as sex argument

    '''
    data_directory = Path("test_data")
    data_file = "Exactly_match_scheme.json"
    with pytest.raises(Exception) as e:
        generate_data_plot_confirmed(load_covid_data(data_directory / data_file),4,None,'total')  
    assert e.match("The entered sex value does not meet the requirements.")

def test_generate_data_plot_confirmed_not_correct_maxage_argument():
    '''
    Use incorrect sex value as input, other values ​​are correct 
    use '1' as maxmax_age argument

    '''
    data_directory = Path("test_data")
    data_file = "Exactly_match_scheme.json"
    with pytest.raises(Exception) as e:
        generate_data_plot_confirmed(load_covid_data(data_directory / data_file),None,'1','total')  
    assert e.match("The entered max_age value does not meet the requirements.")

def test_generate_data_plot_confirmed_not_correct_status_argument():
    '''
    Use incorrect sex value as input, other values ​​are correct 
    use t as status argument

    '''
    data_directory = Path("test_data")
    data_file = "Exactly_match_scheme.json"
    with pytest.raises(Exception) as e:
        generate_data_plot_confirmed(load_covid_data(data_directory / data_file),'male',None,'t')  
    assert e.match("The entered status value does not meet the requirements")

def test_generate_data_plot_confirmed_correct_sex_maxage_argument():
    '''
    Enter the correct sex value and maxage value at the same time
    use 30 as maxmax_age argument
    use 'female' as sex argument

    '''
    data_directory = Path("test_data")
    data_file = "Exactly_match_scheme.json"
    with pytest.raises(Exception) as e:
        generate_data_plot_confirmed(load_covid_data(data_directory / data_file),'female',30,'total')  
    assert e.match("At most one of sex or max_age allowed at a time.")



#Test compute_running_average
def test_compute_running_average_input_odd():
    '''
    test
    Window variables ONLY accept odd numbers
    input_list = [0,3,None,None,None,6,9]
    window = 3 (odd)
    result = [None,1.5,3,None,6,7.5,None]
    '''
    input_list = [0,3,None,None,None,6,9]
    expected_result = [None,1.5,3,None,6,7.5,None]
    assert compute_running_average(input_list,3) == expected_result

def test_compute_running_average_input_even():
    '''
    negative test
    If windows is even (such as 4)
    throw an error: Window must be odd.
    '''
    input_list = [0,3,None,None,None,6,9]
    with pytest.raises(Exception) as e:
        compute_running_average(input_list,4) 
    assert e.match("Window must be odd.")
    


# other test
def test_load_covid_data_generic_case():
    data_directory = Path("test_data")
    data_file = "Exactly_match_scheme.json"
    expected_result = {
                    "metadata": {
                      "time-range": {
                        "start_date": "2020-03-16",
                        "stop_date": "2020-03-17"
                      },
                      "age_binning": {
                        "hospitalizations": [
                         "0-24",
                          "25-49",
                          "50-74",
                          "75-"
                        ],
                        "population": [
                          "0-24",
                          "25-49",
                          "50-74",
                          "75-"
                        ]
                      }
                    },
                    "region": {
                      "name": "Eriador-Minhiriath-Eryn Vorn",
                      "key": "ER-Mi-EV",
                      "latitude": 128.23,
                      "longitude": 0.012,
                      "elevation": -23.47,
                      "area": {
                        "total": 743.34,
                        "rural": 123.89,
                        "urban": 619.45
                      },
                      "population": {
                        "total": 5785312,
                        "male": 2587247,
                        "female": 3198065,
                        "age": [
                          255457,
                          2558068,
                          2673568,
                          298219
                        ],
                        "rural": 1928437,
                        "urban": 3856875
                      },
                      "open_street_maps": 302537,
                      "noaa_station": 1019110349999,
                      "noaa_distance": 12.04
                    },
                    "evolution": {
                      "2020-03-16": {
                        "hospitalizations": {
                          "hospitalized": {
                            "new": {
                              "all": 72,
                              "male": 28,
                              "female": 44,
                              "age": [
                                15,
                                23,
                                21,
                                13
                              ]
                            },
                            "total": {
                              "all": 578603,
                              "male": 289036,
                              "female": 289567,
                              "age": [
                                96544,
                                192772,
                                192930,
                                96357
                              ]
                            },
                            "current": {
                              "all": 17254,
                              "male": 8694,
                              "female": 8560,
                              "age": [
                                2938,
                                5768,
                                5589,
                                2959
                              ]
                            }
                          },
                          "intensive_care": {
                            "new": {
                              "all": 195,
                              "male": 112,
                              "female": 83,
                              "age": [
                                41,
                                50,
                                72,
                                32
                              ]
                            },
                            "total": {
                              "all": 46477,
                              "male": 23324,
                              "female": 23153,
                              "age": [
                                7753,
                                15568,
                                15446,
                                7710
                              ]
                            },
                            "current": {
                              "all": 546,
                              "male": 251,
                              "female": 295,
                              "age": [
                                100,
                                163,
                                186,
                                97
                              ]
                            }
                          },
                          "ventilator": {
                            "new": {
                              "all": 226,
                              "male": 115,
                              "female": 111,
                              "age": [
                                37,
                                81,
                                74,
                                34
                              ]
                            },
                            "total": {
                              "all": 11796,
                              "male": 5891,
                              "female": 5905,
                              "age": [
                                2022,
                                3820,
                                3910,
                                2044
                              ]
                            },
                            "current": {
                              "all": 261,
                              "male": 135,
                              "female": 126,
                              "age": [
                                40,
                                93,
                                85,
                                43
                              ]
                            }
                          }
                        },
                        "epidemiology": {
                          "confirmed": {
                            "new": {
                              "all": 144,
                              "male": 66,
                              "female": 78,
                              "age": [
                                29,
                                49,
                                43,
                                23
                              ]
                            },
                            "total": {
                              "all": 1712595,
                              "male": 855285,
                              "female": 857310,
                              "age": [
                                284931,
                                571866,
                                570702,
                                285096
                              ]
                            }
                          },
                          "deceased": {
                            "new": {
                              "all": 107,
                              "male": 55,
                              "female": 52,
                              "age": [
                                14,
                                41,
                                29,
                                23
                              ]
                            },
                            "total": {
                              "all": 256974,
                              "male": 128729,
                              "female": 128245,
                              "age": [
                                43009,
                                84945,
                                86380,
                                42640
                              ]
                            }
                          },
                          "recovered": {
                            "new": {
                              "all": 360,
                              "male": 178,
                              "female": 182,
                              "age": [
                                59,
                                128,
                                108,
                                65
                              ]
                            },
                            "total": {
                              "all": 1199075,
                              "male": 600308,
                              "female": 598767,
                              "age": [
                                199525,
                                399283,
                                400334,
                                199933
                              ]
                            }
                          },
                          "tested": {
                            "new": {
                              "all": 1008,
                              "male": 489,
                              "female": 519,
                              "age": [
                                180,
                                344,
                                319,
                                165
                              ]
                            },
                            "total": {
                              "all": 6131582,
                              "male": 3068893,
                              "female": 3062689,
                              "age": [
                                1021656,
                                2044302,
                                2042830,
                                1022794
                              ]
                            }
                          }
                        },
                        "weather": {
                          "temperature": {
                            "average": 1.638889,
                            "min": -2.604167,
                            "max": 9.104167
                          },
                          "rainfall": 0.145143,
                          "snowfall": 40.64,
                          "dew_point": -0.706349,
                          "relative_humidity": 84.131573
                        },
                        "government_response": {
                          "school_closing": 0,
                          "workplace_closing": 1,
                          "cancel_public_events": 0,
                          "restrictions_on_gatherings": 0,
                          "public_transport_closing": 0,
                          "stay_at_home_requirements": 1,
                          "restrictions_on_internal_movement": 0,
                          "international_travel_controls": 0,
                          "income_support": 0,
                          "debt_relief": 0,
                          "fiscal_measures": 0,
                          "international_support": 0,
                          "public_information_campaigns": 2,
                          "testing_policy": 1,
                          "contact_tracing": 0,
                          "emergency_investment_in_healthcare": 0,
                          "investment_in_vaccines": 0,
                          "stringency_index": 16.67
                        }
                      },
                      "2020-03-17": {
                        "hospitalizations": {
                          "hospitalized": {
                            "new": {
                              "all": 158,
                              "male": 84,
                              "female": 74,
                              "age": [
                                31,
                                65,
                                37,
                                25
                              ]
                            },
                            "total": {
                              "all": 578761,
                              "male": 289120,
                              "female": 289641,
                              "age": [
                                96575,
                                192837,
                                192967,
                                96382
                              ]
                            },
                            "current": {
                              "all": 16982,
                              "male": 8562,
                              "female": 8420,
                              "age": [
                                2893,
                                5703,
                                5490,
                                2896
                              ]
                            }
                          },
                          "intensive_care": {
                            "new": {
                              "all": 1061,
                              "male": 429,
                              "female": 632,
                              "age": [
                                178,
                                375,
                                330,
                                178
                              ]
                            },
                            "total": {
                              "all": 47538,
                              "male": 23753,
                              "female": 23785,
                              "age": [
                                7931,
                                15943,
                                15776,
                                7888
                              ]
                            },
                            "current": {
                              "all": 1431,
                              "male": 600,
                              "female": 831,
                              "age": [
                                250,
                                484,
                                456,
                                241
                              ]
                            }
                          },
                          "ventilator": {
                            "new": {
                              "all": 246,
                              "male": 128,
                              "female": 118,
                              "age": [
                                53,
                                74,
                                81,
                                38
                              ]
                            },
                            "total": {
                              "all": 12042,
                              "male": 6019,
                              "female": 6023,
                              "age": [
                                2075,
                                3894,
                                3991,
                                2082
                              ]
                            },
                            "current": {
                              "all": 293,
                              "male": 172,
                              "female": 121,
                              "age": [
                                61,
                                94,
                                94,
                                44
                              ]
                            }
                          }
                        },
                        "epidemiology": {
                          "confirmed": {
                            "new": {
                              "all": 790,
                              "male": 424,
                              "female": 366,
                              "age": [
                                130,
                                278,
                                258,
                                124
                              ]
                            },
                            "total": {
                              "all": 1713385,
                              "male": 855709,
                              "female": 857676,
                              "age": [
                                285061,
                                572144,
                                570960,
                                285220
                              ]
                            }
                          },
                          "deceased": {
                            "new": {
                              "all": 159,
                              "male": 74,
                              "female": 85,
                              "age": [
                                22,
                                50,
                                57,
                                30
                              ]
                            },
                            "total": {
                              "all": 257133,
                              "male": 128803,
                              "female": 128330,
                              "age": [
                                43031,
                                84995,
                                86437,
                                42670
                              ]
                            }
                          },
                          "recovered": {
                            "new": {
                              "all": 5018,
                              "male": 2522,
                              "female": 2496,
                              "age": [
                                844,
                                1689,
                                1627,
                                858
                              ]
                            },
                            "total": {
                              "all": 1204093,
                              "male": 602830,
                              "female": 601263,
                              "age": [
                                200369,
                                400972,
                                401961,
                                200791
                              ]
                            }
                          },
                          "tested": {
                            "new": {
                              "all": 3950,
                              "male": 1983,
                              "female": 1967,
                              "age": [
                                640,
                                1328,
                                1321,
                                661
                              ]
                            },
                            "total": {
                              "all": 6135532,
                              "male": 3070876,
                              "female": 3064656,
                              "age": [
                                1022296,
                                2045630,
                                2044151,
                                1023455
                              ]
                            }
                          }
                        },
                        "weather": {
                          "temperature": {
                            "average": 1.920635,
                            "min": -1.984127,
                            "max": 10.849206
                          },
                          "rainfall": 0.08466699999999999,
                          "snowfall": 0,
                          "dew_point": 0.018519,
                          "relative_humidity": 87.152206
                        },
                        "government_response": {
                          "school_closing": 0,
                          "workplace_closing": 1,
                          "cancel_public_events": 1,
                          "restrictions_on_gatherings": 0,
                          "public_transport_closing": 0,
                          "stay_at_home_requirements": 1,
                          "restrictions_on_internal_movement": 0,
                          "international_travel_controls": 0,
                          "income_support": 0,
                          "debt_relief": 1,
                          "fiscal_measures": 0,
                          "international_support": 0,
                          "public_information_campaigns": 2,
                          "testing_policy": 1,
                          "contact_tracing": 0,
                          "emergency_investment_in_healthcare": 0,
                          "investment_in_vaccines": 0,
                          "stringency_index": 22.22
                        }
                      }
                    }
                }
    assert load_covid_data(data_directory / data_file) == expected_result
