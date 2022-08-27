import pandas as pd
import regex as re

def year_make_model(post_title):
    '''
    Looks through post titles and finds results that have the format 'year make model'
    There are obviously several that return back incorrectly but this seems to return a large amount of them
    appropriately, will handle exceptions later.
    '''
    try:
        result = re.search(r'\d\d\d\d \w+ \w+\b', post_title).group()
        return result
    except:
        return 'False'

def year(year_mk_model):
    '''
    Returns the year out of the column made with the 'year make model' format.
    '''
    words = year_mk_model.split()
    return words[0]

def make(year_mk_model):
    '''
    Returns the make out of the column with the 'year make model' format.
    '''
    words = year_mk_model.split()
    return words[1]

def model(year_mk_model):
    '''
    Returns the mode out of the column with the 'year make model' format.
    '''
    words = year_mk_model.split()
    return words[2]

if __name__ == '__main__':
    df = pd.read_csv('all_cars.csv')


    # applying labels for year, make and model
    df['year_make_model'] = df.post_title.apply(year_make_model)
    df = df[df.year_make_model != 'False']
    df['year'] = df.year_make_model.apply(year)
    df['make'] = df.year_make_model.apply(make)
    df['model'] = df.year_make_model.apply(model)

    # save new info to csv
    df.to_csv('all_cars.csv')
    print(df)