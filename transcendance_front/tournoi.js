document.addEventListener("DOMContentLoaded", function() {
    const playerSlots = document.getElementById("playerSlots");
    const startGameButton = document.getElementById("startGame");
    const onlinePlayersList = document.querySelector(".online-players");  //just in case must be deleted if not used
    const onlinePlayers = document.querySelectorAll(".online-players li");   //just in case must be deleted if not used
    let playersInvited = 0;

    function invitePlayer(playerName) {
        const slot = document.createElement("div");
        slot.classList.add("player-slot");
        const img = document.createElement("img");
        img.src = "player.jpg"; // Path to the host player image
        img.alt = "Player Profile Picture";
        slot.appendChild(img);
        playerSlots.appendChild(slot);
        playersInvited++;
        if (playersInvited === 3) {
            startGameButton.style.display = "block";
        }
    }

    function addPlayersFromURL() {
        const urlParams = new URLSearchParams(window.location.search);
        const players = urlParams.getAll("player");
        players.forEach(function(player) {
            invitePlayer(player);
        });
    }

    addPlayersFromURL(); // Add players when the page loads

    startGameButton.addEventListener("click", function() {
        alert("Game starting!");
        // redirct l page dyal tournament
    });
});