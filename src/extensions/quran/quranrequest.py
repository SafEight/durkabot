class QuranRequest:
    _url = 'http://api.alquran.cloud/surah/{}/{}?offset={}&limit={}'

    def __init__(self, req, edition):
        # language not specified, assume english
        if edition.find('.') == -1 and edition.find('-') == -1:
            edition = 'en.' + edition
        self.edition = edition

        request = req.split(':')
        self.surah = int(request[0])

        verse_segment = request[1].split('-')

        self.offset = int(verse_segment[0]) - 1
        self.limit = int(verse_segment[1]) - self.offset if len(verse_segment) > 1 else 1

    @property
    def url(self):
        return self._url.format(self.surah, self.edition, self.offset, self.limit)
