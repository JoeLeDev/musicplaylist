function hidePlaylistDetails() {
    const detailsContainer = document.getElementById('playlist-details-container');
    if (detailsContainer) {
        detailsContainer.style.display = 'none';
    } else {
        console.error("L'élément 'playlist-details-container' est introuvable.");
    }
}

document.addEventListener('DOMContentLoaded', async function () {
    const API_BASE_URL = 'http://127.0.0.1:5002';

    // Sélection des éléments du DOM
    const playlistsList = document.getElementById('playlists-list');
    const playlistDetails = document.getElementById('playlist-details');
    const playlistDetailsContainer = document.getElementById('playlist-details-container');
    const dbSongsList = document.getElementById('db-songs-list');
    const paginationControls = document.getElementById('pagination-controls');
    const searchButton = document.getElementById('search-button');
    const artistSearch = document.getElementById('artist-search');
    const searchResults = document.getElementById('search-results');
    const spotifyPaginationControls = document.getElementById('spotify-pagination-controls');
    const createPlaylistInput = document.getElementById('new-playlist-name');
    const createPlaylistButton = document.getElementById('submit-playlist');
    

    // Fonction pour effectuer les appels API de manière asynchrone
    async function fetchAPI(url, options = {}) {
        try {
            const response = await fetch(url, options);
            if (!response.ok) throw new Error(`Erreur : ${response.statusText}`);
            return await response.json();
        } catch (error) {
            console.error(error);
            alert(error.message);
        }
    }

    async function getSpotifySongsByArtist(artist, page = 1, limit = 10) {
        const offset = (page - 1) * limit;
        const data = await fetchAPI(`${API_BASE_URL}/spotify_songs?artist=${artist}&offset=${offset}&limit=${limit}`);
        if (data) {
            const totalPages = Math.ceil(data.total_songs / limit);
            displaySpotifySongs(data.songs, page, totalPages, artist);
        }
    }

    function displaySpotifySongs(songs, page, totalPages, artist) {
        searchResults.innerHTML = songs.length ? '' : '<li>Aucune chanson trouvée.</li>';
        songs.forEach(song => {
            const li = document.createElement('li');
            li.textContent = `${song.name} - ${song.artist} (${song.album})`;
            const addButton = document.createElement('button');
            addButton.textContent = '+';
            addButton.onclick = () => addSongsToDB(song);
            li.appendChild(addButton);
            searchResults.appendChild(li);
        });
        setupPagination(spotifyPaginationControls, page, totalPages, (i) => getSpotifySongsByArtist(artist, i));
    }

    async function addSongsToDB(song) {
        const formattedSongs = [{ name: song.name, artist: song.artist, album: song.album }];
        const data = await fetchAPI(`${API_BASE_URL}/add_spotify_songs`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ songs: formattedSongs })
        });
        if (data) getSongsFromDB();
    }

    async function getSongsFromDB(page = 1, perPage = 5) {
        const data = await fetchAPI(`${API_BASE_URL}/songs?page=${page}&per_page=${perPage}`);
        
        if (data) {
            dbSongsList.innerHTML = '';
            data.songs.forEach(song => {
                const songItem = document.createElement('li');
                songItem.innerHTML = `${song.name} - ${song.artist} (${song.album})`;
                const buttonContainer = createButtonContainer(song.id);
                songItem.appendChild(buttonContainer);
                dbSongsList.appendChild(songItem);
            });
    
            await getAllPlaylists();  // Appel à getAllPlaylists uniquement ici
        }
    
        setupPagination(paginationControls, page, data.pages, getSongsFromDB);
    }
    
    
    function setupPagination(container, currentPage, totalPages, callback) {
        container.innerHTML = ''; 
    
        for (let page = 1; page <= totalPages; page++) {
            const pageButton = document.createElement('button');
            pageButton.textContent = `Page ${page}`;
            pageButton.disabled = page === currentPage; 
            pageButton.onclick = () => callback(page); 
            container.appendChild(pageButton);
        }
    }

    function createButtonContainer(songId) {
        const buttonContainer = document.createElement('div');
        buttonContainer.classList.add('button-container');

        const editButton = document.createElement('button');
        editButton.innerHTML = '<i class="fas fa-edit"></i>';
        editButton.onclick = () => editSongTitle(songId);

        const deleteButton = document.createElement('button');
        deleteButton.innerHTML = '<i class="fas fa-trash"></i>';
        deleteButton.onclick = () => deleteSong(songId);

        const playlistSelect = document.createElement('select');
        playlistSelect.classList.add('playlist-select');
        playlistSelect.innerHTML = '<option value="" disabled selected>Ajouter à une playlist</option>';
        playlistSelect.onchange = () => {
            const playlistId = playlistSelect.value;
            if (playlistId) {
                addSongToPlaylist(songId, playlistId);
            }
        };

        buttonContainer.appendChild(editButton);
        buttonContainer.appendChild(deleteButton);
        buttonContainer.appendChild(playlistSelect);

        return buttonContainer;
    }

    async function editSongTitle(songId) {
        const newName = prompt("Entrez le nouveau titre de la chanson :");
        if (!newName) return;
        const data = await fetchAPI(`${API_BASE_URL}/songs/${songId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: newName })
        });
        if (data) {
            getSongsFromDB();
            showAlert("Titre de la chanson mis à jour avec succès !", "success");
        } else {
            showAlert("Échec de la mise à jour du titre. Veuillez réessayer.", "error");
        }
    }

    async function deleteSong(songId) {
        if (!confirm("Voulez-vous vraiment supprimer cette chanson ?")) return;
        const data = await fetchAPI(`${API_BASE_URL}/songs/${songId}`, { method: 'DELETE' });
        if (data) getSongsFromDB();
    }

    async function addSongToPlaylist(songId, playlistId) {
        const data = await fetchAPI(`${API_BASE_URL}/playlists/${playlistId}/add_song`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ song_id: songId })
        });
        if (data) {
            showAlert("Chanson ajoutée à la playlist avec succès !", "success");
        } else {
            showAlert("Échec de l'ajout de la chanson. Veuillez réessayer.", "error");
        }
    }

    async function getAllPlaylists() {
        const data = await fetchAPI(`${API_BASE_URL}/playlists`);
        if (data) {
            playlistsList.innerHTML = '';
            displayPlaylists(data);
        }
    }

    function displayPlaylists(playlists) {
        playlistsList.innerHTML = '';
        playlists.forEach(playlist => {
            const playlistItem = document.createElement('li');
            playlistItem.textContent = playlist.name;
            
            const buttonContainer = document.createElement('div');
            buttonContainer.classList.add('button-container');
            buttonContainer.innerHTML = `
                <button onclick="viewPlaylistDetails(${playlist.id})"><i class="fas fa-eye"></i></button>
                <button onclick="editPlaylistName(${playlist.id}, '${playlist.name}')"><i class="fas fa-edit"></i></button>
                <button onclick="deletePlaylist(${playlist.id})"><i class="fas fa-trash"></i></button>`;
            
            playlistItem.appendChild(buttonContainer);
            playlistsList.appendChild(playlistItem);
        });
    
        // Appeler `updatePlaylistSelectOptions` après avoir ajouté les éléments `<select>` au DOM
        playlists.forEach(playlist => {
            updatePlaylistSelectOptions(playlist.id, playlist.name);
        });
    }
    

    function updatePlaylistSelectOptions(playlistId, playlistName) {
        const playlistSelects = document.querySelectorAll('.playlist-select');
        playlistSelects.forEach(select => {
            if (!select.querySelector(`option[value="${playlistId}"]`)) {
                const option = document.createElement('option');
                option.value = playlistId;
                option.textContent = playlistName;
                select.appendChild(option);
            }
        });
    }
    
    

    async function viewPlaylistDetails(playlistId) {
        const data = await fetchAPI(`${API_BASE_URL}/playlists/${playlistId}`);
        if (data) {
            console.log(data)
            playlistDetails.innerHTML = `<h3>Détails de la Playlist: ${data.name}</h3>`;
            const songList = document.createElement('ul');
            if (data.songs && data.songs.length > 0) {
                data.songs.forEach(song => {
                    const songItem = document.createElement('li');
                    songItem.innerHTML = `${song.name} - ${song.artist} (${song.album})`;
    
                    // Créer le bouton de suppression avec song.id correctement défini
                    const deleteButton = document.createElement('button');
                    deleteButton.innerHTML = '<i class="fas fa-trash"></i>';
                    deleteButton.onclick = () => deleteSongFromPlaylist(song.id, playlistId);
    
                    songItem.appendChild(deleteButton);
                    songList.appendChild(songItem);
                });
            } else {
                songList.innerHTML = "<li>Aucune chanson dans cette playlist.</li>";
            }
            playlistDetails.appendChild(songList);
            playlistDetailsContainer.style.display = 'block';
        }
    }
    
    async function createPlaylist() {
        const playlistName = createPlaylistInput.value;
        if (!playlistName) {
            alert("Veuillez entrer un nom pour la playlist.");
            return;
        }
        const data = await fetchAPI(`${API_BASE_URL}/playlists`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: playlistName })
        });
        if (data) {
            createPlaylistInput.value = '';
            getAllPlaylists();
            showAlert("Playlist créée avec succès !", "success");
        } else {
            showAlert("Échec de la création de la playlist. Veuillez réessayer.", "error");
        }
    }
    createPlaylistButton.onclick = createPlaylist;


    async function editPlaylistName(playlistId, currentName) {
        const newName = prompt("Entrez le nouveau nom de la playlist :", currentName);
        if (!newName) return;
        const data = await fetchAPI(`${API_BASE_URL}/playlists/${playlistId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: newName })
        });
        if (data) {
            getAllPlaylists();
            showAlert("Nom de la playlist mis à jour avec succès !", "success");
        } else {
            showAlert("Échec de la mise à jour du nom de la playlist. Veuillez réessayer.", "error");
        }
    }
    async function deletePlaylist(playlistId) {
        if (!confirm("Voulez-vous vraiment supprimer cette playlist ?")) return;
        const data = await fetchAPI(`${API_BASE_URL}/playlists/${playlistId}`, { method: 'DELETE' });
        if (data) {
            getAllPlaylists();
            showAlert("Playlist supprimée avec succès !", "success");
        } else {
            showAlert("Échec de la suppression de la playlist. Veuillez réessayer.", "error");
        }
    }

    createPlaylistButton.onclick = createPlaylist;
    searchButton.onclick = () => {
        const artist = artistSearch.value;
        if (artist) getSpotifySongsByArtist(artist);
    };

    
    window.viewPlaylistDetails = viewPlaylistDetails;
    window.editPlaylistName = editPlaylistName;
    window.deletePlaylist = deletePlaylist;

    async function viewPlaylistDetails(playlistId) {
        const data = await fetchAPI(`${API_BASE_URL}/playlists/${playlistId}`);
        if (data) {
            const playlistsContainer = document.getElementById('playlists-container');
    
            const existingDetails = document.getElementById('playlist-details');
            if (existingDetails) {
                existingDetails.remove();
            }
    
            const playlistDetails = document.createElement('div');
            playlistDetails.id = 'playlist-details';
            playlistDetails.innerHTML = `<h3>Détails de la Playlist: ${data.name}</h3>`;
    
            const hideButton = document.createElement('button');
            hideButton.innerHTML = '<i class="fa fa-times" aria-hidden="true"></i>';
            hideButton.onclick = () => playlistDetails.remove();
    
            playlistDetails.appendChild(hideButton);
    
            const songList = document.createElement('ul');
            if (data.songs && data.songs.length > 0) {
                data.songs.forEach(song => {
                    const songItem = document.createElement('li');
                    songItem.innerHTML = `${song.name} - ${song.artist} (${song.album})`;
    
                    const buttonContainer = document.createElement('div');
                    buttonContainer.classList.add('button-container');
                    
                    const editButton = document.createElement('button');
                    editButton.innerHTML = '<i class="fas fa-edit"></i>';
                    editButton.onclick = () => editSongInPlaylist(song.id, playlistId);
    
                    const deleteButton = document.createElement('button');
                    deleteButton.innerHTML = '<i class="fas fa-trash"></i>';
                    deleteButton.onclick = () => deleteSongFromPlaylist(song.id, playlistId);
    
                    buttonContainer.appendChild(editButton);
                    buttonContainer.appendChild(deleteButton);
                    songItem.appendChild(buttonContainer);
                    songList.appendChild(songItem);
                });
            } else {
                songList.innerHTML = "<li>Aucune chanson dans cette playlist.</li>";
            }
    
            playlistDetails.appendChild(songList);
            playlistsContainer.appendChild(playlistDetails);
        }
    }
    
    
    async function editSongInPlaylist(songId, playlistId) {
        const newName = prompt("Entrez le nouveau titre de la chanson :");
        if (!newName) return;
        const data = await fetchAPI(`${API_BASE_URL}/songs/${songId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: newName })
        });
        if (data) viewPlaylistDetails(playlistId);
    }


    
    async function deleteSongFromPlaylist(songId, playlistId) {
        console.log("Suppression de la chanson avec l'ID :", songId, "de la playlist avec l'ID :", playlistId);
    
        if (!confirm("Voulez-vous vraiment supprimer cette chanson de la playlist ?")) return;
    
        try {
            const response = await fetch(`${API_BASE_URL}/playlists/${playlistId}/remove_song/${songId}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            });
    
            if (!response.ok) {
                throw new Error(`Erreur de suppression : ${response.statusText}`);
            }
    
            const data = await response.json();
            showAlert("Chanson supprimée de la playlist avec succès !", "success");
            viewPlaylistDetails(playlistId);
        } catch (error) {
            console.error("Erreur lors de la suppression :", error);
            showAlert("Échec de la suppression. Veuillez vérifier votre connexion ou réessayer plus tard.", "error");
        }
    }
    
    
    

    // Fonction pour créer une playlist
    async function createPlaylist() {
        const playlistName = createPlaylistInput.value;
        if (!playlistName) {
            alert("Veuillez entrer un nom pour la playlist.");
            return;
        }
        const data = await fetchAPI(`${API_BASE_URL}/playlists`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: playlistName })
        });
        if (data) {
            createPlaylistInput.value = '';
            getAllPlaylists();
        }
    }

    function addFilters() {
        const filterContainer = document.createElement('div');
        filterContainer.innerHTML = `
            <label for="filter-artist"></label>
            <input type="text" id="filter-artist" placeholder="Filtrer par artiste :">
            <button id="apply-filter"><i class="fa fa-search" aria-hidden="true"></i></button>
        `;
        
        const playlistsContainer = document.getElementById('db-songs-container');
        const h2Element = playlistsContainer.querySelector('h2');
    
        if (h2Element) {
            // Insère le filtre juste après le <h2>
            h2Element.insertAdjacentElement('afterend', filterContainer);
        } else {
            console.error("L'élément <h2> dans 'playlists-container' est introuvable.");
        }
    
        const filterArtistInput = document.getElementById('filter-artist');
        const applyFilterButton = document.getElementById('apply-filter');
    
        applyFilterButton.onclick = async () => {
            const artist = filterArtistInput.value.trim();
            if (artist) {
                await getSongsByArtist(artist);
            }
        };
    }
    
    // Nouvelle fonction pour appeler l'API et afficher les chansons filtrées
    async function getSongsByArtist(artist) {
        const data = await fetchAPI(`${API_BASE_URL}/songs/filter?artist=${encodeURIComponent(artist)}`);
        if (data) {
            dbSongsList.innerHTML = ''; // Effacer les chansons précédentes
    
            data.forEach(song => {
                const songItem = document.createElement('li');
                songItem.innerHTML = `${song.name} - ${song.artist} (${song.album})`;
                const buttonContainer = createButtonContainer(song.id);
                songItem.appendChild(buttonContainer);
                dbSongsList.appendChild(songItem);
            });
        }
    }

    addFilters();
    
    // Expose functions globally
    window.viewPlaylistDetails = viewPlaylistDetails;
    window.editPlaylistName = editPlaylistName;
    window.deletePlaylist = deletePlaylist;
    



    function showAlert(message, type = 'success') {
        const alertContainer = document.createElement('div');
        alertContainer.className = `alert alert-${type}`;
        alertContainer.textContent = message;
    
    
        // Masquer automatiquement l'alerte après 3 secondes
        setTimeout(() => {
            alertContainer.remove();
        }, 3000);
    }

    // Chargement initial
    await getSongsFromDB();
});
