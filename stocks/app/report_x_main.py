from stocks.base import db_util

if __name__ == '__main__':
    df = db_util.read_table('uprising_daily')
    industry_count = {}
    concept_count = {}
    for index, row in df.iterrows():
        top_industry = row['industry']
        top_concept = row['concepts']
        industry_array = str.split(top_industry, '\n')
        concept_array = str.split(top_concept, '\n')
        for industry in industry_array:
            if industry == '':
                continue
            if industry in industry_count.keys():
                industry_count[industry] += 1
            else:
                industry_count[industry] = 1
        for concept in concept_array:
            if concept == '':
                continue
            if concept in concept_count.keys():
                concept_count[concept] += 1
            else:
                concept_count[concept] = 1

    print(sorted(industry_count.items(), key=lambda d: d[1]))
    print(sorted(concept_count.items(), key=lambda d: d[1]))
