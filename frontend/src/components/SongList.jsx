import React, { useEffect, useState } from "react";
import { fetchSongs, rateSong } from "../api/api";

const SongList = () => {
  const [songs, setSongs] = useState([]);
  const [userID, setUserID] = useState("user1"); // sabit kullanıcı

  useEffect(() => {
    fetchSongs()
      .then((res) => setSongs(res.data))
      .catch((err) => console.error(err));
  }, []);

  const handleRating = (songID, rate) => {
    rateSong(userID, songID, rate)
      .then(() => alert(`Rated ${songID} with ${rate}`))
      .catch((err) => console.error(err));
  };

  return (
    <div>
      <h2>Song List</h2>
      {songs.map((song) => (
        <div key={song.id} style={{ marginBottom: "1rem" }}>
          <strong>{song.name}</strong>
          <p>Album: {song.albumID}</p>
          <p>Average Rating: {song.avgRateSong?.toFixed(2) || "N/A"}</p>
          {[1, 2, 3, 4, 5].map((star) => (
            <button key={star} onClick={() => handleRating(song.id, star)}>
              {star}
            </button>
          ))}
        </div>
      ))}
    </div>
  );
};

export default SongList;