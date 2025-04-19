require('dotenv').config();

module.exports = {
  appName: process.env.APP_NAME || 'My Express App',
  debug: process.env.DEBUG === 'true'
};
