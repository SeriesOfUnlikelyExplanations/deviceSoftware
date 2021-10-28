import * as cdk from '@aws-cdk/core';
import { Role } from '@aws-cdk/iam';
import { Bucket, BlockPublicAccess, HttpMethods, StorageClass } from '@aws-cdk/aws-s3';
import { BucketDeployment, Source } from '@aws-cdk/aws-s3-deployment';

import { StringParameter } from '@aws-cdk/aws-ssm';
import * as config from './config';

export class DeviceSoftwareStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props: cdk.StackProps) {
    super(scope, id, props);

    const roleArn = StringParameter.fromStringParameterAttributes(this, 'MyValue', {
      parameterName: '/AlwaysOnward/lambdaRoleArn',
    }).stringValue;
    
    const role = Role.fromRoleArn(this, "lambdaRole", roleArn);
    
    const sourceBucket = new Bucket(this, 'Always-Onward-deviceSoftware', {
      bucketName: 'always-onward-devicesoftware',
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
    });
    sourceBucket.grantRead(role);

    new BucketDeployment(this, 'DeployDeviceSoftware', {
      sources: [Source.asset(config.destDir)],
      destinationBucket: sourceBucket
    });

    //export values
    new StringParameter(this, 'deviceSoftwareBucket', {
      parameterName: '/AlwaysOnward/deviceSoftwareBucket',
      stringValue: sourceBucket.bucketName
    });
    new StringParameter(this, 'moviesBucket', {
      parameterName: '/AlwaysOnward/moviesBucket',
      stringValue: moviesBucket.bucketName
    });
    new StringParameter(this, 'currentSoftwareVersion', {
      parameterName: '/AlwaysOnward/currentSoftwareVersion',
      stringValue: config.version
    });
  }
}
