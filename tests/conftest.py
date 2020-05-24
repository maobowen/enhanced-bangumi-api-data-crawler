import pytest
import re


# https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions
@pytest.fixture
def generic_test_helper():
    """Generic test helper."""
    return GenericTestHelper


class GenericTestHelper:
    """Generic test helper class."""

    @staticmethod
    def test_source(source, test_config: dict):
        """Compare source object

        :param source: source object
        :param dict test_config: test case configuration
        """
        assert source.subject_id == test_config['subject_id']
        assert source.service_id == test_config['service_id']
        assert source.paid == test_config['paid']
        if test_config.get('subject_url_id'):
            assert source.subject_url_id == test_config['subject_url_id']
        if test_config.get('subtitle_locales'):
            assert set(source.subtitle_locales) == set(test_config['subtitle_locales'])
        if test_config.get('remark'):
            if test_config.get('is_remark_regex'):
                assert re.search(test_config['remark'], source.remark)
            else:
                assert source.remark == test_config['remark']

    @staticmethod
    def test_episodes(episodes: list, test_config: dict):
        """Compare episode objects

        :param list episodes: list of episode objects
        :param dict test_config: test case configuration
        """
        assert episodes
        assert len(episodes) == test_config['episodes_count']
        test_episodes = test_config['test_episodes']
        for test_episode_item in test_episodes:
            test_episode = episodes[test_episode_item['index']]
            assert test_episode.subject_id == test_config['subject_id']
            assert test_episode.episode_id == test_episode_item['episode_id']
            assert test_episode.service_id == test_config['service_id']
            if test_config.get('episode_url_id_pattern'):
                assert re.search(test_config['episode_url_id_pattern'], test_episode.episode_url_id)
            if test_config.get('video_url_id_pattern'):
                assert re.search(test_config['video_url_id_pattern'], test_episode.video_url_id)
            if test_episode_item.get('remark'):
                if test_episode_item.get('is_remark_regex'):
                    assert re.search(test_episode_item['remark'], test_episode.remark)
                else:
                    assert test_episode.remark == test_episode_item['remark']
