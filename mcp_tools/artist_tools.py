"""
Artist-related tools for Spotify MCP Server
"""

import logging
from typing import Dict, Any
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class ArtistSearchRequest(BaseModel):
    query: str
    limit: int = 10

async def search_artists_tool(spotify_client, request: ArtistSearchRequest) -> Dict[str, Any]:
    """Search for artists on Spotify
    
    Arguments:
        request (ArtistSearchRequest):
            - query (str): Search query for artist name
            - limit (int, optional): Maximum number of results to return (default: 10, max: 50)
    
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
            - total_found (int): Number of artists found
            - message (str): Success message
            - error (str, optional): Error message if failed
    """
    try:
        results = spotify_client.search(
            q=request.query,
            type='artist',
            limit=min(request.limit, 50)
        )
        
        artists = []
        for artist in results['artists']['items']:
            artists.append({
                "id": artist['id'],
                "name": artist['name'],
                "popularity": artist['popularity'],
                "followers": artist['followers']['total'],
                "genres": artist['genres'],
                "spotify_url": artist['external_urls']['spotify']
            })
        
        return {
            "success": True,
            "artists": artists,
            "total_found": len(artists),
            "message": f"Found {len(artists)} artists for '{request.query}'"
        }
        
    except Exception as e:
        logger.error(f"Error searching artists: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to search artists"
        }

async def get_artist_tool(spotify_client, artist_id: str) -> Dict[str, Any]:
    """Get detailed information about an artist
    
    Arguments:
        artist_id (str): Spotify artist ID to get information for
    
    Returns:
        Dict[str, Any]:
            - success (bool): Whether the operation was successful
            - artist (Dict): Detailed artist information containing:
                - id (str): Spotify artist ID
                - name (str): Artist name
                - popularity (int): Artist popularity score (0-100)
                - followers (int): Number of followers
                - genres (List[str]): List of genres
                - spotify_url (str): Spotify profile URL
                - images (List[Dict]): List of artist images with:
                    - url (str): Image URL
                    - height (int): Image height
                    - width (int): Image width
            - message (str): Success message
            - error (str, optional): Error message if failed
    """
    try:
        artist = spotify_client.artist(artist_id)
        
        return {
            "success": True,
            "artist": {
                "id": artist['id'],
                "name": artist['name'],
                "popularity": artist['popularity'],
                "followers": artist['followers']['total'],
                "genres": artist['genres'],
                "spotify_url": artist['external_urls']['spotify'],
                "images": artist.get('images', [])
            },
            "message": f"Retrieved information for {artist['name']}"
        }
        
    except Exception as e:
        logger.error(f"Error getting artist: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to get artist information"
        }

async def get_artist_albums_tool(spotify_client, artist_id: str, include_groups: str = "album,single", limit: int = 20) -> Dict[str, Any]:
    """Get albums for an artist
    
    Arguments:
        artist_id (str): Spotify artist ID to get albums for
        include_groups (str, optional): Album types to include (default: "album,single")
            - "album": Full albums
            - "single": Singles
            - "appears_on": Appearances on other albums
            - "compilation": Compilation albums
        limit (int, optional): Maximum number of albums to return (default: 20, max: 50)
    
    Returns:
        Dict[str, Any]:
            - success (bool): Whether the operation was successful
            - artist (Dict): Basic artist information:
                - id (str): Artist ID
                - name (str): Artist name
            - albums (List[Dict]): List of album objects containing:
                - id (str): Spotify album ID
                - name (str): Album name
                - album_type (str): Type of album (album, single, compilation)
                - release_date (str): Release date
                - total_tracks (int): Number of tracks
                - spotify_url (str): Spotify album URL
                - images (List[Dict]): Album cover images
            - total_albums (int): Number of albums found
            - message (str): Success message
            - error (str, optional): Error message if failed
    """
    try:
        artist = spotify_client.artist(artist_id)
        albums = spotify_client.artist_albums(
            artist_id,
            album_type=include_groups,
            limit=min(limit, 50)
        )
        
        album_list = []
        for album in albums['items']:
            album_list.append({
                "id": album['id'],
                "name": album['name'],
                "album_type": album['album_type'],
                "release_date": album['release_date'],
                "total_tracks": album['total_tracks'],
                "spotify_url": album['external_urls']['spotify'],
                "images": album.get('images', [])
            })
        
        return {
            "success": True,
            "artist": {
                "id": artist['id'],
                "name": artist['name']
            },
            "albums": album_list,
            "total_albums": len(album_list),
            "message": f"Found {len(album_list)} albums for {artist['name']}"
        }
        
    except Exception as e:
        logger.error(f"Error getting artist albums: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to get artist albums"
        }

async def get_artist_top_tracks_tool(spotify_client, artist_id: str, market: str = "US") -> Dict[str, Any]:
    """Get top tracks for an artist
    
    Arguments:
        artist_id (str): Spotify artist ID to get top tracks for
        market (str, optional): Market/country code for track availability (default: "US")
    
    Returns:
        Dict[str, Any]:
            - success (bool): Whether the operation was successful
            - artist (Dict): Information about the artist:
                - id (str): Artist ID
                - name (str): Artist name
            - tracks (List[Dict]): List of track objects containing:
                - id (str): Spotify track ID
                - name (str): Track name
                - album (str): Album name
                - popularity (int): Track popularity score (0-100)
                - duration_ms (int): Track duration in milliseconds
                - spotify_url (str): Spotify track URL
            - message (str): Success message
            - error (str, optional): Error message if failed
    """
    try:
        artist = spotify_client.artist(artist_id)
        tracks = spotify_client.artist_top_tracks(artist_id, country=market)
        
        track_list = []
        for track in tracks['tracks']:
            track_list.append({
                "id": track['id'],
                "name": track['name'],
                "album": track['album']['name'],
                "popularity": track['popularity'],
                "duration_ms": track['duration_ms'],
                "spotify_url": track['external_urls']['spotify']
            })
        
        return {
            "success": True,
            "artist": {
                "id": artist['id'],
                "name": artist['name']
            },
            "tracks": track_list,
            "message": f"Found {len(track_list)} top tracks for {artist['name']}"
        }
        
    except Exception as e:
        logger.error(f"Error getting artist top tracks: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to get artist top tracks"
        } 