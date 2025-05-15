import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import AuthPage from "./components/AuthPage";
import HomePage from "./components/HomePage";
import SongPage from "./components/SongPage";
import SearchResultsPage from "./components/SearchResultsPage";
import SongInfo from "./components/SongInfo";
import AlbumInfo from "./components/AlbumInfo";
import SingerInfo from "./components/SingerInfo";




function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AuthPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/songs" element={<SongPage />} />
        <Route path="/search-results" element={<SearchResultsPage />} />
        <Route path="/songs/:songID" element={<SongInfo />} />
        <Route path="/albums/:albumID" element={<AlbumInfo />} />
        <Route path="/artists/:sid" element={<SingerInfo />} />
        <Route path="/singers/:sid" element={<SingerInfo />} />
      </Routes>
    </Router>
  );
}

export default App;