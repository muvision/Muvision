from . import classification
from . import special_characters as sc
import numpy as np
import os
import tensorflow as tf


def identify_lines(line_info):
    document = "\\begin{align*} "
    for i in range(len(line_info)):
        avg_x = (np.average(line_info[i]['x'].diff()) + np.average(line_info[i]['x1'].diff()))/2
        line_string = classify_characters(line_info[i], avg_x)
        document = document + line_string

        if i != len(line_info) - 1:
            document = document + " \\\\ "
    document = document + " \\end{align*}"
    return document


def classify_characters(df, avg_x):
    line_string = ""
    is_equal = False
    skip_count = 0
    is_script = "reg"
    custom_model_path = os.path.join(os.getcwd(), 'muvision', 'custom_model3.h5')
    custom_model = tf.keras.models.load_model(custom_model_path)

    for i in range(len(df.index)):
        if skip_count > 0:
            skip_count = skip_count - 1
            continue
        image = df['image'].iloc[i]
        res = classification.classify(image, custom_model)

        if res == '-' and sc.determine_equal(i, df, avg_x):
            # Recalculate special character
            new_median = (df['median_y'].iloc[i] + df['median_y'].iloc[i + 1]) / 2
            if new_median < df['median_mean'].iloc[0] + df['std'].iloc[0] and df['y1'].iloc[i] < df['median_mean'].iloc[0]:
                special_char = 'sup'
            elif new_median > df['median_mean'].iloc[0] - df['std'].iloc[0] and df['y'].iloc[i] > df['median_mean'].iloc[0]:
                special_char = 'sub'
            else:
                special_char = 'reg'

            '''
            Special case for equal signs. The other cases are if both are 'reg', both are not 'reg', and if 
            special_char is not 'reg', and is_script is 'reg' in which case we don't want to start the superscript/
            subscript with an equal or division symbol
            '''
            if special_char == 'reg' and is_script != 'reg':
                line_string = line_string + " }"
                is_script = 'reg'

            if is_script == "reg":
                line_string = line_string + " &= "
            else:
                line_string = line_string + " = "
            skip_count = skip_count + 1
        elif res == '-' and sc.determine_div(i, df):
            # Recalculate special character
            new_median = (df['median_y'].iloc[i] + df['median_y'].iloc[i + 1] + df['median_y'].iloc[i + 2])/3

            if new_median < df['median_mean'].iloc[0] + df['std'].iloc[0] and df['y1'].iloc[i] < df['median_mean'].iloc[0]:
                special_char = 'sup'
            elif new_median > df['median_mean'].iloc[0] - df['std'].iloc[0] and df['y'].iloc[i] > df['median_mean'].iloc[0]:
                special_char = 'sub'
            else:
                special_char = 'reg'

            # Special case for division
            if special_char == 'reg' and is_script != 'reg':
                line_string = line_string + " }"
                is_script = 'reg'

            line_string = line_string + "\div "

            skip_count = skip_count + 2
        else:
            line_string, is_script = fix_subscripts(line_string, df, is_script, i, res)
            line_string = line_string + res + " "

    # At the very end of a line
    if is_script != 'reg':
        line_string = line_string + "} "

    return line_string


def fix_subscripts(line_string, df, is_script, i, letter):
    special_char = df['character type'].iloc[i]
    # Changes to scripts (start of a script, can't be equal sign or operator)
    if special_char == 'sup' and is_script == "reg" and letter != "="\
            and letter != '-' and letter != '+' and letter != '\times' and letter != '\div':
        line_string = line_string + '^{'
        is_script = 'sup'
    elif special_char == 'sub' and is_script == "reg" and letter != '.' and letter != "="\
            and letter != '-' and letter != '+' and letter != '\times' and letter != '\div':
        line_string = line_string + '_{'
        is_script = 'sub'
    elif special_char == 'sup' and is_script == "sub" and letter != "="\
            and letter != '-' and letter != '+' and letter != '\times' and letter != '\div':
        line_string =  line_string + '}^{'
        is_script = 'sup'
    elif special_char == 'sub' and is_script == "sup" and letter != "="\
            and letter != '-' and letter != '+' and letter != '\times' and letter != '\div':
        line_string = line_string + '}_{'
        is_script = 'sub'
    elif special_char != is_script:
        # Closing of scripts
        print(special_char)
        print(is_script)
        line_string = line_string + '}'
        is_script = 'reg'
    return line_string, is_script
