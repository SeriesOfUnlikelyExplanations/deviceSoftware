# Device Software

This package includes the static files, lambda code, and CDK deployment pipeline for the always-onward website. You can see the website here - https://www.always-onward.com/.

[![Actions Status](https://github.com/SeriesOfUnlikelyExplanations/deviceSoftware/workflows/Deploy/badge.svg)](https://github.com/SeriesOfUnlikelyExplanations/deviceSoftware/actions) [![codecov](https://codecov.io/gh/SeriesOfUnlikelyExplanations/deviceSoftware/branch/live/graph/badge.svg?token=00SV7PWY60)](https://codecov.io/gh/SeriesOfUnlikelyExplanations/deviceSoftware)

To run unit tests:
npm test

TODO:
1. add log upload feature to van computer
2. Add to van computer config.txt
  disable_audio_dither=1 
  disable_overscan=1
  {retrieve overscan settings from config.txt for server sidd}
