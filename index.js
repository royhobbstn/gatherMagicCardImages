const fs = require('fs');
const rp = require('request-promise');

const card_data = JSON.parse(fs.readFileSync('./data/scryfall-default-cards.json'));

const sets = new Set(card_data.map(d => d.set));
sets.forEach(set => {
  try {
    fs.mkdirSync(`./cards/${set}`);
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

    const card_name = `${card.set}_${card.collector_number}_${card.name}.jpg`;
    const exists = fs.existsSync(`./cards/${card.set}/${card_name}`);
    if (exists) {
      resolve();
    }
    else {
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
            fs.writeFile(`./cards/${card.set}/${card_name}`, response, 'binary', (err) => {
              if (err) {
                // console.log(err);
                resolve();
              }

              console.log(`saved ${card_name}`);
              resolve();
            });

          })
          .catch((e) => {
            resolve();
          });
      }, 700);
    }

  });
}

downloadImages();
