"""
Playlist-related tools for Spotify MCP Server
"""

import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class PlaylistCreateRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    public: bool = False
    collaborative: bool = False

class AddTracksRequest(BaseModel):
    playlist_id: str
    track_uris: List[str]

async def create_playlist_tool(spotify_client, request: PlaylistCreateRequest) -> Dict[str, Any]:
    """Create a new Spotify playlist
    
    Arguments:
        request (PlaylistCreateRequest): 
            - name (str): Name of the playlist to create
            - description (str, optional): Description of the playlist (default: "")
            - public (bool, optional): Whether the playlist is public (default: False)
            - collaborative (bool, optional): Whether the playlist is collaborative (default: False)
    
    Returns:
        Dict[str, Any]: 
            - success (bool): Whether the operation was successful
            - playlist_id (str): ID of the created playlist
            - playlist_name (str): Name of the created playlist
            - playlist_url (str): Spotify URL of the playlist
            - message (str): Success message
            - error (str, optional): Error message if failed
    """
    try:
        user = spotify_client.current_user()
        playlist = spotify_client.user_playlist_create(
            user=user['id'],
            name=request.name,
            public=request.public,
            collaborative=request.collaborative,
            description=request.description
        )
        
        return {
            "success": True,
            "playlist_id": playlist['id'],
            "playlist_name": playlist['name'],
            "playlist_url": playlist['external_urls']['spotify'],
            "message": f"Playlist '{request.name}' created successfully"
        }
        
    except Exception as e:
        logger.error(f"Error creating playlist: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create playlist"
        }

async def add_tracks_to_playlist_tool(spotify_client, request: AddTracksRequest) -> Dict[str, Any]:
    """Add tracks to an existing playlist
    
    Arguments:
        request (AddTracksRequest):
            - playlist_id (str): Spotify playlist ID to add tracks to
            - track_uris (List[str]): List of Spotify track URIs to add
    
    Returns:
        Dict[str, Any]:
            - success (bool): Whether the operation was successful
            - playlist_id (str): ID of the playlist
            - tracks_added (int): Number of tracks added
            - message (str): Success message
            - error (str, optional): Error message if failed
    """
    try:
        spotify_client.playlist_add_items(request.playlist_id, request.track_uris)
        
        return {
            "success": True,
            "playlist_id": request.playlist_id,
            "tracks_added": len(request.track_uris),
            "message": f"Added {len(request.track_uris)} tracks to playlist"
        }
        
    except Exception as e:
        logger.error(f"Error adding tracks to playlist: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to add tracks to playlist"
        }

async def get_user_playlists_tool(spotify_client) -> Dict[str, Any]:
    """Get current user's playlists
    
    Arguments:
        None (no parameters required)
    
    Returns:
        Dict[str, Any]:
            - success (bool): Whether the operation was successful
            - playlists (List[Dict]): List of playlist objects containing:
                - id (str): Spotify playlist ID
                - name (str): Playlist name
                - description (str): Playlist description
                - public (bool): Whether the playlist is public
                - tracks_count (int): Number of tracks in the playlist
                - spotify_url (str): Spotify playlist URL
            - total_playlists (int): Total number of playlists
            - message (str): Success message
            - error (str, optional): Error message if failed
    """
    try:
        user = spotify_client.current_user()
        playlists = spotify_client.current_user_playlists()
        
        playlist_list = []
        for playlist in playlists['items']:
            playlist_list.append({
                "id": playlist['id'],
                "name": playlist['name'],
                "description": playlist.get('description', ''),
                "public": playlist['public'],
                "tracks_count": playlist['tracks']['total'],
                "spotify_url": playlist['external_urls']['spotify']
            })
        
        return {
            "success": True,
            "playlists": playlist_list,
            "total_playlists": len(playlist_list),
            "message": f"Found {len(playlist_list)} playlists for user {user['display_name']}"
        }
        
    except Exception as e:
        logger.error(f"Error getting user playlists: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to get user playlists"
        } 