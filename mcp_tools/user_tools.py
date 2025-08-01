"""
User-related tools for Spotify MCP Server
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)
valid_time_ranges = ["short_term", "medium_term", "long_term"]

async def get_user_top_artists_tool(
    spotify_client,
    time_range: str = "medium_term",
    limit: int = 20,
    offset: int = 0
) -> Dict[str, Any]:
    """Get user's top artists from Spotify
    
    Arguments:
        time_range (str, optional): Time period for top artists (default: "medium_term")
            - "short_term": Last 4 weeks
            - "medium_term": Last 6 months  
            - "long_term": Several years
        limit (int, optional): Maximum number of artists to return (default: 20, max: 50)
        offset (int, optional): Index of the first artist to return (default: 0)
    
    Returns:
        Dict[str, Any]:
            - success (bool): Whether the operation was successful
            - artists (List[Dict]): List of artist objects containing:
                - id (str): Spotify artist ID
                - name (str): Artist name
                - popularity (int): Artist popularity score (0-100)
                - followers (int): Number of followers
                - genres (List[str]): List of genres
                - spotify_url (str): Spotify profile URL
                - images (List[Dict]): Artist images with url, height, width
            - time_range (str): Time range used for the query
            - total_artists (int): Number of artists returned
            - message (str): Success message
            - error (str, optional): Error message if failed
    """
    try:
        if time_range not in valid_time_ranges:
            return {
                "success": False,
                "error": f"Invalid time_range '{time_range}'. Valid options are: {', '.join(valid_time_ranges)}",
                "message": "Invalid time range parameter"
            }
        
        if offset < 0:
            return {
                "success": False,
                "error": "Offset must be non-negative",
                "message": "Invalid offset parameter"
            }
        
        if limit > 50:
            limit = 50
        
        if limit < 1:
            return {
                "success": False,
                "error": "Limit must be at least 1",
                "message": "Invalid limit parameter"
            }
        
        results = spotify_client.current_user_top_artists(
            time_range=time_range,
            limit=limit,
            offset=offset
        )
        
        artists = []
        for artist in results['items']:
            artists.append({
                "id": artist['id'],
                "name": artist['name'],
                "popularity": artist['popularity'],
                "followers": artist['followers']['total'],
                "genres": artist['genres'],
                "spotify_url": artist['external_urls']['spotify'],
                "images": artist.get('images', [])
            })
        
        return {
            "success": True,
            "artists": artists,
            "time_range": time_range,
            "total_artists": len(artists),
            "message": f"Found {len(artists)} top artists for {time_range} period"
        }
        
    except Exception as e:
        logger.error(f"Error getting user top artists: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to get user's top artists"
        }

async def get_user_top_tracks_tool(
    spotify_client,
    time_range: str = "medium_term",
    limit: int = 20,
    offset: int = 0
) -> Dict[str, Any]:
    """Get user's top tracks from Spotify
    
    Arguments:
        time_range (str, optional): Time period for top tracks (default: "medium_term")
            - "short_term": Last 4 weeks
            - "medium_term": Last 6 months
            - "long_term": Several years
        limit (int, optional): Maximum number of tracks to return (default: 20, max: 50)
        offset (int, optional): Index of the first track to return (default: 0)
    
    Returns:
        Dict[str, Any]:
            - success (bool): Whether the operation was successful
            - tracks (List[Dict]): List of track objects containing:
                - id (str): Spotify track ID
                - name (str): Track name
                - album (Dict): Album info with id, name, images
                - artists (List[Dict]): List of artists with id, name
                - popularity (int): Track popularity score (0-100)
                - duration_ms (int): Track duration in milliseconds
                - spotify_url (str): Spotify track URL
            - time_range (str): Time range used for the query
            - total_tracks (int): Number of tracks returned
            - message (str): Success message
            - error (str, optional): Error message if failed
    """
    try:
        if time_range not in valid_time_ranges:
            return {
                "success": False,
                "error": f"Invalid time_range '{time_range}'. Valid options are: {', '.join(valid_time_ranges)}",
                "message": "Invalid time range parameter"
            }
        
        if offset < 0:
            return {
                "success": False,
                "error": "Offset must be non-negative",
                "message": "Invalid offset parameter"
            }
        
        if limit > 50:
            limit = 50
        
        if limit < 1:
            return {
                "success": False,
                "error": "Limit must be at least 1",
                "message": "Invalid limit parameter"
            }
        
        results = spotify_client.current_user_top_tracks(
            time_range=time_range,
            limit=limit,
            offset=offset
        )
        
        tracks = []
        for track in results['items']:
            album_info = {
                "id": track['album']['id'],
                "name": track['album']['name'],
                "images": track['album'].get('images', [])
            }
            
            track_artists = []
            for artist in track.get('artists', []):
                track_artists.append({
                    "id": artist['id'],
                    "name": artist['name']
                })
            
            tracks.append({
                "id": track['id'],
                "name": track['name'],
                "album": album_info,
                "artists": track_artists,
                "popularity": track['popularity'],
                "duration_ms": track['duration_ms'],
                "spotify_url": track['external_urls']['spotify']
            })
        
        return {
            "success": True,
            "tracks": tracks,
            "time_range": time_range,
            "total_tracks": len(tracks),
            "message": f"Found {len(tracks)} top tracks for {time_range} period"
        }
        
    except Exception as e:
        logger.error(f"Error getting user top tracks: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to get user's top tracks"
        }