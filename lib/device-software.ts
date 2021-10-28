#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { DeviceSoftwareStack } from './deviceSoftwareStack';
import * as config from './config';
//~ import console = require('console');

const app = new cdk.App();
const env = {
  account: process.env.CDK_DEFAULT_ACCOUNT,
  region: config.region
}

const DeviceSoftware = new DeviceSoftwareStack(app, "vancomputer", {
  stackName: 'Always-Onward-device-software',
  env: env,
});
