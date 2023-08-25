"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  const response = await fetch(`/api/new-game`, {
    method: "POST",
  });
  const gameData = await response.json();

  // gameId = gameData.gameId;
  gameId = gameData["game_id"];
  let board = gameData.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();
  const $tBody = $("<tbody>");
  for (const row of board) {
    const $row = $("<tr>");
    for (const letter of row) {
      const $die = $("<td>").text(letter);
      $row.append($die);
    }
    $tBody.append($row);
  }
  $table.append($tBody);
}


start();


/**handles word submit */
async function submitWord(evt) {
  evt.preventDefault();
  $message.text("")
  const word = $wordInput.val();

  const response = await fetch(`/api/score-word`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      "game_id": gameId,
      "word": word.toUpperCase()
    })
  });

  const wordScoreData = await response.json();
  if (wordScoreData.result === "ok") {
    displayWord(word);
  }

  else {
    displayMessage(wordScoreData.result);
  }

}

$form.on("submit", submitWord);


/** Displays Message on gameboard when user inputs invalid word  */
function displayMessage(result){

  if(result === "not-word"){
    $message.text("Not Valid Word");
  }
  if (result === "not-on-board"){
    $message.text("Word Not On Board");
  }
// else if here for when we address duplicates
}

/**Displays word on gameboard when user inputs valid word */
function displayWord(word){
  $playedWords.append(`<li>${word}</li>`);

}