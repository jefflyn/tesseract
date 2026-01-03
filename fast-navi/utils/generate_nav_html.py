import zillion.utils.db_util as _dt



def generate_nav_html():
    df = _dt.read_query('app','select * from int_nav_basic')
    columns = df.columns.tolist()

    for record in df.itertuples(index=True, name='Pandas'):
        tr = "<tr>"
        for col in columns:
            if col == 'id':
                continue
            value = getattr(record, col)
            value = value.replace('\n', '<br>')
            td = "<td>{}</td>".format(value)
            tr += td
        tr += "</tr>"
        print(tr)

if __name__ == '__main__':
    generate_nav_html()