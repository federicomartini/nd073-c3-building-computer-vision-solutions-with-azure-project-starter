import sys
sys.path.insert(1, '../step_2')
sys.path.insert(1, '../step_3')
sys.path.insert(1, '../step_4')

import pandas as pd
from tabulate import tabulate
from datetime import datetime
from io import BytesIO
import os
from ID_Document import extract_id_data
from Boarding_Pass import BoardingPass
from face_detection import are_faces_identical
from get_thumbnail import get_custom_face_picture
from lighter_mdl import find_lighter
import argparse

FEDERICOM_ID = 4

def passenger_validation(boarding_pass, id_img_path, luggage_img):

    first_name, last_name, date_of_birth, sex = extract_id_data(id_img_full_path)
    manifest_df_copy = manifest_df.copy()
    manifest_df_copy["Full Name"] = manifest_df_copy["First Name"] + manifest_df_copy["Last Name"]
    passenger_manifest_index = get_passenger_manifest_index(manifest_df, first_name, last_name)
    time_str = manifest_df_copy.loc[passenger_manifest_index, 'Time'].values[0]

    print_line_separator(60)

    if len(passenger_manifest_index):

        if(is_passenger_name_in_ticket(first_name, last_name, boarding_pass_details)):
            manifest_df.loc[passenger_manifest_index, 'NameValidation'] = True
        else:
            print("Dear Sir/Madam,\n"
                "Some of the information on your Boarding Pass does not match the flight manifest data, "
                "so you cannot board the plane. Please see a customer service representative.\n")
            return
        
        if check_date_of_birth(manifest_df_copy, passenger_manifest_index, date_of_birth):
            manifest_df.loc[passenger_manifest_index, 'DoBValidation'] = True
        else:
            print("Dear Sir/Madam,\n"
                "Some of the information on your ID card does not match the flight manifest data, "
                "so you cannot board the plane. Please see a customer service representative.\n")
            return

        if bp_validation(manifest_df_copy, passenger_manifest_index):
            manifest_df.loc[passenger_manifest_index, 'BoardingPassValidation'] = True
        else:
            print("Dear Sir/Madam,\n"
                "Some of the information in your boarding pass does not match the flight manifest data, so you cannot board the plane."
                "Please see a customer service representative.\n")
            return

        print("Dear passenger {} {},\n"
              "You are welcome to flight no {} leaving at {} from {} to {}\n"
              "Your seat number is {}, and it is confirmed.".format(first_name, last_name, flight_number, time_str,
                                                                     from_location, to_destination, seat))

        face_validation = validate_id(id_img_path, first_name, last_name)
        baggage_validation = not(luggage_validation(luggage_img))

        if face_validation and baggage_validation:
            manifest_df.loc[passenger_manifest_index, 'PersonValidation'] = True
            manifest_df.loc[passenger_manifest_index, 'LuggageValidation'] = True
            print("We did not find a prohibited item (lighter) in your carry-on baggage, "
                "thanks for following the procedure.\n"
                "Your identity is verified so please board the plane.\n ")

        elif not face_validation and baggage_validation:
            manifest_df.loc[passenger_manifest_index, 'LuggageValidation'] = True
            print("We did not find a prohibited item (lighter) in your carry-on baggage, "
                "thanks for following the procedure.\n"
                "Your identity could not be verified. Please see a customer service representative.\n ")

        elif face_validation and not baggage_validation:
            manifest_df.loc[passenger_manifest_index, 'PersonValidation'] = True
            print("We have found a prohibited item in your carry-on baggage, "
                "and it is flagged for removal. \n"
                "Your identity is verified. However, your baggage verification failed, so please see a customer service representative.")
        else:
            print("We have found a prohibited item in your carry-on baggage, "
                "and it is flagged for removal. \n"
                "Your identity could not be verified. Please see a customer service representative.\n")
 
    else:
        print("Dear Sir/Madam,\n"
              "Some of the information on your ID card does not match the flight manifest data, "
              "so you cannot board the plane. Please see a customer service representative.\n")

def print_line_separator(line_length):
    print('\n' + '='*line_length + '\n')

def half_field(field):
    field = field[:int(len(field) / 2)]
    return field

def get_passenger_manifest_index(manifest, first_name, last_name):
    manifest_df_copy = manifest.copy()
    manifest_df_copy["Full Name"] = manifest_df_copy["First Name"] + manifest_df_copy["Last Name"]
    full_name = first_name + last_name

    return manifest_df_copy.index[(manifest_df_copy['Full Name'] == full_name)]

def is_passenger_name_in_ticket(first_name, last_name, boarding_pass_data):
    full_ticket_name = half_field(boarding_pass_details["FirstName"].replace(" ", "")) + half_field(boarding_pass_details["LastName"].replace(" ",""))
    full_name = first_name + last_name
    
    return full_name == full_ticket_name

def check_date_of_birth(manifest_df, index, date_of_birth): 
    id_date_of_birth = datetime.strptime(str(date_of_birth), '%Y-%m-%d').date()
    manifest_date_of_birth = datetime.strptime(str(manifest_df.loc[index, 'DateofBirth'].values[0]), '%d %B %Y').date()

    return id_date_of_birth == manifest_date_of_birth

def bp_validation(manifest_df, passenger_index):
    return (manifest_df.loc[passenger_index, 'Flight No'].values[0] == flight_number and
            manifest_df.loc[passenger_index, 'SeatNo'].values[0] and
            manifest_df.loc[passenger_index, 'Origin'].values[0] and
            manifest_df.loc[passenger_index, 'Destination'].values[0] and
            manifest_df.loc[passenger_index, 'Date'].values[0])

def validate_id(id_img_path, name, surname):    
    image_from_id = BytesIO(open(id_img_path, 'rb').read())
    image_from_video = BytesIO(get_custom_face_picture(name, surname))

    return are_faces_identical(image_from_id, image_from_video)

def luggage_validation(luggage_img):
    return find_lighter(luggage_img)

if __name__ == '__main__':

    manifest_df = pd.read_csv("../material_preparation_step/flight_manifest_table.csv", sep=",")
    root_dir = "."
    luggage_dir = "lighter_test_images"
    id_dir = "../material_preparation_step/Digital_ID"
    boarding_pass_dir = "../material_preparation_step/Boarding_Pass"

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--id', default=FEDERICOM_ID, type=int)
    args = args_parser.parse_args()

    id_img_full_path = id_dir + '/ca-dl-{}.png'.format(args.id)
    boarding_pass_full_path = boarding_pass_dir + '/boarding_pass_{}.pdf'.format(args.id)
    luggage_img_full_path = luggage_dir + '/lighter_test_set_{}of5.jpg'.format(args.id)
    
    boarding_pass_details = BoardingPass().get_flight_details_from_custom_Form(boarding_pass_full_path)
    flight_number = boarding_pass_details.get('FlightNumber')
    seat = half_field(boarding_pass_details.get('Seat'))
    from_location = half_field(boarding_pass_details.get('From'))
    to_destination = half_field(boarding_pass_details.get('To'))

    passenger_validation(boarding_pass_details, id_img_full_path, luggage_img_full_path)

    manifest_df.to_csv('manifest_final.csv', index=False)