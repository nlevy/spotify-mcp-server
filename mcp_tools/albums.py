"""
Album-related tools for Spotify MCP Server
"""

import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

async def get_album_tool(spotify_client, album_id: str, market: str = "US") -> Dict[str, Any]:
    """Get detailed information about an album
    
    Arguments:
        album_id (str): Spotify album ID to get information for
        market (str, optional): Market/country code for album availability (default: "US")
    
    Returns:
        Dict[str, Any]:
            - success (bool): Whether the operation was successful
            - album (Dict): Detailed album information containing:
                - id (str): Spotify album ID
                - name (str): Album name
                - album_type (str): Type of album (album, single, compilation)
                - release_date (str): Release date
                - total_tracks (int): Number of tracks
                - popularity (int): Album popularity score (0-100)
                - spotify_url (str): Spotify album URL
                - artists (List[Dict]): List of artists with:
                    - id (str): Artist ID
                    - name (str): Artist name
                - images (List[Dict]): Album cover images
                - genres (List[str]): List of genres
            - message (str): Success message
            - error (str, optional): Error message if failed
    """
    try:
        album = spotify_client.album(album_id, market=market)
        
        artists = []
        for artist in album.get('artists', []):
            artists.append({
                "id": artist['id'],
                "name": artist['name']
            })
        
        return {
            "success": True,
            "album": {
                "id": album['id'],
                "name": album['name'],
                "album_type": album['album_type'],
                "release_date": album['release_date'],
                "total_tracks": album['total_tracks'],
                "popularity": album.get('popularity', 0),
                "spotify_url": album['external_urls']['spotify'],
                "artists": artists,
                "images": album.get('images', []),
                "genres": album.get('genres', [])
            },
            "message": f"Retrieved information for album '{album['name']}'"
        }
        
    except Exception as e:
        logger.error(f"Error getting album: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to get album information"
        }

async def get_album_tracks_tool(spotify_client, album_id: str, market: str = "US", limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """Get tracks from an album
    
    Arguments:
        album_id (str): Spotify album ID to get tracks for
        market (str, optional): Market/country code for track availability (default: "US")
        limit (int, optional): Maximum number of tracks to return (default: 20, max: 50)
        offset (int, optional): Index of the first track to return (default: 0)
    
    Returns:
        Dict[str, Any]:
            - success (bool): Whether the operation was successful
            - album (Dict): Basic album information:
                - id (str): Album ID
                - name (str): Album name
            - tracks (List[Dict]): List of track objects containing:
                - id (str): Spotify track ID
                - name (str): Track name
                - track_number (int): Track number on the album
                - duration_ms (int): Track duration in milliseconds
                - spotify_url (str): Spotify track URL
                - artists (List[Dict]): List of artists with:
                    - id (str): Artist ID
                    - name (str): Artist name
            - total_tracks (int): Total number of tracks in the album
            - message (str): Success message
            - error (str, optional): Error message if failed
    """
    try:
        album = spotify_client.album(album_id, market=market)
        tracks = spotify_client.album_tracks(
            album_id,
            market=market,
            limit=min(limit, 50),
            offset=offset
        )
        
        track_list = []
        for track in tracks['items']:
            track_artists = []
            for artist in track.get('artists', []):
                track_artists.append({
                    "id": artist['id'],
                    "name": artist['name']
                })
            
            track_list.append({
                "id": track['id'],
                "name": track['name'],
                "track_number": track['track_number'],
                "duration_ms": track['duration_ms'],
                "spotify_url": track['external_urls']['spotify'],
                "artists": track_artists
            })
        
        return {
            "success": True,
            "album": {
                "id": album['id'],
                "name": album['name']
            },
            "tracks": track_list,
            "total_tracks": tracks['total'],
            "message": f"Found {len(track_list)} tracks from album '{album['name']}'"
        }
        
    except Exception as e:
        logger.error(f"Error getting album tracks: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to get album tracks"
        }

async def get_new_releases_tool(spotify_client, country: str = "US", limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """Get new album releases
    
    Arguments:
        country (str, optional): Country code to get new releases for (default: "US")
        limit (int, optional): Maximum number of albums to return (default: 20, max: 50)
        offset (int, optional): Index of the first album to return (default: 0)
    
    Returns:
        Dict[str, Any]:
            - success (bool): Whether the operation was successful
            - albums (List[Dict]): List of new release albums containing:
                - id (str): Spotify album ID
                - name (str): Album name
                - album_type (str): Type of album (album, single, compilation)
                - release_date (str): Release date
                - total_tracks (int): Number of tracks
                - spotify_url (str): Spotify album URL
                - artists (List[Dict]): List of artists with:
                    - id (str): Artist ID
                    - name (str): Artist name
                - images (List[Dict]): Album cover images
            - total_albums (int): Number of albums found
            - message (str): Success message
            - error (str, optional): Error message if failed
    """
    try:
        new_releases = spotify_client.new_releases(
            country=country,
            limit=min(limit, 50),
            offset=offset
        )
        
        album_list = []
        for album in new_releases['albums']['items']:
            artists = []
            for artist in album.get('artists', []):
                artists.append({
                    "id": artist['id'],
                    "name": artist['name']
                })
            
            album_list.append({
                "id": album['id'],
                "name": album['name'],
                "album_type": album['album_type'],
                "release_date": album['release_date'],
                "total_tracks": album['total_tracks'],
                "spotify_url": album['external_urls']['spotify'],
                "artists": artists,
                "images": album.get('images', [])
            })
        
        return {
            "success": True,
            "albums": album_list,
            "total_albums": len(album_list),
            "message": f"Found {len(album_list)} new releases for {country}"
        }
        
    except Exception as e:
        logger.error(f"Error getting new releases: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to get new releases"
        } 