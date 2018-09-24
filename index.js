const fs = require('fs');
const rp = require('request-promise');

const card_set = (process.argv[2]).toLowerCase();

if (!card_set) {
  console.log('all cards disabled.  please specify set');
}

const card_data = JSON.parse(fs.readFileSync('./data/scryfall-default-cards.json'));
const selected_cards = card_data.filter(d => d.set === card_set);
const number_of_cards = selected_cards.length;


if (!number_of_cards) {
  console.log('no cards found. exiting.');
  process.exit();
}
else {
  console.log(`found ${number_of_cards} in set: ${card_set}`);
}

try {
  fs.rmdirSync(`./cards/${card_set}`);
}
catch (e) {
  console.log(`./cards/${card_set} does not exist.  creating.`);
}

fs.mkdirSync(`./cards/${card_set}`);

async function downloadImages() {
  for (const card of selected_cards) {
    await mockDownload(card);
  }
}


function mockDownload(card) {
  return new Promise((resolve, reject) => {
    setTimeout(function() {
      const options = {
        uri: card.image_uris.small,
        method: "GET",
        encoding: null,
        headers: {
          "Content-type": "applcation/jpeg"
        }
      };
      rp(options)
        .then((response) => {
          const card_name = `${card_set}_${card.collector_number}_${card.name}.jpg`;
          fs.writeFile(`./cards/${card_set}/${card_name}`, response, 'binary', () => {
            console.log(`saved ${card_name}`);
            resolve();
          });

        })
        .catch((e) => {
          console.log(e);
          process.exit();
        });
    }, 500);
  });
}

downloadImages();
