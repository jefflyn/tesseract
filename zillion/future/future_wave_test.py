import pandas as pd

from zillion.future import future_util
from zillion.future import future_wave
from zillion.utils import db_util

if __name__ == '__main__':
    code = 'A2201.DCE,A2203.DCE,A2205.DCE,AG2206.SHF,AL2205.SHF,AP2201.ZCE,AP2205.ZCE,AU2206.SHF,BU2206.SHF,C2201.DCE,C2205.DCE,CF2201.ZCE,CF2205.ZCE,CJ2201.ZCE,CJ2205.ZCE,CU2205.SHF,EB2205.DCE,EG2201.DCE,EG2205.DCE,FG2201.ZCE,FG2205.ZCE,FU2201.SHF,FU2205.SHF,HC2201.SHF,HC2205.SHF,I2201.DCE,I2205.DCE,J2201.DCE,J2205.DCE,JD2201.DCE,JD2205.DCE,JM2201.DCE,JM2205.DCE,L2201.DCE,L2205.DCE,LH2201.DCE,LH2205.DCE,LU2205.INE,M2201.DCE,M2205.DCE,MA2201.ZCE,MA2205.ZCE,NI2205.SHF,NR2205.INE,OI2201.ZCE,OI2205.ZCE,P2201.DCE,P2205.DCE,PB2205.SHF,PF2201.ZCE,PF2205.ZCE,PG2205.DCE,PK2204.ZCE,PP2201.DCE,PP2205.DCE,RB2201.SHF,RB2205.SHF,RM2201.ZCE,RM2205.ZCE,RU2201.SHF,RU2205.SHF,SA2201.ZCE,SA2205.ZCE,SC2205.INE,SF2201.ZCE,SF2205.ZCE,SM2201.ZCE,SM2205.ZCE,SN2205.SHF,SP2201.SHF,SP2205.SHF,SR2201.ZCE,SR2205.ZCE,SS2205.SHF,TA2201.ZCE,TA2205.ZCE,UR2201.ZCE,UR2205.ZCE,V2201.DCE,V2205.DCE,Y2201.DCE,Y2205.DCE,ZN2205.SHF'  # SHF ZCE DCE
    code_list = code.split(",")
    wave_data_list = []
    for code in code_list:
        df_data = future_util.get_ts_future_daily(code)[['ts_code', 'trade_date', 'open', 'high', 'low', 'close']]
        df_data.columns = ['code', 'date', 'open', 'high', 'low', 'close']
        wave_df = future_wave.get_wave(code, hist_data=df_data, begin_low=True, duration=0, change=0)
        wave_str = future_wave.wave_to_str(wave_df)
        wave_list = future_wave.get_wave_list(wave_str)
        wave_list.insert(0, code)
        wave_list.insert(1, code.split('.')[0])
        wave_list.insert(2, list(wave_df['begin'])[0])
        wave_list.insert(3, list(wave_df['end'])[-1])
        print(wave_df)
        print(wave_str)
        print(wave_list)
        wave_data_list.append(wave_list)
    wave_df_result = pd.DataFrame(wave_data_list,
                                  columns=['ts_code', 'code', 'start', 'end', 'a', 'b', 'c', 'd', 'ap', 'bp', 'cp', 'dp'])
    db_util.to_db(wave_df_result, 'future_wave_test')
