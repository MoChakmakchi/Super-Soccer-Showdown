document.addEventListener("DOMContentLoaded", function () {
  const canvas = document.getElementById("myCanvas");
  const ctx = canvas.getContext("2d");
  const container = document.getElementById("canvasContainer");
  const pokeDrawData = {};
  const swDrawData = {};
  const allPlayersData = [];

  setCanvasSize();

  // This will store the original content of all buttons
  const originalButtonContents = new Map();

  createTeamsAndDraw();

  window.addEventListener("resize", function () {
    drawCanvas();
  });

  // button management
  (function () {
    const changePokeTeamButton = document.getElementById("changePokeTeam");
    const changeSwTeamButton = document.getElementById("changeSwTeam");
    const radioButtons = document.querySelectorAll('input[type="radio"]');

    reactiveButton(
      changePokeTeamButton,
      "http://127.0.0.1:8000/api/poketeam",
      pokeDrawData,
      "pokemon"
    );
    reactiveButton(
      changeSwTeamButton,
      "http://127.0.0.1:8000/api/swteam",
      swDrawData,
      "starWars"
    );
    radioButtons.forEach((radio) => {
      if (radio.classList.contains("sw-radio")) {
        reactiveButton(
          radio,
          `http://127.0.0.1:8000/api/swteam/strategy`,
          swDrawData,
          "starWars",
          radio.value
        );
      } else if (radio.classList.contains("poke-radio")) {
        reactiveButton(
          radio,
          `http://127.0.0.1:8000/api/poketeam/strategy`,
          pokeDrawData,
          "pokemon",
          radio.value
        );
      }
    });
  })();

  // dialog popup management
  (function () {
    // Get the dialog and buttons
    const dialog = document.getElementById("myDialog");
    const openBtn = document.getElementById("openDialogBtn");
    const closeBtn = document.getElementById("closeDialogBtn");

    // Function to open the dialog
    openBtn.addEventListener("click", () => {
      dialog.style.display = "block";
    });

    // Function to close the dialog
    closeBtn.addEventListener("click", () => {
      dialog.style.display = "none";
    });

    // Close the dialog if user clicks outside of the dialog content
    window.addEventListener("click", (event) => {
      if (event.target == dialog) {
        dialog.style.display = "none";
      }
    });
  })();

  async function createTeamsAndDraw() {
    setAllButtonsToSpinners();
    await Promise.all([
      fetchAndUpdateTeamData(
        "http://127.0.0.1:8000/api/poketeam",
        pokeDrawData,
        "POST"
      ),
      fetchAndUpdateTeamData(
        "http://127.0.0.1:8000/api/swteam",
        swDrawData,
        "POST"
      ),
    ]);
    drawCanvas();
    restoreAllButtonsFromSpinners();
  }
  // *********** CANVAS DRAWING ************ //
  function drawCanvas() {
    allPlayersData.length = 0; // emptyArray
    setCanvasSize();
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
    preparePokeData();
    prepareSwData();
    drawPlayerImages(); // Redraw after resizing
    populatePlayersDialog();
  }
  function setCanvasSize() {
    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;
    canvas.width = containerWidth;
    canvas.height = containerHeight;
  }

  function drawPlayerImages() {
    if (allPlayersData.length != 10) return; // Ensure we have data to draw

    allPlayersData.forEach((player) => {
      const img = new Image();
      img.src = player.img_url;
      img.onload = () => {
        if (player.origin === "pokemon")
          ctx.drawImage(img, player.x, player.y, player.width, player.height);
        // star wars are rectangular, so turn to circles
        else {
          const radius = Math.min(player.width, player.height) / 2;
          const centerX = player.x + player.width / 2;
          const centerY = player.y + player.height / 2;
          ctx.save();
          ctx.beginPath();
          ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
          ctx.clip();
          ctx.drawImage(img, player.x, player.y, player.width, player.height);
          ctx.restore();
        }
      };
    });
  }

  function populatePlayersDialog() {
    // Function to create player cards
    function createPlayerCard(player) {
      const card = document.createElement("div");
      card.className = "card";

      card.innerHTML = `
           <img src="${player.img_url}" alt="${player.name}">
           <h4>${player.name}</h4>
           <p>Height: ${player.realHeight}</p>
           <p>Weight: ${player.weight}</p>
       `;

      return card;
    }

    // Populate the dialog with player cards
    const pokemonPlayersRow = document.getElementById("pokemonPlayersRow");
    const starwarsPlayersRow = document.getElementById("starwarsPlayersRow");

    pokemonPlayersRow.innerHTML = "";
    starwarsPlayersRow.innerHTML = "";
    console.log(allPlayersData)
    allPlayersData.forEach((player) => {
      const playerCard = createPlayerCard(player);
      if (player.origin === "pokemon") {
        pokemonPlayersRow.appendChild(playerCard);
      } else {
        starwarsPlayersRow.appendChild(playerCard);
      }
    });
  }
  // *********** DATA ************ //
  async function fetchAndUpdateTeamData(
    url,
    fetchedData,
    method = "GET",
    body = null
  ) {
    try {
      // Configure fetch options
      const options = {
        method,
        headers: {
          "Content-Type": "application/json", // Assuming JSON payloads
        },
      };

      // Include the body only if it's provided and method is not GET
      if (body && method !== "GET") {
        options.body = JSON.stringify(body);
      }

      const response = await fetch(url, options);

      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }

      // Parse and handle the response
      const data = await response.json();

      // Update fetchedData with the response data

      fetchedData.goalie = data.goalie;
      fetchedData.defenders = data.defenders;
      fetchedData.attackers = data.attackers;
    } catch (error) {
      console.error("Error fetching or updating data:", error);
    }
  }
  function preparePokeData() {
    if (!pokeDrawData) return;
    const playerDimensions = {
      width: canvas.width / 11,
      height: canvas.height / 4.5,
      origin: "pokemon",
    };
    const defenderPosition = {
      x: canvas.width / 4.5,
    };
    const attackerPosition = {
      x: canvas.width / 1.7,
    };
    const goalie = {
      name: pokeDrawData.goalie.name,
      x: canvas.width / 14,
      y: canvas.height / 2 - playerDimensions.height / 2,
      img_url: pokeDrawData.goalie.img_url,
      realHeight: pokeDrawData.goalie.height,
      weight: pokeDrawData.goalie.weight,
      ...playerDimensions,
    };

    allPlayersData.push(
      goalie,
      ...extractDefAndAttData(
        pokeDrawData,
        playerDimensions,
        defenderPosition,
        attackerPosition
      )
    );
  }

  function prepareSwData() {
    if (!swDrawData) return;
    const playerDimensions = {
      width: canvas.width / 16.5,
      height: canvas.height / 7,
      origin: "starWars",
    };
    const defenderPosition = {
      x: canvas.width / 1.4,
    };
    const attackerPosition = {
      x: canvas.width / 2.8,
    };
    const goalie = {
      x: canvas.width / 1.15,
      y: canvas.height / 2 - playerDimensions.height / 2,
      img_url: swDrawData.goalie.img_url,
      realHeight: swDrawData.goalie.height,
      weight: swDrawData.goalie.weight,
      ...playerDimensions,
    };
    allPlayersData.push(
      goalie,
      ...extractDefAndAttData(
        swDrawData,
        playerDimensions,
        defenderPosition,
        attackerPosition
      )
    );
  }

  function extractDefAndAttData(
    fetchedData,
    playerDimensions,
    defenderPosition,
    attackerPosition
  ) {
    const playersData = [];
    fetchedData.defenders.forEach((defender, index, array) => {
      const positionY =
        (canvas.height / (array.length + 1)) * (index + 1) -
        playerDimensions.height / 2;
      const defenderObj = {
        name: defender.name,
        x: defenderPosition.x,
        y: positionY,
        img_url: defender.img_url,
        realHeight: defender.height,
        weight: defender.weight,
        ...playerDimensions,
      };

      playersData.push(defenderObj);
    });
    fetchedData.attackers.forEach((attacker, index, array) => {
      const positionY =
        (canvas.height / (array.length + 1)) * (index + 1) -
        playerDimensions.height / 2;
      const attackerObj = {
        name: attacker.name,
        x: attackerPosition.x,
        y: positionY,
        img_url: attacker.img_url,
        realHeight: attacker.height,
        weight: attacker.weight,
        ...playerDimensions,
      };

      playersData.push(attackerObj);
    });
    return playersData;
  }

  // *********** BUTTONS ************ //
  function reactiveButton(button, endpoint, fetchedData, universe, strategy) {
    button.addEventListener("click", async function () {
      await updateDataAndDraw();
      if (button.classList.contains("change-team-button")) {
        document.getElementById(
          universe == "pokemon" ? "poke-balanced" : "sw-balanced"
        ).checked = true;
      }
    });

    async function updateDataAndDraw() {
      setAllButtonsToSpinners();
      try {
        if (button.classList.contains("change-team-button")) {
          await fetchAndUpdateTeamData(endpoint, fetchedData, "PUT");
        } else {
          await fetchAndUpdateTeamData(endpoint, fetchedData, "PATCH", {
            strategy: strategy,
          });
        }
        preparePokeData();
        prepareSwData();
        drawCanvas();
      } catch (error) {
        console.error("Error updating PokePlan:", error);
        alert("Failed to update the PokePlan.");
      } finally {
        restoreAllButtonsFromSpinners();
      }
    }
  }

  function buttonToSpinner(button) {
    // Store the original button content in the Map
    const originalContent = button.innerHTML;
    originalButtonContents.set(button, originalContent);

    // Disable the button and set it to a spinner
    button.disabled = true;
    button.innerHTML = '<div class="spinner"></div>';
  }

  function spinnerToButton(button) {
    // Retrieve the original content from the Map
    const originalContent = originalButtonContents.get(button);

    if (originalContent) {
      button.disabled = false;
      button.innerHTML = originalContent;

      // Remove it from the map once restored
      originalButtonContents.delete(button);
    }
  }

  // Function to apply the spinner to all buttons
  function setAllButtonsToSpinners() {
    const buttons = document.querySelectorAll(".change-team-button");
    const radios = document.querySelectorAll(".radio-label");
    const playerStatsButton = document.getElementById("openDialogBtn");
    buttons.forEach((button) => buttonToSpinner(button));
    radios.forEach((button) => buttonToSpinner(button));
    buttonToSpinner(playerStatsButton);
  }

  // Function to restore all buttons to their original state
  function restoreAllButtonsFromSpinners() {
    const buttons = document.querySelectorAll(".change-team-button");
    const radios = document.querySelectorAll(".radio-label");
    const playerStatsButton = document.getElementById("openDialogBtn");
    buttons.forEach((button) => spinnerToButton(button));
    radios.forEach((button) => spinnerToButton(button));
    spinnerToButton(playerStatsButton);
  }
});
