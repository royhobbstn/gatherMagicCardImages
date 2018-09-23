const fs = require('fs');

const card_data = JSON.parse(fs.readFileSync('./data/scryfall-default-cards.json'));

console.log(card_data.length);

const slice = card_data.filter(d => d.set === "3ed");


async function downloadImages() {
  for (const card of slice) {
    await mockDownload(card);
  }
}


function mockDownload(card) {
  return new Promise((resolve, reject) => {
    setTimeout(function() {
      console.log(card.name);
      resolve();
    }, 1000);
  });
}

downloadImages();
