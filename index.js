const fs = require('fs');
const rp = require('request-promise');

const card_data = JSON.parse(fs.readFileSync('./card_data/scryfall-default-cards.json'));

const sets = new Set(card_data.map(d => d.set));
sets.forEach(set => {
  try {
    fs.mkdirSync(`./medium_cards/${set}`);
  }
  catch (e) {
    // exists
  }

});


async function downloadImages() {
  for (const card of card_data) {
    await mockDownload(card);
  }
}


function mockDownload(card) {
  return new Promise((resolve, reject) => {

    if (!card.image_uris || !card.image_uris.small) {
      return resolve();
    }

    const card_name = `${card.set}_${card.collector_number}_${card.name}.jpg`;
    const exists = fs.existsSync(`./medium_cards/${card.set}/${card_name}`);

    if (exists) {
      return resolve();
    }
    else {
      setTimeout(function() {
        const options = {
          uri: card.image_uris.normal,
          method: "GET",
          encoding: null
        };
        rp(options)
          .then((response) => {
            fs.writeFile(`./medium_cards/${card.set}/${card_name}`, response, 'binary', (err) => {
              if (err) {
                console.log(`A. error saving ${card_name}`);
                return resolve();
              }

              console.log(`saved ${card_name}`);
              return resolve();
            });

          })
          .catch((e) => {
            console.log(`B. error fetching ${card_name}`);
            return resolve();
          });
      }, 700);
    }

  });
}

downloadImages();
