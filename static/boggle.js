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

async function submitWord(evt) {
  evt.preventDefault();
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
    //TODO:put it on the DOM
  }
}

$form.on("submit", submitWord);
