"""
Spotify MCP Server 
Provides Spotify integration through Model Context Protocol 
"""

import os
import logging
from typing import List, Dict, Any, Optional

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from mcp.server.fastmcp.server import FastMCP
from pydantic import BaseModel
from dotenv import load_dotenv

from mcp_tools import search_artists_tool, get_artist_top_tracks_tool, get_artist_tool, get_artist_albums_tool, ArtistSearchRequest
from mcp_tools import create_playlist_tool, add_tracks_to_playlist_tool, get_user_playlists_tool, PlaylistCreateRequest, AddTracksRequest
from mcp_tools import get_album_tool, get_album_tracks_tool, get_new_releases_tool
from mcp_tools import get_user_top_artists_tool, get_user_top_tracks_tool

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimilarArtistPlaylistRequest(BaseModel):
    artist_name: str
    playlist_name: str
    playlist_description: Optional[str] = ""
    track_limit: int = 20
    include_artist_tracks: bool = True

app = FastMCP("Spotify MCP Server")

spotify = None

def _setup_spotify_client():
    """Initialize Spotify client with OAuth"""
    global spotify
    try:
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI', 'http://127.0.0.1:8888/callback')

        if not client_id or not client_secret:
            raise ValueError("Spotify credentials not found in environment variables")

        # Setup Spotify OAuth with persistent cache in home directory
        scope = "playlist-modify-public playlist-modify-private user-library-read user-read-private user-top-read"

        # Get cache directory from env or use home directory
        cache_dir = os.getenv('SPOTIFY_CACHE_DIR')
        if not cache_dir:
            cache_dir = os.path.expanduser('~/.spotify_mcp_cache')
            logger.info(f'expanded {cache_dir}')

        # Ensure cache directory exists
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)
            logger.info(f"Created cache directory: {cache_dir}")

        # Cache file path (Spotify expects a file, not a directory)
        cache_path = os.path.join(cache_dir, '.spotify_cache')
        logger.info(f"Using cache file: {cache_path}")

        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            cache_path=cache_path
        )
        
        spotify = spotipy.Spotify(auth_manager=auth_manager)
        logger.info("Spotify client initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize Spotify client: {e}")
        raise

_setup_spotify_client()

# Create wrapper functions that preserve names and documentation
async def create_playlist(request: PlaylistCreateRequest) -> Dict[str, Any]:
    return await create_playlist_tool(spotify, request)

async def search_artists(request: ArtistSearchRequest) -> Dict[str, Any]:
    return await search_artists_tool(spotify, request)

async def get_artist(artist_id: str) -> Dict[str, Any]:
    return await get_artist_tool(spotify, artist_id)

async def get_artist_albums(artist_id: str, include_groups: str = "album,single", limit: int = 20) -> Dict[str, Any]:
    return await get_artist_albums_tool(spotify, artist_id, include_groups, limit)

async def get_artist_top_tracks(artist_id: str, market: str = "US") -> Dict[str, Any]:
    return await get_artist_top_tracks_tool(spotify, artist_id, market)

async def add_tracks_to_playlist(request: AddTracksRequest) -> Dict[str, Any]:
    return await add_tracks_to_playlist_tool(spotify, request)

async def get_user_playlists() -> Dict[str, Any]:
    return await get_user_playlists_tool(spotify)

async def get_album(album_id: str, market: str = "US") -> Dict[str, Any]:
    return await get_album_tool(spotify, album_id, market)

async def get_album_tracks(album_id: str, market: str = "US", limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    return await get_album_tracks_tool(spotify, album_id, market, limit, offset)

async def get_new_releases(country: str = "US", limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    return await get_new_releases_tool(spotify, country, limit, offset)

async def get_user_top_artists(time_range: str = "medium_term", limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    return await get_user_top_artists_tool(spotify, time_range, limit, offset)

async def get_user_top_tracks(time_range: str = "medium_term", limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    return await get_user_top_tracks_tool(spotify, time_range, limit, offset)

# Copy docstrings from original functions
create_playlist.__doc__ = create_playlist_tool.__doc__
search_artists.__doc__ = search_artists_tool.__doc__
get_artist.__doc__ = get_artist_tool.__doc__
get_artist_albums.__doc__ = get_artist_albums_tool.__doc__
get_artist_top_tracks.__doc__ = get_artist_top_tracks_tool.__doc__
add_tracks_to_playlist.__doc__ = add_tracks_to_playlist_tool.__doc__
get_user_playlists.__doc__ = get_user_playlists_tool.__doc__
get_album.__doc__ = get_album_tool.__doc__
get_album_tracks.__doc__ = get_album_tracks_tool.__doc__
get_new_releases.__doc__ = get_new_releases_tool.__doc__
get_user_top_artists.__doc__ = get_user_top_artists_tool.__doc__
get_user_top_tracks.__doc__ = get_user_top_tracks_tool.__doc__

# Register tools with FastMCP
app.tool()(create_playlist)
app.tool()(search_artists)
app.tool()(get_artist)
app.tool()(get_artist_albums)
app.tool()(get_artist_top_tracks)
app.tool()(add_tracks_to_playlist)
app.tool()(get_user_playlists)
app.tool()(get_album)
app.tool()(get_album_tracks)
app.tool()(get_new_releases)
app.tool()(get_user_top_artists)
app.tool()(get_user_top_tracks)

def main():
    """Entry point for the MCP server"""
    app.run()

if __name__ == "__main__":
    main()
