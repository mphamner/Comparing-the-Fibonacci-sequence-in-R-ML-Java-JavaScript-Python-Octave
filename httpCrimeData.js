var fs = require('fs');
var https = require('https');

// Download crime data from https://data.baltimorecity.gov/Public-Safety/BPD-Part-1-Victim-Based-Crime-Data/wsfq-mvij/data
// from file_url = 'https://data.baltimorecity.gov/api/views/wsfq-mvij/rows.csv?accessType=DOWNLOAD';

var file = fs.createWriteStream("crimeData.csv");

var request = https.get("https://data.baltimorecity.gov/api/views/wsfq-mvij/rows.csv?accessType=DOWNLOAD", function(response) {
  response.pipe(file);
});

