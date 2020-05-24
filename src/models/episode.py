class Episode:
    """Episode class."""

    def __init__(self, subject_id: int, service_id: str, episode_id=-1, episode_url_id=None, video_url_id=None, remark=None):
        """Initializer.

        :param int subject_id: Bangumi subject ID, required
        :param int episode_id: Bangumi episode ID, with default value -1
        :param str service_id: service ID, required
        :param str episode_url_id: episode URL ID to construct episode URL, with default value None
        :param str video_url_id: video URL ID to construct video URL, with default value None
        :param str remark: episode remark, with default value None
        """
        self._subject_id = subject_id
        self._episode_id = episode_id
        self._service_id = service_id
        self._episode_url_id = episode_url_id
        self._video_url_id = video_url_id
        self._remark = remark

    @property
    def subject_id(self) -> int:
        """Get Bangumi subject ID.

        :return: Bangumi subject ID
        :rtype: int
        """
        return self._subject_id

    @property
    def episode_id(self) -> int:
        """Get Bangumi episode ID.

        :return: Bangumi episode ID
        :rtype: int
        """
        return self._episode_id

    @property
    def service_id(self) -> str:
        """Get service ID.

        :return: service ID
        :rtype: str
        """
        return self._service_id

    @property
    def episode_url_id(self) -> str:
        """Get episode URL ID.

        :return: episode URL ID to construct episode URL
        :rtype: str
        """
        return self._episode_url_id

    @property
    def video_url_id(self) -> str:
        """Get video URL ID.

        :return: video URL ID to construct video URL
        :rtype: str
        """
        return self._video_url_id

    @property
    def remark(self) -> str:
        """Get episode remark.

        :return: episode remark
        :rtype: str
        """
        return self._remark

    def __str__(self) -> str:
        """Get the string representation of an Episode object.

        :return: string representation of the Episode object
        :rtype: str
        """
        return self._str_csv()

    def _str_csv(self) -> str:
        """Get the string representation of an Episode object in CSV format.

        :return: string representation of the Episode object in CSV format
        :rtype: str
        """
        return '%d,%s,%s,%s,%s,%s' % (
            self._subject_id,
            str(self._episode_id) if self._episode_id >= 0 else '',
            self._service_id,
            self._episode_url_id if self._episode_url_id else '',
            self._video_url_id if self._video_url_id else '',
            self._remark if self._remark else '',
        )
