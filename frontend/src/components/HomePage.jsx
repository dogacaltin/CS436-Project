import React, { useEffect, useState } from "react";
import { Button, Typography, Box } from "@mui/material";
import { useNavigate } from "react-router-dom";

const HomePage = () => {
  const [proID, setProID] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const storedID = localStorage.getItem("proID");
    if (!storedID) {
      // Giriş yapılmamışsa login sayfasına yönlendir
      navigate("/");
    } else {
      setProID(storedID);
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("proID");
    navigate("/");
  };

  return (
    <Box
      sx={{
        textAlign: "center",
        mt: 10,
        display: "flex",
        flexDirection: "column",
        gap: 2,
      }}
    >
      <Typography variant="h4">Welcome to the Music Rating App!</Typography>
      <Typography variant="body1">Your ID: {proID}</Typography>

      <Button variant="contained" onClick={() => navigate("/songs")}>
        Go to Song List
      </Button>

      <Button variant="outlined" color="error" onClick={handleLogout}>
        Logout
      </Button>
    </Box>
  );
};

export default HomePage;