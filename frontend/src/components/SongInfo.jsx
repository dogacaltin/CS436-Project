import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Box,
  Typography,
  CircularProgress,
  Button,
} from "@mui/material";
import axios from "axios";
import Rating from "@mui/material/Rating";
import { API_BASE } from "../api/api"; // ✅ Import base URL

const SongInfo = () => {
  const { songID } = useParams();
  const navigate = useNavigate();
  const [song, setSong] = useState(null);
  const [loading, setLoading] = useState(true);
  const [rateValue, setRateValue] = useState(null);
  const [albumData, setAlbumData] = useState(null);
  const [artistID, setArtistID] = useState(null);
  const [artistName, setArtistName] = useState("");

  useEffect(() => {
    axios
      .get(`${API_BASE}/songs`)
      .then((res) => {
        const match = res.data.find((s) => s.songID === songID);
        setSong(match);
        setLoading(false);

        if (match?.albumID) {
          axios
            .get(`${API_BASE}/albums/${match.albumID}`)
            .then((albumRes) => {
              const album = albumRes.data;
              setAlbumData(album);
              setArtistID(album.sid);

              if (album.sid) {
                axios
                  .get(`${API_BASE}/singers/${album.sid}`)
                  .then((singerRes) => {
                    setArtistName(singerRes.data.name);
                  })
                  .catch((err) => console.error("Artist fetch error:", err));
              }
            })
            .catch((err) => {
              console.error("Album fetch error:", err);
            });
        }
      })
      .catch((err) => {
        console.error("Song fetch error:", err);
        setLoading(false);
      });
  }, [songID]);

  const handleRateSubmit = () => {
    const proID = localStorage.getItem("proID");

    if (!proID) {
      alert("You must be logged in to rate.");
      return;
    }

    const rating = parseInt(rateValue);
    if (isNaN(rating) || rating < 1 || rating > 5) {
      alert("Please enter a rating between 1 and 5.");
      return;
    }

    axios
      .post(`${API_BASE}/rate`, {
        songID,
        proID,
        rate: rating,
      })
      .then(() => {
        alert("Rating submitted!");
        window.location.reload(); // sayfayı yenile
      })
      .catch((err) => {
        console.error("Rate submit error:", err);
        alert("Error submitting rating.");
      });
  };

  if (loading) {
    return (
      <Box sx={{ bgcolor: "#000", color: "#fff", minHeight: "100vh", p: 4 }}>
        <Typography>Loading song...</Typography>
        <CircularProgress sx={{ color: "#fff", mt: 2 }} />
      </Box>
    );
  }

  if (!song) {
    return (
      <Box sx={{ bgcolor: "#000", color: "#fff", minHeight: "100vh", p: 4 }}>
        <Typography>Song not found.</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ bgcolor: "#000", color: "#fff", minHeight: "100vh", p: 4 }}>
      <Typography variant="h4" gutterBottom>
        🎵 {song.name}
      </Typography>

      <Typography
        variant="body1"
        sx={{ mb: 1, cursor: "pointer", textDecoration: "underline" }}
        onClick={() => navigate(`/albums/${albumData?.albumID}`)}
      >
        📀 Album: {albumData?.name || "Unknown"}
      </Typography>

      <Typography
        variant="body1"
        sx={{ mb: 2, cursor: "pointer", textDecoration: "underline" }}
        onClick={() => navigate(`/singers/${artistID}`)}
      >
        🎤 Artist: {artistName || "Unknown"}
      </Typography>

      <Typography variant="body1">
        ⭐ Average Rating: {song.avgRateSong.toFixed(2) || "N/A"}
      </Typography>

      <Box sx={{ mt: 4 }}>
        <Typography variant="h6">Rate this song (1–5):</Typography>
        <Rating
          name="song-rating"
          value={rateValue}
          onChange={(event, newValue) => {
            setRateValue(newValue);
          }}
          max={5}
          size="large"
          sx={{ mt: 1 }}
        />
        <Button
          variant="contained"
          sx={{ mt: 2 }}
          onClick={handleRateSubmit}
        >
          Submit Rating
        </Button>
      </Box>
    </Box>
  );
};

export default SongInfo;
