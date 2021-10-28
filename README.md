# Van Computer

This package includes the static files, lambda code, and CDK deployment pipeline for the always-onward website. You can see the website here - https://www.always-onward.com/.

[![Actions Status](https://github.com/SeriesOfUnlikelyExplanations/vanComputer/workflows/Deploy/badge.svg)](https://github.com/SeriesOfUnlikelyExplanations/vanComputer/actions) [![codecov](https://codecov.io/gh/SeriesOfUnlikelyExplanations/vanComputer/branch/live/graph/badge.svg?token=00SV7PWY60)](https://codecov.io/gh/SeriesOfUnlikelyExplanations/vanComputer)

To run the website locally, use:
npm run serve

To run unit tests:
npm test

Many parts of the site are restricted to Admin use only. Users can be made Admin users with the isAdmin flag. This can only be set via the CLI right now using the command below

aws cognito-idp admin-update-user-attributes \
    --user-pool-id xxx \
    --username yyy \
    --user-attributes Name="custom:isAdmin",Value=True

TODO:
1. add log upload feature to van computer
2. Add to van computer config.txt
  disable_audio_dither=1 
  disable_overscan=1
  {retrieve overscan settings from config.txt for server sidd}
