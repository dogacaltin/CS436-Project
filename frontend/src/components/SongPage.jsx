import React, { useEffect, useState } from "react";
import { Box, Typography, Stack, Rating } from "@mui/material";
import axios from "axios";
import { API_BASE } from "../api/api"; 

const SongPage = () => {
  const [songs, setSongs] = useState([]);
  const [ratings, setRatings] = useState({});

  useEffect(() => {
    axios
      .get(`${API_BASE}/songs`)
      .then((res) => setSongs(res.data))
      .catch((err) => console.error("Song fetch error:", err));
  }, []);

  const handleRate = (songID, newValue) => {
    const proID = localStorage.getItem("proID");
    if (!proID) return alert("Not logged in!");

    setRatings({ ...ratings, [songID]: newValue });

    axios
      .post(`${API_BASE}/rate`, {
        songID,
        proID,
        rate: newValue,
      })
      .then(() => alert("Rating saved!"))
      .catch((err) => {
        console.error("Rating error:", err);
        alert("Error saving rating");
      });
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        bgcolor: "#000",
        color: "#fff",
        px: 4,
        py: 6,
      }}
    >
      <Typography variant="h4" textAlign="center" gutterBottom>
        🎶 Song List
      </Typography>

      <Stack spacing={3} mt={4}>
        {songs.map((song) => (
          <Box
            key={song.songID}
            sx={{
              p: 3,
              border: "1px solid #444",
              borderRadius: 2,
              bgcolor: "#111",
            }}
          >
            <Typography variant="h6">{song.name}</Typography>
            <Rating
              name={`rating-${song.songID}`}
              value={ratings[song.songID] || 0}
              onChange={(_, newValue) => handleRate(song.songID, newValue)}
              max={5}
              sx={{ mt: 1 }}
            />
          </Box>
        ))}
      </Stack>
    </Box>
  );
};

export default SongPage;
