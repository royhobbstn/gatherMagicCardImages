const fs = require('fs');
const rimraf = require('rimraf');

async function main() {

  await removeRecursive('../3ed_sorted');

  const dir_pr = fs.promises.mkdir('../3ed_sorted');
  const file_pr = fs.promises.readdir('../3ed_output', {});

  const [dir, files] = await Promise.all([dir_pr, file_pr]);

  const folders_to_create = [];

  files.forEach(file => {
    // start at index 3.  (accounts for 2 unique cards with same name... ie Forests)
    const split_name = file.split('_').slice(3).join('_').split('.jpg_')[0];
    folders_to_create.push(split_name);
  });

  const unique_folders = Array.from(new Set(folders_to_create));

  // make directories
  await unique_folders.map(folder_name => {
    return fs.promises.mkdir(`../3ed_sorted/${folder_name}`);
  });

  // copy files sync (don't try to async 10,000 files at once -inodes)
  files.forEach(file_name => {
    const folder_name = file_name.split('_').slice(3).join('_').split('.jpg_')[0];
    const new_file_name = file_name.split('.jpg_')[1];

    fs.copyFileSync(`../3ed_output/${file_name}`, `../3ed_sorted/${folder_name}/${new_file_name}`);
  });

  console.log('done');
}

main();


function removeRecursive(dir) {
  return new Promise((resolve, reject) => {
    rimraf(dir, {}, (err) => {
      if (err) {
        return reject('There was an error removing directory');
      }
      return resolve('finished');
    })
  })
}