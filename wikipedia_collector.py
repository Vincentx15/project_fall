import wikipediaapi
import wikipedia
import pandas as pd
import random
import time

wiki_en = wikipediaapi.Wikipedia('en')
wiki_fr = wikipediaapi.Wikipedia('fr')

# page_py = wiki_en.page('Python_(programming_language)')
# page_fr = wiki_fr.page('Poulet')
# page_en = wiki_en.page('Chicken')


def get_other_language(page, language):
    """
    Get the langlink if it exists
    :param page: Wikipedia page
    :param language: language code such as 'fr', 'en'...
    :return: the link to the requested page
    """
    try:
        langlinks = page.langlinks
        v = langlinks[language]
    except:
        # print('Pas de page en %s' % language)
        return 0
    return v


def sample_bilingual_batch(iteration):
    """
    Get random wiki pages, to be called by the function below
    :param iteration: to track the progress
    :return: nothing, writes csv
    """
    wikipedia.set_lang('fr')
    random_pages = (wikipedia.random(500))
    count = 0
    data = []
    time.sleep(random.random())
    for i, page_fr in enumerate(random_pages):
        if not i % 30:
            print('pages visited =', iteration + i)
        page_fr = wiki_fr.page(page_fr)
        page_en = get_other_language(page_fr, 'en')
        if page_en:
            count += 1
            id = page_fr.pageid
            summary_fr = page_fr.summary
            summary_en = page_en.summary
            row = {'id': id, 'summary_fr': summary_fr, 'summary_en': summary_en}
            data.append(row)
            if not count % 20:
                df = pd.DataFrame(data=data)
                df.to_csv('data/wikipedia/samples.csv', mode='a')
                data = []
    df = pd.DataFrame(data=data)
    df.to_csv('data/wikipedia/samples.csv', mode='a')


def sample_bilingual(number=10000):
    """
    Repeatedly call the former function to randomly sample wiki pages and check for an english page.
    :param number: The number after which we should stop
    :return: nothing, the called function writes csv
    """
    sampled = 0
    while sampled < number:
        sample_bilingual_batch(sampled)
        sampled += 500


sample_bilingual(10000)


# df = pd.read_csv('data/wikipedia/samples.csv')
# print(df)



