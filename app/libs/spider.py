import requests


class BookSpider:
    """
        鱼书API提供数据
    """
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    @classmethod
    def search_by_isbn(cls, isbn):
        """
            isbn搜索的结果可以被缓存
        """
        url = cls.isbn_url.format(isbn)
        res = cls.get(url)
        return {
            'total': 1,
            'books': [res]
        } if res else None

    @classmethod
    def search_by_keyword(cls, keyword, start, count):
        """
            keyword不缓存，意义不大
        """
        url = cls.keyword_url.format(keyword, count, start)
        res = cls.get(url)
        return {
            'total': res['total'],
            'books': res['books']
        } if res else None

    @classmethod
    def get(cls, url, is_json=True):
        res = requests.get(url)
        if res.status_code == 200:
            return res.json() if is_json else res.text
        return {} if is_json else ''
