import React, { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import {
  Box,
  Typography,
  Stack,
  CircularProgress,
  Paper,
} from "@mui/material";
import axios from "axios";
import { API_BASE } from "../api/api"; // ✅ Import backend base

const SearchResultsPage = () => {
  const [searchParams] = useSearchParams();
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);

  const query = searchParams.get("query");
  const type = searchParams.get("type");

  const navigate = useNavigate();

  useEffect(() => {
    if (!query || !type) return;

    setLoading(true);
    axios
      .get(`${API_BASE}/search`, {
        params: { query, type },
      })
      .then((res) => {
        setResults(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Search error:", err);
        setLoading(false);
      });
  }, [query, type]);

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
      <Typography variant="h4" gutterBottom>
        🔍 Search Results for "{query}" ({type})
      </Typography>

      {loading ? (
        <CircularProgress sx={{ color: "#fff", mt: 4 }} />
      ) : results.length === 0 ? (
        <Typography variant="body1">No results found.</Typography>
      ) : (
        <Stack spacing={2} mt={3}>
          {results.map((item, index) => (
            <Paper
              key={index}
              sx={{
                p: 2,
                bgcolor: "#111",
                color: "#fff",
                cursor: type === "song" ? "pointer" : "default",
                "&:hover": type === "song" ? { bgcolor: "#222" } : {},
              }}
              onClick={() => {
                if (type === "song") {
                  navigate(`/songs/${item.songID}`);
                } else if (type === "album") {
                  navigate(`/albums/${item.albumID}`);
                } else if (type === "artist") {
                  navigate(`/artists/${item.sid}`);
                }
              }}
            >
              <Typography variant="h6">{item.name || "Unnamed item"}</Typography>
              {type === "album" && <Typography>Year: {item.year}</Typography>}
              {type === "song" && (
                <Typography>
                  Average Rate: {item.avgRateSong.toFixed(2) || "N/A"}
                </Typography>
              )}
              {type === "artist" && (
                <Typography>
                  Genres: {item.genres?.join(", ") || "N/A"}
                </Typography>
              )}
            </Paper>
          ))}
        </Stack>
      )}
    </Box>
  );
};

export default SearchResultsPage;
