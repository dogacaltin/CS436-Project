import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Typography,
  Stack,
  TextField,
  MenuItem,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import StarIcon from "@mui/icons-material/Star";
import StarBorderIcon from "@mui/icons-material/StarBorder";
import axios from "axios";
import { API_BASE } from "../api/api"; 

const HomePage = () => {
  const [, setProID] = useState("");
  const [logs, setLogs] = useState([]);
  const [searchText, setSearchText] = useState("");
  const [nick, setNick] = useState("");
  const [searchType, setSearchType] = useState("song");
  const navigate = useNavigate();

  useEffect(() => {
    const storedID = localStorage.getItem("proID");
    if (!storedID) {
      navigate("/");
    } else {
      setProID(storedID);
    }
  }, [navigate]);

  useEffect(() => {
    const storedID = localStorage.getItem("proID");
    if (!storedID) {
      navigate("/");
    } else {
      setProID(storedID);
      axios
        .get(`${API_BASE}/users/${storedID}`)
        .then((res) => {
          setNick(res.data.nick);
        })
        .catch((err) => {
          console.error("User fetch error:", err);
        });
    }
  }, [navigate]);

  useEffect(() => {
    axios
      .get(`${API_BASE}/logs/random`)
      .then((res) => setLogs(res.data))
      .catch((err) => console.error("Log fetch error:", err));
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("proID");
    navigate("/");
  };

  const handleSearch = () => {
    if (!searchText.trim()) {
      alert("Please enter a search term.");
      return;
    }

    navigate(
      `/search-results?query=${encodeURIComponent(
        searchText
      )}&type=${searchType}`
    );
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        bgcolor: "#000",
        color: "#fff",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        px: 3,
      }}
    >
      <Stack spacing={4} sx={{ width: "100%", maxWidth: 600 }}>
        <Typography variant="h3" fontWeight="bold">
          Welcome to the Music Rating App!
        </Typography>
        <Typography variant="h3" fontWeight="bold">
          {nick}
        </Typography>

        <Stack direction="row" spacing={2} justifyContent="center">
          <TextField
            label="Search"
            variant="outlined"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            sx={{ bgcolor: "#fff", borderRadius: 1, flex: 1 }}
            InputProps={{
              sx: {
                color: "#000",
              },
            }}
            InputLabelProps={{
              sx: {
                color: "#000",
              },
            }}
          />
          <TextField
            select
            value={searchType}
            onChange={(e) => setSearchType(e.target.value)}
            variant="outlined"
            sx={{ minWidth: 120, bgcolor: "#fff", borderRadius: 1 }}
            InputProps={{
              sx: {
                color: "#000",
              },
            }}
            InputLabelProps={{
              sx: {
                color: "#000",
              },
            }}
          >
            <MenuItem value="song">Song</MenuItem>
            <MenuItem value="artist">Artist</MenuItem>
            <MenuItem value="album">Album</MenuItem>
          </TextField>
          <Button variant="contained" onClick={handleSearch}>
            Search
          </Button>
        </Stack>

        <Button variant="outlined" color="error" onClick={handleLogout}>
          Logout
        </Button>

        {logs.length > 0 && (
          <Box>
            <Typography variant="h5" sx={{ mt: 4 }}>
              🎵 Songs For You 🎵
            </Typography>

            <Stack spacing={2} mt={2}>
              {logs.map((log, index) => (
                <Box
                  key={index}
                  onClick={() => navigate(`/songs/${log.songID}`)}
                  sx={{
                    p: 2,
                    border: "1px solid #444",
                    borderRadius: 2,
                    bgcolor: "#111",
                    cursor: "pointer",
                    transition: "0.2s",
                    "&:hover": {
                      bgcolor: "#222",
                      transform: "scale(1.01)",
                    },
                  }}
                >
                  <Typography variant="subtitle1">{log.songName}</Typography>
                  <Box display="flex" justifyContent="center">
                    {[1, 2, 3, 4, 5].map((star) =>
                      star <= log.rate ? (
                        <StarIcon key={star} sx={{ color: "#ff0" }} />
                      ) : (
                        <StarBorderIcon key={star} sx={{ color: "#555" }} />
                      )
                    )}
                  </Box>
                </Box>
              ))}
            </Stack>
          </Box>
        )}
      </Stack>
    </Box>
  );
};

export default HomePage;
