class Source:
    """Source class."""

    def __init__(self, subject_id: int, service_id: str, paid=-1, subject_url_id=None, subtitle_locales=[], remark=None):
        """Initializer.

        :param int subject_id: Bangumi subject ID, required
        :param str service_id: service ID, required
        :param int paid: paid status, with default value -1
        :param str subject_url_id: subject URL ID to construct subject URL, with default value None
        :param list subtitle_locales: list of subtitle locales, with default value an empty list
        :param str remark: source remark, with default value None
        """
        self._subject_id = subject_id
        self._service_id = service_id
        self._paid = paid
        self._subject_url_id = subject_url_id
        self._subtitle_locales = sorted(subtitle_locales)
        self._remark = remark

    @property
    def subject_id(self) -> int:
        """Get Bangumi subject ID.

        :return: Bangumi subject ID
        :rtype: int
        """
        return self._subject_id

    @property
    def service_id(self) -> str:
        """Get service ID.

        :return: service ID
        :rtype: str
        """
        return self._service_id

    @property
    def paid(self) -> int:
        """Get paid status.

        :return: paid status, with value -1 (unknown) , 0 (all episodes free), 1 (the first two episodes free) or 2 (all episodes paid)
        :rtype: int
        """
        return self._paid

    @property
    def subject_url_id(self) -> str:
        """Get subject URL ID.

        :return: subject URL ID to construct subject URL
        :rtype: str
        """
        return self._subject_url_id

    @property
    def subtitle_locales(self) -> list:
        """Get a list of subtitle locales.

        :return: list of subtitle locales, each in the format of 'xx_XX'
        :rtype: list
        """
        return self._subtitle_locales

    @property
    def remark(self) -> str:
        """Get source remark.

        :return: source remark
        :rtype: str
        """
        return self._remark

    def __str__(self) -> str:
        """Get the string representation of a Source object.

        :return: string representation of the Source object
        :rtype: str
        """
        return self._str_csv()

    def _str_csv(self) -> str:
        """Get the string representation of a Source object in CSV format.

        :return: string representation of the Source object in CSV format
        :rtype: str
        """
        return '%d,%s,%d,%s,%s,%s' % (
            self._subject_id,
            self._service_id,
            self._paid,
            self._subject_url_id if self._subject_url_id else '',
            ':'.join(self.subtitle_locales),
            self._remark if self._remark else '',
        )
