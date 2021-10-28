import * as fs from 'fs';
import * as targz from 'targz';
import * as config from './config';
const AWS = require('aws-sdk')
const DynamoDB = AWS.DynamoDB;

predeploy()

async function predeploy() {
  if (!fs.existsSync(config.destDir)) {
    fs.mkdirSync(config.destDir);
  }
  var ssm = new AWS.SSM({signatureVersion: 'v4', region: config.region });
  const data = await ssm
    .getParameter({ Name: '/AlwaysOnward/devicesTable', WithDecryption: true})
    .promise();
  const ddbTable = data.Parameter.Value;

  const ddb = new DynamoDB.DocumentClient({signatureVersion: 'v4', region: config.region});
  var newConfig;
  for(const device of config.devices) {
    newConfig = JSON.parse(fs.readFileSync('./'+device+'/config.json', 'utf8'));
    newConfig.version = config.version;
    
    const result = await ddb.scan({
      FilterExpression: "#name = :name",
      ExpressionAttributeValues: {
        ":name": device
      },
      ExpressionAttributeNames: {
        "#name": 'name'
      },
      TableName: ddbTable  
    }).promise()
    newConfig.token = result.Items[0].token;
    console.log(newConfig);

    fs.writeFileSync('./'+device+'/config.json',
      JSON.stringify(newConfig),
      {flag:'w'}
    );


    targz.compress({
      src: './'+device,
      dest: config.destDir + '/'+device+'.tar.gz'
    }, function(err:any){
      if(err) {
        console.log(err);
      } else {
        console.log(device + " Compressed!");
      }
    });
  }
}
