acronym_list = ('TSB', 'TCB', 'SYS', 'LAG', 'IOU', 'GRN', 'THS', 'YAZ', 'TCT', 'CNC', 'MSG', 'TMI', 'TCP', 'IIL', 'FHG', 'SYM', 'LSC', 'PRN', 'EWM', 'TCM', 'ELT', 'HRG', 'TGP', 'MUN','WSU', 'IST', 'BAG', 'EVL', 'MCS', 'WLT', 'TCC', 'ASS')



prices_header = "Date, Time, TSB, TCB, SYS, LAG, IOU, GRN, THS, YAZ, TCT, CNC, MSG, TMI, TCP, IIL, FHG, SYM, LSC, PRN, EWM, TCM, ELT, HRG, TGP, 'MUN', WSU, IST, BAG, EVL, MCS, WLT, TCC, ASS\n"

df_header = ['TSB', 'TCB', 'SYS', 'LAG', 'IOU', 'GRN', 'THS', 'YAZ', 'TCT', 'CNC', 'MSG', 'TMI', 'TCP', 'IIL', 'FHG', 'SYM', 'LSC', 'PRN', 'EWM', 'TCM', 'ELT', 'HRG', 'TGP', 'MUN', 'WSU', 'IST', 'BAG', 'EVL', 'MCS', 'WLT', 'TCC', 'ASS']

df_header_w_dt = ['Date', 'Time', 'TSB', 'TCB', 'SYS', 'LAG', 'IOU', 'GRN', 'THS', 'YAZ', 'TCT', 'CNC', 'MSG', 'TMI', 'TCP', 'IIL', 'FHG', 'SYM', 'LSC', 'PRN', 'EWM', 'TCM', 'ELT', 'HRG', 'TGP', 'MUN', 'WSU', 'IST', 'BAG', 'EVL', 'MCS', 'WLT', 'TCC', 'ASS']

option_choices = ['stock', 'value', 'direction', 'change', 'command', 'help', 'duration', 'percent', 'filter', 'delay']
commands = ['notify', 'stocks', 'list', 'help', 'remove', 'bug']
directions = ['above', 'below', 'over', 'under', 'tops', 'bottoms' 'greater', 'less']
change = ['rises' , 'drops', 'falls', 'drop', 'fall', 'gain', 'gains', 'rise']
dir_up = ['above', 'over', 'rises', 'tops', 'gain', 'greater', 'gains', 'rise']
dir_down = ['below', 'under', 'falls', 'bottoms', 'drops', 'drop', 'fall', 'less']
alert_types = ['Value Change', 'Percent Change', 'Global Change']
extra_words = ['if', 'than']

proj_omissions = {'_id':0, 'discord_id':0, 'discord_name':0}

percent_precision = 4