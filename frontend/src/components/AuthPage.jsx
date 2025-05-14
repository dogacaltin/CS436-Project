import React, { useState } from "react";
import { login, signup } from "../api/api";
import {
  Box,
  Button,
  TextField,
  Typography,
  Tabs,
  Tab,
  Stack,
  Paper,
  Grid,
} from "@mui/material";
import { useNavigate } from "react-router-dom";

const AuthPage = () => {
  const [mode, setMode] = useState("signin");
  const [nick, setNick] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleTabChange = (_, newValue) => setMode(newValue);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res =
        mode === "signin"
          ? await login(nick, password)
          : await signup(nick, password);
      localStorage.setItem("proID", res.data.proID);
      navigate("/home");
    } catch (err) {
      alert(
        `${mode === "signin" ? "Login" : "Signup"} failed: ` +
          (err.response?.data?.detail || "unknown error")
      );
    }
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        bgcolor: "#000",
        color: "text.primary",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        p: 2,
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* SOL GÖRSEL - siyah boşluk yerine */}
      <Box
  component="img"
  src="/images/hetfield.JPG"
  alt="Hetfield"
  sx={{
    position: "absolute",
    left: 150,
    top: 0,
    height: "100vh", // sayfanın tamamı
    width: "300px",
    objectFit: "cover",
    opacity: 0.3, // daha belirgin hale getirdik
    zIndex: 0,
  }}
/>
<Box
  component="img"
  src="/images/sebnem2.JPG"
  alt="Sebnem"
  sx={{
    position: "absolute",
    left: 1000,
    top: 0,
    height: "100vh", // sayfanın tamamı
    width: "400px",
    objectFit: "cover",
    opacity: 0.3, // daha belirgin hale getirdik
    zIndex: 0,
  }}
/>

      {/* ORTA FORM */}
      <Paper
        elevation={4}
        sx={{
          zIndex: 1,
          maxWidth: 400,
          width: "100%",
          p: 4,
          borderRadius: 3,
          bgcolor: "background.paper",
          position: "relative",
        }}
      >
        <Typography variant="h4" align="center" gutterBottom>
          {mode === "signin" ? "Sign in" : "Sign up"}
        </Typography>

        <Tabs
          value={mode}
          onChange={handleTabChange}
          variant="fullWidth"
          textColor="primary"
          indicatorColor="primary"
          sx={{ mb: 3 }}
        >
          <Tab value="signin" label="Sign In" />
          <Tab value="signup" label="Sign Up" />
        </Tabs>

        <form onSubmit={handleSubmit}>
          <Stack spacing={2}>
            <TextField
              label="Nickname"
              value={nick}
              onChange={(e) => setNick(e.target.value)}
              fullWidth
              required
            />
            <TextField
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              fullWidth
              required
            />
            <Button type="submit" variant="contained" fullWidth size="large">
              {mode === "signin" ? "Sign in" : "Create Account"}
            </Button>
          </Stack>
        </form>
      </Paper>
    </Box>
  );
};

export default AuthPage;