import React, { useEffect, useState } from "react";
import { fetchSongs, rateSong } from "../api/api";

const SongList = () => {
  const [songs, setSongs] = useState([]);
  const userId = "user1"; // örnek kullanıcı

  useEffect(() => {
    fetchSongs().then((res) => setSongs(res.data));
  }, []);

  const handleRating = async (songId, rating) => {
    try {
      await rateSong(userId, songId, rating);
      alert(`You rated song ${songId} with ${rating} stars`);
    } catch (err) {
      console.error("Rating error:", err);
    }
  };

  return (
    <div>
      <h2>Rate the Songs</h2>
      {songs.map((song) => (
        <div key={song.song_id} style={{ marginBottom: "20px" }}>
          <h4>{song.name} – {song.group_name}</h4>
          {[1, 2, 3, 4, 5].map((star) => (
            <button key={star} onClick={() => handleRating(song.song_id, star)}>
              {star}
            </button>
          ))}
        </div>
      ))}
    </div>
  );
};

export default SongList;