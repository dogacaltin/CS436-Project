import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Box,
  Typography,
  CircularProgress,
  Stack,
  Paper,
  Divider,
} from "@mui/material";
import axios from "axios";

const SingerInfo = () => {
  const { sid } = useParams(); // sanatçı ID
  const [singer, setSinger] = useState(null);
  const [albums, setAlbums] = useState([]);
  const [songs, setSongs] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // Sanatçı bilgisi al
  useEffect(() => {
    axios
      .get(`http://localhost:8000/singers/${sid}`)
      .then((res) => {
        setSinger(res.data);
      })
      .catch((err) => {
        console.error("Singer fetch error:", err);
        setSinger(null);
      });
  }, [sid]);

  // Albüm ve şarkı verilerini çek
  useEffect(() => {
    const fetchAlbumsAndSongs = async () => {
      try {
        const [albumsRes, songsRes] = await Promise.all([
          axios.get("http://localhost:8000/albums"),
          axios.get("http://localhost:8000/songs"),
        ]);

        const artistAlbums = albumsRes.data.filter((a) => a.sid === sid);
        const artistAlbumIDs = artistAlbums.map((a) => a.albumID);
        const filteredSongs = songsRes.data.filter((song) =>
          artistAlbumIDs.includes(song.albumID)
        );

        setAlbums(artistAlbums);
        setSongs(filteredSongs);
        setLoading(false);
      } catch (err) {
        console.error("Data fetch error:", err);
        setLoading(false);
      }
    };

    fetchAlbumsAndSongs();
  }, [sid]);

  if (loading) {
    return (
      <Box sx={{ bgcolor: "#000", color: "#fff", minHeight: "100vh", p: 4 }}>
        <Typography>Loading artist...</Typography>
        <CircularProgress sx={{ color: "#fff", mt: 2 }} />
      </Box>
    );
  }

  if (!singer) {
    return (
      <Box sx={{ bgcolor: "#000", color: "#fff", minHeight: "100vh", p: 4 }}>
        <Typography variant="h5">Artist not found.</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ bgcolor: "#000", color: "#fff", minHeight: "100vh", p: 4 }}>
      <Typography variant="h4" gutterBottom>
        🎤 {singer.name}
      </Typography>

      <Typography variant="body1" sx={{ mb: 2 }}>
        Genres: {singer.genres?.join(", ") || "N/A"}
      </Typography>

      <Typography variant="body1" sx={{ mb: 2 }}>
        Average Rating: {singer.avgRateSinger.toFixed(2) || "N/A"}
      </Typography>

      <Typography variant="h6" sx={{ mt: 4 }}>
        Albums:
      </Typography>

      <Stack spacing={2} mt={2}>
        {albums.length === 0 ? (
          <Typography>No albums found for this artist.</Typography>
        ) : (
          albums.map((album) => (
            <Paper
              key={album.albumID}
              sx={{
                p: 2,
                bgcolor: "#111",
                color: "#fff",
              }}
            >
              <Box
                sx={{
                  cursor: "pointer",
                  "&:hover": { textDecoration: "underline" },
                }}
                onClick={() => navigate(`/albums/${album.albumID}`)}
              >
                <Typography variant="h6">{album.name}</Typography>
                <Typography variant="body2">Year: {album.year}</Typography>
                <Typography variant="body2">Genre: {album.genre}</Typography>
                <Typography variant="body2">
                  Avg. Rating: {album.avgRateAlbum.toFixed(2) || "N/A"}
                </Typography>
              </Box>

              <Divider sx={{ my: 2, borderColor: "#444" }} />

              <Typography variant="body2" sx={{ mb: 1 }}>
                Songs:
              </Typography>

              <Stack spacing={1}>
                {songs
                  .filter((s) => s.albumID === album.albumID)
                  .map((song) => (
                    <Box
                      key={song.songID}
                      onClick={() => navigate(`/songs/${song.songID}`)}
                      sx={{
                        pl: 2,
                        cursor: "pointer",
                        color: "#ccc",
                        "&:hover": { color: "#fff" },
                      }}
                    >
                      🎵 {song.name}
                    </Box>
                  ))}
              </Stack>
            </Paper>
          ))
        )}
      </Stack>
    </Box>
  );
};

export default SingerInfo;