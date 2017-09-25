var fs = require('fs');
var https = require('https');

// Download camera data from https://data.baltimorecity.gov/Transportation/Baltimore-Fixed-Speed-Cameras/dz54-2aru
// from file_url = 'https://data.baltimorecity.gov/api/views/dz54-2aru/rows.csv?accessType=DOWNLOAD';

var file = fs.createWriteStream("cameraData.csv");

var request = https.get("https://data.baltimorecity.gov/api/views/dz54-2aru/rows.csv?accessType=DOWNLOAD", function(response) {
  response.pipe(file);
});


//https://data.baltimorecity.gov/api/resource/4ih5-d5d5.csv 
//https://data.baltimorecity.gov/api/views/wsfq-mvij/rows.csv?accessType=DOWNLOAD

