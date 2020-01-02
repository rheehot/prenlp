import os
import json
from pathlib import Path

from .base import Dataset
from ..utils import download_from_url

class WikiText2(Dataset):
    """WikiText-2 word-level dataset for language modeling.
    
    From:
        Salesforce, https://blog.einstein.ai/the-wikitext-long-term-dependency-language-modeling-dataset/
    
    License:
        Creative Commons Attribution-ShareAlike
    
    Args:
        root (str): path to the dataset's highest level directory
    
    Examples:
    >>> wikitext2 = prenlp.data.WikiText2()
    >>> len(wikitext2)
    3
    >>> train, valid, test = prenlp.data.WikiText2()
    >>> len(train), len(valid), len(test)
    (23767, 2461, 2891)
    >>> train[0]
    = Valkyria Chronicles III =
    """

    def __init__(self, root: str='.data'):
        self.url = 'https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-2-v1.zip'
        self.root = Path(root)
        self.dirname = 'wikitext-2'
        
        self.skip_empty = True # Whether to skip the empty samples (only for WikiText)

        if not (self.root/self.dirname).exists():
            super(WikiText2, self)._download(to_path = self.root)
        
        super(WikiText2, self).__init__(self._get_data())

    def _get_data(self, train: str='wiki.train.tokens', valid: str='wiki.valid.tokens',
                  test: str='wiki.test.tokens') -> list:
        dataset = []
        for i, data in enumerate([train, valid, test]):
            filename = self.root/self.dirname/data
            with open(filename, 'r', encoding='utf-8') as reader:
                if self.skip_empty:                    
                    samples = [line.strip() for line in reader.readlines() if line.strip()]
                else:
                    samples = [line.strip() for line in reader.readlines()]
                dataset.append(samples)
        
        return dataset


class WikiText103(Dataset):
    """WikiText-103 word-level dataset for language modeling.
    
    From:
        Salesforce, https://blog.einstein.ai/the-wikitext-long-term-dependency-language-modeling-dataset/
    
    License:
        Creative Commons Attribution-ShareAlike
    
    Args:
        root (str): path to the dataset's highest level directory
    
    Examples:
    >>> wikitext103 = prenlp.data.WikiText103()
    >>> len(wikitext103)
    3
    >>> train, valid, test = prenlp.data.WikiText103()
    >>> len(train), len(valid), len(test)
    (1165029, 2461, 2891)
    >>> train[0]
    = Valkyria Chronicles III =
    """

    def __init__(self, root: str='.data'):
        self.url = 'https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-v1.zip'
        self.root = Path(root)
        self.dirname = 'wikitext-103'
        
        self.skip_empty = True # Whether to skip the empty samples (only for WikiText)

        if not (self.root/self.dirname).exists():
            super(WikiText103, self)._download(to_path = self.root)
        
        super(WikiText103, self).__init__(self._get_data())

    def _get_data(self, train: str='wiki.train.tokens', valid: str='wiki.valid.tokens',
                  test: str='wiki.test.tokens') -> list:
        dataset = []
        for i, data in enumerate([train, valid, test]):
            filename = self.root/self.dirname/data
            with open(filename, 'r', encoding='utf-8') as reader:
                if self.skip_empty:                    
                    samples = [line.strip() for line in reader.readlines() if line.strip()]
                else:
                    samples = [line.strip() for line in reader.readlines()]
                dataset.append(samples)
        
        return dataset


class WikiTextKo(Dataset):
    """Wikipedia database dump (Korean) for language modeling.

    From:
        Wikipedia, https://dumps.wikimedia.org/kowiki/
    
    Args:
        root (str): path to the dataset's highest level directory
    
    Examples:
    >>> wikitextko = prenlp.data.WikiTextKo()
    >>> len(wikitextko)
    2334771
    >>> wikitextko[0]
    '지미 카터'
    >>> wikitextko[1]
    '제임스 얼 "지미" 카터 주니어(, 1924년 10월 1일 ~ )는 민주당 출신 미국 39번째 대통령 (1977년 ~ 1981년)이다.'
    """

    def __init__(self, root: str='.data'):
        self.url = 'https://dumps.wikimedia.org/kowiki/latest/kowiki-latest-pages-articles.xml.bz2'
        self.root = Path(root)
        self.dirname = 'wikitext-ko'
        
        # WikiExtractor
        self.url_wikiextractor = 'https://raw.githubusercontent.com/attardi/wikiextractor/master/WikiExtractor.py'
        self.wikiextractor = 'WikiExtractor.py'

        if not (self.root/self.dirname).exists():
            self._download(to_path = self.root)

        super(WikiTextKo, self).__init__(self._get_data())
    
    def _download(self, to_path: str) -> None:
        """Override method of 'Dataset' class.
        """
        download_filename = self.url.split('/')[-1]
        from_path = download_from_url(self.url, download_filename, to_path)
        
        # Extracts and cleans text from a Wikipedia database dump using WikiExtractor.
        # WikiExtractor: https://github.com/attardi/wikiextractor
        wikiextractor_path = download_from_url(self.url_wikiextractor, self.wikiextractor, to_path)
        os.system(f'python {self.root/self.wikiextractor} -o {to_path/self.dirname} --json {from_path}')
        
    def _get_data(self) -> list:
        dataset = []
        filenames = [str(filename) for filename in (self.root/self.dirname).glob('**/wiki_*')]
        for filename in sorted(filenames):
            with open(filename, 'r', encoding='utf-8') as reader:
                for line in reader.readlines(): # line = a document
                    text = json.loads(line)['text']
                    # split document into sentences(len > 0)
                    samples = list(filter(lambda x: len(x) > 0, text.split('\n')))
                    dataset += samples
                    # If sample is a document, use below code not above two lines.
                    # sample = '\n'.join(list(filter(lambda x: len(x) > 0, text.split('\n'))))
                    # dataset.append(sample)

        return dataset