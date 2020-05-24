def get_episode_id(index: int, episode_ids: list) -> int:
    """Get the Bangumi episode ID from a list based on the index.

    :param int index: index of the episode in the list
    :param list episode_ids: list of all Bangumi episode IDs
    :return: Bangumi episode ID corresponding to the index
    :rtype: int
    """
    episode_id = -1
    if index < len(episode_ids) and episode_ids[index] != -1:
        episode_id = episode_ids[index]
    return episode_id


def get_paid_status(count: int, free_count: int) -> int:
    """Get paid status of a source.

    :param int count: number of episodes
    :param int free_count: number of episodes that are free to watch
    :return: paid status, with value -1 (unknown) , 0 (all episodes free), 1 (the first two episodes free) or 2 (all episodes paid)
    :rtype: int
    """
    if count == 1 and 0 <= free_count <= 1:
        paid = 1 - free_count
    else:
        if free_count == 0:
            paid = 2
        elif free_count <= 2:
            paid = 1
        else:
            paid = 0
    return paid
