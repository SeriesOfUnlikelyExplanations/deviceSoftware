import * as cdk from '@aws-cdk/core';
import { Bucket, BlockPublicAccess, HttpMethods, StorageClass } from '@aws-cdk/aws-s3';
import { BucketDeployment, Source } from '@aws-cdk/aws-s3-deployment';
import { Function } from "@aws-cdk/aws-lambda";
import { StringParameter } from '@aws-cdk/aws-ssm';
import * as config from './config';

export class DeviceSoftwareStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props: cdk.StackProps) {
    super(scope, id, props);

    const lambdaArn = StringParameter.fromStringParameterAttributes(this, 'MyValue', {
      parameterName: '/AlwaysOnward/lambdaArn',
    }).stringValue;
    
    const handler = Function.fromFunctionArn(this, 'external-lambda-from-arn', 
      lambdaArn
    );
    
    const sourceBucket = new Bucket(this, 'Always-Onward-deviceSoftware', {
      bucketName: 'always-onward-devicesoftware',
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
    });
    sourceBucket.grantRead(handler);

    new BucketDeployment(this, 'DeployWebsite', {
      sources: [Source.asset(config.destDir)],
      destinationBucket: sourceBucket
    });

    const moviesBucket = new Bucket(this, 'Always-Onward-movies', {
      bucketName: 'always-onward-movies',
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
      cors: [
        {
          allowedMethods: [
            HttpMethods.POST,
            HttpMethods.PUT,
          ],
          allowedOrigins: [config.localName, config.siteName].map(i => `https://${i}`),
          allowedHeaders: ['*'],
        },
      ],
      lifecycleRules: [
        {
          abortIncompleteMultipartUploadAfter: cdk.Duration.days(30),
          expiration: cdk.Duration.days(365),
          transitions: [
            {
              storageClass: StorageClass.ONE_ZONE_INFREQUENT_ACCESS,
              transitionAfter: cdk.Duration.days(30),
            }
          ],
        },
      ],
    });
    moviesBucket.grantReadWrite(handler);

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
