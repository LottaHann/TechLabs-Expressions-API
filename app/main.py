import os
from flask import Flask, jsonify,request, render_template
from dotenv import load_dotenv
from flask_cors import CORS
import requests
import json
import copy

# Load variables from .env
load_dotenv()
print(os.environ.get('HELLO'))

# Create Flask instance
app = Flask(__name__)
laptop_ip = "193.167.36.67"
rpi_ip = "193.166.180.103"
detection_port = 8008
main_server_port = 5100
main_frontend_port = 5500
rpi_server_port = 5000
#etection_server_url = os.environ.get('SERVER_URL', 'http://127.0.0.1:8008')
detection_server_url = f'http://{rpi_ip}:{detection_port}'
main_server_url = f'http://{laptop_ip}:{main_server_port}'
main_frontend_url = f'http://{laptop_ip}:{main_frontend_port}'
rpi_server_url = f'http://{rpi_ip}:{rpi_server_port}'



#Allowing acess for our localhost only 
CORS(app, resources={r'/*':{'origins':[main_frontend_url, main_server_url, detection_server_url, rpi_server_url, "http://localhost:5000"]}})

#Allows UTF-8 in JSON
app.config['JSON_AS_ASCII']=False


#Expression data
face_data=[
    {
        'id':0,
        'name':"smile",
        'mouth':"m 97.3423,213.19999 c 8.4419,6.97268 18.84406,16.35992 28.37838,20.03725 3.58744,1.33113 17.55481,6.18499 21.34908,6.12313 4.22117,0.0132 19.81861,-5.38315 21.89891,-6.42613 11.61071,-4.43883 20.13472,-11.22679 29.13472,-19.46698 -11.78149,8.72469 -11.86217,9.78333 -25.06561,16.51813 -4.33334,2.21034 -22.59321,7.84542 -25.97284,8.04015 -2.96885,-0.11472 -17.77123,-4.37283 -24.46975,-7.51833 -9.76665,-4.58625 -13.51862,-9.44092 -25.25289,-17.30722 z",
        'eb_right':"m 169.90029,126.15476 c 11.71726,-15.67218 23.43453,-14.55742 35.15179,0" ,
        'eb_left':"m 85.422617,126.15477 c 11.717261,-15.67218 23.434523,-14.55742 35.151783,0" ,
        'eye_left':"m 121.33035,159.60567 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.49688,17.55811 -16.15268,17.55811 -7.809906,0 -14.376598,-7.71512 -16.270204,-18.17396 -0.358721,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -2e-6,-13.46441 7.530545,-24.37947 16.819944,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z",
        'eye_right':"m 203.91816,159.79463 c 0,2.22245 -0.20517,4.37545 -0.58956,6.42136 -1.94436,10.34897 -8.4743,17.95811 -16.23038,17.95811 -7.49813,0 -13.85032,-7.11143 -16.02129,-16.93483 -0.51864,-2.34676 -0.79865,-4.8483 -0.79865,-7.44464 0,-13.4644 7.53054,-24.37946 16.81994,-24.37946 9.2894,0 16.81994,10.91506 16.81994,24.37946 z",
    },
    {
        'id':1,
        'name':"neutral",
        'mouth': "m 94.938837,213.06828 c 11.182233,-0.21635 12.957763,-0.39527 23.742453,0.0919 8.66395,0.60599 17.0513,0.82029 23.91524,1.67053 9.13486,0.55376 14.88731,0.98009 24.71612,1.64509 13.90796,2.01439 20.38005,0.11545 31.9476,1.50621 -11.51422,0.47088 -8.93666,0.91308 -15.63422,1.00931 -5.29019,0.076 -37.6628,-2.40964 -41.04243,-2.60437 -2.96885,0.11472 -23.4912,-1.90285 -31.41506,-2.52167 -8.19966,-0.64036 -7.07039,-0.18198 -16.229703,-0.79696 z",
        'eb_left':"m 85.422617,126.15477 c 11.717261,-15.67218 23.434523,-14.55742 35.151783,0" ,
        'eb_right':"m 169.9003,126.15476 c 12.84896,1.53048 25.28882,2.45467 35.15178,0" ,#"M169.9 126.155h35.152",
        'eye_left':"m 121.33035,159.60567 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.49688,17.55811 -16.15268,17.55811 -7.809906,0 -14.376598,-7.71512 -16.270204,-18.17396 -0.358721,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -2e-6,-13.46441 7.530545,-24.37947 16.819944,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z",
        'eye_right':"m 203.91816,159.79463 c 0,2.22245 -0.20517,4.37545 -0.58956,6.42136 -1.94436,10.34897 -8.4743,17.95811 -16.23038,17.95811 -7.49813,0 -13.85032,-7.11143 -16.02129,-16.93483 -0.51864,-2.34676 -0.79865,-4.8483 -0.79865,-7.44464 0,-13.4644 7.53054,-24.37946 16.81994,-24.37946 9.2894,0 16.81994,10.91506 16.81994,24.37946 z"
    },
    {
        'id':2,
        'name':"sad",
        'mouth':"m 96.029224,210.17896 c 8.441896,-6.97268 18.309516,-13.95449 27.843836,-17.63182 3.58744,-1.33113 17.55481,-6.18499 21.34908,-6.12313 4.22117,-0.0132 19.81861,5.38315 21.89891,6.42613 11.61071,4.43883 20.13472,11.22679 29.13472,19.46698 -11.78149,-8.72469 -11.86217,-9.78333 -25.06561,-16.51813 -4.33334,-2.21034 -22.59321,-7.84542 -25.97284,-8.04015 -2.96885,0.11472 -17.77123,4.37283 -24.46975,7.51833 -9.76665,4.58625 -12.98408,7.03549 -24.718346,14.90179 z" ,
        'eb_left':"m 85.422617,126.15477 c 8.830391,3.29868 19.312573,12.52967 35.151783,0",
        'eb_right':"m 169.9003,126.15476 c 10.61618,6.97353 21.55612,11.89655 35.15178,0",
        'eye_left':"m 121.33035,159.60567 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.49688,17.55811 -16.15268,17.55811 -7.809906,0 -14.376598,-7.71512 -16.270204,-18.17396 -0.358721,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -2e-6,-13.46441 7.530545,8.76195 16.819944,8.76195 9.2894,0 16.81994,-22.22636 16.81994,-8.76195 z" ,
        'eye_right':"m 203.91816,159.79463 c 0,2.22245 -0.20517,4.37545 -0.58956,6.42136 -1.94436,10.34897 -8.4743,17.95811 -16.23038,17.95811 -7.49813,0 -13.85032,-7.11143 -16.02129,-16.93483 -0.51864,-2.34676 -0.79865,-4.8483 -0.79865,-7.44464 0,-13.4644 7.24706,9.20757 16.53646,9.20757 9.2894,0 17.10342,-22.67197 17.10342,-9.20757 z",
    }
    ,
    { 
        'id':3,
        'name': "blushing",
        'mouth':"m 138.88292,214.70953 c 0.29018,0.8923 0.73034,2.66914 2.94324,4.51457 1.13812,0.7337 1.71617,1.26725 4.70458,2.55054 3.18718,-1.09241 4.35076,-1.59128 5.16825,-2.26725 2.32008,-1.791 2.63783,-3.77683 3.01839,-4.6003 0.76394,-2.17464 -1.25519,-5.94491 -4.37523,-5.95313 -1.83622,-0.005 -3.43527,2.74021 -3.51653,3.87374 -0.18418,-0.82611 -1.92366,-3.93027 -4.46815,-3.89235 -2.47016,0.0368 -3.95468,3.65146 -3.47455,5.77418 z",
        'eb_right':"m 169.90029,126.15476 c 11.71726,-15.67218 23.43453,-14.55742 35.15179,0" ,
        'eb_left':"m 85.422617,126.15477 c 11.717261,-15.67218 23.434523,-14.55742 35.151783,0" ,
        'eye_left':"m 121.33035,159.60567 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.49688,-14.19189 -16.15268,-14.19189 -7.80991,0 -14.3766,24.03488 -16.2702,13.57604 -0.35872,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -1e-5,-13.46441 7.53054,-24.37947 16.81994,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z",
        'eye_right':"m 203.91816,159.79463 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.68587,-13.90841 -16.34167,-13.90841 -7.80991,0 -14.18761,23.7514 -16.08121,13.29256 -0.35872,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -1e-5,-13.46441 7.53054,-24.37947 16.81994,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z"
    },
    {
        'id':4,
        'name':"wink",
        'mouth':"m 91.711557,197.0722 c 11.182233,-0.21635 9.309533,11.81226 20.234543,13.93646 8.66395,1.26745 9.78694,1.55259 17.18005,2.13825 9.13486,0.55376 5.1587,0.23174 14.98751,0.89674 14.16117,0.38312 17.59856,0.39821 18.57075,2.06747 -10.73573,0.026 -11.74419,-0.61486 -18.4566,-0.51006 -5.29009,0.0826 -15.38319,-0.94366 -18.76282,-1.13839 -3.06239,-0.16591 -8.9179,-0.74165 -16.72471,-2.23301 -8.19966,-1.5664 -7.86941,-14.54248 -17.028723,-15.15746 z",
        'eb_right':"m 169.90029,126.15476 c 11.71726,-15.67218 23.43453,-14.55742 35.15179,0" ,
        'eb_left':"m 85.422617,126.15477 c 11.717261,-15.67218 23.434523,-14.55742 35.151783,0" ,
        'eye_left':"m 121.29728,159.58913 c -0.0143,2.36869 -1.37809,4.07896 -5.52898,5.64727 -13.07005,4.93819 -17.409562,4.61818 -22.139519,6.1363 -4.728294,1.51759 -5.224377,-1.34308 -3.625335,-2.85344 0.519994,-0.49116 28.012874,-6.48054 26.725034,-8.45057 -7.44858,-11.39419 -25.928037,-10.16916 -27.933518,-11.37211 -8.879725,-5.32634 32.583468,-2.56653 32.502318,10.89255 z"  ,
        'eye_right':"m 203.91816,159.79463 c 0,2.22245 -0.20517,4.37545 -0.58956,6.42136 -1.94436,10.34897 -8.4743,17.95811 -16.23038,17.95811 -7.49813,0 -13.85032,-7.11143 -16.02129,-16.93483 -0.51864,-2.34676 -0.79865,-4.8483 -0.79865,-7.44464 0,-13.4644 7.53054,-24.37946 16.81994,-24.37946 9.2894,0 16.81994,10.91506 16.81994,24.37946 z",
    },
    {
        'id':5,
        'name':"angry",
        'mouth':"m 111.26358,221.58814 c 6.03316,-8.98786 13.08523,-17.98748 19.8991,-22.7276 2.56383,-1.71584 12.54586,-7.97251 15.25751,-7.89278 3.01673,-0.017 14.16372,6.93894 15.65045,8.28334 8.2978,5.7217 14.38964,14.47145 20.82165,25.09315 -8.41985,-11.24623 -8.47751,-12.61081 -17.91359,-21.29205 -3.0969,-2.84914 -16.14664,-10.11282 -18.56196,-10.36383 -2.12174,0.14788 -12.70053,5.63662 -17.48775,9.6912 -6.97991,5.91174 -9.2793,9.06882 -17.66541,19.20857 z" ,
        'eb_right':"m 166.96034,130.96561 c 10.50128,6.54269 22.0775,-1.98396 38.09174,-4.81085" ,
        'eb_left':"m 87.57119,127.94781 c 6.142657,-0.15429 27.89735,10.94465 37.28994,2.67269",
        'eye_left':"m 121.33035,159.60567 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.49688,17.55811 -16.15268,17.55811 -7.809906,0 -14.376598,-7.71512 -16.270204,-18.17396 -0.358721,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -2e-6,-13.46441 7.530545,-24.37947 16.819944,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z",
        'eye_right':"m 203.91816,159.79463 c 0,2.22245 -0.20517,4.37545 -0.58956,6.42136 -1.94436,10.34897 -8.4743,17.95811 -16.23038,17.95811 -7.49813,0 -13.85032,-7.11143 -16.02129,-16.93483 -0.51864,-2.34676 -0.79865,-4.8483 -0.79865,-7.44464 0,-13.4644 7.53054,-24.37946 16.81994,-24.37946 9.2894,0 16.81994,10.91506 16.81994,24.37946 z",
    },
    
    {
        'id':6,
        'name':"kissyface",
        'mouth':"m 158.81775,203.16294 c 1.08386,2.41124 -26.34992,-23.77613 -32.36834,-16.71145 -6.34406,5.58316 11.49629,19.35001 11.48673,18.42923 4.21086,-2.00757 -17.57163,-0.2754 -15.12308,9.93032 1.08615,5.105 27.89775,-0.57272 36.46706,-6.42629 -13.38713,-0.0399 -22.52042,8.70209 -33.18849,5.60002 -6.47758,-1.88356 11.20976,-8.07198 13.79179,-9.67083 -1.26571,-2.3837 -14.64765,-7.23555 -11.69141,-15.79888 2.22404,-6.4424 26.90493,15.87286 30.62574,14.64788 z",
        'eb_right':"m 169.90029,126.15476 c 11.71726,-15.67218 23.43453,-14.55742 35.15179,0" ,
        'eb_left':"m 85.422617,126.15477 c 11.717261,-15.67218 23.434523,-14.55742 35.151783,0" ,
        'eye_left':"m 121.33035,159.60567 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.49688,-14.19189 -16.15268,-14.19189 -7.80991,0 -14.3766,24.03488 -16.2702,13.57604 -0.35872,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -1e-5,-13.46441 7.53054,-24.37947 16.81994,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z",
        'eye_right':"m 203.91816,159.79463 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.68587,-13.90841 -16.34167,-13.90841 -7.80991,0 -14.18761,23.7514 -16.08121,13.29256 -0.35872,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -1e-5,-13.46441 7.53054,-24.37947 16.81994,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z"
    },

    
    {
       'id':7,
       'name':"bigsmile",
       'mouth':"m 97.3423,213.19999 c 8.4419,6.97268 18.84406,16.35992 28.37838,20.03725 3.58744,1.33113 17.55481,6.18499 21.34908,6.12313 4.22117,0.0132 19.81861,-5.38315 21.89891,-6.42613 11.61071,-4.43883 20.04023,-11.51027 29.04023,-19.75046 0.89423,-1.4741 -7.72232,3.95215 -22.45498,-0.14709 -6.25038,-1.73911 -24.96079,-1.16739 -28.77246,-1.09563 -3.1708,-0.12766 -20.5042,-0.4686 -27.5892,1.26042 -15.62835,3.81393 -23.011444,-1.4896 -21.84996,-0.001 z",
       'eb_right':"m 169.90029,126.15476 c 11.71726,-15.67218 23.43453,-14.55742 35.15179,0" ,
      'eb_left':"m 85.422617,126.15477 c 11.717261,-15.67218 23.434523,-14.55742 35.151783,0" ,
      'eye_left':"m 121.33035,159.60567 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.49688,-14.19189 -16.15268,-14.19189 -7.80991,0 -14.3766,24.03488 -16.2702,13.57604 -0.35872,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -1e-5,-13.46441 7.53054,-24.37947 16.81994,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z",
      'eye_right':"m 203.91816,159.79463 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.68587,-13.90841 -16.34167,-13.90841 -7.80991,0 -14.18761,23.7514 -16.08121,13.29256 -0.35872,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -1e-5,-13.46441 7.53054,-24.37947 16.81994,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z" ,  

    },
    {
        'id':8,
        'name':"suprise",
        'mouth':"m 124.81841,213.7151 c -0.50314,-5.3786 0.21034,-12.48141 8.18722,-13.53477 5.32582,-0.0674 11.82992,-0.12094 15.79523,-0.0715 5.62721,0.11303 9.15529,-0.79773 15.06544,0.6827 7.576,2.13184 6.34395,9.55799 6.45734,12.34556 -0.0432,7.14087 -3.23758,11.9041 -8.26441,14.48764 -1.95389,1.0042 -10.88043,3.83217 -14.1023,3.83188 -3.23875,10e-4 -10.34102,-2.34916 -12.4575,-3.27668 -5.6516,-2.47676 -10.79,-6.88865 -10.68102,-14.46479 z" ,
        'eb_right':"m 176.57418,118.7518 c 17.50399,-17.36647 35.60305,-5.76424 33.43143,6.14698" ,
        'eb_left':"m 82.020831,125.02084 c 2.267857,-16.80611 23.812499,-20.98301 35.529759,-6.42559" ,
        'eye_left':"m 121.33035,159.60567 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.49688,17.55811 -16.15268,17.55811 -7.809906,0 -14.376598,-7.71512 -16.270204,-18.17396 -0.358721,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -2e-6,-13.46441 7.530545,-24.37947 16.819944,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z",
        'eye_right':"m 203.91816,159.79463 c 0,2.22245 -0.20517,4.37545 -0.58956,6.42136 -1.94436,10.34897 -8.4743,17.95811 -16.23038,17.95811 -7.49813,0 -13.85032,-7.11143 -16.02129,-16.93483 -0.51864,-2.34676 -0.79865,-4.8483 -0.79865,-7.44464 0,-13.4644 7.53054,-24.37946 16.81994,-24.37946 9.2894,0 16.81994,10.91506 16.81994,24.37946 z",
    }
    
]

def get_eye_coordinates():
    try:
        response = requests.get(detection_server_url+"/see")
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
    except requests.exceptions.RequestException as e:
        # This will catch any request-related errors
        print(f"An error occurred: {e}")
        data = []  # Set data to an empty list or handle the error as needed
    
    
    if isinstance(data, list) and len(data) > 0:
        first_item = data[0]
        if isinstance(first_item, dict) and 'spatialCoordinates' in first_item:
            coordinates = first_item['spatialCoordinates']
            x = coordinates['x']
            y = coordinates['y']
            # Process the coordinates as needed
            return {'x_cord': x, 'y_cord': y}
    
    return {'x_cord': 0, 'y_cord': 0}

def modify_eye_path(face):
    new_face = copy.deepcopy(face)

    base_coordinates = {
        'eye_left': {'x': 121.33035, 'y': 159.60567},
        'eye_right': {'x': 203.91816, 'y': 159.79463},
        'eb_left': {'x': 85.422617, 'y': 126.15477},
        'eb_right': {'x': 169.90029, 'y': 126.15476},
        'mouth': {'x': 97.3423, 'y': 213.19999}  
    }



    face_eye_left_string = face['eye_left']
    face_eye_right_string = face['eye_right']
    eye_left_x = 121.33035
    eye_left_y = 159.60567
    eye_right_x = 203.91816
    eye_right_y = 159.79463

    new_coordinates = get_eye_coordinates()
    # Define multipliers for eyes and other elements
    eye_multiplier_x = -0.15
    eye_multiplier_y = -0.12
    face_multiplier_x = -0.1
    face_multiplier_y = -0.1
    
    # Calculate offsets
    eye_x_offset = float(new_coordinates['x_cord']) * eye_multiplier_x
    eye_y_offset = float(new_coordinates['y_cord']) * eye_multiplier_y
    face_x_offset = float(new_coordinates['x_cord']) * face_multiplier_x
    face_y_offset = float(new_coordinates['y_cord']) * face_multiplier_y
    
    # Modify each element
    for element, base in base_coordinates.items():
        element_string = face[element]
        if element.startswith('eye'):
            # Apply larger offsets to eyes
            modified_string = element_string.replace(
                str(base['x']), str(base['x'] + eye_x_offset)
            ).replace(
                str(base['y']), str(base['y'] + eye_y_offset)
            )
        else:
            # Apply smaller offsets to other elements
            modified_string = element_string.replace(
                str(base['x']), str(base['x'] + face_x_offset)
            ).replace(
                str(base['y']), str(base['y'] + face_y_offset)
            )
        new_face[element] = modified_string

    return new_face

# Default route to /
@app.route("/")
def index():
    return render_template('index.html')

# Store the current facial expression
current_expression = {'name': 'neutral'}

# Endpoint to receive facial expression updates from the external server
@app.route('/update_expression', methods=['GET'])
def update_expression():
    global current_expression
    #print("request args:", request.args)
    if 'name' in request.args:
        name = request.args['name']
        print("----------------------name:", name)
        print("\n\n\n")
        for face in face_data:
            if face['name'] == name:
                current_expression = face
                return jsonify({'status': 'success', 'message': f'Expression updated to {name}'})
    return jsonify({'status': 'error', 'message': 'Invalid expression name'})

# Endpoint to get the current facial expression
@app.route('/current_expression', methods=['GET'])
def get_current_expression():
    try:
        if current_expression['name'] != 'neutral':
            new_face = modify_eye_path(current_expression)
            results = new_face
        else:
            results = current_expression

        
        return jsonify(results), 200# Explicitly set status 200

    except Exception as e:
        print("Error in get_current_expression:", str(e))
        return jsonify({"error": str(e)}), 500

#Getting all the API data in face/all
@app.route('/face/all', methods=['GET'])
def faces():
    return jsonify(face_data)


#Example of URL
# http://YOUR-LOCALHOST/face?name=smile
@app.route('/face',methods=['GET']) 
def get_name():
    if 'name' in request.args:
        name=str(request.args['name'])
    else:
        return "ERROR: Name needed"
    
    
    results = {}
    for face in face_data:
        if face['name'] == name:
            if face['name'] != 'neutral':
                new_face = modify_eye_path(face)
                results = new_face
            else:
                results = face

    # convert list of Python dictionaries to the JSON format
    return jsonify(results)


if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000)