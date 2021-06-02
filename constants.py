acronym_list = ('TSB', 'TCB', 'SYS', 'LAG', 'IOU', 'GRN', 'THS', 'YAZ', 'TCT', 'CNC', 'MSG', 'TMI', 'TCP', 'IIL', 'FHG', 'SYM', 'LSC', 'PRN', 'EWM', 'TCM', 'ELT', 'HRG', 'TGP', 'WSU', 'IST', 'BAG', 'EVL', 'MCS', 'WLT', 'TCC')

help_text = """```

I send custom notifications for stocks.

Commands: 
!help       You already figured this out
!stocks     Lists all stocks and most recent value
!notify     Add an alert
            [stock] [above/below] [value] [note (optional)]
!list       List alerts
!remove     Remove all notifications
!bug        Send a bug report, add text after to describe the problem.

Example: 
!notify TCB above 900 time to sell!


I hope to eventually have forward indicators on price movements.
        ```"""

prices_header = "Date, Time, TSB, TCB, SYS, LAG, IOU, GRN, THS, YAZ, TCT, CNC, MSG, TMI, TCP, IIL, FHG, SYM, LSC, PRN, EWM, TCM, ELT, HRG, TGP, WSU, IST, BAG, EVL, MCS, WLT, TCC\n"

df_header = ['TSB', 'TCB', 'SYS', 'LAG', 'IOU', 'GRN', 'THS', 'YAZ', 'TCT', 'CNC', 'MSG', 'TMI', 'TCP', 'IIL', 'FHG', 'SYM', 'LSC', 'PRN', 'EWM', 'TCM', 'ELT', 'HRG', 'TGP', 'WSU', 'IST', 'BAG', 'EVL', 'MCS', 'WLT', 'TCC']

df_header_w_dt = ['Date', 'Time', 'TSB', 'TCB', 'SYS', 'LAG', 'IOU', 'GRN', 'THS', 'YAZ', 'TCT', 'CNC', 'MSG', 'TMI', 'TCP', 'IIL', 'FHG', 'SYM', 'LSC', 'PRN', 'EWM', 'TCM', 'ELT', 'HRG', 'TGP', 'WSU', 'IST', 'BAG', 'EVL', 'MCS', 'WLT', 'TCC']