const path = require('path');

module.exports = {
    entry: './hot_osm/media/js/hot_osm.js',
    output: {
        filename: 'hot-osm-bundle.js',
        path: path.resolve(__dirname, 'hot_osm/static'), // Django static directory path
    },
}
