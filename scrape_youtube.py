import os
from typing import List, Tuple, Optional
from googleapiclient.discovery import build, Resource


def create_youtube_client(api_key: str) -> Resource:
    """
    Creates a YouTube client given an API key.

    Args:
        api_key: A string containing the YouTube Data API key.

    Returns:
        A YouTube Resource object to interact with the client.
    """
    return build("youtube", "v3", developerKey=api_key)


def get_channel_id_by_username(
    youtube: Resource, channel_username: str
) -> Optional[str]:
    """
    Retrieves the channel ID for a given YouTube username.

    Args:
        youtube: A YouTube Resource object.
        channel_username: A string containing the YouTube channel username.

    Returns:
        The channel ID as a string if found, None otherwise.
    """
    channel_response = (
        youtube.channels().list(part="id", forUsername=channel_username).execute()
    )

    if "items" in channel_response and len(channel_response["items"]) > 0:
        return channel_response["items"][0]["id"]
    else:
        return None


def get_channel_uploads_playlist_id(youtube: Resource, channel_id: str) -> str:
    """
    Retrieves the uploads playlist ID for a given YouTube channel ID.

    Args:
        youtube: A YouTube Resource object.
        channel_id: A string containing the YouTube channel ID.

    Returns:
        The uploads playlist ID as a string.
    """
    channel_response = (
        youtube.channels().list(part="contentDetails", id=channel_id).execute()
    )

    return channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def get_recent_video_ids(
    youtube: Resource, uploads_playlist_id: str, num_videos: int
) -> List[str]:
    """
    Retrieves the most recent video IDs from a given uploads playlist.

    Args:
        youtube: A YouTube Resource object.
        uploads_playlist_id: A string containing the uploads playlist ID.
        num_videos: An integer specifying the number of video IDs to retrieve.

    Returns:
        A list of strings containing the recent video IDs.
    """
    playlist_items_response = (
        youtube.playlistItems()
        .list(part="snippet", playlistId=uploads_playlist_id, maxResults=num_videos)
        .execute()
    )

    return [
        item["snippet"]["resourceId"]["videoId"]
        for item in playlist_items_response["items"]
    ]


def get_video_details(youtube: Resource, video_ids: List[str]) -> List[Tuple[str, str]]:
    """
    Retrieves details for a list of video IDs.

    Args:
        youtube: A YouTube Resource object.
        video_ids: A list of strings containing video IDs.

    Returns:
        A list of tuples, each containing the video title and description.
    """
    video_response = (
        youtube.videos().list(part="snippet", id=",".join(video_ids)).execute()
    )

    videos = []
    for item in video_response["items"]:
        video_title = item["snippet"]["title"]
        video_description = item["snippet"]["description"]
        videos.append((video_title, video_description))

    return videos


def get_recent_videos(
    channel_id: str, num_videos: int, api_key: str
) -> List[Tuple[str, str]]:
    """
    Retrieves details of recent videos for a given YouTube channel.

    Args:
        channel_id: A string containing the YouTube channel ID.
        num_videos: An integer specifying the number of recent videos to retrieve.
        api_key: A string containing the YouTube Data API key.

    Returns:
        A list of tuples, each containing the video title and description.
    """
    youtube = create_youtube_client(api_key)
    uploads_playlist_id = get_channel_uploads_playlist_id(youtube, channel_id)
    recent_video_ids = get_recent_video_ids(youtube, uploads_playlist_id, num_videos)
    recent_videos = get_video_details(youtube, recent_video_ids)
    return recent_videos


if __name__ == "__main__":
    # Example usage
    channel_id = "UCBJycsmduvYEL83R_U4JriQ"
    num_videos = 5
    api_key = os.getenv("YOUTUBE_DATA_API_KEY")

    recent_videos = get_recent_videos(channel_id, num_videos, api_key)

    for title, description in recent_videos:
        print(f"Title: {title}")
        print(f"Description: {description}")
        print("---")
