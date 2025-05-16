import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Box,
  Typography,
  CircularProgress,
  Stack,
  Paper,
} from "@mui/material";
import axios from "axios";
import { API_BASE } from "../api/api"; // ✅ Import base URL

const AlbumInfo = () => {
  const { albumID } = useParams();
  const [album, setAlbum] = useState(null);
  const [songs, setSongs] = useState([]);
  const [singerName, setSingerName] = useState("");
  const [singerID, setSingerID] = useState("");
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    axios
      .get(`${API_BASE}/albums/${albumID}`)
      .then((res) => {
        if (res.data && res.data.name) {
          setAlbum(res.data);

          if (res.data.sid) {
            setSingerID(res.data.sid);

            axios
              .get(`${API_BASE}/singers/${res.data.sid}`)
              .then((singerRes) => setSingerName(singerRes.data.name))
              .catch((err) => console.error("Singer fetch error:", err));
          }
        } else {
          setAlbum(null);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("Album fetch error:", err);
        setAlbum(null);
        setLoading(false);
      });
  }, [albumID]);

  useEffect(() => {
    axios
      .get(`${API_BASE}/songs`)
      .then((res) => {
        const filtered = res.data.filter((s) => s.albumID === albumID);
        setSongs(filtered);
      })
      .catch((err) => {
        console.error("Song fetch error:", err);
      });
  }, [albumID]);

  if (loading) {
    return (
      <Box sx={{ bgcolor: "#000", color: "#fff", minHeight: "100vh", p: 4 }}>
        <Typography>Loading album...</Typography>
        <CircularProgress sx={{ color: "#fff", mt: 2 }} />
      </Box>
    );
  }

  if (!album) {
    return (
      <Box sx={{ bgcolor: "#000", color: "#fff", minHeight: "100vh", p: 4 }}>
        <Typography variant="h5">Album not found.</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ bgcolor: "#000", color: "#fff", minHeight: "100vh", p: 4 }}>
      <Typography variant="h4" gutterBottom>
        📀 {album.name}
      </Typography>
      <Typography variant="body1" sx={{ mb: 2 }}>
        Year: {album.year}
      </Typography>
      <Typography variant="body1" sx={{ mb: 2 }}>
        Genre: {album.genre}
      </Typography>

      <Typography
        variant="body1"
        sx={{ mb: 2, textDecoration: "underline", cursor: "pointer" }}
        onClick={() => navigate(`/singers/${singerID}`)}
      >
        🎤 Artist: {singerName || "Loading..."}
      </Typography>

      <Typography variant="body1" sx={{ mb: 2 }}>
        Average Rating: {album.avgRateAlbum.toFixed(2) || "N/A"}
      </Typography>

      <Typography variant="h6" sx={{ mt: 4 }}>
        Songs in this album:
      </Typography>

      <Stack spacing={2} mt={2}>
        {songs.map((song) => (
          <Paper
            key={song.songID}
            sx={{
              p: 2,
              bgcolor: "#111",
              color: "#fff",
              cursor: "pointer",
              "&:hover": { bgcolor: "#222" },
            }}
            onClick={() => navigate(`/songs/${song.songID}`)}
          >
            <Typography>{song.name}</Typography>
          </Paper>
        ))}
      </Stack>
    </Box>
  );
};

export default AlbumInfo;
