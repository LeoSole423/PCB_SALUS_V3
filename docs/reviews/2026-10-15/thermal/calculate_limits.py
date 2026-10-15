"""Sensitivity estimate, not validated thermal model of the enclosure.
Run from any directory. Standard library only. No design modifications.
"""
from pathlib import Path
import csv,json
out=Path(__file__).resolve().parent
rows=[]
# 110 C is a chosen 15 C margin to manufacturer max125 C, not a manufacturer rating.
# 10mA ground-current reserve is an assumption, not a measured/spec max.
for vin in [4.6,5.0]:
 for current in [.15,.2,.25,.3,.35,.4,.5]:
  power=(vin-3.3)*current+vin*.01
  for theta in [60,80,100]:
   rise=power*theta
   rows.append(dict(vin_regulator_v=vin,load_current_a=current,ground_current_reserve_a=.01,power_w=round(power,4),theta_ja_assumed_c_per_w=theta,rise_c=round(rise,2),tj_at_ambient50_c=round(50+rise,2),tj_at_ambient60_c=round(60+rise,2),ambient_for_tj110_c=round(110-rise,2),ambient_for_tj125_c=round(125-rise,2)))
with (out/'thermal_scenarios.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)
(out/'thermal_scenarios.json').write_text(json.dumps({'assumptions':{'output_v':3.3,'junction_limit_manufacturer_c':125,'junction_design_target_c':110,'ground_current_reserve_a':.01,'theta_range':'60 exploratory,80 reference,100 adverse sensitivity; none measured on actualPCB','vin':'afterD7;4.6V nominal illustrative and5.0V elevated illustrative','current':'continuous or thermal-average; not pulse peak; not measured'},'rows':rows},indent=2)+'\n')
for vin in [4.6,5.0]:
 print('VIN',vin)
 for i in [.2,.3,.4,.5]:
  rr=[r for r in rows if r['vin_regulator_v']==vin and r['load_current_a']==i and r['theta_ja_assumed_c_per_w'] in [80,100]]
  print(i,'power',rr[0]['power_w'],'Tj60',[r['tj_at_ambient60_c'] for r in rr],'ambient110',[r['ambient_for_tj110_c'] for r in rr])
