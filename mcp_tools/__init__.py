"""
MCP Tools package for Spotify integration
"""

from .artist_tools import search_artists_tool, get_artist_top_tracks_tool, get_artist_tool, get_artist_albums_tool, ArtistSearchRequest
from .playlist_tools import create_playlist_tool, add_tracks_to_playlist_tool, get_user_playlists_tool, PlaylistCreateRequest, AddTracksRequest
from .albums import get_album_tool, get_album_tracks_tool, get_new_releases_tool

__all__ = [
    'search_artists_tool',
    'get_artist_top_tracks_tool',
    'get_artist_tool',
    'get_artist_albums_tool',
    'ArtistSearchRequest',
    'create_playlist_tool',
    'add_tracks_to_playlist_tool',
    'get_user_playlists_tool',
    'PlaylistCreateRequest',
    'AddTracksRequest',
    'get_album_tool',
    'get_album_tracks_tool',
    'get_new_releases_tool'
] 