//
const fs = require('fs');
const path = require('path');
const node_ssh = require('node-ssh');
const ssh = new node_ssh();

const AWS = require('aws-sdk');
AWS.config.loadFromPath('./config.json');
const ec2 = new AWS.EC2({apiVersion: '2016-11-15', region: 'us-west-2'});

// AMIs are region-specific
const instanceParams = {
  ImageId: 'ami-0bbe6b35405ecebdb',
  InstanceType: 't1.micro',
  KeyName: 'key_acs',
  MinCount: 1,
  MaxCount: 1
};

main();


async function main() {

  const instance_details = await ec2.runInstances(instanceParams).promise();
  console.log(JSON.stringify(instance_details));

  const instance_id = instance_details.Instances[0].InstanceId;

  console.log('Waiting for Instance to be ready.  Please be patient...');

  const params = {InstanceIds: [instance_id]};
  const ready_instance = await waitForInstance(params);

  console.log(JSON.stringify(ready_instance));
  console.log('Instance Ready');


}

async function waitForInstance(params) {
  return new Promise((resolve, reject) => {
    ec2.waitFor('instanceStatusOk', params, function (err, data) {
      if (err) {
        console.log(err);
        reject(err);
      } else {
        resolve(data);
      }
    });
  })
}


// sudo apt install -y python3-pip
// pip3 install numpy Pillow Augmentor

// installing nodejs only gets nodejs 8.1 (use nvm)
//