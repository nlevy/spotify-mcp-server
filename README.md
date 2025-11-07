# Spotify MCP Server

A Model Context Protocol (MCP) server that provides Spotify integration, allowing AI assistants and applications to interact with Spotify's music streaming service.

## Features

### Artist Tools

- **Search Artists** - Search for artists by name
- **Get Artist** - Get detailed information about a specific artist
- **Get Artist Albums** - Get all albums for an artist
- **Get Artist Top Tracks** - Get an artist's most popular tracks

### Album Tools

- **Get Album** - Get detailed information about a specific album
- **Get Album Tracks** - Get all tracks from an album
- **Get New Releases** - Get new album releases

### Playlist Tools

- **Create Playlist** - Create new playlists
- **Add Tracks to Playlist** - Add tracks to existing playlists
- **Get User Playlists** - Get current user's playlists

### User Tools

- **Get User Top Artists** - Get user's most listened to artists
- **Get User Top Tracks** - Get user's most listened to tracks

## Installation

### For Claude Desktop Users (Recommended)

The easiest way to use this server with Claude Desktop is via PyPI:

1. Get your Spotify API credentials (see [Spotify API Setup](#spotify-api-setup) below)
2. Add to your Claude Desktop config at `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "Spotify": {
      "command": "uvx",
      "args": ["spotify-mcp-server"],
      "env": {
        "SPOTIFY_CLIENT_ID": "your_client_id_here",
        "SPOTIFY_CLIENT_SECRET": "your_client_secret_here",
        "SPOTIFY_REDIRECT_URI": "http://localhost:8888/callback"
      }
    }
  }
}
```

3. Restart Claude Desktop
4. On first use, authenticate with Spotify when prompted


## Development Setup

### Prerequisites

- Python 3.10+
- Spotify Developer Account
- MCP Client (like Claude Desktop, Cursor, etc.)

## Setup

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Spotify API Setup {#spotify-api-setup}

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Add `http://localhost:8888/callback` to your app's Redirect URIs
4. Copy your Client ID and Client Secret

### 3. Environment Configuration

Create a `.env` file in the project root:

```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

### 4. Authentication

On first run, the server will open a browser window for Spotify authentication. Follow the OAuth flow to authorize the application.

## Usage

### Running the Server

```bash
# Development mode with inspector
mcp dev spotify_mcp_server.py

# Or run directly
python spotify_mcp_server.py
```

### Available Tools

#### Artist Management

```python
# Search for artists
search_artists(query="The Beatles", limit=10)

# Get artist details
get_artist(artist_id="3WrFJ7ztbogyGnTHbHJFl2")

# Get artist albums
get_artist_albums(artist_id="3WrFJ7ztbogyGnTHbHJFl2", include_groups="album,single")

# Get artist top tracks
get_artist_top_tracks(artist_id="3WrFJ7ztbogyGnTHbHJFl2", market="US")
```

#### Album Management

```python
# Get album details
get_album(album_id="4aawyAB9vmqN3uQ7FjRGTy", market="US")

# Get album tracks
get_album_tracks(album_id="4aawyAB9vmqN3uQ7FjRGTy", limit=20)

# Get new releases
get_new_releases(country="US", limit=20)
```

#### Playlist Management

```python
# Create a new playlist
create_playlist(name="My New Playlist", description="A great playlist", public=False)

# Add tracks to playlist
add_tracks_to_playlist(playlist_id="playlist_id", track_uris=["spotify:track:track_id"])

# Get user playlists
get_user_playlists()
```

#### User Data

```python
# Get user's top artists
get_user_top_artists(time_range="medium_term", limit=20)

# Get user's top tracks
get_user_top_tracks(time_range="short_term", limit=10)
```

## Project Structure

```
spotify-mcp/
├── spotify_mcp_server.py    # Main MCP server
├── mcp_tools/              # Tool modules
│   ├── __init__.py
│   ├── artist_tools.py     # Artist-related tools
│   ├── playlist_tools.py   # Playlist-related tools
│   ├── albums.py          # Album-related tools
│   └── user_tools.py      # User-related tools
├── .env                    # Environment variables
├── .spotify_cache         # Spotify OAuth cache
├── requirements.txt        # Python dependencies
└── README.md             # This file
```

## API Reference

### Artist Tools

#### `search_artists`

Search for artists on Spotify.

**Parameters:**

- `query` (str): Search query for artist name
- `limit` (int, optional): Maximum number of results (default: 10, max: 50)

**Returns:**

- List of artists with ID, name, popularity, followers, genres, and Spotify URL

#### `get_artist`

Get detailed information about an artist.

**Parameters:**

- `artist_id` (str): Spotify artist ID

**Returns:**

- Detailed artist information including images, genres, and popularity

#### `get_artist_albums`

Get albums for an artist.

**Parameters:**

- `artist_id` (str): Spotify artist ID
- `include_groups` (str, optional): Album types to include (default: "album,single")
- `limit` (int, optional): Maximum albums to return (default: 20, max: 50)

**Returns:**

- List of albums with details including release date, track count, and cover images

#### `get_artist_top_tracks`

Get top tracks for an artist.

**Parameters:**

- `artist_id` (str): Spotify artist ID
- `market` (str, optional): Market/country code (default: "US")

**Returns:**

- List of top tracks with popularity, duration, and album information

### Album Tools

#### `get_album`

Get detailed information about an album.

**Parameters:**

- `album_id` (str): Spotify album ID
- `market` (str, optional): Market/country code (default: "US")

**Returns:**

- Detailed album information including artists, images, and genres

#### `get_album_tracks`

Get tracks from an album.

**Parameters:**

- `album_id` (str): Spotify album ID
- `market` (str, optional): Market/country code (default: "US")
- `limit` (int, optional): Maximum tracks to return (default: 20, max: 50)
- `offset` (int, optional): Starting index (default: 0)

**Returns:**

- List of tracks with track number, duration, and artist information

#### `get_new_releases`

Get new album releases.

**Parameters:**

- `country` (str, optional): Country code (default: "US")
- `limit` (int, optional): Maximum albums to return (default: 20, max: 50)
- `offset` (int, optional): Starting index (default: 0)

**Returns:**

- List of new release albums with artist and image information

### Playlist Tools

#### `create_playlist`

Create a new Spotify playlist.

**Parameters:**

- `name` (str): Name of the playlist
- `description` (str, optional): Description of the playlist
- `public` (bool, optional): Whether the playlist is public (default: False)
- `collaborative` (bool, optional): Whether the playlist is collaborative (default: False)

**Returns:**

- Playlist information including ID, name, and Spotify URL

#### `add_tracks_to_playlist`

Add tracks to an existing playlist.

**Parameters:**

- `playlist_id` (str): Spotify playlist ID
- `track_uris` (List[str]): List of Spotify track URIs

**Returns:**

- Success status and number of tracks added

#### `get_user_playlists`

Get current user's playlists.

**Parameters:**

- None

**Returns:**

- List of user's playlists with details including track count and privacy settings

### User Tools

#### `get_user_top_artists`

Get user's most listened to artists from Spotify.

**Parameters:**

- `time_range` (str, optional): Time period for top artists (default: "medium_term")
  - `"short_term"`: Last 4 weeks
  - `"medium_term"`: Last 6 months
  - `"long_term"`: Several years
- `limit` (int, optional): Maximum number of artists to return (default: 20, max: 50)
- `offset` (int, optional): Index of the first artist to return (default: 0)

**Returns:**

- List of top artists with ID, name, popularity, followers, genres, and Spotify URL

#### `get_user_top_tracks`

Get user's most listened to tracks from Spotify.

**Parameters:**

- `time_range` (str, optional): Time period for top tracks (default: "medium_term")
  - `"short_term"`: Last 4 weeks
  - `"medium_term"`: Last 6 months
  - `"long_term"`: Several years
- `limit` (int, optional): Maximum number of tracks to return (default: 20, max: 50)
- `offset` (int, optional): Index of the first track to return (default: 0)

**Returns:**

- List of top tracks with ID, name, album info, artists, popularity, duration, and Spotify URL

## Development

### Adding New Tools

1. Create a new function in the appropriate tool module (`artist_tools.py`, `playlist_tools.py`, `albums.py`, or `user_tools.py`)
2. Add the function to the `__init__.py` exports
3. Create a wrapper function in `spotify_mcp_server.py`
4. Copy the docstring and register the tool

### Testing

```bash
# Run the server in development mode
mcp dev spotify_mcp_server.py

# The MCP Inspector will open at http://localhost:6274
# Use it to test your tools interactively
```

## Troubleshooting

### Authentication Issues

- Ensure your `.env` file has the correct Spotify credentials
- Check that your redirect URI matches exactly: `http://localhost:8888/callback`
- Clear the `.spotify_cache` file if you encounter token issues

### API Rate Limits

- Spotify has rate limits on API calls
- The server includes error handling for rate limit responses
- Consider implementing caching for frequently accessed data
