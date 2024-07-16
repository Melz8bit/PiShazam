function fetchSongData() {
    var timestamp = new Date().getTime();
    var imageUrl = 'res/cover.jpg?' + timestamp;
    var jsonUrl = 'res/song_info.json?' + timestamp;

    // Use fetch API to load the JSON file
    fetch(jsonUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok for song_info.json');
            }
            return response.json();
        })
        .then(data => {
            var tracks = "";

            document.getElementById('album-cover').src = imageUrl;
            document.getElementById('song-title').textContent = data.title || 'Title not found';
            document.getElementById('song-artist').textContent = data.artist || 'Artist not found';
            document.getElementById('song-album').textContent = data.album || 'Album not found';

            for (let i = 1; i <= Object.keys(data.track_list).length; i++) {
                if (data.track_list[i] == data.title) {
                    tracks += "<b>" + i + " - " + data.track_list[i] + "</b><br>";
                }
                else {
                    tracks += i + " - " + data.track_list[i] + "<br>";
                }
            }
            document.getElementById('album-tracks').innerHTML = tracks || 'Track list not found';
        })
        .catch(error => {
            console.error('Error fetching song data:', error);
        });
}

// Update the song data every 1 seconds
setInterval(fetchSongData, 1000);

// Fetch the initial song data on page load
fetchSongData();
