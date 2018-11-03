// ABOUT THIS NODE.JS SAMPLE: This sample is part of the SDK for JavaScript Developer Guide topic at
// https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide//ec2-example-creating-an-instance.html
// Load the AWS SDK for Node.js
var AWS = require('aws-sdk');

// Load credentials and set region from JSON file
AWS.config.loadFromPath('./config.json');

// Create EC2 service object
var ec2 = new AWS.EC2({apiVersion: '2016-11-15', region: 'us-west-2'});

// AMIs are region-specific
var instanceParams = {
  ImageId: 'ami-0bbe6b35405ecebdb',
  InstanceType: 't1.micro',
  KeyName: 'key_acs',
  MinCount: 1,
  MaxCount: 1
};


// ec2.describeKeyPairs(function(err, data) {
//   if (err) {
//     console.log("Error", err);
//   } else {
//     console.log("Success", JSON.stringify(data.KeyPairs));
//   }
// });

// Create a promise on an EC2 service object
var instancePromise = ec2.runInstances(instanceParams).promise();

// Handle promise's fulfilled/rejected states
instancePromise.then(
  function(data) {
    console.log(data);
    var instanceId = data.Instances[0].InstanceId;
    console.log("Created instance", instanceId);

  }).catch(
  function(err) {
    console.error(err, err.stack);
  });