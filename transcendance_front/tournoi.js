document.addEventListener("DOMContentLoaded", function() {
    const playerSlots = document.getElementById("playerSlots");
    const startGameButton = document.getElementById("startGame");
    const inviteButton = document.querySelector(".invite-button");
    const onlinePlayersList = document.querySelector(".online-players");
    const onlinePlayers = document.querySelectorAll(".online-players li");
    let playersInvited = 0;

    function invitePlayer(playerName) {
        const slot = document.createElement("div");
        slot.classList.add("player-slot");
        const img = document.createElement("img");
        img.src = "player.jpg"; // Path to default player image
        img.alt = "Player Profile Picture";
        slot.appendChild(img);
        playerSlots.appendChild(slot);
        playersInvited++;
        if (playersInvited === 3) {
            startGameButton.style.display = "block";
        }
        if (playersInvited >= 1) {
            inviteButton.style.display = "block"; // Keep the plus button visible after clicking
        }
        if (playersInvited >= 3) {
            inviteButton.style.display = "none"; // Hide the plus button after reaching maximum players
        }
    }

    inviteButton.addEventListener("click", function() {
        onlinePlayersList.style.display = "block";
    });

    onlinePlayers.forEach(function(player) {
        player.addEventListener("click", function() {
            const playerName = this.textContent;
            invitePlayer(playerName);
            onlinePlayersList.style.display = "none";
        });
    });

    startGameButton.addEventListener("click", function() {
        alert("Game starting!");
        // Add your game starting functionality here
    });
});
