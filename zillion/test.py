import pandas as pd

from zillion.future import db_util

data = [['johnny😄', 'alice']]

output = pd.DataFrame(data=data, columns=['a', 'b'])

print(output)
db_util.to_db(data=output, tb_name='test_emoji', db_name='future')
